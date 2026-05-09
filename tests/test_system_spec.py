"""SystemSpec tests — paper §sec:description rendered as data.

The frame is descriptive, not gating: structural items (1-7) are exhibitable for any `System`
by construction, and reproducibility metadata (8-11) is communication hygiene the implementer
fills in. There is no pass/fail.
"""

from __future__ import annotations

from emergent_systems import (
    ComplexityReport,
    DescriptorReport,
    EntityReport,
    RNGReport,
    SystemSpec,
    ViabilityReport,
)
from emergent_systems.spec import REPRODUCIBILITY_FIELDS


def test_from_system_populates_structural_items(toy_system):
    """Items 1-7 are exhibitable for any System by construction."""
    spec = SystemSpec.from_system(toy_system)
    assert spec.substrate is not None
    assert spec.variation is not None
    assert spec.viability is not None
    assert spec.topology is not None
    assert spec.observer is not None
    assert spec.iteration_order == ("dynamics", "variation", "viability")


def test_from_system_leaves_reproducibility_unfilled(toy_system):
    """Items 8-11 (descriptor, rng, complexity, pseudocode) are user-supplied."""
    spec = SystemSpec.from_system(toy_system)
    assert spec.missing_reproducibility_fields() == REPRODUCIBILITY_FIELDS


def test_filling_reproducibility_clears_missing(toy_system):
    spec = SystemSpec.from_system(toy_system)
    filled = SystemSpec(
        substrate=spec.substrate,
        entity=EntityReport(
            supporting_set_rule="trivial — empty topology yields no entities",
            scale_projection_description="identity",
        ),
        variation=spec.variation,
        viability=ViabilityReport(
            formalism_name="custom",
            predicate_description="identity (toy)",
        ),
        topology=spec.topology,
        observer=spec.observer,
        iteration_order=spec.iteration_order,
        descriptor=DescriptorReport(
            descriptor_space="N/A (toy system)",
            archive_update_rule="N/A",
            saturation_criterion="N/A",
            boundedness_or_open_endedness_test="N/A",
        ),
        rng=RNGReport(
            scheme="Philox 4x32-10 via jax.random.split",
            key_triple_description="(global seed, slot index, tick)",
        ),
        complexity=ComplexityReport(
            per_tick_wall_clock_seconds=None,
            theoretical_complexity="O(1) per tick (toy)",
        ),
        pseudocode="for tick in range(N): step(system, joint_state, key, tick)",
    )
    assert filled.missing_reproducibility_fields() == ()


def test_partial_fill_lists_only_remaining_gaps():
    """Reproducibility gaps are reported in paper-item order (descriptor, rng, complexity, pseudocode)."""
    spec = SystemSpec(
        rng=RNGReport(scheme="x", key_triple_description="y"),
        complexity=ComplexityReport(
            per_tick_wall_clock_seconds=None, theoretical_complexity="O(1)"
        ),
    )
    assert spec.missing_reproducibility_fields() == ("descriptor", "pseudocode")
