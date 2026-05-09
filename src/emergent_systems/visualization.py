"""Substrate-agnostic plotting helpers for `RunResult` inspection.

The library deliberately ships no concrete substrates, so this module operates only on
`RunResult` fields and Protocol-exposed methods. It does not assume a particular shape for the
substrate state `X`; substrate-specific renderers (Lenia grid frames, Boids scatters) belong in
the per-example notebooks.

The four helpers each return a `matplotlib.figure.Figure`:

* `plot_population_mass`         — total `M+(X)` mass over time (sanity check that `F` is not
                                   zeroing the population).
* `plot_observer_trace`          — observer score components over time.
* `plot_viability_filter_ratio`  — per-tick mass ratio `M(t+1) / M(t)`. This is exact when V_T
                                   and Φ are mass-preserving (so the ratio captures `F`'s
                                   effect alone); otherwise it is the end-to-end per-tick mass
                                   change.
* `plot_topology_degree`         — degree distribution of the interaction topology, sampled at
                                   each tick where entities are detected.

Matplotlib is the only plotting dependency; this module imports it lazily so importing
`emergent_systems` does not pay matplotlib's import cost.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import jax.numpy as jnp
import numpy as np

from emergent_systems.entity import EntityDetector
from emergent_systems.system import RunResult
from emergent_systems.topology import InteractionTopology

if TYPE_CHECKING:
    from matplotlib.figure import Figure


__all__ = [
    "plot_population_mass",
    "plot_observer_trace",
    "plot_viability_filter_ratio",
    "plot_topology_degree",
]


def _trajectory_masses(result: RunResult[Any]) -> list[float]:
    return [float(joint_state.population.total_mass) for joint_state in result.trajectory]


def plot_population_mass(result: RunResult[Any]) -> Figure:
    """Plot total population mass `Σ μ` over the trajectory — paper: M+(X) total mass."""
    import matplotlib.pyplot as plt

    masses = _trajectory_masses(result)
    ticks = list(range(len(masses)))

    fig, ax = plt.subplots()
    ax.plot(ticks, masses, marker=".")
    ax.set_xlabel("tick")
    ax.set_ylabel("total mass")
    ax.set_title("Population mass M+(X) over time")
    ax.grid(True, alpha=0.3)
    return fig


def plot_observer_trace(
    result: RunResult[Any],
    observer_name: str | None = None,
) -> Figure:
    """Plot the observer's per-tick score vector — paper: O_s output over the run.

    Each component of the `Float[Array, "k"]` score becomes one line. `observer_name` is used as
    a title prefix; pass `None` to omit it.
    """
    import matplotlib.pyplot as plt

    if not result.observer_scores:
        raise ValueError(
            "RunResult.observer_scores is empty; the run produced no observations "
            "(window length may exceed n_ticks)."
        )

    scores = jnp.stack(list(result.observer_scores))  # shape (T, k)
    scores_np = np.asarray(scores)
    if scores_np.ndim == 1:
        scores_np = scores_np[:, None]

    n_observations, n_components = scores_np.shape
    fig, ax = plt.subplots()
    for component_index in range(n_components):
        ax.plot(
            range(n_observations),
            scores_np[:, component_index],
            marker=".",
            label=f"component {component_index}",
        )
    ax.set_xlabel("observation")
    ax.set_ylabel("score")
    title = "Observer trace"
    if observer_name is not None:
        title = f"{observer_name} — {title}"
    ax.set_title(title)
    if n_components > 1:
        ax.legend()
    ax.grid(True, alpha=0.3)
    return fig


def plot_viability_filter_ratio(result: RunResult[Any]) -> Figure:
    """Plot the per-tick mass ratio `M(t+1) / M(t)` — paper: F's effect on total mass.

    When V_T and Φ are mass-preserving (the typical case), this ratio captures `F`'s effect
    alone; otherwise it is the end-to-end per-tick mass change. Ticks where `M(t) == 0` are
    plotted as `0.0` to keep the trace finite — a flat zero line indicates a collapsed
    population. The dashed reference line at `1.0` marks mass conservation.
    """
    import matplotlib.pyplot as plt

    masses = _trajectory_masses(result)
    if len(masses) < 2:
        raise ValueError(
            f"Trajectory has {len(masses)} state(s); need at least 2 to compute a ratio."
        )

    ratios = [(masses[t + 1] / masses[t]) if masses[t] > 0 else 0.0 for t in range(len(masses) - 1)]
    ticks = list(range(1, len(masses)))

    fig, ax = plt.subplots()
    ax.plot(ticks, ratios, marker=".")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.7)
    ax.set_xlabel("tick")
    ax.set_ylabel("M(t+1) / M(t)")
    ax.set_title("Population mass ratio per tick (F's effect when V_T, Φ are mass-preserving)")
    ax.grid(True, alpha=0.3)
    return fig


def plot_topology_degree(
    result: RunResult[Any],
    topology: InteractionTopology,
    detect_entities: EntityDetector[Any],
) -> Figure:
    """Plot per-entity hyperedge-incidence counts at each tick — paper: T_t degree distribution.

    For each tick the helper detects entities, asks the topology for `T_t`, and counts how many
    hyperedges each entity participates in. Snapshots are overlaid as histograms; ticks where
    no entities are detected (e.g. `ImplicitInSubstrate` populations with no detector) are
    skipped silently.

    The topology and entity detector are passed explicitly because `RunResult` only carries the
    joint-state trajectory — the slot Protocols are needed to recover the time-varying
    hypergraph the paper denotes `T_t`.
    """
    import matplotlib.pyplot as plt

    snapshots: list[tuple[int, np.ndarray]] = []
    for tick, joint_state in enumerate(result.trajectory):
        entities: Sequence[Any] = detect_entities(joint_state.state, joint_state.population)
        if not entities:
            continue
        hypergraph = topology.at(tick, entities)
        degrees = np.zeros(len(entities), dtype=np.int64)
        for edge in hypergraph.edges:
            for member_index in np.asarray(edge.members).reshape(-1):
                degrees[int(member_index)] += 1
        snapshots.append((tick, degrees))

    fig, ax = plt.subplots()
    if not snapshots:
        ax.text(
            0.5,
            0.5,
            "no entities detected at any tick",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        ax.set_axis_off()
        return fig

    max_degree = max(int(degrees.max()) for _, degrees in snapshots) if snapshots else 0
    bin_edges: list[float] = [i - 0.5 for i in range(max_degree + 2)]
    for tick, degrees in snapshots:
        ax.hist(degrees, bins=bin_edges, alpha=0.4, label=f"tick {tick}")
    ax.set_xlabel("degree")
    ax.set_ylabel("entity count")
    ax.set_title("Topology degree distribution per tick")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig
