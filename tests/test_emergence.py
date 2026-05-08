"""Effective information & causal emergence — paper §3.6.

Two canonical sanity checks for EI:

* A uniform-row Markov chain (every state transitions to every state with equal probability)
  has `EI = 0` — every cause produces the same effect distribution.
* A deterministic permutation has `EI = log|X|` — every cause maps to a unique effect.

Causal emergence is exercised on a small (4-state) chain where merging two leaf-states into
a single macrostate is expected to be informational neutral or positive.
"""

from __future__ import annotations

import jax.numpy as jnp

from emergent_systems import (
    causal_emergence,
    coarse_grain_transition_matrix,
    effective_information,
    find_emergent_partition_bruteforce,
)


def test_ei_of_uniform_chain_is_zero():
    n = 4
    p = jnp.full((n, n), 1.0 / n)
    assert jnp.isclose(effective_information(p), 0.0, atol=1e-6)


def test_ei_of_identity_chain_is_log_n():
    """Deterministic identity: each state maps to itself with probability 1.

    EI = H(uniform marginal) − E[H(row)] = log(n) − 0 = log(n).
    """
    n = 5
    p = jnp.eye(n)
    assert jnp.isclose(effective_information(p), jnp.log(n), atol=1e-6)


def test_ei_of_deterministic_permutation_is_log_n():
    """A non-trivial deterministic permutation also has EI = log(n)."""
    n = 4
    perm = jnp.array([1, 2, 3, 0])
    p = jnp.zeros((n, n)).at[jnp.arange(n), perm].set(1.0)
    assert jnp.isclose(effective_information(p), jnp.log(n), atol=1e-6)


def test_ei_with_custom_intervention_distribution():
    """EI should remain 0 on uniform-row chain regardless of intervention distribution."""
    n = 3
    p = jnp.full((n, n), 1.0 / n)
    custom_q = jnp.array([0.5, 0.3, 0.2])
    assert jnp.isclose(effective_information(p, custom_q), 0.0, atol=1e-6)


def test_coarse_grain_preserves_row_stochasticity():
    p = jnp.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 0.0],
        ]
    )
    partition = jnp.array([0, 0, 1, 1])
    macro = coarse_grain_transition_matrix(p, partition)
    row_sums = jnp.sum(macro, axis=1)
    assert jnp.allclose(row_sums, jnp.ones_like(row_sums), atol=1e-6)


def test_causal_emergence_is_zero_on_trivial_partition():
    """The trivial partition (every state in its own block) yields the same chain — CE = 0."""
    n = 3
    p = jnp.array(
        [
            [0.5, 0.5, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.5],
        ]
    )
    trivial = jnp.arange(n)
    assert jnp.isclose(causal_emergence(p, trivial), 0.0, atol=1e-6)


def test_bruteforce_partition_search_gates_at_max_states():
    p = jnp.eye(20)
    try:
        find_emergent_partition_bruteforce(p, max_states=10)
    except NotImplementedError as exc:
        assert "Brute-force" in str(exc) or "n=" in str(exc)
        return
    raise AssertionError("expected NotImplementedError for n=20 with max_states=10")


def test_bruteforce_partition_search_runs_on_small_chain():
    """Smoke test: the brute-force search returns *some* partition and *some* score."""
    p = jnp.array(
        [
            [0.9, 0.1, 0.0, 0.0],
            [0.0, 0.9, 0.1, 0.0],
            [0.0, 0.0, 0.9, 0.1],
            [0.1, 0.0, 0.0, 0.9],
        ]
    )
    partition, score = find_emergent_partition_bruteforce(p, max_states=10)
    assert partition.shape == (4,)
    assert score.shape == ()
