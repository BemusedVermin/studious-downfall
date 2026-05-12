# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A typed JAX scaffold for the substrate-agnostic emergent-systems framework defined in [docs/emergent_systems.tex](docs/emergent_systems.tex). The library is the harness; **slot implementations are user-supplied** via Protocols. The library does not ship concrete simulators.

> **2026-05-11 framing pivot.** The framework was repositioned from a descriptive vocabulary for existing artificial-life systems to a **predictive characterisation theorem** for all life — biological, artificial, and culturally constituted. The full audit is in [`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md); the downstream task tracker is [`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md). Major consequences for code: the observer leaves the system tuple (4-slot, not 5-slot); `Sys` becomes an SMC of $\mathcal{O}_W$-algebras in $\mathbf{Stoch}$; `LifeCat` membership is given by a vitality profile $(k, \boldsymbol{\sigma})$ computed per [`docs/vitality_computation.md`](docs/vitality_computation.md). The code refactor is pending as of the pivot date; see the same task tracker Part 2. **Until the code has caught up to the v2 design, treat the v1 description in this file as historical for the system-tuple typing, and refer to FRAMING_AUDIT.md for the current target.**

**The paper is a work in progress.** Re-read [docs/emergent_systems.tex](docs/emergent_systems.tex) at the start of any non-trivial change — definitions, conjectures, and section numbering can shift between sessions, and this CLAUDE.md may lag behind. When the paper and this file disagree, the paper wins; update CLAUDE.md to match.

**Conjecture and open-problem status lives in [RESULTS.md](RESULTS.md).** When a conjecture's or open problem's status changes (e.g. a result paper lands under [docs/papers/](docs/papers/)), update `RESULTS.md` and link the result paper. New top-level conjectures introduced by the 2026-05-11 pivot — `S1` (sufficiency), `N1` (necessity), `CAT1` (characterisation), `LE` (level emergence) — are tracked there alongside the original `C1`–`C3` / `OP1`–`OP3`.

The plan that drove the initial implementation is committed at [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md). Read it when in doubt about a design decision — it records the alternatives that were considered and rejected. The plan is a snapshot of the v1 design, not a live document; if you make a load-bearing decision that contradicts it, append a note to that file rather than silently diverging. A v2 addendum at the bottom of `IMPLEMENTATION_PLAN.md` records the post-pivot design changes; both the v1 plan and the v2 addendum should be consulted together.

The downstream expository and proof work is developed as a **series of focused result papers** under [`docs/papers/`](docs/papers/), not as a textbook. The previous textbook draft under `docs/textbook/` was deleted on 2026-05-11; see `CHANGELOG.md`. Do not propose reconstituting it.

## Commands

Use [justfile](justfile) for everything. Common recipes:

- `just install` — sync the dev environment (`uv sync --extra dev`).
- `just check` — run lint + typecheck + coverage-gated test (the full pre-commit gauntlet; mirrors CI).
- `just test` / `just test-one tests/test_emergence.py` — pytest on the suite or one node (no coverage gate; faster iteration).
- `just cov` — pytest with statement + branch coverage; fails if total coverage drops below 80%. The threshold is set on the CLI (`--cov-fail-under=80`) rather than read from `pyproject.toml` because pytest-cov's propagation of `fail_under` is version-sensitive. Same gate runs in CI.
- `just lint` / `just fix` / `just fmt` — ruff.
- `just typecheck` — pyright (basic mode).
- `just paper` — rebuild the scaffolding-paper PDF (uses latexmk).
- `just paper-result <slug>` — rebuild one per-result proof paper at `docs/papers/<slug>/`. See [docs/papers/README.md](docs/papers/README.md).

There is no separate build step — `pyproject.toml` uses hatchling; the package is installed editable by `uv sync`.

## Architecture: the four-slot model (v2, post-pivot)

The paper defines a system as a typed 4-tuple `S = (X, V, F, T)` operating on a joint state space `Z = X × M+(X)` via the iteration rule `(x_{t+1}, μ_{t+1}) = (S̃_F ∘ Ṽ_T ∘ Φ̃)(x_t, μ_t)`. The observer `O` is **outside** the system — a category-theoretic functor `O: Sys → Obs` consumed by `observe(system, trajectory, observer)`, not stored on the `System` dataclass.

Each slot is a `@runtime_checkable Protocol` parameterised with PEP 695 generics:

