"""Finite positive measures over the substrate state space.

Paper §3.1: a population is `μ ∈ M+(X)`, the type of finite positive measures on the substrate
state space. Viability has signature `F : M+(X) → M+(X)`. The lifted operators on the joint
state space `Z = X × M+(X)` mention `Φ_* μ` (paper line 285), the push-forward of μ along Φ.

Two concrete representations cover the cases the paper distinguishes:

* `WeightedSamples` — explicit population, batched states + nonneg weights. This is the natural
  representation for swarms, digital organisms, programs, agents.
* `ImplicitInSubstrate` — the substrate-as-population paradigm (Lenia, NCA, Flow-Lenia) where μ
  is encoded in the state itself. Paper §3.1 line 289: `Φ_* μ` is then the identity.

Push-forward is split into deterministic and stochastic methods. The stochastic case requires
a PRNG key and changes weight semantics (each particle's offspring is a single sample, so
the pushed-forward measure is a fresh empirical approximation), and conflating the two leads
to subtle bugs under jit.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

import jax
import jax.numpy as jnp
from jaxtyping import Array, Float

from emergent_systems._types import PRNGKey


@runtime_checkable
class Population[State](Protocol):
    """A finite positive measure on the substrate state space — paper: μ ∈ M+(X)."""

    @property
    def total_mass(self) -> Float[Array, ""]: ...

    def pushforward_deterministic(
        self,
        dynamics: Callable[[State], State],
    ) -> Population[State]:
        """Push the measure along a deterministic map — paper: Φ_* μ when Φ is deterministic."""
        ...

    def pushforward_stochastic(
        self,
        key: PRNGKey,
        kernel: Callable[[PRNGKey, State], State],
    ) -> Population[State]:
        """Push the measure along a stochastic kernel.

        Each particle (or implicit field cell) is updated by drawing one sample from the
        kernel. The result is an empirical approximation to the true `μ * Φ` (kernel
        composition); higher-fidelity approximations are out of scope for the scaffold.
        """
        ...


# ---------------------------------------------------------------------------
# Explicit case: WeightedSamples (paper: empirical measure with nonneg weights).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WeightedSamples[State](Population[State]):
    """An empirical measure: a batch of states with nonneg weights — paper: M+(X), explicit case.

    The leading axis of `states` (which is a batched pytree) is the population axis, with the
    same length as `weights`. The type parameter `State` refers to the per-particle type; the
    actual stored field is a batched pytree of leading-axis N, by convention.
    """

    states: State
    """Batched pytree; leading axis is the population axis."""

    weights: Float[Array, "N"]
    """Nonneg weight per particle; total mass is `sum(weights)`."""

    @property
    def total_mass(self) -> Float[Array, ""]:
        return jnp.sum(self.weights)

    def pushforward_deterministic(
        self,
        dynamics: Callable[[State], State],
    ) -> WeightedSamples[State]:
        new_states = jax.vmap(dynamics)(self.states)
        return WeightedSamples(states=new_states, weights=self.weights)

    def pushforward_stochastic(
        self,
        key: PRNGKey,
        kernel: Callable[[PRNGKey, State], State],
    ) -> WeightedSamples[State]:
        n = self.weights.shape[0]
        keys = jax.random.split(key, n)
        new_states = jax.vmap(kernel)(keys, self.states)
        return WeightedSamples(states=new_states, weights=self.weights)


# ---------------------------------------------------------------------------
# Implicit case: ImplicitInSubstrate (paper: substrate-as-population paradigms).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ImplicitInSubstrate[State](Population[State]):
    """The substrate-as-population paradigm — paper §3.1 line 289.

    The population is encoded in the substrate state itself (Lenia mass field, NCA cell values,
    Flow-Lenia density). Φ updates the substrate; the pushed-forward measure is therefore the
    identity — Φ_* μ is the same implicit measure, now reading off the new state.

    `total_mass` defaults to 1, but a substrate-specific instance may override it (Flow-Lenia's
    mass-conservation reduction reports the literal lattice mass).
    """

    nominal_mass: Float[Array, ""] = field(default_factory=lambda: jnp.asarray(1.0))

    @property
    def total_mass(self) -> Float[Array, ""]:
        return self.nominal_mass

    def pushforward_deterministic(
        self,
        dynamics: Callable[[State], State],
    ) -> ImplicitInSubstrate[State]:
        del dynamics
        return self

    def pushforward_stochastic(
        self,
        key: PRNGKey,
        kernel: Callable[[PRNGKey, State], State],
    ) -> ImplicitInSubstrate[State]:
        del key, kernel
        return self
