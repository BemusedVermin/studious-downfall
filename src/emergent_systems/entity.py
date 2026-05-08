"""Entities: supporting sets and scale projections.

Paper §3.2: an entity is a pair `e = (S, π)` consisting of a supporting set `S ⊆ P` of
substrate sites and a scale projection `π : ∏_{p∈S} X_p → Y_S`. The pair separates *what*
supports the entity (the sites) from *the scale of description* committed to (the projection).

The paper specifies three properties (E1, E2, E3) and asks the implementer to verify them:

* (E1) Persistence — information closure of `π` against the substrate's complement.
* (E2) Boundedness — `1 ≤ |S| < ∞`.
* (E3) Compositionality — disjoint entities can be combined hierarchically.

(E1) requires a conditional-mutual-information estimator over substrate trajectories and is
inherently sample-based; the framework exposes it as a hook rather than implementing a
specific estimator. (E2) is mechanical. (E3) is a constructor.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

import jax.numpy as jnp
from jaxtyping import Array, Float, Int

from emergent_systems.population import Population


@dataclass(frozen=True)
class Entity[State, Feature]:
    """An entity — paper: e = (S, π).

    Type parameters:
        State:    the substrate state space — paper: X.
        Feature:  the scale-projection codomain — paper: Y_S, the macroscale description.
    """

    supporting_set: Int[Array, "K"]
    """Indices of the substrate sites supporting this entity — paper: S ⊆ P.

    Sites are integers; for multi-axis substrates (a 2D lattice, a graph) the implementer is
    responsible for choosing a flattening convention.
    """

    scale_projection: Callable[[State], Feature]
    """Paper: π : ∏_{p∈S} X_p → Y_S.

    The function may close over `supporting_set` and slice the full state internally; or it may
    accept the full state and project. Both styles are valid — the framework only uses the
    callable's output.
    """


# ---------------------------------------------------------------------------
# (E2) Boundedness — paper §3.2.
# ---------------------------------------------------------------------------


def verify_boundedness(entity: Entity[Any, Any]) -> bool:
    """Check (E2): the supporting set has finite, nonzero size.

    Returns True iff `1 ≤ |S| < ∞`. Trivially satisfied by any finite array; left here as a
    named predicate so the conformance check (`spec.py`) has something concrete to call.
    """
    n = entity.supporting_set.shape[0]
    return 1 <= n < jnp.iinfo(jnp.int32).max


# ---------------------------------------------------------------------------
# (E1) Persistence — paper §3.2 Definition 3.2.1.
# ---------------------------------------------------------------------------


type ConditionalMutualInformationEstimator = Callable[
    [Float[Array, "T ..."], Float[Array, "T ..."], Float[Array, "T ..."]],
    Float[Array, ""],
]
"""Estimator of `I(A; B | C)` from three batched-time-series arguments.

Estimation strategy is implementer-defined (k-NN, kernel, neural). The framework takes one as
a parameter rather than committing to a specific estimator — both because no choice dominates
in practice and because the choice has measurable effect on E1 outcomes.
"""


def verify_persistence_estimate(
    *,
    projection_history: Float[Array, "T ..."],
    inside_history: Float[Array, "T ..."],
    outside_history: Float[Array, "T ..."],
    tau: int,
    tolerance: float,
    estimator: ConditionalMutualInformationEstimator,
) -> bool:
    """Check (E1): the projection's future is predicted internally, conditional on the outside.

    Verifies:
        I(π(x_S^{t+τ}); π(x_S^t) | x_{S^c}^t)  ≥  I(π(x_S^{t+τ}); x_S^t) − ε

    using a user-supplied estimator. The two MI terms are estimated independently and compared.

    PERF[entity-persistence-estimation]: information-theoretic estimators on long trajectories
    are quadratic-or-worse in T and dominate entity-detection cost. Port to a faster language
    (or to GPU-resident k-NN MI) for production use.
    """
    if projection_history.shape[0] <= tau:
        raise ValueError(
            f"trajectory length T={projection_history.shape[0]} must exceed tau={tau}."
        )

    proj_future = projection_history[tau:]
    proj_now = projection_history[:-tau]
    inside_now = inside_history[:-tau]
    outside_now = outside_history[:-tau]

    cmi_internal = estimator(proj_future, proj_now, outside_now)
    mi_full_inside = estimator(proj_future, inside_now, jnp.zeros_like(outside_now[..., :0]))
    return bool(cmi_internal >= mi_full_inside - tolerance)


# ---------------------------------------------------------------------------
# (E3) Compositionality — paper §3.2.
# ---------------------------------------------------------------------------


def compose_entities[State](
    entities: Sequence[Entity[State, Any]],
) -> Entity[State, tuple[Any, ...]]:
    """Combine disjoint entities into a hierarchical one — paper §3.2 (E3).

    Returns an entity whose supporting set is the union of the components' supporting sets,
    and whose scale projection is the tuple of the components' projections.

    The caller is responsible for checking (E1) at the *joint* scale (paper line 491-494). We
    do not check (E1) here because doing so requires a trajectory and an estimator.
    """
    if not entities:
        raise ValueError("compose_entities requires at least one entity.")

    union = jnp.concatenate([e.supporting_set for e in entities])
    if union.shape[0] != jnp.unique(union).shape[0]:
        raise ValueError(
            "Components' supporting sets are not disjoint; (E3) requires disjointness."
        )

    projections = tuple(e.scale_projection for e in entities)

    def joint_projection(state: State) -> tuple[Any, ...]:
        return tuple(p(state) for p in projections)

    return Entity(supporting_set=union, scale_projection=joint_projection)


# ---------------------------------------------------------------------------
# Entity detection — implementer-supplied.
# ---------------------------------------------------------------------------


@runtime_checkable
class EntityDetector[State](Protocol):
    """Detects entities in a (state, population) pair — paper §3.2 implementation note.

    For lattice substrates this is typically a connected-component scan above a threshold; for
    particles, a clustering step; for program substrates, the identity (each program is an
    atomic entity).

    PERF[entity-detection]: paper §3.2 notes both sub-steps (search over S, search over π) are
    embarrassingly parallel across candidates. Pure-Python implementations are usually a
    bottleneck; consider GPU connected-component algorithms or batched cluster detectors.
    """

    def __call__(
        self,
        state: State,
        population: Population[State],
    ) -> Sequence[Entity[State, Any]]: ...
