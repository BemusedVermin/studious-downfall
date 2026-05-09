"""Tests for code paths that the slot-focused suites don't reach.

The pipeline tests exercise the implicit-population short-circuit; this file covers the
explicit-population orchestration paths (V_T construction, multiplex), the entity-property
helpers (E2/E3/E1), the closure-operator verifier, composed-substrate helpers, and the
multiplex topology weight check.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import pytest
from jaxtyping import Array, Float, Int

from emergent_systems import (
    Distribution,
    Entity,
    Hyperedge,
    Hypergraph,
    InteractionTopology,
    JointState,
    MultiplexLayer,
    MultiplexTopology,
    PointMass,
    Population,
    PRNGKey,
    StatefulObserver,
    Substrate,
    System,
    SystemSpec,
    TickIndex,
    Variation,
    ViabilityFilter,
    WeightedSamples,
    compose_entities,
    compose_substrates_independently,
    run,
    step,
    verify_boundedness,
    verify_is_closure_operator,
    verify_persistence_estimate,
)

# ---------------------------------------------------------------------------
# verify_is_closure_operator — viability.py lines 129-143.
# ---------------------------------------------------------------------------


def _frozenset_subset(a: frozenset[int], b: frozenset[int]) -> bool:
    return a.issubset(b)


def test_closure_verifier_accepts_a_closure_operator():
    elements = [frozenset(), frozenset({1}), frozenset({1, 2}), frozenset({1, 2, 3})]

    def identity_closure(s: frozenset[int]) -> frozenset[int]:
        return s

    assert verify_is_closure_operator(identity_closure, elements, _frozenset_subset)


def test_closure_verifier_rejects_non_extensive():
    elements = [frozenset({1}), frozenset({1, 2})]

    def shrinks(s: frozenset[int]) -> frozenset[int]:
        del s
        return frozenset()

    assert not verify_is_closure_operator(shrinks, elements, _frozenset_subset)


def test_closure_verifier_rejects_non_idempotent():
    elements = [frozenset({1}), frozenset({1, 2})]

    def adds_one_each_time(s: frozenset[int]) -> frozenset[int]:
        # closure({1}) = {1, 99}; closure(closure({1})) = {1, 99, 100} — not idempotent.
        if s == frozenset({1}):
            return frozenset({1, 99})
        if s == frozenset({1, 99}):
            return frozenset({1, 99, 100})
        return s | {-1}

    assert not verify_is_closure_operator(adds_one_each_time, elements, _frozenset_subset)


def test_closure_verifier_rejects_non_monotonic():
    # Three sample points so the closure is total, idempotent, and extensive on the sample
    # but fails monotonicity: {1} ⊑ {1,2} yet closure({1})={1,2,3} ⊄ closure({1,2})={1,2}.
    # Including {1,2,3} in `elements` lets the idempotence loop (which runs first) pass on the
    # image of {1} so the verifier reaches the monotonicity check rather than short-circuiting
    # on idempotence.
    elements = [frozenset({1}), frozenset({1, 2}), frozenset({1, 2, 3})]

    def antitone(s: frozenset[int]) -> frozenset[int]:
        if s == frozenset({1}):
            return frozenset({1, 2, 3})
        if s == frozenset({1, 2}):
            return frozenset({1, 2})
        if s == frozenset({1, 2, 3}):
            return frozenset({1, 2, 3})
        return s

    assert not verify_is_closure_operator(antitone, elements, _frozenset_subset)


# ---------------------------------------------------------------------------
# entity.py — verify_boundedness, compose_entities, verify_persistence_estimate.
# ---------------------------------------------------------------------------


def test_verify_boundedness_true_on_normal_entity():
    entity = Entity(supporting_set=jnp.asarray([0, 1, 2]), scale_projection=lambda s: s)
    assert verify_boundedness(entity)


def test_verify_boundedness_false_on_empty_set():
    entity = Entity(supporting_set=jnp.asarray([], dtype=jnp.int32), scale_projection=lambda s: s)
    assert not verify_boundedness(entity)


def test_compose_entities_unions_supports_and_tuples_projections():
    a = Entity(supporting_set=jnp.asarray([0, 1]), scale_projection=lambda s: ("A", s))
    b = Entity(supporting_set=jnp.asarray([2, 3]), scale_projection=lambda s: ("B", s))
    composed = compose_entities([a, b])
    assert composed.supporting_set.shape == (4,)
    out = composed.scale_projection("x")
    assert out == (("A", "x"), ("B", "x"))


def test_compose_entities_rejects_overlapping_supports():
    a = Entity(supporting_set=jnp.asarray([0, 1]), scale_projection=lambda s: s)
    b = Entity(supporting_set=jnp.asarray([1, 2]), scale_projection=lambda s: s)
    with pytest.raises(ValueError, match="disjoint"):
        compose_entities([a, b])


def test_compose_entities_rejects_empty_input():
    with pytest.raises(ValueError, match="at least one"):
        compose_entities([])


def test_verify_persistence_estimate_uses_user_estimator():
    """The verifier compares two MI estimates supplied by the user; here we stub them."""

    def estimator(
        a: Float[Array, "T"],
        b: Float[Array, "T"],
        c: Float[Array, "T"],
    ) -> Float[Array, ""]:
        del a, b
        # First call receives `outside_now` of shape (T-tau,); second call receives an empty
        # conditioning array of shape (0,) from the `[..., :0]` slice in verify_persistence_estimate.
        return jnp.asarray(1.0) if c.shape[-1] > 0 else jnp.asarray(0.0)

    history = jnp.zeros((10,))
    assert verify_persistence_estimate(
        projection_history=history,
        inside_history=history,
        outside_history=history,
        tau=1,
        tolerance=0.0,
        estimator=estimator,
    )


def test_verify_persistence_estimate_rejects_short_trajectory():
    history = jnp.zeros((3,))
    with pytest.raises(ValueError, match="must exceed tau"):
        verify_persistence_estimate(
            projection_history=history,
            inside_history=history,
            outside_history=history,
            tau=5,
            tolerance=0.0,
            estimator=lambda *_: jnp.asarray(0.0),
        )


# ---------------------------------------------------------------------------
# system.py — explicit-population V_T construction (build_population_variation),
# multiplex variant (build_population_variation_multiplex), and _default_focal_entity_params.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _ScalarSubstrateExplicitPop(Substrate[Float[Array, ""], None]):
    """Scalar substrate; initial population is two unit-weight particles at 0.5 and 1.5."""

    dynamics_param_space: type[None] = type(None)
    default_dynamics_param: None = None

    def dynamics(self, key: PRNGKey, param: None, state: Float[Array, ""]) -> Float[Array, ""]:
        del key, param
        return state + jnp.asarray(0.0)  # identity, but keeps the call shape honest

    def initial_state(self, key: PRNGKey) -> Float[Array, ""]:
        del key
        return jnp.asarray(0.0)

    def initial_population(self, key: PRNGKey) -> Population[Float[Array, ""]]:
        del key
        return WeightedSamples(
            states=jnp.asarray([0.5, 1.5]),
            weights=jnp.asarray([1.0, 1.0]),
        )


@dataclass(frozen=True)
class _PointVariation(Variation[Float[Array, ""], Float[Array, ""]]):
    """Returns a Dirac on `state + params` so V_T's outputs are easy to assert."""

    def __call__(
        self,
        state: Float[Array, ""],
        params: Float[Array, ""],
    ) -> Distribution[Float[Array, ""]]:
        return PointMass(value=state + params)


