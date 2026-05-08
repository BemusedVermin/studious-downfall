"""Substrates and their composition operators.

Paper §3.3: a substrate is a triple `X = (X, Φ, μ_0)` — state space, dynamics, initial measure.
The framework is permissive about what `X` is (lattice, particle field, program space), so
this module exposes a `Substrate` protocol that the implementer fills in.

Two composition operators (paper §3.3):

* `compose_substrates_independently` — paper: `⊠`, the free product. Cartesian state, dynamics
  applied componentwise, no cross-substrate coupling.
* `compose_substrates_coupled` — paper: `⊠_κ`. A `Coupling` provides the cross-substrate maps
  `κ_{i→j} : X_i → Param(Φ_j)` that re-shape each component's dynamics from the other's state.

Coupled composition is the paper's foundation for modular heterogeneous systems
(biological ⊠ atmospheric ⊠ cultural — paper §3.3 implementation note). Each component keeps
its own kernel; the coupling kernels are independent code paths.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import jax

from emergent_systems._types import PRNGKey
from emergent_systems.population import Population


@runtime_checkable
class Substrate[State, DynamicsParam](Protocol):
    """A substrate — paper: X = (X, Φ, μ_0).

    Type parameters:
        State:           the substrate state space — paper: X.
        DynamicsParam:   the parameter space that re-shapes the dynamics — paper: Param(Φ).
                         Coupled composition (`⊠_κ`) writes into this slot.
    """

    dynamics_param_space: type[DynamicsParam]
    """The parameter type that `dynamics` accepts — paper: Param(Φ). Required for `⊠_κ`."""

    default_dynamics_param: DynamicsParam
    """The parameter used when the substrate is run uncoupled."""

    def dynamics(
        self,
        key: PRNGKey,
        param: DynamicsParam,
        state: State,
    ) -> State:
        """Advance the substrate by one tick — paper: Φ.

        The framework allows Φ to be deterministic or stochastic; both signatures collapse to
        this one because deterministic implementations simply ignore `key`.
        """
        ...

    def initial_state(self, key: PRNGKey) -> State:
        """Sample an initial state — paper: x_0."""
        ...

    def initial_population(self, key: PRNGKey) -> Population[State]:
        """Sample an initial population measure — paper: μ_0."""
        ...


# ---------------------------------------------------------------------------
# Coupling between two substrates — paper: κ.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Coupling[StateA, StateB, ParamA, ParamB]:
    """A cross-substrate coupling datum — paper: κ = (κ_{1→2}, κ_{2→1}).

    Each map re-parameterises the *other* substrate's dynamics from this one's current state
    (paper §3.3 line 401). Free composition (no coupling) is recovered by the
    `compose_substrates_independently` factory below.
    """

    a_to_b: Callable[[StateA], ParamB]
    """Paper: κ_{A→B} : X_A → Param(Φ_B). Re-parameterises B's dynamics from A's state."""

    b_to_a: Callable[[StateB], ParamA]
    """Paper: κ_{B→A} : X_B → Param(Φ_A). Re-parameterises A's dynamics from B's state."""


# ---------------------------------------------------------------------------
# Composition operators.
#
# Both produce a substrate over `tuple[StateA, StateB]` with parameter space
# `tuple[ParamA, ParamB]`. Heterogeneous chains (paper §3.3 'biological ⊠ atmospheric ⊠ LLM')
# are built by repeated application; the resulting nested-tuple state spaces match the
# 'associativity up to canonical isomorphism' from the paper's Proposition 3.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ComposedSubstrate[StateA, StateB, ParamA, ParamB](
    Substrate[tuple[StateA, StateB], tuple[ParamA, ParamB]]
):
    a: Substrate[StateA, ParamA]
    b: Substrate[StateB, ParamB]
    coupling: Coupling[StateA, StateB, ParamA, ParamB] | None
    """`None` for free composition (paper: ⊠), else paper: ⊠_κ."""

    @property
    def dynamics_param_space(self) -> type[tuple[ParamA, ParamB]]:  # type: ignore[override]
        return tuple  # type: ignore[return-value]

    @property
    def default_dynamics_param(self) -> tuple[ParamA, ParamB]:  # type: ignore[override]
        return (self.a.default_dynamics_param, self.b.default_dynamics_param)

    def dynamics(
        self,
        key: PRNGKey,
        param: tuple[ParamA, ParamB],
        state: tuple[StateA, StateB],
    ) -> tuple[StateA, StateB]:
        x_a, x_b = state
        key_a, key_b = jax.random.split(key, 2)

        if self.coupling is None:
            param_a, param_b = param
        else:
            # Paper §3.3 line 405-407: each component's parameter is replaced by the
            # cross-substrate coupling, evaluated on the *other* component's current state.
            param_a = self.coupling.b_to_a(x_b)
            param_b = self.coupling.a_to_b(x_a)

        return (
            self.a.dynamics(key_a, param_a, x_a),
            self.b.dynamics(key_b, param_b, x_b),
        )

    def initial_state(self, key: PRNGKey) -> tuple[StateA, StateB]:
        key_a, key_b = jax.random.split(key, 2)
        return (self.a.initial_state(key_a), self.b.initial_state(key_b))

    def initial_population(self, key: PRNGKey) -> Population[tuple[StateA, StateB]]:
        # The composed initial population is constructed from each component's. The paper's
        # free-composition definition uses the product measure μ_0^(1) ⊗ μ_0^(2); for two
        # WeightedSamples populations the natural realisation is to zip them. Mixed-mode
        # composition (one implicit, one explicit) is currently not supported — a paired
        # implementer should provide an explicit join. See paper §3.8 worked example.
        del key
        raise NotImplementedError(
            "Composed initial populations are user-supplied in v1. Paper §3.3 free-composition "
            "uses the tensor product μ_0^(1) ⊗ μ_0^(2); pick an explicit Population type and "
            "construct it directly from the components."
        )


def compose_substrates_independently[StateA, StateB, ParamA, ParamB](
    a: Substrate[StateA, ParamA],
    b: Substrate[StateB, ParamB],
) -> Substrate[tuple[StateA, StateB], tuple[ParamA, ParamB]]:
    """Free composition — paper: ⊠ (Definition 3.3.1).

    No cross-substrate coupling; each component's dynamics runs with its own default
    parameter. Recovers the Cartesian product as a degenerate case of `⊠_κ`.
    """
    return _ComposedSubstrate(a=a, b=b, coupling=None)


def compose_substrates_coupled[StateA, StateB, ParamA, ParamB](
    a: Substrate[StateA, ParamA],
    b: Substrate[StateB, ParamB],
    coupling: Coupling[StateA, StateB, ParamA, ParamB],
) -> Substrate[tuple[StateA, StateB], tuple[ParamA, ParamB]]:
    """Coupled composition — paper: ⊠_κ (Definition 3.3.2).

    The `coupling` re-parameterises each component's dynamics from the *other* component's
    state. The resulting substrate's `dynamics(key, param, state)` ignores its `param`
    argument because the coupling fully determines the per-component parameters at each tick.
    """
    return _ComposedSubstrate(a=a, b=b, coupling=coupling)
