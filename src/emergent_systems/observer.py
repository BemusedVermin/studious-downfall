"""Observer/evaluator and the windowed trajectory it consumes.

Paper §3.5: the observer-evaluator `O` acts on trajectories, not on single ticks. Stateless
observers are functionals `Z^w → ℝ^k`; stateful observers (novelty search, Quality-Diversity)
also carry an observer state `a_t ∈ A_O`:

    O_s : Z^w × A_O → ℝ^k × A_O.

The window length `w` (paper §3.5) is part of the observer specification and is reported in
the system description (structural item 6).

`JointState` and `WindowedTrajectory` live in this module because the system orchestrator
imports them from here; circular imports are avoided by keeping the dependency one-way
(`system.py` imports `observer.py`, never the reverse).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from jaxtyping import Array, Float

from emergent_systems._types import PRNGKey
from emergent_systems.population import Population


@dataclass(frozen=True)
class JointState[State]:
    """One element of the joint state space — paper: `z = (x, μ) ∈ Z = X × M+(X)`."""

    state: State
    """Paper: x ∈ X."""

    population: Population[State]
    """Paper: μ ∈ M+(X)."""


@dataclass(frozen=True)
class WindowedTrajectory[State]:
    """A bounded buffer of recent `JointState`s — paper: a window over `Z^w`.

    Most-recent state is at the end. Construction is the orchestrator's responsibility; this
    type is plain data.

    PERF[windowed-trajectory-list]: a Python list of dataclasses is fine for short windows but
    breaks `jit`/`scan` for long ones. For long windows, replace with a pre-allocated buffer
    of arrays (one leaf per JointState field) and a write-index — JAX-idiomatic and traceable.
    """

    states: Sequence[JointState[State]]

    @property
    def length(self) -> int:
        return len(self.states)


# ---------------------------------------------------------------------------
# Observer protocols.
#
# Paper §3.5 distinguishes stateless `O` from stateful `O_s`. We expose the stateful one as
# the primary interface — the stateless case is recovered by setting the observer state to
# `None`-or-equivalent and ignoring it.
# ---------------------------------------------------------------------------


@runtime_checkable
class StatefulObserver[State, ObserverState](Protocol):
    """A stateful observer-evaluator — paper: `O_s : Z^w × A_O → ℝ^k × A_O`.

    Type parameters:
        State:           the substrate state space — paper: X.
        ObserverState:   the observer's internal state — paper: A_O. Holds archives, learned
                         embeddings, reference distributions, saturation criteria, etc.
    """

    window_length: int
    """Paper: w (§3.5). Number of consecutive ticks the observer consumes."""

    def initial_state(self, key: PRNGKey) -> ObserverState:
        """Sample an initial observer state."""
        ...

    def observe(
        self,
        window: WindowedTrajectory[State],
        observer_state: ObserverState,
    ) -> tuple[Float[Array, "k"], ObserverState]:
        """Score the window and update the observer state — paper: O_s.

        Returns the score vector (one component per observed quantity — novelty, complexity,
        learnability, value, …) alongside the new observer state.
        """
        ...