@dataclass(frozen=True)
class _FocalEntityVariation(Variation[Float[Array, ""], Entity[Float[Array, ""], Any]]):
    """Variation whose params are an Entity — accepts the focal-entity default from V_T."""

    def __call__(
        self,
        state: Float[Array, ""],
        params: Entity[Float[Array, ""], Any],
    ) -> Distribution[Float[Array, ""]]:
        feature = params.scale_projection(state)
        return PointMass(value=state + jnp.asarray(feature))


@dataclass(frozen=True)
class _IdentityViabilityFloat(ViabilityFilter[Float[Array, ""]]):
    def __call__(
        self,
        population: Population[Float[Array, ""]],
    ) -> Population[Float[Array, ""]]:
        return population


@dataclass(frozen=True)
class _OnePerEntityDetector:
    """Wraps each population particle in a single-site Entity with a unit-feature projection."""

    def __call__(
        self,
        state: Float[Array, ""],
        population: Population[Float[Array, ""]],
    ) -> Sequence[Entity[Float[Array, ""], Float[Array, ""]]]:
        del state
        if not isinstance(population, WeightedSamples):
            return ()
        n = int(population.weights.shape[0])
        return [
            Entity(
                supporting_set=jnp.asarray([i]),
                scale_projection=lambda _s, i=i: jnp.asarray(float(i + 1)),
            )
            for i in range(n)
        ]


@dataclass(frozen=True)
class _SelfLoopTopology(InteractionTopology):
    """One unit-weight self-loop hyperedge per detected entity."""

    def at(
        self,
        tick: TickIndex,
        entities: Sequence[Entity[Any, Any]],
    ) -> Hypergraph:
        del tick
        return Hypergraph(
            edges=tuple(
                Hyperedge(members=jnp.asarray([i]), weight=jnp.asarray(1.0))
                for i in range(len(entities))
            )
        )