| Slot | Module | Paper | Protocol |
| --- | --- | --- | --- |
| Substrate | [substrate.py](src/emergent_systems/substrate.py) | `X = (X, Φ, μ_0)` | `Substrate[State, DynamicsParam]` |
| Variation | [variation.py](src/emergent_systems/variation.py) | `V : X × Θ → P(X)` | `Variation[State, Params]` |
| Viability | [viability.py](src/emergent_systems/viability.py) | `F : M+(X) → M+(X)` | `ViabilityFilter[State]` |
| Topology | [topology.py](src/emergent_systems/topology.py) | `T_t` | `InteractionTopology` |

The Observer Protocol (`observer.py` — `StatefulObserver[State, ObserverState]`) still exists as a type for external observers consumed by `observe()`, but is no longer a slot of `System`.

The orchestrator at [system.py](src/emergent_systems/system.py) is the only module that knows about all four slots at once. It owns:

- `JointState` and `RunResult`
- The `System` dataclass (paper's 4-tuple plus optional `detect_entities`, `hyperedge_params`, `iteration_order`)
- `build_population_variation` / `build_population_variation_multiplex` — the **V_T construction** lives here as a free function, not on `Variation` or `InteractionTopology`. V doesn't know about T; T doesn't know about V.
- `step` (interprets `iteration_order`) and `run` (the main loop; the observer is passed as an argument to `run`, not stored on the system).

**Note**: the actual code may still reflect the v1 5-slot typing until the code refactor in [`FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md) Part 2 lands. This table describes the v2 target. The v1 5-slot description is preserved in [git history of CLAUDE.md](#) for reference.

## Load-bearing design decisions

These are the choices that propagate across the codebase. Don't undo them without re-reading the plan.

1. **The observer is external (v2, post-pivot).** Per the 2026-05-11 framing pivot, `O` is no longer a slot inside `System`. The system tuple is `(X, V, F, T)`. The observer is a separate functor `O: Sys → Obs` applied by a free function `observe(system, trajectory, observer)` at the call site. The pre-pivot system-tuple typing (5-slot) is **superseded**. See [`FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md) §2.1–§2.2 for the formal statement and [`FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md) Part 2 for the code-refactor checklist.
2. **`P(X)` vs `M+(X)` is a deliberate split.** [distribution.py](src/emergent_systems/distribution.py) (`Distribution[State]`, codomain of V) is **separate** from [population.py](src/emergent_systems/population.py) (`Population[State]`, codomain of F). The paper's V_T formula `Σ_e w_e · V(...)` is a sum of measures, so V cannot be a bare sampler.
3. **Two pushforward methods, not one.** `Population.pushforward_deterministic` vs `pushforward_stochastic` — the stochastic case requires a key and changes weight semantics. Conflating them breaks under jit.
4. **`Substrate` exposes `dynamics_param_space` for `⊠_κ`.** Coupled composition (paper §3.3 line 401) re-parameterises each component's dynamics from the *other* component's state, so `Φ` must be parameterisable. Removing `dynamics_param_space` makes `compose_substrates_coupled` uncheckable.
5. **Iteration order is data, not behaviour.** `System.iteration_order: tuple[Literal["dynamics", "variation", "viability"], ...]` — structural item 7 of the paper's "System Description" section requires this.
6. **The four viability formalisms are NOT unified.** `MarkovBlanketViability`, `AutopoieticClosureViability`, `RAFSetViability`, `MinimalCriterionViability` are separate Protocols. Conjecture C1 (paper §5.1) is open; the library deliberately does not prejudge it. Do not introduce a `ClosureViability` superclass.
7. **`H_max` is the default, not the only choice.** `effective_information(P, intervention_distribution=None)` — paper §3.6 line 893 calls the uniform intervention "conventional, not unique." Keep the parameter optional.
8. **`ImplicitInSubstrate` short-circuits.** For substrate-as-population paradigms (Lenia, NCA, Flow-Lenia), V_T is the identity (paper §3.1 line 289). The orchestrator checks `isinstance(population, ImplicitInSubstrate)` and bypasses entity detection.
9. **Vitality profile is computed by `vitality.py`, not by `spec.py` (v2 addition).** `LifeCat` membership is given by the vitality profile $(k, \boldsymbol{\sigma})$, computed by the new `vitality.py` module per [`docs/vitality_computation.md`](docs/vitality_computation.md). `spec.py` continues to handle the System Description schema; the two modules compose at the call site.

## Naming convention

Identifiers are plain English. Each identifier whose paper-side name is a Greek letter or single symbol carries a `# paper: <symbol>` sibling comment. Examples:

- `def dynamics(...)  # paper: Φ`
- `class Coupling  # paper: κ`
- `compose_variation_channels  # paper: ⋄_ρ`
- `("dynamics", "variation", "viability")  # paper: Φ, V, F`

Maintain this convention when adding code. The user explicitly asked for it; reverting to Greek symbols defeats the readability goal.

## Performance flagging

Hot paths likely to bottleneck in pure Python/JAX are tagged with `# PERF[<name>]: <reason>` source comments. There's also a runtime helper `flag_bottleneck(name, reason, port_target)` in [perf.py](src/emergent_systems/perf.py) for when a comment isn't enough. The flags exist so a future port to a faster language has clear targets — preserve and add to them, don't quietly delete.

A source-level test ([tests/test_typing.py](tests/test_typing.py)) forbids `@beartype` and `@jaxtyped` decorators inside the package. This protects the perf claim: structural-typing checks on hot paths are a 10-100× silent slowdown. Runtime type checks (when needed) belong at factory boundaries (`System.__init__`, `compose_substrates_coupled`, etc.) only — never inside `step`, `run`, `vmap`, or `jit`.

## System description / `SystemSpec`

[spec.py](src/emergent_systems/spec.py) renders the paper's System Description schema as structured data. The frame is **descriptive, not gating**: the 4-tuple `(X, V, F, T)` is a vocabulary in which any emergent system is read, so the structural items (substrate, entity, variation, viability, topology, iteration order) are exhibitable for any `System` by construction. `SystemSpec.from_system(system)` returns a populated description for those items.

The reproducibility metadata (descriptor space, RNG provenance, complexity figures, pseudocode) is **not** implied by being an emergent system — it's communication hygiene the implementer supplies for replication. Those fields are `None` until filled, and `SystemSpec.missing_reproducibility_fields()` lists which remain.

There is no `check_conformance` and no pass/fail. If you find yourself wanting to gatekeep what counts as conformant, re-read the paper: structural conformance is implied by the system being an emergent system at all.

**v2 split (post-pivot, pending refactor).** The observer-side metadata (window length, observer state, descriptor space, archive update rule, saturation criterion) moves out of `SystemSpec` into a new `ObservationSpec`. The two compose at the call site rather than being combined upstream. See `FRAMING_AUDIT.md` §6 and `FRAMING_PIVOT_TASKS.md` `C-4` for the refactor task.

## Where things deliberately don't go yet

- **Φ-ID emergence** (paper §3.6 line 882) — TODO comment in [emergence.py](src/emergent_systems/emergence.py), out of v1.
- **Ω open-endedness metric and FM-embedding observers** — observer-side; ship as user code patterns once examples exist.
- **Concrete substrate implementations** — [examples/gol/](src/emergent_systems/examples/gol/), [lenia/](src/emergent_systems/examples/lenia/), [boids/](src/emergent_systems/examples/boids/), [coupled_lenia_stub/](src/emergent_systems/examples/coupled_lenia_stub/) are intentionally empty stubs with the slot-default summary in their `__init__.py`. The paper's worked composite example (§3.8) is the template for `coupled_lenia_stub`.

## CI / reviewer

Two GitHub Actions workflows:

- `.github/workflows/ci.yml` — ruff lint + format check, pyright, pytest on every push/PR.
- `.github/workflows/claude-review.yml` — delegates to the `everything-claude-code:python-reviewer` subagent on every non-draft PR. Posts as `github-actions[bot]` (we bypass the action's OIDC → GitHub App exchange because of [anthropics/claude-code-action#1206](https://github.com/anthropics/claude-code-action/issues/1206)). The reviewer applies a **severity ratchet**: round 1 blocks on CRITICAL/HIGH/MEDIUM, round 2+ blocks only on CRITICAL/HIGH so freshly-discovered nits don't loop forever.

The reviewer posts via [scripts/post-pr-review.sh](scripts/post-pr-review.sh) (a one-shot wrapper around `POST /repos/{owner}/{repo}/pulls/{pr}/reviews`) — never via the REST reviews API directly, never via MCP comment-tools, never more than once per run. See [scripts/README.md](scripts/README.md) for payload shape.

Required secrets (add via `Settings → Secrets and variables → Actions`):

- `CLAUDE_CODE_OAUTH_TOKEN` — for the reviewer workflow.

The pattern is adapted from `BemusedVermin/evolution-simulation`'s Rust reviewer; the rationale comments at the top of [claude-review.yml](.github/workflows/claude-review.yml) explain the trigger and authentication choices.

## ruff lint config caveats

`F722`, `F821`, `UP037` are ignored project-wide because jaxtyping uses string-shape annotations like `Float[Array, "N D"]` that ruff misreads as forward references. `N803`/`N806` are ignored because the codebase uses uppercase locals (`X`, `P`, `M`) for paper-symbol fidelity. Don't add `# noqa` comments for these; the project-wide ignore is intentional.
