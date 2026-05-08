"""Channel composition tests — paper §3.4 ⋄_ρ.

The trivial coupling (`IndependentChannelCoupling`) recovers tensor-product variation
`V_a ⊗ V_b`. Non-trivial couplings let one channel's parameter be conditioned on the other's
state.
"""

from __future__ import annotations

from dataclasses import dataclass

import jax
import jax.numpy as jnp
from jaxtyping import Array, Float

from emergent_systems import (
    ChannelCoupling,
    Distribution,
    Gaussian,
    IndependentChannelCoupling,
    PointMass,
    PRNGKey,
    Variation,
    compose_variation_channels,
)


@dataclass(frozen=True)
class GaussianMutation(Variation[Float[Array, "d"], Float[Array, ""]]):
    """`V(x, σ) = N(x, σ² I)`."""

    def __call__(
        self, state: Float[Array, "d"], params: Float[Array, ""]
    ) -> Distribution[Float[Array, "d"]]:
        return Gaussian(loc=state, scale=jnp.full_like(state, params))


@dataclass(frozen=True)
class ConstantPointMass(Variation[Float[Array, "d"], Float[Array, ""]]):
    """A degenerate variation that always returns its current state."""

    def __call__(
        self, state: Float[Array, "d"], params: Float[Array, ""]
    ) -> Distribution[Float[Array, "d"]]:
        del params
        return PointMass(value=state)


def test_independent_coupling_returns_inputs_unchanged():
    coupling = IndependentChannelCoupling()
    state_a = jnp.zeros((2,))
    state_b = jnp.zeros((3,))
    params_a = jnp.asarray(0.1)
    params_b = jnp.asarray(0.5)
    out_a, out_b = coupling.sample(jax.random.key(0), state_a, state_b, params_a, params_b)
    assert jnp.allclose(out_a, params_a)
    assert jnp.allclose(out_b, params_b)


def test_compose_with_independent_coupling_samples_each_component():
    """With IndependentChannelCoupling, the composed distribution samples each V independently."""
    composed = compose_variation_channels(
        variation_a=ConstantPointMass(),
        variation_b=GaussianMutation(),
        coupling=IndependentChannelCoupling(),
    )

    state_a = jnp.array([1.0, 2.0])
    state_b = jnp.array([10.0, 20.0])
    distribution = composed((state_a, state_b), (jnp.asarray(0.0), jnp.asarray(0.5)))
    sample = distribution.sample(jax.random.key(0))

    a, b = sample
    assert jnp.allclose(a, state_a), "constant channel A should reproduce input"
    assert b.shape == state_b.shape


@dataclass(frozen=True)
class ConditionalCoupling(
    ChannelCoupling[Float[Array, "d"], Float[Array, "d"], Float[Array, ""], Float[Array, ""]]
):
    """A non-trivial coupling: B's mutation scale is conditioned on A's state norm."""

    def sample(
        self,
        key: PRNGKey,
        state_a: Float[Array, "d"],
        state_b: Float[Array, "d"],
        params_a: Float[Array, ""],
        params_b: Float[Array, ""],
    ) -> tuple[Float[Array, ""], Float[Array, ""]]:
        del key, state_b, params_b
        return params_a, jnp.linalg.norm(state_a)


def test_nontrivial_coupling_overrides_b_params():
    composed = compose_variation_channels(
        variation_a=ConstantPointMass(),
        variation_b=GaussianMutation(),
        coupling=ConditionalCoupling(),
    )
    state_a = jnp.array([3.0, 4.0])  # norm = 5
    state_b = jnp.array([0.0, 0.0])
    distribution = composed((state_a, state_b), (jnp.asarray(0.0), jnp.asarray(0.0)))

    # B's effective scale is 5 (the norm of A). After many samples, sample variance ~ 25.
    keys = jax.random.split(jax.random.key(42), 1024)
    samples = jax.vmap(distribution.sample)(keys)
    _, b_samples = samples
    sample_var = jnp.var(b_samples)
    # Expected variance is 5^2 = 25; loose tolerance for 1024 draws.
    assert 15.0 < float(sample_var) < 40.0