@dataclass(frozen=True)
class _NoHyperedgesTopology(InteractionTopology):
    def at(
        self,
        tick: TickIndex,
        entities: Sequence[Entity[Any, Any]],
    ) -> Hypergraph:
        del tick, entities
        return Hypergraph(edges=())


@dataclass(frozen=True)
class _ZeroValuedObserver(StatefulObserver[Float[Array, ""], Int[Array, ""]]):
    window_length: int = 1

    def initial_state(self, key: PRNGKey) -> Int[Array, ""]:
        del key
        return jnp.asarray(0, dtype=jnp.int32)

    def observe(
        self,
        window: Any,
        observer_state: Int[Array, ""],
    ) -> tuple[Float[Array, "k"], Int[Array, ""]]:
        del window
        return jnp.asarray([0.0]), observer_state + 1


def _hyperedge_params_from_focal(
    entities: Sequence[Entity[Float[Array, ""], Float[Array, ""]]],
) -> Float[Array, ""]:
    """Use the focal entity's projection (called on a dummy state) as the variation param."""
    return entities[0].scale_projection(jnp.asarray(0.0))


def test_step_with_explicit_population_runs_v_t():
    """Drives build_population_variation's inner v_t closure for a non-implicit population."""
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_SelfLoopTopology(),
        observer=_ZeroValuedObserver(),
        detect_entities=_OnePerEntityDetector(),
        hyperedge_params=_hyperedge_params_from_focal,
        iteration_order=("variation",),
    )
    initial = JointState(
        state=jnp.asarray(0.0),
        population=WeightedSamples(
            states=jnp.asarray([0.5, 1.5]),
            weights=jnp.asarray([1.0, 1.0]),
        ),
    )
    after = step(system, initial, jax.random.key(0), tick=0)
    assert isinstance(after.population, WeightedSamples)
    # PointVariation samples state (0.0) + params (1.0 or 2.0) = 1.0, 2.0.
    assert after.population.states.shape == (2,)
    assert jnp.allclose(after.population.weights, jnp.asarray([1.0, 1.0]))


def test_step_with_explicit_population_handles_no_hyperedges():
    """Topology with zero edges → V_T returns an empty WeightedSamples."""
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_NoHyperedgesTopology(),
        observer=_ZeroValuedObserver(),
        detect_entities=_OnePerEntityDetector(),
        hyperedge_params=_hyperedge_params_from_focal,
        iteration_order=("variation",),
    )
    initial = JointState(
        state=jnp.asarray(0.0),
        population=WeightedSamples(
            states=jnp.asarray([0.5]),
            weights=jnp.asarray([1.0]),
        ),
    )
    after = step(system, initial, jax.random.key(0), tick=0)
    assert isinstance(after.population, WeightedSamples)
    assert after.population.weights.shape == (0,)


def test_apply_variation_rejects_explicit_population_without_detector():
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_SelfLoopTopology(),
        observer=_ZeroValuedObserver(),
        detect_entities=None,  # explicit population requires a detector
        iteration_order=("variation",),
    )
    initial = JointState(
        state=jnp.asarray(0.0),
        population=WeightedSamples(
            states=jnp.asarray([0.5]),
            weights=jnp.asarray([1.0]),
        ),
    )
    with pytest.raises(ValueError, match="detect_entities"):
        step(system, initial, jax.random.key(0), tick=0)


def test_run_with_explicit_population_records_trajectory():
    """End-to-end with WeightedSamples — exercises run's main loop alongside V_T."""
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_SelfLoopTopology(),
        observer=_ZeroValuedObserver(),
        detect_entities=_OnePerEntityDetector(),
        hyperedge_params=_hyperedge_params_from_focal,
        iteration_order=("dynamics", "variation", "viability"),
    )
    result = run(system, n_ticks=2, key=jax.random.key(0))
    assert len(result.trajectory) == 3


