"""Variation operators and channel composition.

Paper §3.4: a variation operator has signature

    V : X × Θ → P(X)

— it accepts a substrate state and a parameter (mutation rate, recombination probability,
gradient step size, prompt-perturbation distribution, …) and returns a probability measure
over the next-state space. Stochastic, deterministic, and gradient-based variation are unified
by allowing V to be a Markov kernel; deterministic variation returns a `PointMass`.

Channel composition (paper Definition 3.4.1):

    (V_1 ⋄_ρ V_2)((x_1, x_2), (θ_1, θ_2))
        = ∫ V_1(x_1, θ_1') V_2(x_2, θ_2') ρ(dθ_1', dθ_2' | x_1, x_2, θ_1, θ_2)

The coupling rule `ρ` lets one channel's sampling condition another's — gene–culture
co-evolution, niche construction, stigmergic coupling. Trivial `ρ` (independent product)
recovers the tensor product `V_1 ⊗ V_2`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import jax

from emergent_systems._types import PRNGKey
from emergent_systems.distribution import Distribution


@runtime_checkable
class Variation[State, Params](Protocol):
    """A variation operator — paper: V : X × Θ → P(X).

    Type parameters:
        State:   the substrate state space — paper: X.
        Params:  the parameter space for this variation channel — paper: Θ.
    """

    def __call__(self, state: State, params: Params) -> Distribution[State]: ...


# ---------------------------------------------------------------------------
# Channel composition — paper: ⋄_ρ.
# ---------------------------------------------------------------------------


@runtime_checkable
class ChannelCoupling[StateA, StateB, ParamsA, ParamsB](Protocol):
    """A coupling rule between two variation channels — paper: ρ.

    Given the current joint state `(x_a, x_b)` and the channels' nominal parameters
    `(θ_a, θ_b)`, samples a new pair of parameters `(θ_a', θ_b')` that the channels then use
    on this tick.
    """

    def sample(
        self,
        key: PRNGKey,
        state_a: StateA,
        state_b: StateB,
        params_a: ParamsA,
        params_b: ParamsB,
    ) -> tuple[ParamsA, ParamsB]: ...


@dataclass(frozen=True)
class IndependentChannelCoupling[StateA, StateB, ParamsA, ParamsB](
    ChannelCoupling[StateA, StateB, ParamsA, ParamsB]
):
    """The trivial coupling — paper: ρ as the independent product.

    Recovers tensor-product variation `V_a ⊗ V_b`. Useful as a default and as a baseline for
    ablations of more complex couplings.
    """

    def sample(
        self,
        key: PRNGKey,
        state_a: StateA,
        state_b: StateB,
        params_a: ParamsA,
        params_b: ParamsB,
    ) -> tuple[ParamsA, ParamsB]:
        del key, state_a, state_b
        return (params_a, params_b)


@dataclass(frozen=True)
class _ComposedDistribution[StateA, StateB, ParamsA, ParamsB](
    Distribution[tuple[StateA, StateB]]
):
    """The distribution emitted by a composed variation channel — paper: V_1 ⋄_ρ V_2.

    Sampling proceeds in three keyed steps: draw the coupled `(θ_a', θ_b')` from `ρ`, then
    construct each component's distribution at the new parameters, then draw one state from
    each and return the pair.
    """

    state_a: StateA
    state_b: StateB
    params_a: ParamsA
    params_b: ParamsB
    variation_a: Variation[StateA, ParamsA]
    variation_b: Variation[StateB, ParamsB]
    coupling: ChannelCoupling[StateA, StateB, ParamsA, ParamsB]

    def sample(self, key: PRNGKey) -> tuple[StateA, StateB]:
        key_rho, key_a, key_b = jax.random.split(key, 3)
        params_a_prime, params_b_prime = self.coupling.sample(
            key_rho, self.state_a, self.state_b, self.params_a, self.params_b
        )
        dist_a = self.variation_a(self.state_a, params_a_prime)
        dist_b = self.variation_b(self.state_b, params_b_prime)
        return (dist_a.sample(key_a), dist_b.sample(key_b))

    def log_prob(self, state: tuple[StateA, StateB]) -> object:
        del state
        raise NotImplementedError(
            "log_prob on a ⋄_ρ-composed distribution requires marginalising the coupling kernel; "
            "this is well-defined only for special ρ. Provide a typed subclass if you need it."
        )


@dataclass(frozen=True)
class _ComposedVariation[StateA, StateB, ParamsA, ParamsB](
    Variation[tuple[StateA, StateB], tuple[ParamsA, ParamsB]]
):
    variation_a: Variation[StateA, ParamsA]
    variation_b: Variation[StateB, ParamsB]
    coupling: ChannelCoupling[StateA, StateB, ParamsA, ParamsB]

    def __call__(
        self,
        state: tuple[StateA, StateB],
        params: tuple[ParamsA, ParamsB],
    ) -> Distribution[tuple[StateA, StateB]]:
        return _ComposedDistribution(
            state_a=state[0],
            state_b=state[1],
            params_a=params[0],
            params_b=params[1],
            variation_a=self.variation_a,
            variation_b=self.variation_b,
            coupling=self.coupling,
        )


def compose_variation_channels[StateA, StateB, ParamsA, ParamsB](
    variation_a: Variation[StateA, ParamsA],
    variation_b: Variation[StateB, ParamsB],
    coupling: ChannelCoupling[StateA, StateB, ParamsA, ParamsB],
) -> Variation[tuple[StateA, StateB], tuple[ParamsA, ParamsB]]:
    """Compose two variation channels under a coupling rule — paper: V_1 ⋄_ρ V_2.

    Pass `IndependentChannelCoupling()` for the trivial case (recovers `V_1 ⊗ V_2`).
    """
    return _ComposedVariation(
        variation_a=variation_a,
        variation_b=variation_b,
        coupling=coupling,
    )
