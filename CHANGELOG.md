# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-07
### Added
- Initial release: typed JAX scaffold for the substrate-agnostic emergent-systems framework.
- Five-slot model (`Substrate`, `Variation`, `ViabilityFilter`, `InteractionTopology`, `StatefulObserver`) as `@runtime_checkable` Protocols with PEP 695 generics.
- `System` orchestrator with configurable `iteration_order` and population/multiplex `V_T` construction.
- `Population` / `Distribution` split with deterministic and stochastic pushforwards.
- Four independent viability formalisms (Markov-blanket, autopoietic-closure, RAF-set, minimal-criterion).
- Effective-information emergence metric with optional intervention distribution.
- `SystemSpec` conformance helper for the paper's §4 11-item checklist.
- Empty example stubs for Game of Life, Lenia, Boids, and a coupled-Lenia composite.
- Working-paper source under `docs/emergent_systems.tex` and implementation plan under `docs/IMPLEMENTATION_PLAN.md`.

[Unreleased]: https://github.com/BemusedVermin/studious-downfall/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/BemusedVermin/studious-downfall/releases/tag/v0.1.0
