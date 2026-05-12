# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Framing pivot (2026-05-11)

This release contains a major shift in the project's central thesis,
documented in detail in [`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md).
The downstream code and paper edits required to realise the pivot
are tracked in
[`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md); they
are pending as of this entry.

The pivot is from a **descriptive vocabulary** for existing
artificial-life systems to a **predictive characterisation theorem**
for all life — biological, artificial, and culturally constituted.
Concretely:

- The system tuple changes from $\mathcal{S} = (\mathbf{X}, V, F, T, O)$
  to $\mathcal{S} = (\mathbf{X}, V, F, T)$ — the observer $O$ moves
  outside the system as a category-theoretic functor
  $O: \mathbf{Sys} \to \mathbf{Obs}$.
- The ambient category $\mathbf{Sys}$ is now committed to the
  symmetric monoidal category of $\mathcal{O}_W$-algebras in
  $\mathbf{Stoch}$ (Vagner–Spivak–Lerman operad of wiring diagrams),
  with an interpretive lift to a sheaf topos via
  Schultz–Spivak 2019.
- $\mathbf{LifeCat}$ membership is given by a **vitality profile**
  $(k, \boldsymbol{\sigma})$ — search-hierarchy depth $k$ plus a
  level-indexed self-reference vector $\boldsymbol{\sigma}$.
  Membership requires $k \geq 1$. The full profile is reported as
  an attribute of each member.
- The level structure is defined **recursively**, with no fixed
  taxonomy of "substrate / entity / population / meta" levels.
- Composition has two axes: **vertical** (recursive level-raising)
  and **horizontal** ($\boxtimes_\kappa$ at fixed level).
- A new conjecture, **Level Emergence (LE)**, gives the four-condition
  structural mechanism by which a system at depth $k$ transitions
  to depth $k + 1$.

### Added

- [`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md): full audit and
  design document for the framing pivot, including resolutions of
  the four framing-prior questions (Q1: ambient category;
  Q2: $\mathbf{LifeCat}$ membership predicate; Q3: necessity-side
  ambient framework; Q4: descriptive vs. predictive).
- [`docs/vitality_computation.md`](docs/vitality_computation.md):
  algorithmic specification for computing $(k, \boldsymbol{\sigma})$
  on `System` instances, plus composite-system handling, comparison
  machinery, and level-transition detection.
- [`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md):
  comprehensive task tracker for the downstream edit pass across
  paper, code, and trackers; unproven statements are marked
  UNPROVEN.

### Changed

- Reframed the paper's §sec:description ("System Description",
  formerly "Implementation Checklist") and `spec.py` from a
  conformance-gate frame to a descriptive lens: structural items
  (1–7) follow from the slot decomposition and are exhibitable by
  construction, reproducibility metadata (8–11) is communication
  hygiene the implementer supplies. Iteration order moves from
  item 8 to item 7; descriptor moves from item 7 to item 8.
  *Note*: with the framing pivot, this section is further restructured
  — see FRAMING_AUDIT §6.

### Removed

- `ConformanceReport`, `SystemSpec.check_conformance`,
  `is_conformant`, and the `ConformanceStatus` literal. Replaced by
  `SystemSpec.missing_reproducibility_fields() -> tuple[str, ...]`.
- `docs/textbook/` (entire directory: `book.tex`, `preface.tex`,
  `math-primer.tex`, `ch01-what-is-artificial-life.tex` through
  `ch09-frontiers.tex`, and `README.md`). The textbook draft
  articulated the descriptive-vocabulary stance that the framing
  pivot retires; compiling a textbook is premature until the
  framework's claims have empirical and formal support. Future
  expository work moves to focused result papers under
  [`docs/papers/`](docs/papers/) per the existing template.
- `textbook` recipe from `justfile` (built the deleted textbook).

### Pending (tracked in FRAMING_PIVOT_TASKS.md)

- Main-paper rewrite (`docs/emergent_systems.tex`) against the new
  framing.
- Code refactor: `System` dataclass loses the observer slot;
  `run`/`step` signatures change; `spec.py` splits into `SystemSpec` + `ObservationSpec`; new `vitality.py` module.
- Tracker updates to `RESULTS.md`, `IMPLEMENTATION_PLAN.md`,
  `proof_techniques.md`, `CLAUDE.md`, `README.md`.
- A **series of result papers** developed under `docs/papers/`
  rather than a textbook compilation. Each conjecture, worked
  example, and methodology piece becomes its own focused paper
  using the existing `docs/papers/_template/` structure.

### Unproven (tracked in FRAMING_PIVOT_TASKS.md)

The framing pivot introduces new conjectures `S1`, `N1`, `CAT1`,
`LE` alongside the existing `C1`–`C3`, `OP1`–`OP3` (re-pointed as
`C1'`–`C3'`, `L1`, `OP2'`, `OP3'`). All are UNPROVEN as of this
entry. Proof obligations are documented in FRAMING_AUDIT.md §3 and
§5; status is tracked in `RESULTS.md`.

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
