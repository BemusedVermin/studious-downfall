"""Structured description of an emergent system.

The framework's purpose is to elucidate the structure of any emergent system, not to gate
which systems "conform." The 5-tuple `(X, V, F, T, O)` is a vocabulary in which any emergent
system is read; the items here are *what description looks like* in that vocabulary, not a
checklist a system must pass.

Two groups, matching the paper's "System Description" section:

* Structural items (1-7): substrate, entity, variation, viability, topology, observer,
  iteration order. These are exhibitable for any `System` by construction —
  `SystemSpec.from_system(system)` populates them via introspection.

* Reproducibility metadata (8-11): descriptor space, RNG provenance, complexity figures,
  pseudocode. These are not implied by being an emergent system; the implementer supplies
  them so others can replicate the simulator. Until filled, those fields are `None`, and
  `SystemSpec.missing_reproducibility_fields()` lists which remain.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from emergent_systems.system import SlotName, System
from emergent_systems.topology import MultiplexTopology
from emergent_systems.viability import (
    AutopoieticClosureViability,
    MarkovBlanketViability,
    MinimalCriterionViability,
    RAFSetViability,
)

# ---------------------------------------------------------------------------
# Per-slot reports.
#
# Each is a small dataclass that a user fills in with concrete values. `from_system` populates
# what it can introspect; the remainder defaults to `None` and is reported as "missing" in
# `missing_reproducibility_fields`.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SubstrateReport:
    """System Description, structural item 1."""

    state_space_description: str
    """Plain-English description of `X` — e.g. 'toroidal lattice [0,1]^{H×W}'."""

    composition: str | None = None
    """If composite, the `⊠_κ`-decomposition — e.g. 'X_FL ⊠_κ X_LLM'."""


@dataclass(frozen=True)
class EntityReport:
    """System Description, structural item 2."""

    supporting_set_rule: str
    """How `S` is determined — e.g. 'connected components above mass threshold θ=0.1'."""

    scale_projection_description: str
    """How `π` is built — e.g. 'centroid + total mass'."""


@dataclass(frozen=True)
class VariationReport:
    """System Description, structural item 3."""

    channels: tuple[str, ...]
    """Each channel — e.g. ('Gaussian-on-kernel-weights', 'prompt-token-resample')."""

    couplings: tuple[str, ...] = ()
    """Channel couplings `ρ` — empty tuple if all channels are independent (`⋄_ρ` trivial)."""


@dataclass(frozen=True)
class ViabilityReport:
    """System Description, structural item 4 — name the formalism, not just its type."""

    formalism_name: Literal["markov-blanket", "autopoietic", "raf", "mcc", "custom", "unknown"]
    predicate_description: str
    """Plain-English description of the predicate, e.g. 'GoL-glider preimage closure'."""

    closure_operator_verified: bool | None = None
    """If `verify_is_closure_operator` was run on this F, the result; otherwise `None`."""


@dataclass(frozen=True)
class TopologyReport:
    """System Description, structural item 5."""

    family: str
    """Plain-English description — e.g. 'Moore neighbourhood' or 'k-NN, k=8'."""

    multiplex_layers: tuple[tuple[str, float], ...] = ()
    """If multiplex, `(layer_name, alpha)` per layer; empty otherwise."""


@dataclass(frozen=True)
class ObserverReport:
    """System Description, structural item 6."""

    family: Literal["density-distance", "fm-embedding", "information-theoretic", "custom"]
    window_length: int
    """Paper: w (§3.5)."""

    state_variables: str
    """Plain-English — e.g. 'archive of size 1024, no learned model'."""


@dataclass(frozen=True)
class DescriptorReport:
    """System Description, reproducibility item 8."""

    descriptor_space: str
    archive_update_rule: str
    saturation_criterion: str
    boundedness_or_open_endedness_test: str


@dataclass(frozen=True)
class RNGReport:
    """System Description, reproducibility item 9."""

    scheme: str
    """E.g. 'Philox 4x32-10 via jax.random.split'."""

    key_triple_description: str
    """E.g. '(global seed, worker id, tick)'."""


@dataclass(frozen=True)
class ComplexityReport:
    """System Description, reproducibility item 10."""

    per_tick_wall_clock_seconds: float | None
    theoretical_complexity: str
    """E.g. 'O(|X|/P + N/P + log|X|)' per the paper's 'Many-threaded complexity' table."""


