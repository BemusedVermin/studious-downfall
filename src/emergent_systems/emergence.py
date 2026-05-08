"""Effective information and causal emergence.

Paper §3.6: Hoel-style causal emergence is anchored on *effective information*

    EI(M) = (1/|X|) · Σ_i KL(P_{i,·} || P̄_·)

where `P̄_· = (1/|X|) · Σ_i P_{i,·}` is the marginal effect distribution under uniform
interventions. Equivalently `EI = H(P̄) − (1/|X|)·Σ_i H(P_{i,·})`.

*Causal emergence* at a coarse-graining `Π` is

    CE(M, Π) = EI(M^Π) − EI(M).

A system is causally emergent iff `sup_Π CE(M, Π) > 0` (paper Definition 3.6.2). The
supremum is intractable in general (paper §3.6 line 894); we ship `EI`, a `CE` that takes
the partition as data, a brute-force partition search gated at small `n`, and a placeholder
for the heuristic from Klein & Hoel 2020.

Φ-ID (paper §3.6 line 882) is an extension that replaces partition-based coarse-grainings
with arbitrary supervenient features. It is methodologically more demanding and is left as
TODO; a partition-based API does not extend to it naturally.
"""

# TODO: Φ-ID — replace partition-based coarse-grainings with arbitrary supervenient features.
# References: Rosas et al. 2020 "Reconciling..."; Mediano et al. 2022. Out of v1 scope.

from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

import jax.numpy as jnp
from jaxtyping import Array, Float, Int

# ---------------------------------------------------------------------------
# Effective information — paper Definition 3.6.1.
# ---------------------------------------------------------------------------


def effective_information(
    transition_matrix: Float[Array, "n n"],
    intervention_distribution: Float[Array, "n"] | None = None,
) -> Float[Array, ""]:
    """Effective information of a finite-state Markov chain — paper: EI(M).

    Args:
        transition_matrix:
            Row-stochastic matrix `P` with `P[i, j] = Pr[x^{t+1} = j | x^t = i]`.
        intervention_distribution:
            The intervention distribution over causes — paper: H_max. Defaults to uniform,
            which the paper notes is "conventional, not unique" (line 893). Pass an explicit
            distribution to follow Dewhurst-2021's critique.

    Returns:
        EI(M) as a scalar in nats.
    """
    n = transition_matrix.shape[0]
    if intervention_distribution is None:
        intervention_distribution = jnp.full((n,), 1.0 / n)

    marginal_effect = intervention_distribution @ transition_matrix
    row_entropies = -jnp.sum(_xlogx(transition_matrix), axis=1)
    marginal_entropy = -jnp.sum(_xlogx(marginal_effect))
    expected_row_entropy = jnp.sum(intervention_distribution * row_entropies)
    return marginal_entropy - expected_row_entropy


def _xlogx(x: Float[Array, "..."]) -> Float[Array, "..."]:
    """`x · log(x)` with the convention `0 · log(0) = 0`. Returns 0 where x ≤ 0."""
    return jnp.where(x > 0, x * jnp.log(jnp.where(x > 0, x, 1.0)), 0.0)


# ---------------------------------------------------------------------------
# Causal emergence — paper Definition 3.6.2.
# ---------------------------------------------------------------------------


def coarse_grain_transition_matrix(
    transition_matrix: Float[Array, "n n"],
    partition: Int[Array, "n"],
) -> Float[Array, "m m"]:
    """Lift `P` to a macroscale transition matrix at coarse-graining `Π` — paper §3.6.

    The canonical choice (Klein & Hoel 2020) averages micro-transitions weighted by the
    uniform intra-class distribution: each macrostate's outgoing distribution is the average
    of its members' outgoing distributions, summed within the destination macrostate.

    Args:
        transition_matrix: row-stochastic `P` of shape (n, n).
        partition:         an array of length n where `partition[i]` ∈ {0, ..., m-1} is the
                           macrostate index containing micro-state i.

    Returns:
        The macroscale transition matrix `P^Π` of shape (m, m).
    """
    num_macrostates = int(jnp.max(partition)) + 1

    # Indicator matrix S of shape (n, m): S[i, c] = 1 iff i belongs to macrostate c.
    membership = jnp.eye(num_macrostates)[partition]  # (n, m)

    # Average-out distribution: for each micro-state, sum over destination macrostate.
    micro_to_macro = transition_matrix @ membership  # (n, m)

    # Average-in: for each source macrostate, average over its constituent micro-states.
    class_sizes = jnp.sum(membership, axis=0)  # (m,)
    macro_transition = (membership.T @ micro_to_macro) / class_sizes[:, None]
    return macro_transition