def test_step_with_multiplex_topology_runs_mixture():
    """Drives build_population_variation_multiplex via the MultiplexTopology branch."""
    layers = [
        MultiplexLayer(alpha=jnp.asarray(0.5), topology=_SelfLoopTopology()),
        MultiplexLayer(alpha=jnp.asarray(0.5), topology=_SelfLoopTopology()),
    ]
    multiplex = MultiplexTopology(layers=layers)
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=multiplex,
        observer=_ZeroValuedObserver(),
        detect_entities=_OnePerEntityDetector(),
        hyperedge_params=_hyperedge_params_from_focal,
        iteration_order=("variation",),
    )
    initial = JointState(
        state=jnp.asarray(0.0),
        population=WeightedSamples(
            states=jnp.asarray([0.5]),
            weights=jnp.asarray([1.0]),
        ),
    )
    after = step(system, initial, jax.random.key(0), tick=0)
    assert isinstance(after.population, WeightedSamples)
    # Two layers, one entity, one self-loop edge each → 2 mixture particles, weight 0.5 each.
    assert after.population.weights.shape == (2,)
    assert jnp.allclose(after.population.weights, jnp.asarray([0.5, 0.5]))


def test_step_uses_default_focal_entity_params_when_user_provides_none():
    """Integration: a System with hyperedge_params=None falls back to the focal-entity rule.

    Drives the `hyperedge_params or _default_focal_entity_params` path inside _apply_variation
    via the public step() API rather than invoking the private helper directly.
    """
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_FocalEntityVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_SelfLoopTopology(),
        observer=_ZeroValuedObserver(),
        detect_entities=_OnePerEntityDetector(),
        hyperedge_params=None,  # forces the default focal-entity rule
        iteration_order=("variation",),
    )
    initial = JointState(
        state=jnp.asarray(0.0),
        population=WeightedSamples(
            states=jnp.asarray([0.5, 1.5]),
            weights=jnp.asarray([1.0, 1.0]),
        ),
    )
    after = step(system, initial, jax.random.key(0), tick=0)
    assert isinstance(after.population, WeightedSamples)
    assert after.population.weights.shape == (2,)


# ---------------------------------------------------------------------------
# substrate.py — composed initial_state + initial_population NotImplementedError.
# ---------------------------------------------------------------------------


def test_composed_substrate_initial_state_pairs_components():
    a = _ScalarSubstrateExplicitPop()
    b = _ScalarSubstrateExplicitPop()
    composed = compose_substrates_independently(a, b)
    initial = composed.initial_state(jax.random.key(0))
    assert isinstance(initial, tuple) and len(initial) == 2


def test_composed_substrate_initial_population_is_unsupported():
    a = _ScalarSubstrateExplicitPop()
    b = _ScalarSubstrateExplicitPop()
    composed = compose_substrates_independently(a, b)
    with pytest.raises(NotImplementedError, match="user-supplied"):
        composed.initial_population(jax.random.key(0))


def test_composed_substrate_default_param_is_pair():
    a = _ScalarSubstrateExplicitPop()
    b = _ScalarSubstrateExplicitPop()
    composed = compose_substrates_independently(a, b)
    assert composed.default_dynamics_param == (None, None)


# ---------------------------------------------------------------------------
# topology.py — Hypergraph.num_edges and MultiplexTopology validation.
# ---------------------------------------------------------------------------


def test_hypergraph_num_edges_reports_count():
    edges = (
        Hyperedge(members=jnp.asarray([0]), weight=jnp.asarray(1.0)),
        Hyperedge(members=jnp.asarray([1]), weight=jnp.asarray(1.0)),
    )
    assert Hypergraph(edges=edges).num_edges == 2


def test_multiplex_topology_rejects_empty_layer_list():
    with pytest.raises(ValueError, match="at least one layer"):
        MultiplexTopology(layers=[])


def test_multiplex_topology_rejects_non_unit_alpha_sum():
    layers = [
        MultiplexLayer(alpha=jnp.asarray(0.3), topology=_NoHyperedgesTopology()),
        MultiplexLayer(alpha=jnp.asarray(0.3), topology=_NoHyperedgesTopology()),
    ]
    with pytest.raises(ValueError, match="must sum to 1"):
        MultiplexTopology(layers=layers)


# ---------------------------------------------------------------------------
# spec.py — exercises the viability-name introspection through the public API
# (SystemSpec.from_system) rather than calling the private _infer_viability_name helper.
# ---------------------------------------------------------------------------


def test_systemspec_reports_custom_for_unrecognised_viability_callable():
    """A user-supplied ViabilityFilter that doesn't match any of the four named formalisms is
    reported as 'custom'. The 'unknown' branch isn't reachable through System construction
    (the type system requires a callable viability), so it isn't asserted here.
    """
    system = System(
        substrate=_ScalarSubstrateExplicitPop(),
        variation=_PointVariation(),
        viability=_IdentityViabilityFloat(),
        topology=_NoHyperedgesTopology(),
        observer=_ZeroValuedObserver(),
    )
    spec = SystemSpec.from_system(system)
    assert spec.viability is not None
    assert spec.viability.formalism_name == "custom"
