"""Viability filters and the four named formalisms.

Paper §3.4 (viability): `F : M+(X) → M+(X)` is the rule that says which proposed entities
remain in the run, with what weight. The paper enumerates four formalisms: Markov-blanket
viability, autopoietic closure, RAF set viability, and minimal-criterion coevolution (MCC).

Conjecture C1 (paper §5.1) asks whether all four are instances of the same closure operator.
**Until C1 is settled the four formalisms are not in general substitutable in code** (paper
line 644). We therefore ship them as four separate protocols — *not* as subclasses of a
shared `ClosureViability` base — and provide a generic helper for users who want to verify
that their custom `F` *is* a closure operator on a particular lattice.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Protocol, runtime_checkable

from emergent_systems.population import Population


@runtime_checkable
class ViabilityFilter[State](Protocol):
    """A viability filter — paper: F : M+(X) → M+(X).

    Implementers re-weight or sub-select the proposed population. Selection (zeroing weights),
    fitness-proportional reweighting, and threshold filters all share this signature.
    """

    def __call__(self, population: Population[State]) -> Population[State]: ...


# ---------------------------------------------------------------------------
# The four named formalisms — paper §3.4. Separate, deliberately not unified.
#
# Each formalism specifies the *kind of predicate* an implementer must supply. Sharing
# `ViabilityFilter` lets them slot into the same scaffold; otherwise they are independent
# until conjecture C1 is settled.
# ---------------------------------------------------------------------------


@runtime_checkable
class MarkovBlanketViability[State](ViabilityFilter[State], Protocol):
    """Markov-blanket viability — paper: Friston/Kirchhoff line of work.

    The supporting set must admit a sparse-coupling decomposition into internal/blanket/external
    states. Caveats apply (paper line 619-622); see Aguilera et al. 2022.
    """

    def decompose_blanket(self, state: State) -> tuple[Any, Any, Any]:
        """Return `(internal, blanket, external)` for the given state.

        The framework does not commit to a representation of these substates — implementers
        choose what `Any` means in their substrate.
        """
        ...


@runtime_checkable
class AutopoieticClosureViability[State](ViabilityFilter[State], Protocol):
    """Autopoietic closure — paper: Maturana/Varela; Beer's Game-of-Life glider analysis.

    The supporting set must be closed under the network of constitutive transitions; e.g. a
    GoL glider's support is closed under the GoL preimage relation restricted to the entity's
    reaction network.
    """

    def is_closed_under_reactions(self, supporting_set: Any) -> bool:
        """True iff the supporting set is closed under this entity's reaction network."""
        ...


@runtime_checkable
class RAFSetViability[State](ViabilityFilter[State], Protocol):
    """Reflexively-Autocatalytic Food-generated set viability — paper: Hordijk-Steel.

    A reaction set `R'` passes iff every reaction in `R'` is catalysed by something in `R'` (or
    in the food set) and every reactant is producible from the food set within `R'`.
    """

    def is_raf(self, reaction_set: Any, food_set: Any) -> bool:
        """True iff `reaction_set` is reflexively autocatalytic and food-generated."""
        ...


@runtime_checkable
class MinimalCriterionViability[State](ViabilityFilter[State], Protocol):
    """Minimal Criterion Coevolution — paper: Brant-Stanley; Lehman-Stanley novelty search.

    An entity passes iff it satisfies a minimal qualifying predicate (e.g. 'solves at least
    one maze'), with co-evolutionary feedback supplying the predicate's content.
    """

    def passes_criterion(self, entity: Any) -> bool:
        """True iff the entity satisfies the current minimal criterion."""
        ...


# ---------------------------------------------------------------------------
# Closure-operator verifier — paper §3.1, lines 263-266.
#
# Provided so users who write a *custom* viability filter can check whether it happens to be
# a closure operator on their domain. The framework does not infer or assume this property.
# ---------------------------------------------------------------------------


def verify_is_closure_operator[T](
    closure: Callable[[T], T],
    elements: Iterable[T],
    is_subset: Callable[[T, T], bool],
) -> bool:
    """Check that `closure` is a closure operator on the given lattice — paper §3.1.

    Verifies the three axioms across all elements of the supplied lattice fragment:

    * (i)   Extensivity:    `A ⊆ closure(A)`
    * (ii)  Monotonicity:   `A ⊆ B  ⇒  closure(A) ⊆ closure(B)`
    * (iii) Idempotence:    `closure(closure(A)) == closure(A)`

    Args:
        closure:    The candidate closure operator.
        elements:   A finite sample of lattice points to test against. The check is sound only
                    on the supplied sample; this is a unit-test aid, not a proof tactic.
        is_subset:  The lattice's partial order — `is_subset(a, b)` returns `a ⊑ b`.

    PERF[closure-verifier-quadratic]: monotonicity is checked as a quadratic comparison over
    `elements`; for large lattices, restrict the test sample.
    """
    sample = list(elements)

    for element in sample:
        closed = closure(element)
        if not is_subset(element, closed):
            return False  # extensivity failed
        if not is_subset(closed, closure(closed)) or not is_subset(closure(closed), closed):
            return False  # idempotence failed

    for a in sample:
        for b in sample:
            if is_subset(a, b) and not is_subset(closure(a), closure(b)):
                return False  # monotonicity failed

    return True