# ---------------------------------------------------------------------------
# The aggregate description.
# ---------------------------------------------------------------------------


REPRODUCIBILITY_FIELDS: tuple[str, ...] = ("descriptor", "rng", "complexity", "pseudocode")
"""Field names of `SystemSpec` that are reproducibility metadata, in paper-item order
(items 8-11). Used by `missing_reproducibility_fields`."""


@dataclass(frozen=True)
class SystemSpec:
    """A structured description of an emergent system — paper's "System Description" section.

    Structural items (1-7) follow from the slot decomposition and are exhibitable for any
    `System` by construction: `SystemSpec.from_system(system)` populates them. Reproducibility
    metadata (items 8-11) is communication hygiene the implementer supplies; those fields are
    `None` until filled, and `missing_reproducibility_fields()` lists which remain.
    """

    substrate: SubstrateReport | None = None
    entity: EntityReport | None = None
    variation: VariationReport | None = None
    viability: ViabilityReport | None = None
    topology: TopologyReport | None = None
    observer: ObserverReport | None = None
    iteration_order: tuple[SlotName, ...] | None = None
    descriptor: DescriptorReport | None = None
    rng: RNGReport | None = None
    complexity: ComplexityReport | None = None
    pseudocode: str | None = None

    @classmethod
    def from_system(cls, system: System[Any, Any, Any, Any]) -> SystemSpec:
        """Populate the structural items (1-7) by introspection. Reproducibility fields stay `None`.

        The user is expected to copy the returned spec and fill in the reproducibility fields
        (descriptor, rng, complexity, pseudocode) with substrate-specific text before
        publishing the description as part of a paper's supplementary materials.
        """
        viability_name = _infer_viability_name(system.viability)
        topology_layers = _infer_multiplex_layers(system.topology)
        observer_window = getattr(system.observer, "window_length", None)

        return cls(
            substrate=SubstrateReport(
                state_space_description=type(system.substrate).__name__,
            ),
            entity=(
                None
                if system.detect_entities is None
                else EntityReport(
                    supporting_set_rule=type(system.detect_entities).__name__,
                    scale_projection_description="user-supplied (not introspectable)",
                )
            ),
            variation=VariationReport(
                channels=(type(system.variation).__name__,),
            ),
            viability=ViabilityReport(
                formalism_name=viability_name,
                predicate_description=type(system.viability).__name__,
            ),
            topology=TopologyReport(
                family=type(system.topology).__name__,
                multiplex_layers=topology_layers,
            ),
            observer=(
                ObserverReport(
                    family="custom",
                    window_length=observer_window,
                    state_variables="user-supplied (not introspectable)",
                )
                if observer_window is not None
                else None
            ),
            iteration_order=system.iteration_order,
        )

    def missing_reproducibility_fields(self) -> tuple[str, ...]:
        """Names of the reproducibility-metadata fields (items 8-11) that are still `None`.

        Empty tuple means every reproducibility item has been filled in. This is communication
        hygiene, not a conformance gate: a system can be a perfectly real emergent system and
        still have unfilled reproducibility metadata — that just means it isn't ready to be
        replicated by someone else yet.
        """
        return tuple(name for name in REPRODUCIBILITY_FIELDS if getattr(self, name) is None)


# ---------------------------------------------------------------------------
# Introspection helpers.
# ---------------------------------------------------------------------------


def _infer_viability_name(
    viability: object,
) -> Literal["markov-blanket", "autopoietic", "raf", "mcc", "custom", "unknown"]:
    """Recognise the four named formalisms; everything else is 'custom'."""
    if isinstance(viability, MarkovBlanketViability):
        return "markov-blanket"
    if isinstance(viability, AutopoieticClosureViability):
        return "autopoietic"
    if isinstance(viability, RAFSetViability):
        return "raf"
    if isinstance(viability, MinimalCriterionViability):
        return "mcc"
    if callable(viability):
        return "custom"
    return "unknown"


def _infer_multiplex_layers(topology: object) -> tuple[tuple[str, float], ...]:
    """Pull `(layer_name, alpha)` out of a multiplex topology; empty for single-layer."""
    if not isinstance(topology, MultiplexTopology):
        return ()
    return tuple((type(layer.topology).__name__, float(layer.alpha)) for layer in topology.layers)
