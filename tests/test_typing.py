"""Source-level guards on the typing-vs-perf trade-off.

The plan agent's finding Q6 was that `@beartype` on `Protocol` parameters can be a 10-100×
slowdown on hot paths. We commit to placing runtime checks only at construction-time
boundaries, never inside `step()` / `run()` / `vmap` / `jit`.

These tests source-check the package: no `@beartype` or `@jaxtyped` decorators may appear in
modules reachable from the orchestrator. Documentation strings can mention the names; only
actual decorator-syntax is forbidden.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).parent.parent / "src" / "emergent_systems"
DECORATOR_PATTERN = re.compile(r"^\s*@(?:beartype|jaxtyped)\b", re.MULTILINE)


@pytest.mark.parametrize("source_file", sorted(PACKAGE_ROOT.rglob("*.py")))
def test_no_runtime_typecheck_decorators_in_package(source_file: Path):
    """Forbid `@beartype` / `@jaxtyped` decorator syntax in package modules.

    The library's perf claim depends on hot paths being plain functions. Decorating reachable
    code with `@beartype` would silently break that claim.
    """
    text = source_file.read_text(encoding="utf-8")
    matches = DECORATOR_PATTERN.findall(text)
    assert not matches, (
        f"Found runtime-typecheck decorator(s) in {source_file}: {matches}. "
        f"Move runtime checks to factory-boundary (e.g. System.__init__) instead."
    )


def test_protocol_imports_resolve():
    """The five slot Protocols must all be importable from the public API."""
    import emergent_systems as es

    for name in (
        "Substrate",
        "Variation",
        "ViabilityFilter",
        "InteractionTopology",
        "StatefulObserver",
    ):
        assert hasattr(es, name), f"Missing public export: {name}"
