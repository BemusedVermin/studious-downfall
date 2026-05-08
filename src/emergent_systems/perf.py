"""Performance-bottleneck flagging.

The paper (§4) maps each slot of the framework onto its own kernel, and the user has asked us
to surface places where pure Python/JAX is unlikely to be fast enough so they can be ported to
a faster language.

Two mechanisms:

1. The `# PERF[reason]: ...` comment convention. Greppable, no runtime cost.
2. `flag_bottleneck(...)` — emits a structured warning the first time a known-slow path runs at
   nontrivial scale. Use sparingly; comments are usually enough.
"""

from __future__ import annotations

import warnings

PERF_FLAG = "PERF"
"""Convention: source comments tagged `# PERF[reason]: ...` mark candidates for porting."""


class PerformanceWarning(UserWarning):
    """A known-slow path has been entered at nontrivial scale."""


_already_warned: set[str] = set()


def flag_bottleneck(name: str, reason: str, port_target: str = "C++/CUDA") -> None:
    """Warn once per process that a known-slow path has been entered.

    Args:
        name: A stable identifier for the call site (used to dedupe).
        reason: Why this path is slow.
        port_target: Suggested language/runtime for a faster reimplementation.
    """
    if name in _already_warned:
        return
    _already_warned.add(name)
    warnings.warn(
        f"[{PERF_FLAG}:{name}] {reason} — consider porting to {port_target}.",
        PerformanceWarning,
        stacklevel=2,
    )
