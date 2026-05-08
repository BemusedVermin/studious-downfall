"""Smoke tests for the three concrete distributions in `distribution.py`."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import pytest

from emergent_systems import Categorical, Distribution, Gaussian, PointMass


def test_pointmass_sample_returns_value():
    value = jnp.asarray([1.0, 2.0, 3.0])
    distribution = PointMass(value=value)
    sampled = distribution.sample(jax.random.key(0))
    assert jnp.allclose(sampled, value)


def test_pointmass_log_prob_raises():
    distribution: Distribution[object] = PointMass(value=42)
    with pytest.raises(NotImplementedError):
        distribution.log_prob(42)


def test_gaussian_sample_has_correct_shape():
    loc = jnp.zeros((3,))
    scale = jnp.ones((3,))
    distribution = Gaussian(loc=loc, scale=scale)
    sampled = distribution.sample(jax.random.key(0))
    assert sampled.shape == (3,)


def test_gaussian_log_prob_at_mean_matches_closed_form():
    """At x = loc the per-dim log-density is `-log(scale) - 0.5 log(2π)`; sum over dims."""
    loc = jnp.array([1.0, 2.0])
    scale = jnp.array([0.5, 2.0])
    distribution = Gaussian(loc=loc, scale=scale)

    expected = jnp.sum(-jnp.log(scale) - 0.5 * jnp.log(2.0 * jnp.pi))
    actual = distribution.log_prob(loc)
    assert jnp.allclose(actual, expected)


def test_categorical_sample_in_range():
    logits = jnp.array([0.0, 1.0, -1.0, 2.0])
    distribution = Categorical(logits=logits)
    sampled = distribution.sample(jax.random.key(0))
    assert 0 <= int(sampled) < 4


def test_categorical_log_prob_normalised():
    """Probabilities of all categories should sum to 1."""
    logits = jnp.array([0.0, 1.0, 2.0])
    distribution = Categorical(logits=logits)
    log_probs = jnp.array([distribution.log_prob(jnp.asarray(i)) for i in range(3)])
    total_prob = jnp.sum(jnp.exp(log_probs))
    assert jnp.allclose(total_prob, 1.0, atol=1e-6)
