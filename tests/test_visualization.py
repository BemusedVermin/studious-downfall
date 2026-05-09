"""Smoke tests for the substrate-agnostic visualization helpers.

The helpers must:
* Operate on `RunResult` and Protocol-exposed methods only — no concrete-substrate imports.
* Return a `matplotlib.figure.Figure` with the expected number of axes / lines.
* Raise informative errors when given inputs that genuinely cannot be plotted.

The tests use the toy `BinaryFlipSubstrate` system from `conftest.py` for the implicit-
population helpers, plus a small explicit-population fixture for `plot_topology_degree` so the
topology actually has entities to enumerate.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # noqa: E402 — headless backend must be set before pyplot import

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import pytest
from jaxtyping import Array, Float, Int
from matplotlib.figure import Figure

from emergent_systems import (
    Entity,
    EntityDetector,
    Hyperedge,
    Hypergraph,
    InteractionTopology,
    RunResult,
    TickIndex,
    run,
)
from emergent_systems.visualization import (
    plot_observer_trace,
    plot_population_mass,
    plot_topology_degree,
    plot_viability_filter_ratio,
)


@pytest.fixture
def toy_run_result(toy_system) -> RunResult[Int[Array, ""]]:
    return run(toy_system, n_ticks=5, key=jax.random.key(0))


def test_plot_population_mass_returns_figure_with_one_line(toy_run_result):
    fig = plot_population_mass(toy_run_result)
    assert isinstance(fig, Figure)
    [ax] = fig.axes
    assert len(ax.lines) == 1
    # ImplicitInSubstrate has nominal_mass=1.0; trajectory is initial + 5 ticks = 6 points.
    xy = np.asarray(ax.lines[0].get_xydata())
    assert xy.shape == (6, 2)
    assert xy[:, 1] == pytest.approx([1.0] * 6)


def test_plot_observer_trace_one_line_per_component(toy_run_result):
    fig = plot_observer_trace(toy_run_result, observer_name="TickCounter")
    assert isinstance(fig, Figure)
    [ax] = fig.axes
    # TickCountingObserver returns a 1-component score per tick; one observation per tick.
    assert len(ax.lines) == 1
    assert "TickCounter" in ax.get_title()


def test_plot_observer_trace_rejects_empty_scores(toy_system):
    # window_length is 1, so any non-zero n_ticks gives at least one observation; force the
    # empty case by running for zero ticks.
    empty_result = run(toy_system, n_ticks=0, key=jax.random.key(0))
    with pytest.raises(ValueError, match="empty"):
        plot_observer_trace(empty_result)


def test_plot_viability_filter_ratio_axhline_at_one(toy_run_result):
    fig = plot_viability_filter_ratio(toy_run_result)
    assert isinstance(fig, Figure)
    [ax] = fig.axes
    assert len(ax.lines) == 2  # ratio trace + reference axhline
    # Mass is constant 1.0, so all ratios should be exactly 1.0.
    ratio_line, _ref_line = ax.lines
    ratio_xy = np.asarray(ratio_line.get_xydata())
    assert ratio_xy[:, 1] == pytest.approx([1.0] * 5)


def test_plot_viability_filter_ratio_rejects_short_trajectory(toy_system):
    short_result = run(toy_system, n_ticks=0, key=jax.random.key(0))
    with pytest.raises(ValueError, match="at least 2"):
        plot_viability_filter_ratio(short_result)


# ---------------------------------------------------------------------------
# Explicit-population fixture for plot_topology_degree.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _SingletonEntityDetector(EntityDetector[Int[Array, ""]]):
    """Treat each integer in {0, 1, 2} as a separate entity at every tick."""

    def __call__(
        self,
        state: Int[Array, ""],
        population: Any,
    ) -> Sequence[Entity[Int[Array, ""], Float[Array, ""]]]:
        del population
        return tuple(
            Entity(
                supporting_set=jnp.asarray([i], dtype=jnp.int32),
                scale_projection=lambda _state, idx=i: jnp.asarray(float(idx)),
            )
            for i in range(3)
        )


@dataclass(frozen=True)
class _RingTopology(InteractionTopology):
    """A trivially-non-empty topology: 3 pairwise edges in a ring."""

    def at(
        self,
        tick: TickIndex,
        entities: Sequence[Entity[Any, Any]],
    ) -> Hypergraph:
        del tick
        n = len(entities)
        return Hypergraph(
            edges=tuple(
                Hyperedge(
                    members=jnp.asarray([i, (i + 1) % n], dtype=jnp.int32),
                    weight=jnp.asarray(1.0),
                )
                for i in range(n)
            )
        )


def test_plot_topology_degree_returns_figure_with_histogram_bars(toy_run_result):
    detector = _SingletonEntityDetector()
    topology = _RingTopology()
    fig = plot_topology_degree(toy_run_result, topology, detector)
    assert isinstance(fig, Figure)
    [ax] = fig.axes
    # One histogram per tick where entities were detected (all 6 trajectory snapshots).
    # Each ring edge contributes 2 incidences across 3 entities, so degree distribution is
    # {2: 3} per snapshot — a single non-empty bin per snapshot.
    assert len(ax.patches) > 0
    assert ax.get_xlabel() == "degree"


def test_plot_topology_degree_handles_no_entities(toy_run_result):
    @dataclass(frozen=True)
    class _NoEntitiesDetector(EntityDetector[Any]):
        def __call__(self, state: Any, population: Any) -> Sequence[Entity[Any, Any]]:
            del state, population
            return ()

    fig = plot_topology_degree(toy_run_result, _RingTopology(), _NoEntitiesDetector())
    assert isinstance(fig, Figure)
    # When no entities are detected at any tick, the helper produces an axis-off placeholder.
    [ax] = fig.axes
    assert not ax.get_xlabel()  # axis was turned off — no labels set


def test_visualization_module_does_not_import_concrete_substrates():
    """Guard against the module accidentally pulling in a concrete substrate implementation."""
    import emergent_systems.visualization as viz_module

    source = viz_module.__file__ and __import__("pathlib").Path(viz_module.__file__).read_text(
        encoding="utf-8"
    )
    assert source is not None
    for forbidden in ("examples.gol", "examples.lenia", "examples.boids", "coupled_lenia_stub"):
        assert forbidden not in source, (
            f"visualization.py must remain substrate-agnostic; found {forbidden!r}"
        )
