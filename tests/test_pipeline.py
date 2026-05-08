"""End-to-end pipeline test on the toy system from `conftest.py`.

Exercises the iteration-order interpreter, the lifted operators, the implicit-population
short-circuit, and the windowed-observer state.
"""

from __future__ import annotations

import jax
import pytest

from emergent_systems import ImplicitInSubstrate, run, step


def test_step_advances_state(toy_system, toy_initial_state):
    after = step(toy_system, toy_initial_state, jax.random.key(0), tick=0)
    assert int(after.state) == 1
    assert isinstance(after.population, ImplicitInSubstrate)


def test_step_alternates_state(toy_system, toy_initial_state):
    state = toy_initial_state
    for tick in range(4):
        state = step(toy_system, state, jax.random.key(tick), tick=tick)
    # 0 → 1 → 0 → 1 → 0 after four flips.
    assert int(state.state) == 0


def test_run_produces_expected_trajectory_length(toy_system):
    result = run(toy_system, n_ticks=5, key=jax.random.key(0))
    assert len(result.trajectory) == 6  # initial + 5 ticks
    # Observation happens after each tick once the window has filled (window=1 → all 5 ticks).
    assert len(result.observer_scores) == 5


def test_run_observer_state_updates_each_tick(toy_system):
    result = run(toy_system, n_ticks=3, key=jax.random.key(0))
    # The TickCountingObserver returns increasing tick-count scalars.
    final_count = int(result.final_observer_state)
    assert final_count == len(result.observer_scores)


def test_iteration_order_alternative_is_accepted(toy_system):
    from emergent_systems import System

    permuted = System(
        substrate=toy_system.substrate,
        variation=toy_system.variation,
        viability=toy_system.viability,
        topology=toy_system.topology,
        observer=toy_system.observer,
        iteration_order=("variation", "viability", "dynamics"),
    )
    result = run(permuted, n_ticks=2, key=jax.random.key(0))
    assert len(result.trajectory) == 3


def test_iteration_order_rejects_unknown_slot(toy_system):
    from emergent_systems import System

    with pytest.raises(ValueError):
        System(
            substrate=toy_system.substrate,
            variation=toy_system.variation,
            viability=toy_system.viability,
            topology=toy_system.topology,
            observer=toy_system.observer,
            iteration_order=("dynamics", "observer"),  # type: ignore[arg-type]
        )
