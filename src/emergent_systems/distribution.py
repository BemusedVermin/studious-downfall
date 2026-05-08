"""Probability measures on the substrate state space.

Paper §3.4: a variation operator has signature
    V : X × Θ → P(X)
where P(X) denotes probability measures on X. This module defines the `Distribution` protocol
that V's codomain must satisfy, plus three concrete building blocks (`PointMass`, `Gaussian`,
`Categorical`) used by canonical variation operators (Gaussian/uniform mutation, bit-flip,
prompt-token resampling, …).

A `Distribution` is *measure-like*, not just a sampler. The framework's V_T construction
(paper §3.4 lines 577-603) treats V's outputs as measures that get summed across hyperedges:

    V_T(μ; x) = Σ_e w_e · V(state(e), θ_e)

A bare sampler would lose the weight semantics that make this sum well-defined, so we keep
`sample` and (optionally) `log_prob` together on the protocol.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import jax
import jax.numpy as jnp
from jaxtyping import Array, Float, Int

from emergent_systems._types import PRNGKey


@runtime_checkable
class Distribution[State](Protocol):
    """A probability measure on the substrate state space — paper: P(X)."""

    def sample(self, key: PRNGKey) -> State:
        """Draw a single state from this distribution."""
        ...

    def log_prob(self, state: State) -> Float[Array, ""]:
        """Log-density (or log-probability mass) at `state`.

        Distributions are free to raise `NotImplementedError`. The framework only requires
        `log_prob` for observers and assessment routines that explicitly opt in.
        """
        ...


# ---------------------------------------------------------------------------
# Concrete building blocks.
#
# These are deliberately small. They are the atoms canonical variation operators use; richer
# distributions are out of scope for the scaffold and live in user code.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PointMass[State](Distribution[State]):
    """A Dirac measure concentrated at a single state — paper: δ_x.

    This is the deterministic case mentioned throughout §3.4: gradient descent, deterministic
    rewrite rules, etc. `log_prob` is degenerate (0 at the atom, −∞ elsewhere) and we don't
    attempt to test equality on arbitrary state types — call sites that need it should override.
    """

    value: State

    def sample(self, key: PRNGKey) -> State:
        del key
        return self.value

    def log_prob(self, state: State) -> Float[Array, ""]:
        del state
        raise NotImplementedError(
            "log_prob on a Dirac measure requires equality on the state type; "
            "supply a typed subclass if you need it."
        )


@dataclass(frozen=True)
class Gaussian(Distribution[Float[Array, "d"]]):
    """An isotropic-or-diagonal Gaussian on ℝ^d — paper §3.4 'Gaussian/uniform mutation'.

    `loc` and `scale` broadcast against each other; `scale` is the per-coordinate standard
    deviation (diagonal covariance), not a full matrix.
    """

    loc: Float[Array, "d"]
    scale: Float[Array, "d"]

    def sample(self, key: PRNGKey) -> Float[Array, "d"]:
        return self.loc + self.scale * jax.random.normal(key, shape=self.loc.shape)

    def log_prob(self, state: Float[Array, "d"]) -> Float[Array, ""]:
        z = (state - self.loc) / self.scale
        per_dim = -0.5 * z**2 - jnp.log(self.scale) - 0.5 * jnp.log(2.0 * jnp.pi)
        return jnp.sum(per_dim)


@dataclass(frozen=True)
class Categorical(Distribution[Int[Array, ""]]):
    """A categorical distribution over a finite alphabet — paper §3.4 'bit-flip', token resampling.

    `logits` are unnormalised log-probabilities over `K` categories.
    """

    logits: Float[Array, "K"]

    def sample(self, key: PRNGKey) -> Int[Array, ""]:
        return jax.random.categorical(key, self.logits)

    def log_prob(self, state: Int[Array, ""]) -> Float[Array, ""]:
        log_normaliser = jax.scipy.special.logsumexp(self.logits)
        return self.logits[state] - log_normaliser
