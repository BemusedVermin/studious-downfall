"""SystemSpec / ConformanceReport tests — paper §4 checklist as data."""

from __future__ import annotations

from emergent_systems import (
    ComplexityReport,
    ConformanceReport,
    DescriptorReport,
    EntityReport,
    RNGReport,
    SystemSpec,
    ViabilityReport,
)


def test_from_system_extracts_what_it_can(toy_system):
    spec = SystemSpec.from_system(toy_system)
    assert spec.substrate is not None
    assert spec.variation is not None
    assert spec.viability is not None
    assert spec.topology is not None
    assert spec.observer is not None
    assert spec.iteration_order == ("dynamics", "variation", "viability")


def test_unfilled_spec_is_not_conformant(toy_system):
    """A spec that hasn't been filled in by hand fails on items 7, 9, 10, 11."""
    spec = SystemSpec.from_system(toy_system)
    report = spec.check_conformance()
    assert not report.is_conformant()
    for missing_item in ("7-descriptor", "9-rng", "10-complexity", "11-pseudocode"):
        assert report.items[missing_item] == "missing"


def test_fully_filled_spec_is_conformant(toy_system):
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
        descriptor=DescriptorReport(
            descriptor_space="N/A (toy system)",
            archive_update_rule="N/A",
            saturation_criterion="N/A",
            boundedness_or_open_endedness_test="N/A",
        ),
        iteration_order=spec.iteration_order,
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
    report = filled.check_conformance()
    assert report.is_conformant(), report.items


def test_conformance_report_round_trips_dict():
    """Items dict is the artefact a paper's supplementary materials would include."""
    from typing import Literal

    items: dict[str, Literal["pass", "fail", "missing"]] = {
        f"item-{i}": "pass" for i in range(11)
    }
    report = ConformanceReport(items=items)
    assert report.is_conformant()
    assert len(report.items) == 11
