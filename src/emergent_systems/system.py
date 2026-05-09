"""The orchestrator: lifted operators, V_T construction, step, and run.

Paper §3.1 defines the system as a tuple `S = (X, V, F, T, O)` with iteration rule

    (x_{t+1}, μ_{t+1}) = (S̃_F ∘ Ṽ_T ∘ Φ̃)(x_t, μ_t)

This module assembles the user's slot implementations into a runnable pipeline. The five
slots are deliberately decoupled: this module is the only place that knows about all of them
at once.

Three nontrivial pieces live here rather than on the per-slot modules:

* `build_population_variation` — paper §3.4 lines 577-603 V_T construction. V doesn't know
  about T; T doesn't know about V; the construction belongs at the orchestration level.
* The lifted operators Φ̃, Ṽ_T, S̃_F (paper §3.1 line 285-289).
* The iteration-order interpreter — paper §sec:description structural item 7 explicitly
  requires the order to be reportable as data, so we represent it as a tuple of slot names.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

import jax
import jax.numpy as jnp
from jaxtyping import Array, Float

from emergent_systems._types import PRNGKey, TickIndex
from emergent_systems.entity import Entity, EntityDetector
from emergent_systems.observer import JointState, StatefulObserver, WindowedTrajectory
from emergent_systems.population import ImplicitInSubstrate, Population, WeightedSamples
from emergent_systems.substrate import Substrate
from emergent_systems.topology import InteractionTopology, MultiplexTopology
from emergent_systems.variation import Variation
from emergent_systems.viability import ViabilityFilter

SlotName = Literal["dynamics", "variation", "viability"]
"""The three slot operators interpreted by `step` — paper: Φ, V, F."""

PopulationVariation = Callable[
    [PRNGKey, TickIndex, Any, Population[Any]],
    Population[Any],
]
"""Signature of a built `V_T` — paper: V_T : M+(X) × X → M+(X), evaluated at a tick."""


# ---------------------------------------------------------------------------
# V_T construction — paper §3.4 lines 577-603.
# ---------------------------------------------------------------------------


def build_population_variation[State, Params](
    variation: Variation[State, Params],
    topology: InteractionTopology,
    detect_entities: EntityDetector[State],
    hyperedge_params: Callable[[Sequence[Entity[State, Any]]], Params],
) -> PopulationVariation:
    """Construct the topology-mediated population variation operator — paper: V_T.

    For each hyperedge `e ∈ E(T_t)` over the detected entities, sample one offspring from
    `V(x, θ_e)` and emit it with weight `w_e`. The resulting population is

        V_T(μ; x) = Σ_e w_e · V(x, θ_e)

    realised empirically (one particle per hyperedge). For substrate-as-population paradigms
    (`ImplicitInSubstrate`), V_T is the identity in line with paper §3.1 line 289 — variation
    is achieved through stochastic Φ in those substrates.

    PERF[v_t-python-loop]: the per-hyperedge loop is Python-side (different hyperedges may
    have different arities). For lattice/swarm systems with O(N) or O(Nk) edges per tick this
    becomes the bottleneck. Replace with a fixed-arity flat-array representation under jit.
    """

    def v_t(
        key: PRNGKey,
        tick: TickIndex,
        state: State,
        population: Population[State],
    ) -> Population[State]:
        if isinstance(population, ImplicitInSubstrate):
            return population

        entities = list(detect_entities(state, population))
        hypergraph = topology.at(tick, entities)

        if hypergraph.num_edges == 0:
            # An empty topology yields a measure with total mass zero. We use an
            # empty WeightedSamples; the State pytree shape is irrelevant since there are no
            # particles, so we elide it.
            empty: Population[State] = WeightedSamples(  # type: ignore[type-arg]
                states=jnp.zeros((0,)),
                weights=jnp.zeros((0,)),
            )
            return empty

        edge_keys = jax.random.split(key, hypergraph.num_edges)
        sampled_states = []
        weights = []
        for edge_key, edge in zip(edge_keys, hypergraph.edges, strict=True):
            members = [entities[int(idx)] for idx in edge.members.tolist()]
            params = hyperedge_params(members)
            distribution = variation(state, params)
            sampled_states.append(distribution.sample(edge_key))
            weights.append(edge.weight)

        result: Population[State] = WeightedSamples(  # type: ignore[type-arg]
            states=jnp.stack(sampled_states),
            weights=jnp.stack(weights),
        )
        return result

    return v_t


def build_population_variation_multiplex[State](
    layers: Sequence[tuple[Float[Array, ""], Variation[State, Any], InteractionTopology]],
    detect_entities: EntityDetector[State],
    hyperedge_params: Callable[[Sequence[Entity[State, Any]]], Any],
) -> PopulationVariation:
    """The multiplex mixture form of V_T — paper §3.7 line 711.

    Realises `V_T(μ; x) = Σ_ℓ α_ℓ V^(ℓ)_{T^(ℓ)}(μ; x)` by concatenating each layer's hyperedge
    contributions with weights scaled by `α_ℓ`. Layer weights must already sum to one — the
    `MultiplexTopology` constructor enforces this.
    """

    layer_v_ts = [
        build_population_variation(
            variation=variation,
            topology=topology,
            detect_entities=detect_entities,
            hyperedge_params=hyperedge_params,
        )
        for (_, variation, topology) in layers
    ]

    def v_t_mixture(
        key: PRNGKey,
        tick: TickIndex,
        state: State,
        population: Population[State],
    ) -> Population[State]:
        if isinstance(population, ImplicitInSubstrate):
            return population

        layer_keys = jax.random.split(key, len(layers))
        all_states: list[Any] = []
        all_weights: list[Float[Array, ""]] = []
        for layer_key, (alpha, _, _), layer_v_t in zip(layer_keys, layers, layer_v_ts, strict=True):
            layer_population = layer_v_t(layer_key, tick, state, population)
            if not isinstance(layer_population, WeightedSamples):
                continue
            for particle_idx in range(layer_population.weights.shape[0]):
                all_states.append(
                    jax.tree.map(lambda leaf, i=particle_idx: leaf[i], layer_population.states)
                )
                all_weights.append(alpha * layer_population.weights[particle_idx])

        if not all_states:
            empty: Population[State] = WeightedSamples(  # type: ignore[type-arg]
                states=jnp.zeros((0,)),
                weights=jnp.zeros((0,)),
            )
            return empty

        result: Population[State] = WeightedSamples(  # type: ignore[type-arg]
            states=jax.tree.map(lambda *xs: jnp.stack(xs), *all_states),
            weights=jnp.stack(all_weights),
        )
        return result

    return v_t_mixture


# ---------------------------------------------------------------------------
# The system tuple — paper: S = (X, V, F, T, O), plus the entity-detection inputs to V_T.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class System[State, DynamicsParam, Params, ObserverState]:
    """A substrate-agnostic emergent system — paper: S = (X, V, F, T, O).

    The five slots are independent: switching the viability formalism, the topology, or the
    observer family does not require touching the others. The four optional fields below make
    the V_T construction concrete (paper §3.4) and let the iteration order be declared as
    data (paper §sec:description structural item 7).
    """

    substrate: Substrate[State, DynamicsParam]
    variation: Variation[State, Params]
    viability: ViabilityFilter[State]
    topology: InteractionTopology | MultiplexTopology
    observer: StatefulObserver[State, ObserverState]

    detect_entities: EntityDetector[State] | None = None
    """Required for explicit populations (V_T construction); unused for implicit ones."""

    hyperedge_params: Callable[[Sequence[Entity[State, Any]]], Params] | None = None
    """Paper: g, the measurable rule for hyperedge parameters (§3.4 line 588).
    Default behaviour (focal-entity-only) is implemented inline if this is `None`."""

    iteration_order: tuple[SlotName, ...] = field(default=("dynamics", "variation", "viability"))
    """Paper §3.1 default; deviations declared per §sec:description structural item 7."""

    def __post_init__(self) -> None:
        for slot in self.iteration_order:
            if slot not in ("dynamics", "variation", "viability"):
                raise ValueError(
                    f"Unknown slot name {slot!r} in iteration_order; "
                    f"expected one of 'dynamics', 'variation', 'viability'."
                )


# ---------------------------------------------------------------------------
# The lifted operators — paper §3.1 line 285-289.
#
# Each accepts `(joint_state, key, tick)` and returns a new joint_state. The system supplies
# the slot implementations these need.
# ---------------------------------------------------------------------------


def _apply_dynamics[State, DynamicsParam, Params, ObserverState](
    system: System[State, DynamicsParam, Params, ObserverState],
    joint_state: JointState[State],
    key: PRNGKey,
) -> JointState[State]:
    """Lifted Φ̃ — paper: Φ̃(x, μ) = (Φ(x), Φ_*μ)."""
    state_key, pop_key = jax.random.split(key, 2)
    new_state = system.substrate.dynamics(
        state_key,
        system.substrate.default_dynamics_param,
        joint_state.state,
    )

    # PERF[stochastic-pushforward-default]: we always take the stochastic pushforward path,
    # which splits per-particle keys. For deterministic Φ this is wasted work; expose a
    # deterministic-Φ flag on Substrate if it becomes hot.
    def kernel(particle_key: PRNGKey, particle_state: State) -> State:
        return system.substrate.dynamics(
            particle_key,
            system.substrate.default_dynamics_param,
            particle_state,
        )

    new_population = joint_state.population.pushforward_stochastic(pop_key, kernel)
    return JointState(state=new_state, population=new_population)


def _apply_variation[State, DynamicsParam, Params, ObserverState](
    system: System[State, DynamicsParam, Params, ObserverState],
    joint_state: JointState[State],
    key: PRNGKey,
    tick: TickIndex,
) -> JointState[State]:
    """Lifted Ṽ_T — paper: Ṽ_T(x, μ) = (x, V_T(μ; x))."""
    if isinstance(joint_state.population, ImplicitInSubstrate):
        return joint_state

    if system.detect_entities is None:
        raise ValueError(
            "Variation step requires `detect_entities` on the System for explicit populations."
        )

    hyperedge_params = system.hyperedge_params or _default_focal_entity_params

    if isinstance(system.topology, MultiplexTopology):
        layer_triples = [
            (layer.alpha, system.variation, layer.topology) for layer in system.topology.layers
        ]
        v_t = build_population_variation_multiplex(
            layers=layer_triples,
            detect_entities=system.detect_entities,
            hyperedge_params=hyperedge_params,
        )
    else:
        v_t = build_population_variation(
            variation=system.variation,
            topology=system.topology,
            detect_entities=system.detect_entities,
            hyperedge_params=hyperedge_params,
        )

    new_population = v_t(key, tick, joint_state.state, joint_state.population)
    return JointState(state=joint_state.state, population=new_population)


def _apply_viability[State, DynamicsParam, Params, ObserverState](
    system: System[State, DynamicsParam, Params, ObserverState],
    joint_state: JointState[State],
) -> JointState[State]:
    """Lifted S̃_F — paper: S̃_F(x, μ) = (x, F(μ))."""
    return JointState(
        state=joint_state.state,
        population=system.viability(joint_state.population),
    )


def _default_focal_entity_params[State](
    entities: Sequence[Entity[State, Any]],
) -> Any:
    """Paper §3.4 line 588: default `g` depends only on the focal entity.

    The first entity in the hyperedge is treated as focal and its scale-projected feature is
    returned as the parameter. Substrates with non-trivial recombination supply their own.
    """
    if not entities:
        raise ValueError("Hyperedge has no entities; cannot derive a focal-entity parameter.")
    return entities[0]


# ---------------------------------------------------------------------------
# Step — interprets the iteration order. Run — drives the main loop.
# ---------------------------------------------------------------------------


def step[State, DynamicsParam, Params, ObserverState](
    system: System[State, DynamicsParam, Params, ObserverState],
    joint_state: JointState[State],
    key: PRNGKey,
    tick: TickIndex,
) -> JointState[State]:
    """Apply one tick of the iteration rule.

    The slots are run in `system.iteration_order`. Each slot draws an independent key from a
    split of the supplied tick key — paper §4 'Random-number considerations'.
    """
    slot_keys = jax.random.split(key, len(system.iteration_order))
    current = joint_state
    for slot_name, slot_key in zip(system.iteration_order, slot_keys, strict=True):
        if slot_name == "dynamics":
            current = _apply_dynamics(system, current, slot_key)
        elif slot_name == "variation":
            current = _apply_variation(system, current, slot_key, tick)
        elif slot_name == "viability":
            current = _apply_viability(system, current)
    return current


@dataclass(frozen=True)
class RunResult[State]:
    """The output of `run`. Trajectory + observer scores + final observer state."""

    trajectory: list[JointState[State]]
    observer_scores: list[Float[Array, "k"]]
    final_observer_state: Any


def run[State, DynamicsParam, Params, ObserverState](
    system: System[State, DynamicsParam, Params, ObserverState],
    n_ticks: int,
    key: PRNGKey,
) -> RunResult[State]:
    """Run the system for `n_ticks` ticks and return a trajectory and observer scores.

    The observer is consulted once its windowed buffer has filled (paper §3.5 'window length
    w'). Earlier ticks' window views are not scored; this matches the paper's definition that
    `O_s : Z^w × A_O → ℝ^k × A_O` requires a full-width window.

    PERF[run-python-loop]: this is a Python-level for-loop. For long runs, replace with
    `jax.lax.scan` once the slot operators are pure (no Python branches). The user's slot
    implementations determine how easily that lift goes.
    """
    keys = jax.random.split(key, n_ticks + 3)
    init_key_state, init_key_pop, init_key_obs = keys[0], keys[1], keys[2]

    initial_state = system.substrate.initial_state(init_key_state)
    initial_population = system.substrate.initial_population(init_key_pop)
    joint_state = JointState(state=initial_state, population=initial_population)

    observer_state = system.observer.initial_state(init_key_obs)

    trajectory: list[JointState[State]] = [joint_state]
    observer_scores: list[Float[Array, "k"]] = []
    window_buffer: list[JointState[State]] = [joint_state]

    for tick in range(n_ticks):
        joint_state = step(system, joint_state, keys[tick + 3], tick)
        trajectory.append(joint_state)

        window_buffer.append(joint_state)
        if len(window_buffer) > system.observer.window_length:
            window_buffer.pop(0)

        if len(window_buffer) >= system.observer.window_length:
            window = WindowedTrajectory(states=tuple(window_buffer))
            score, observer_state = system.observer.observe(window, observer_state)
            observer_scores.append(score)

    return RunResult(
        trajectory=trajectory,
        observer_scores=observer_scores,
        final_observer_state=observer_state,
    )
