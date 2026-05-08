"""Lenia ⊠_κ stub-LLM — paper §3.8 worked composite example.

Defaults from paper §3.8:
    Substrate:   X = X_FL ⊠_κ X_LLM with κ = (render_frame, naming_score).
    π:           Flow-Lenia entities → (centroid, mass); LLM agents atomic.
    V:           Gaussian on FL kernel weights ⋄_ρ token-resampling on prompts.
    F:           hierarchical filter — autopoietic FL + MCC LLM + non-extinction joint.
    T:           three-layer multiplex (spatial-overlap ⊔ random-pairing ⊔ stigmergic).
    O:           (Ω-metric, CLIP-novelty) with window w = W.

Stub for v1. The 'stub' in the package name marks that the LLM channel is a deterministic
mock — the worked example is implementation-faithful with no external API dependency.
"""
