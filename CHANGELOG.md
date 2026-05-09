# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Reframed the paper's §sec:description ("System Description", formerly "Implementation Checklist") and `spec.py` from a conformance-gate frame to a descriptive lens: structural items (1–7) follow from the slot decomposition and are exhibitable by construction, reproducibility metadata (8–11) is communication hygiene the implementer supplies. Iteration order moves from item 8 to item 7; descriptor moves from item 7 to item 8.

### Removed

- `ConformanceReport`, `SystemSpec.check_conformance`, `is_conformant`, and the `ConformanceStatus` literal. Replaced by `SystemSpec.missing_reproducibility_fields() -> tuple[str, ...]`.

## [0.1.0] - 2026-05-07
### Added
- Initial release: typed JAX scaffold for the substrate-agnostic emergent-systems framework.
- Five-slot model (`Substrate`, `Variation`, `ViabilityFilter`, `InteractionTopology`, `StatefulObserver`) as `@runtime_checkable` Protocols with PEP 695 generics.
- `System` orchestrator with configurable `iteration_order` and population/multiplex `V_T` construction.
- `Population` / `Distribution` split with deterministic and stochastic pushforwards.
- Four independent viability formalisms (Markov-blanket, autopoietic-closure, RAF-set, minimal-criterion).
- Effective-information emergence metric with optional intervention distribution.
- `SystemSpec` helper for the paper's §4 11-item description schema (later reframed in [Unreleased] from a conformance gate to a descriptive lens).
- Empty example stubs for Game of Life, Lenia, Boids, and a coupled-Lenia composite.
- Working-paper source under `docs/emergent_systems.tex` and implementation plan under `docs/IMPLEMENTATION_PLAN.md`.

[Unreleased]: https://github.com/BemusedVermin/studious-downfall/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/BemusedVermin/studious-downfall/releases/tag/v0.1.0
