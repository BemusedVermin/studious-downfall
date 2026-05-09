# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A typed JAX scaffold for the substrate-agnostic emergent-systems framework defined in [docs/emergent_systems.tex](docs/emergent_systems.tex). The library is the harness; **slot implementations are user-supplied** via Protocols. The library does not ship concrete simulators.

**The paper is a work in progress.** Re-read [docs/emergent_systems.tex](docs/emergent_systems.tex) at the start of any non-trivial change — definitions, conjectures, and section numbering can shift between sessions, and this CLAUDE.md may lag behind. When the paper and this file disagree, the paper wins; update CLAUDE.md to match.

**Conjecture and open-problem status lives in [RESULTS.md](RESULTS.md).** When a conjecture's or open problem's status changes (e.g. a result paper lands under [docs/papers/](docs/papers/)), update `RESULTS.md` and link the result paper.

The plan that drove the initial implementation is committed at [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md). Read it when in doubt about a design decision — it records the alternatives that were considered and rejected. The plan is a snapshot of the v1 design, not a live document; if you make a load-bearing decision that contradicts it, append a note to that file rather than silently diverging.

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

## Architecture: the five-slot model

The paper defines a system as a typed 5-tuple `S = (X, V, F, T, O)` operating on a joint state space `Z = X × M+(X)` via the iteration rule `(x_{t+1}, μ_{t+1}) = (S̃_F ∘ Ṽ_T ∘ Φ̃)(x_t, μ_t)`. Each slot is a `@runtime_checkable Protocol` parameterised with PEP 695 generics:

| Slot | Module | Paper | Protocol |
| --- | --- | --- | --- |
| Substrate | [substrate.py](src/emergent_systems/substrate.py) | `X = (X, Φ, μ_0)` | `Substrate[State, DynamicsParam]` |
| Variation | [variation.py](src/emergent_systems/variation.py) | `V : X × Θ → P(X)` | `Variation[State, Params]` |
| Viability | [viability.py](src/emergent_systems/viability.py) | `F : M+(X) → M+(X)` | `ViabilityFilter[State]` |
| Topology | [topology.py](src/emergent_systems/topology.py) | `T_t` | `InteractionTopology` |
| Observer | [observer.py](src/emergent_systems/observer.py) | `O_s` | `StatefulObserver[State, ObserverState]` |

The orchestrator at [system.py](src/emergent_systems/system.py) is the only module that knows about all five slots at once. It owns:

- `JointState` and `RunResult`
- The `System` dataclass (paper's 5-tuple plus optional `detect_entities`, `hyperedge_params`, `iteration_order`)
- `build_population_variation` / `build_population_variation_multiplex` — the **V_T construction** lives here as a free function, not on `Variation` or `InteractionTopology`. V doesn't know about T; T doesn't know about V.
- `step` (interprets `iteration_order`) and `run` (the main loop with windowed-observer state)

## Load-bearing design decisions

These are the choices that propagate across the codebase. Don't undo them without re-reading the plan.

1. **`P(X)` vs `M+(X)` is a deliberate split.** [distribution.py](src/emergent_systems/distribution.py) (`Distribution[State]`, codomain of V) is **separate** from [population.py](src/emergent_systems/population.py) (`Population[State]`, codomain of F). The paper's V_T formula `Σ_e w_e · V(...)` is a sum of measures, so V cannot be a bare sampler.
2. **Two pushforward methods, not one.** `Population.pushforward_deterministic` vs `pushforward_stochastic` — the stochastic case requires a key and changes weight semantics. Conflating them breaks under jit.
3. **`Substrate` exposes `dynamics_param_space` for `⊠_κ`.** Coupled composition (paper §3.3 line 401) re-parameterises each component's dynamics from the *other* component's state, so `Φ` must be parameterisable. Removing `dynamics_param_space` makes `compose_substrates_coupled` uncheckable.
4. **Iteration order is data, not behaviour.** `System.iteration_order: tuple[Literal["dynamics", "variation", "viability"], ...]` — paper §4 conformance item 8 requires this.
5. **The four viability formalisms are NOT unified.** `MarkovBlanketViability`, `AutopoieticClosureViability`, `RAFSetViability`, `MinimalCriterionViability` are separate Protocols. Conjecture C1 (paper §5.1) is open; the library deliberately does not prejudge it. Do not introduce a `ClosureViability` superclass.
6. **`H_max` is the default, not the only choice.** `effective_information(P, intervention_distribution=None)` — paper §3.6 line 893 calls the uniform intervention "conventional, not unique." Keep the parameter optional.
7. **`ImplicitInSubstrate` short-circuits.** For substrate-as-population paradigms (Lenia, NCA, Flow-Lenia), V_T is the identity (paper §3.1 line 289). The orchestrator checks `isinstance(population, ImplicitInSubstrate)` and bypasses entity detection.

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

## Conformance / `SystemSpec`

[spec.py](src/emergent_systems/spec.py) turns the paper's §4 11-item checklist into structured data. `SystemSpec.from_system(system)` introspects what it can; the user fills in the rest (descriptor space, RNG provenance, complexity figures, pseudocode). `SystemSpec.check_conformance()` returns a per-item `pass/fail/missing` report. This is the artefact a paper using the library should paste into supplementary materials.

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
