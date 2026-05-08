"""Shared fixtures: a minimal toy system used by the pipeline and conformance tests.

The toy is small but exercises every slot:

* Substrate:    binary scalar in {0, 1}; Φ deterministically flips.
* Variation:    Dirac on the input (no-op).
* Viability:    identity.
* Topology:     trivial — no hyperedges.
* Observer:     counts ticks; window=1, scalar output.
* Population:   ImplicitInSubstrate (μ encoded in state).

Implicit-population mode means V_T short-circuits to identity (paper §3.1 line 289), so
detect_entities and hyperedge_params can be `None`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import jax.numpy as jnp
import pytest
from jaxtyping import Array, Float, Int

from emergent_systems import (
    Distribution,
    Entity,
    Hypergraph,
    ImplicitInSubstrate,
    InteractionTopology,
    JointState,
    PointMass,
    Population,
    PRNGKey,
    StatefulObserver,
    Substrate,
    System,
    TickIndex,
    Variation,
    ViabilityFilter,
    WindowedTrajectory,
)


@dataclass(frozen=True)
class BinaryFlipSubstrate(Substrate[Int[Array, ""], None]):
    dynamics_param_space: type[None] = type(None)
    default_dynamics_param: None = None

    def dynamics(self, key: PRNGKey, param: None, state: Int[Array, ""]) -> Int[Array, ""]:
        del key, param
        return 1 - state

    def initial_state(self, key: PRNGKey) -> Int[Array, ""]:
        del key
        return jnp.asarray(0, dtype=jnp.int32)

    def initial_population(self, key: PRNGKey) -> Population[Int[Array, ""]]:
        del key
        return ImplicitInSubstrate()


@dataclass(frozen=True)
class IdentityVariation(Variation[Int[Array, ""], None]):
    def __call__(self, state: Int[Array, ""], params: None) -> Distribution[Int[Array, ""]]:
        del params
        return PointMass(value=state)


@dataclass(frozen=True)
class IdentityViability(ViabilityFilter[Int[Array, ""]]):
    def __call__(self, population: Population[Int[Array, ""]]) -> Population[Int[Array, ""]]:
        return population


@dataclass(frozen=True)
class EmptyTopology(InteractionTopology):
    def at(
        self,
        tick: TickIndex,
        entities: Sequence[Entity[Any, Any]],
    ) -> Hypergraph:
        del tick, entities
        return Hypergraph(edges=())


@dataclass(frozen=True)
class TickCountingObserver(StatefulObserver[Int[Array, ""], Int[Array, ""]]):
    window_length: int = 1

    def initial_state(self, key: PRNGKey) -> Int[Array, ""]:
        del key
        return jnp.asarray(0, dtype=jnp.int32)

    def observe(
        self,
        window: WindowedTrajectory[Int[Array, ""]],
        observer_state: Int[Array, ""],
    ) -> tuple[Float[Array, "k"], Int[Array, ""]]:
        del window
        new_count = observer_state + 1
        return jnp.asarray([float(new_count)]), new_count


@pytest.fixture
def toy_system() -> System[Int[Array, ""], None, None, Int[Array, ""]]:
    return System(
        substrate=BinaryFlipSubstrate(),
        variation=IdentityVariation(),
        viability=IdentityViability(),
        topology=EmptyTopology(),
        observer=TickCountingObserver(),
    )


@pytest.fixture
def toy_initial_state() -> JointState[Int[Array, ""]]:
    return JointState(
        state=jnp.asarray(0, dtype=jnp.int32),
        population=ImplicitInSubstrate(),
    )
