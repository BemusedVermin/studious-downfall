"""The 11-item conformance checklist as data.

Paper §4 lines 1297-1321 define an 11-item checklist that a reproducible implementation must
report. Line 1346 (item iii) makes conformance a typed property: 'two implementations are
conformant when they agree on the typing of each slot, report all eleven items with values,
preserve the iteration order, and specify the entity-detection rule consistently.'

This module turns the checklist into structured data. `SystemSpec.from_system(system)` extracts
what can be introspected; the user fills in the rest (descriptor space, RNG provenance,
complexity figures, pseudocode). `check_conformance()` returns a per-item pass/fail/missing
report — the artefact suitable for pasting into a paper's supplementary materials.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from emergent_systems.system import SlotName, System
from emergent_systems.topology import MultiplexTopology
from emergent_systems.viability import (
    AutopoieticClosureViability,
    MarkovBlanketViability,
    MinimalCriterionViability,
    RAFSetViability,
)

ConformanceStatus = Literal["pass", "fail", "missing"]


# ---------------------------------------------------------------------------
# Per-slot reports.
#
# Each is a small dataclass that a user fills in with concrete values. `from_system` populates
# what it can introspect; the remainder defaults to `None` and is reported as "missing".
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SubstrateReport:
    """Paper §4 checklist item 1."""

    state_space_description: str
    """Plain-English description of `X` — e.g. 'toroidal lattice [0,1]^{H×W}'."""

    composition: str | None = None
    """If composite, the `⊠_κ`-decomposition — e.g. 'X_FL ⊠_κ X_LLM'."""


@dataclass(frozen=True)
class EntityReport:
    """Paper §4 checklist item 2."""

    supporting_set_rule: str
    """How `S` is determined — e.g. 'connected components above mass threshold θ=0.1'."""

    scale_projection_description: str
    """How `π` is built — e.g. 'centroid + total mass'."""


@dataclass(frozen=True)
class VariationReport:
    """Paper §4 checklist item 3."""

    channels: tuple[str, ...]
    """Each channel — e.g. ('Gaussian-on-kernel-weights', 'prompt-token-resample')."""

    couplings: tuple[str, ...] = ()
    """Channel couplings `ρ` — empty tuple if all channels are independent (`⋄_ρ` trivial)."""


@dataclass(frozen=True)
class ViabilityReport:
    """Paper §4 checklist item 4 — name the formalism, not just its type."""

    formalism_name: Literal[
        "markov-blanket", "autopoietic", "raf", "mcc", "custom", "unknown"
    ]
    predicate_description: str
    """Plain-English description of the predicate, e.g. 'GoL-glider preimage closure'."""

    closure_operator_verified: bool | None = None
    """If `verify_is_closure_operator` was run on this F, the result; otherwise `None`."""


@dataclass(frozen=True)
class TopologyReport:
    """Paper §4 checklist item 5."""

    family: str
    """Plain-English description — e.g. 'Moore neighbourhood' or 'k-NN, k=8'."""

    multiplex_layers: tuple[tuple[str, float], ...] = ()
    """If multiplex, `(layer_name, alpha)` per layer; empty otherwise."""


@dataclass(frozen=True)
class ObserverReport:
    """Paper §4 checklist item 6."""

    family: Literal["density-distance", "fm-embedding", "information-theoretic", "custom"]
    window_length: int
    """Paper: w (§3.5)."""

    state_variables: str
    """Plain-English — e.g. 'archive of size 1024, no learned model'."""


@dataclass(frozen=True)
class DescriptorReport:
    """Paper §4 checklist item 7."""

    descriptor_space: str
    archive_update_rule: str
    saturation_criterion: str
    boundedness_or_open_endedness_test: str


@dataclass(frozen=True)
class RNGReport:
    """Paper §4 checklist item 9."""

    scheme: str
    """E.g. 'Philox 4x32-10 via jax.random.split'."""

    key_triple_description: str
    """E.g. '(global seed, worker id, tick)'."""


@dataclass(frozen=True)
class ComplexityReport:
    """Paper §4 checklist item 10."""

    per_tick_wall_clock_seconds: float | None
    theoretical_complexity: str
    """E.g. 'O(|X|/P + N/P + log|X|)' per paper §4 'Many-threaded complexity'."""


# ---------------------------------------------------------------------------
# The aggregate spec and conformance report.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SystemSpec:
    """A snapshot of the 11 conformance items — paper §4."""

    substrate: SubstrateReport | None = None
    entity: EntityReport | None = None
    variation: VariationReport | None = None
    viability: ViabilityReport | None = None
    topology: TopologyReport | None = None
    observer: ObserverReport | None = None
    descriptor: DescriptorReport | None = None
    iteration_order: tuple[SlotName, ...] | None = None
    rng: RNGReport | None = None
    complexity: ComplexityReport | None = None
    pseudocode: str | None = None

    @classmethod
    def from_system(cls, system: System[Any, Any, Any, Any]) -> SystemSpec:
        """Populate what can be introspected from a `System`. The rest stays `None`.

        The user is expected to copy the returned spec, fill in the remaining fields with
        substrate-specific text, and pass the populated spec to `check_conformance`.
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

    def check_conformance(self) -> ConformanceReport:
        """Return per-item pass/fail/missing status — paper §4 line 1346."""
        items: dict[str, ConformanceStatus] = {}
        items["1-substrate"] = "pass" if self.substrate is not None else "missing"
        items["2-entity"] = "pass" if self.entity is not None else "missing"
        items["3-variation"] = "pass" if self.variation is not None else "missing"
        items["4-viability"] = (
            "pass"
            if self.viability is not None and self.viability.formalism_name != "unknown"
            else "missing" if self.viability is None else "fail"
        )
        items["5-topology"] = "pass" if self.topology is not None else "missing"
        items["6-observer"] = "pass" if self.observer is not None else "missing"
        items["7-descriptor"] = "pass" if self.descriptor is not None else "missing"
        items["8-iteration-order"] = (
            "pass" if self.iteration_order is not None else "missing"
        )
        items["9-rng"] = "pass" if self.rng is not None else "missing"
        items["10-complexity"] = "pass" if self.complexity is not None else "missing"
        items["11-pseudocode"] = "pass" if self.pseudocode is not None else "missing"
        return ConformanceReport(items=items)


@dataclass(frozen=True)
class ConformanceReport:
    """Per-item pass/fail/missing status — paper §4 line 1346."""

    items: dict[str, ConformanceStatus] = field(default_factory=dict)

    def is_conformant(self) -> bool:
        """True iff every item is `pass`."""
        return all(status == "pass" for status in self.items.values())


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
    return tuple(
        (type(layer.topology).__name__, float(layer.alpha))
        for layer in topology.layers
    )
