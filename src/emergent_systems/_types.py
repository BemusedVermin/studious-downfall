"""Shared type aliases for the framework.

The paper uses single-letter symbols for clarity in mathematical text. In code we use
descriptive English names; the paper symbol is recorded next to each one so readers can move
between the two without translation.
"""

from __future__ import annotations

from jaxtyping import Array, UInt

type PRNGKey = UInt[Array, "2"]
"""A JAX random key. Counter-based PRNG (Philox) — paper §4 'Random-number considerations'."""

type TickIndex = int
"""A discrete time index — paper: t ∈ ℕ."""
