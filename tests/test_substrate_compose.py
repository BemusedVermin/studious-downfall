"""Free vs coupled substrate composition — paper §3.3.

The free product runs each substrate's dynamics independently; the coupling re-parameterises
each component's dynamics from the *other* component's state.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import jax
import jax.numpy as jnp
from jaxtyping import Array, Float

from emergent_systems import (
    Coupling,
    ImplicitInSubstrate,
    Population,
    PRNGKey,
    Substrate,
    compose_substrates_coupled,
    compose_substrates_independently,
)


@dataclass(frozen=True)
class IncrementBy(Substrate[Float[Array, ""], Float[Array, ""]]):
    """`Φ(x) = x + step`. The increment is the dynamics parameter."""

    default_dynamics_param: Float[Array, ""] = field(default_factory=lambda: jnp.asarray(1.0))
    dynamics_param_space: type[Float[Array, ""]] = Array  # type: ignore[assignment]

    def dynamics(
        self, key: PRNGKey, param: Float[Array, ""], state: Float[Array, ""]
    ) -> Float[Array, ""]:
        del key
        return state + param

    def initial_state(self, key: PRNGKey) -> Float[Array, ""]:
        del key
        return jnp.asarray(0.0)

    def initial_population(self, key: PRNGKey) -> Population[Float[Array, ""]]:
        del key
        return ImplicitInSubstrate()


def test_free_composition_is_componentwise():
    a = IncrementBy(default_dynamics_param=jnp.asarray(1.0))
    b = IncrementBy(default_dynamics_param=jnp.asarray(10.0))
    composed = compose_substrates_independently(a, b)

    initial = (jnp.asarray(0.0), jnp.asarray(0.0))
    after = composed.dynamics(
        key=jax.random.key(0),
        param=composed.default_dynamics_param,
        state=initial,
    )
    assert jnp.allclose(after[0], 1.0)
    assert jnp.allclose(after[1], 10.0)


def test_coupled_composition_uses_kappa_not_default():
    """Paper §3.3 line 405-407: each component's parameter is replaced by κ_{j→i}(x_j)."""
    a = IncrementBy(default_dynamics_param=jnp.asarray(1.0))
    b = IncrementBy(default_dynamics_param=jnp.asarray(1.0))

    def a_to_b(x_a: Float[Array, ""]) -> Float[Array, ""]:
        return jnp.asarray(2.0) * x_a

    def b_to_a(x_b: Float[Array, ""]) -> Float[Array, ""]:
        return x_b + jnp.asarray(100.0)

    coupling = Coupling(a_to_b=a_to_b, b_to_a=b_to_a)
    composed = compose_substrates_coupled(a, b, coupling)

    # Initial: (5, 7). The κ-derived params are:
    #   param_a = b_to_a(7) = 107
    #   param_b = a_to_b(5) = 10
    # New state: (5 + 107, 7 + 10) = (112, 17).
    initial = (jnp.asarray(5.0), jnp.asarray(7.0))
    after = composed.dynamics(
        key=jax.random.key(0),
        param=composed.default_dynamics_param,
        state=initial,
    )
    assert jnp.allclose(after[0], 112.0)
    assert jnp.allclose(after[1], 17.0)


def test_free_composition_associativity_up_to_canonical_iso():
    """Paper §3.3 Proposition: (a ⊠ b) ⊠ c ≅ a ⊠ (b ⊠ c) up to canonical iso (nested tuples).

    We exercise the nesting rather than re-asserting the iso, because Python's type system
    materialises composed substrates as nested tuples (paper acknowledges this; see plan).
    """
    s = IncrementBy(default_dynamics_param=jnp.asarray(1.0))
    left = compose_substrates_independently(compose_substrates_independently(s, s), s)
    right = compose_substrates_independently(s, compose_substrates_independently(s, s))

    initial_left = ((jnp.asarray(0.0), jnp.asarray(0.0)), jnp.asarray(0.0))
    initial_right = (jnp.asarray(0.0), (jnp.asarray(0.0), jnp.asarray(0.0)))

    after_left = left.dynamics(
        key=jax.random.key(0),
        param=left.default_dynamics_param,
        state=initial_left,
    )
    after_right = right.dynamics(
        key=jax.random.key(1),
        param=right.default_dynamics_param,
        state=initial_right,
    )

    # Three-tuple of 1.0s in either grouping.
    flat_left = (after_left[0][0], after_left[0][1], after_left[1])
    flat_right = (after_right[0], after_right[1][0], after_right[1][1])
    assert all(jnp.allclose(a, 1.0) for a in flat_left)
    assert all(jnp.allclose(a, 1.0) for a in flat_right)
