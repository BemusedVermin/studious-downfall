"""Interaction topology — who interacts with whom.

Paper §3.5: an interaction topology is a measurable family `T = (T_t)_{t∈ℕ}` where each `T_t`
is a hypergraph on the current entity set with edge weights in some semiring (typically `ℝ≥0`
or `{0, 1}`). It is *not* the substrate's intrinsic geometry — that is implicit in the
substrate dynamics. Examples: Moore neighbourhoods on a lattice, k-NN on positions, social
graphs, donor-recipient pairings, stigmergic indirect coupling.

Multi-regime topologies (paper §3.5 'Multi-regime topologies', line 702-715) are layered
multiplexes: `T = ⊔_ℓ T^(ℓ)` with non-negative layer weights `(α_ℓ)` summing to one. The
mixture appears at the V_T level in `system.py`, not here.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

import jax.numpy as jnp
from jaxtyping import Array, Float, Int

from emergent_systems._types import TickIndex
from emergent_systems.entity import Entity


@dataclass(frozen=True)
class Hyperedge:
    """One hyperedge — paper §3.5: an edge connecting r entities with a scalar weight."""

    members: Int[Array, "r"]
    """Indices into the current entity set — paper: `(e_1, ..., e_r)`."""

    weight: Float[Array, ""]
    """Edge weight — paper: `w_e`. Nonneg in the standard semiring."""


@dataclass(frozen=True)
class Hypergraph:
    """A weighted hypergraph on the current entity set — paper: T_t.

    Stored as an explicit list of hyperedges. For dense or fixed-arity topologies, an array
    representation would be faster; this list-of-edges form prioritises legibility for the
    scaffold.

    PERF[topology-list-of-edges]: large-population systems with O(N) or O(Nk) edges per tick
    will spend a noticeable fraction of time iterating Python-side. Replace with a flat
    `edges: Int[Array, "E max_arity"]` representation (and an `arity_mask`) when porting hot
    paths.
    """

    edges: Sequence[Hyperedge]

    @property
    def num_edges(self) -> int:
        return len(self.edges)


@runtime_checkable
class InteractionTopology(Protocol):
    """An interaction topology — paper: T = (T_t)_{t∈ℕ}.

    Implementers return the hypergraph appropriate for the current tick and entity set. Static
    topologies (a fixed lattice neighbourhood) ignore both arguments after first use; dynamic
    topologies (k-NN, sampled pairings) recompute each tick.
    """

    def at(
        self,
        tick: TickIndex,
        entities: Sequence[Entity[Any, Any]],
    ) -> Hypergraph: ...


# ---------------------------------------------------------------------------
# Multiplex layered topology — paper §3.5, multi-regime topologies.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MultiplexLayer:
    """One layer of a multi-regime topology — paper: `(α_ℓ, T^(ℓ))`."""

    alpha: Float[Array, ""]
    """Layer weight — paper: `α_ℓ`. Required to be nonneg; the suite must sum to one."""

    topology: InteractionTopology


@dataclass(frozen=True)
class MultiplexTopology:
    """A multiplex of interaction topologies — paper §3.5 line 706.

    Layer weights `α_ℓ` are required to sum to one so total interaction load per tick is
    preserved (paper line 708-714). The mixture is realised at the V_T level: see
    `build_population_variation_multiplex` in `system.py`.
    """

    layers: Sequence[MultiplexLayer]

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("MultiplexTopology requires at least one layer.")
        total = jnp.sum(jnp.stack([layer.alpha for layer in self.layers]))
        if not bool(jnp.isclose(total, 1.0)):
            raise ValueError(f"MultiplexTopology layer weights must sum to 1, got {float(total)}.")
