"""Boids/swarm — paper §3.7 particle-like case.

Defaults from paper Table II:
    π:           flock identifier → centroid + inertia tensor.
    V:           Gaussian on per-particle parameters.
    F:           spatial-cohesion threshold (cluster persists ≥ τ ticks).
    T:           k-NN on positions.
    O:           density-distance archive on ℝ^d.

Stub for v1.
"""
