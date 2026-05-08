"""Pushforward tests on both Population implementations.

Paper §3.1 line 285-289: Φ̃ pushes μ along Φ. The implicit case is identity; the explicit case
applies Φ per-particle (deterministic) or samples once per particle (stochastic).
"""

from __future__ import annotations

import jax
import jax.numpy as jnp

from emergent_systems import ImplicitInSubstrate, WeightedSamples


def test_implicit_pushforward_is_identity_deterministic():
    population = ImplicitInSubstrate()

    def dynamics(x):
        return x + 1

    pushed = population.pushforward_deterministic(dynamics)
    assert pushed is population


def test_implicit_pushforward_is_identity_stochastic():
    population = ImplicitInSubstrate()
    pushed = population.pushforward_stochastic(
        jax.random.key(0),
        lambda key, x: x,
    )
    assert pushed is population


def test_weighted_samples_total_mass():
    weights = jnp.array([0.5, 1.0, 0.25])
    pop = WeightedSamples(states=jnp.zeros((3, 2)), weights=weights)
    assert jnp.isclose(pop.total_mass, jnp.sum(weights))


def test_weighted_samples_pushforward_deterministic_applies_to_each_particle():
    states = jnp.array([1.0, 2.0, 3.0])
    weights = jnp.array([1.0, 1.0, 1.0])
    pop = WeightedSamples(states=states, weights=weights)

    pushed = pop.pushforward_deterministic(lambda x: x * 2)

    assert isinstance(pushed, WeightedSamples)
    assert jnp.allclose(pushed.states, jnp.array([2.0, 4.0, 6.0]))
    assert jnp.allclose(pushed.weights, weights), "weights must be preserved"


def test_weighted_samples_pushforward_stochastic_keeps_weights():
    """The stochastic pushforward changes states but preserves weights (paper §3.1)."""
    states = jnp.zeros((4,))
    weights = jnp.array([0.1, 0.2, 0.3, 0.4])
    pop = WeightedSamples(states=states, weights=weights)

    pushed = pop.pushforward_stochastic(
        jax.random.key(0),
        lambda key, x: x + jax.random.normal(key),
    )

    assert isinstance(pushed, WeightedSamples)
    assert pushed.states.shape == states.shape
    assert jnp.allclose(pushed.weights, weights)