def causal_emergence(
    transition_matrix: Float[Array, "n n"],
    partition: Int[Array, "n"],
) -> Float[Array, ""]:
    """`CE(M, Π) = EI(M^Π) − EI(M)` — paper Definition 3.6.2.

    Positive values mean the macroscale at `Π` carries more effective information than the
    microscale; negative values mean the coarse-graining loses information.
    """
    macro = coarse_grain_transition_matrix(transition_matrix, partition)
    return effective_information(macro) - effective_information(transition_matrix)


# ---------------------------------------------------------------------------
# Partition search.
#
# Paper §3.6 line 894: 'Sup-over-Π is only computable for small |X|; tractable algorithmic
# relaxations exist but do not exhaust the supremum.' We expose two functions: an honest
# brute-force enumerator gated at small n, and a stub for the Klein-2020-style heuristic
# whose contract is 'good Π, not necessarily the supremum.'
# ---------------------------------------------------------------------------


def find_emergent_partition_bruteforce(
    transition_matrix: Float[Array, "n n"],
    max_states: int = 10,
) -> tuple[Int[Array, "n"], Float[Array, ""]]:
    """Enumerate all partitions of `{0, ..., n-1}` and return the one maximising CE.

    PERF[ce-bruteforce-bell-number]: enumeration is `O(B_n)` (Bell number). `B_10 ≈ 1.16e5`,
    `B_15 ≈ 1.4e9`, `B_20 ≈ 5.8e13`. Gated at `max_states` — raises `NotImplementedError` on
    larger systems. For production scale, use a heuristic search (see
    `find_emergent_partition_heuristic`) or port partition enumeration to a faster language.
    """
    n = transition_matrix.shape[0]
    if n > max_states:
        raise NotImplementedError(
            f"Brute-force partition search is gated at n={max_states}; got n={n}. "
            f"Use find_emergent_partition_heuristic, or supply Π explicitly. "
            f"Paper §3.6 line 894."
        )

    best_partition = jnp.zeros((n,), dtype=jnp.int32)
    best_score = causal_emergence(transition_matrix, best_partition)

    for assignment in _enumerate_partitions(n):
        candidate = jnp.asarray(assignment, dtype=jnp.int32)
        score = causal_emergence(transition_matrix, candidate)
        if bool(score > best_score):
            best_score = score
            best_partition = candidate

    return best_partition, best_score


def find_emergent_partition_heuristic(
    transition_matrix: Float[Array, "n n"],
    method: Literal["klein2020"] = "klein2020",
) -> tuple[Int[Array, "n"], Float[Array, ""]]:
    """Heuristic partition search — paper §3.6 line 894-895.

    PERF[ce-heuristic-stub]: not yet implemented. Plug in Klein & Hoel 2020's greedy-merge
    routine (or another heuristic) as the substrate-agnostic default. The contract is
    'good Π, not necessarily the supremum' — see paper Definition 3.6.2.
    """
    del transition_matrix, method
    raise NotImplementedError(
        "Heuristic partition search not yet implemented. Implementer-supplied for now; "
        "see Klein & Hoel 2020 (paper §3.6 line 894) for the canonical greedy-merge approach."
    )


def _enumerate_partitions(n: int) -> Iterator[list[int]]:
    """Yield all set-partitions of `{0, ..., n-1}` as restricted-growth functions.

    Each yielded list `a` of length `n` has `a[0] == 0` and `a[i+1] ≤ 1 + max(a[:i+1])`.
    Worst-case output count is the Bell number `B_n`.
    """

    def helper(i: int, max_so_far: int, current: list[int]) -> Iterator[list[int]]:
        if i == n:
            yield list(current)
            return
        for k in range(max_so_far + 2):
            current.append(k)
            yield from helper(i + 1, max(max_so_far, k), current)
            current.pop()

    yield from helper(0, -1, [])
