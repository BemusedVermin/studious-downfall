# emergent-systems

[![CI](https://github.com/BemusedVermin/studious-downfall/actions/workflows/ci.yml/badge.svg)](https://github.com/BemusedVermin/studious-downfall/actions/workflows/ci.yml)
[![Claude review](https://github.com/BemusedVermin/studious-downfall/actions/workflows/claude-review.yml/badge.svg)](https://github.com/BemusedVermin/studious-downfall/actions/workflows/claude-review.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Powered by JAX](https://img.shields.io/badge/powered%20by-JAX-orange.svg)](https://github.com/google/jax)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A typed JAX scaffold for the substrate-agnostic emergent-systems framework defined in
[`docs/emergent_systems.tex`](docs/emergent_systems.tex).

> **2026-05-11 framing pivot.** The framework was repositioned from a descriptive vocabulary
> for existing artificial-life systems to a **predictive characterisation theorem** for all
> life — biological, artificial, and culturally constituted. The full audit and the new
> conjecture set (S1, N1, CAT1, LE) live in
> [`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md). The downstream task tracker is in
> [`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md). The code refactor (4-slot
> system, external observer functor, vitality-profile module) is pending as of the pivot
> date; the description below reflects the v2 target.

## What this is

The paper specifies an emergent system as a typed 4-tuple

```text
S = (X, V, F, T)
```

— substrate, variation, viability, interaction topology — operating on a joint state
space `Z = X × M+(X)` via the iteration rule
`(x_{t+1}, μ_{t+1}) = (S̃_F ∘ Ṽ_T ∘ Φ̃)(x_t, μ_t)`. The observer is an external
category-theoretic functor `O: Sys → Obs` applied to the system's trajectory; it is not part
of the tuple.

This library encodes those types as Python `Protocol`s and provides the harness that wires them
together. **The library does not ship concrete simulators.** Implementers supply the slots; the
library composes, validates, and runs them. A new `vitality.py` module (pending implementation)
computes the vitality profile $(k, \boldsymbol{\sigma})$ that determines `LifeCat` membership
per [`docs/vitality_computation.md`](docs/vitality_computation.md).

## What the user supplies

| Slot | Protocol | Paper symbol |
|---|---|---|
| Substrate | `Substrate[State, DynamicsParam]` | `X = (X, Φ, μ_0)` |
| Variation | `Variation[State, Params]` | `V : X × Θ → P(X)` |
| Viability | `ViabilityFilter[State]` | `F : M+(X) → M+(X)` |
| Topology | `InteractionTopology` | `T_t` |
| Entity detection | `EntityDetector[State]` | `e = (S, π)` |
| Observer (external) | `StatefulObserver[State, ObserverState]` | `O: Sys → Obs` |

## Naming convention

Identifiers are plain English. Each one carries a `# paper: <symbol>` comment so the code and
the paper can be navigated together without translation.

## Quickstart

```bash
uv sync
uv run pytest
```

## Inspecting runs

Substrate-agnostic plotting helpers live in
[`src/emergent_systems/visualization.py`](src/emergent_systems/visualization.py). They take a
`RunResult` (and, for the topology helper, a topology + entity detector) and return a
`matplotlib.figure.Figure`. Matplotlib is an **optional** dependency — install it with the
`visualization` extra:

```bash
pip install 'emergent-systems[visualization]'
```

```python
from emergent_systems import run
from emergent_systems.visualization import plot_population_mass, plot_observer_trace

result = run(system, n_ticks=200, key=key)
plot_population_mass(result).savefig("mass.png")
plot_observer_trace(result, observer_name="EI").savefig("ei.png")
```

The four helpers are `plot_population_mass`, `plot_observer_trace`,
`plot_viability_filter_ratio`, and `plot_topology_degree`. Substrate-specific renderers
(Lenia grid frames, Boids scatters) belong in per-example notebooks, not here.

## Performance bottlenecks

The library flags hot paths likely to become bottlenecks in pure Python/JAX with the
`PERF` convention (see [`src/emergent_systems/perf.py`](src/emergent_systems/perf.py)). Comments
of the form `# PERF[reason]: ...` mark candidates for a port to a faster language.

## Results

Status of every conjecture (S1, N1, CAT1, LE, C1–C3) and open problem (L1 = OP1, OP2, OP3) is
tracked in [`RESULTS.md`](RESULTS.md). Per-result proof papers live under
[`docs/papers/`](docs/papers/), one self-contained LaTeX project per result; copy
[`docs/papers/_template/`](docs/papers/_template/) to start one.

The catalogue of result papers to be written is in
[`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md) Part 5.

## Status

The framework's conjectures are deliberately **not** baked into the type hierarchy. See
[`docs/emergent_systems.tex`](docs/emergent_systems.tex) and the new conjecture set introduced
by the 2026-05-11 framing pivot (S1, N1, CAT1, LE). The pivot's audit is in
[`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md); the v2 design rationale is in
[`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).
