# Plan: `emergent_systems` Python library

## Context

The paper at [docs/emergent_systems.tex](docs/emergent_systems.tex) defines a substrate-agnostic emergent-systems framework as a typed 5-tuple `S = (X, V, F, T, O)` with composition operators (`⊠_κ`, `⋄_ρ`), an information-theoretic entity definition, and a Hoel-style causal-emergence assessment. The repository currently contains the paper but no code.

The user wants a Python library where:

- **Code is the documentation.** Identifiers are plain English; the paper's symbol (`X`, `Φ`, `V`, `F`, `T`, `O`, `Z`, `π`, `κ`, `ρ`, `Θ`, `μ`, `EI`, `CE`) is recorded in a sibling comment so readers can navigate between the code and the paper without translation. Example: `def dynamics(...)  # paper: Φ`, `class Coupling  # paper: κ`.
- **Types enforce the paper's constraints.** The signatures `V : X × Θ → P(X)`, `F : M+(X) → M+(X)`, `Φ : X → X` (or `X → P(X)`), `π : ∏_{p∈S} X_p → Y_S` are expressed in the type system (under English names — see naming convention above), not just in docstrings.
- **JAX is the runtime.** Pure functions, jit-compatible, `jax.random.split` for counter-based PRNG (Philox, paper §4).
- **Python is scaffold; components are user-supplied.** Each slot is a Protocol; users write concrete classes; the library composes and runs them.
- **Performance bottlenecks are flagged**, not silently absorbed, so they can be ported to a faster language.

## Package layout

```text
emergent-systems/
  pyproject.toml                # uv-managed; deps: jax, jaxtyping, beartype
  README.md                     # one screen: "read the paper, then read src/"
  src/emergent_systems/
    __init__.py                 # public API surface
    _types.py                   # PRNGKey, type vars (State, Params, DynamicsParam, ObserverState), aliases
    distribution.py             # Distribution[State] Protocol — paper: P(X), codomain of V
    population.py               # Population Protocol — paper: M+(X); WeightedSamples, ImplicitInSubstrate
    substrate.py                # Substrate Protocol (state space, dynamics, initial measure, dynamics_param_space); free + coupled composition — paper: ⊠, ⊠_κ
    variation.py                # Variation Protocol — paper: V: X×Θ → P(X); compose_variation_channels — paper: ⋄_ρ
    topology.py                 # InteractionTopology Protocol — paper: T; Hypergraph; MultiplexTopology
    viability.py                # ViabilityFilter Protocol — paper: F : M+(X) → M+(X); closure-operator helper; named formalisms as separate classes
    observer.py                 # Observer + StatefulObserver Protocols — paper: O, O_s; WindowedTrajectory buffer
    entity.py                   # Entity dataclass — paper: e = (S, π); E1/E2/E3 validators; EntityDetector Protocol
    emergence.py                # effective_information — paper: EI; causal_emergence — paper: CE; partition search (gated + flagged)
    system.py                   # System — paper: S = (X,V,F,T,O); JointState — paper: Z; lifted operators; build_population_variation — paper: V_T; run()
    spec.py                     # SystemSpec; ConformanceReport (the 11-item checklist as data)
    perf.py                     # PERF_FLAG marker + structured-log helper
    examples/
      gol/__init__.py           # stub
      lenia/__init__.py         # stub
      boids/__init__.py         # stub
      coupled_lenia_stub/__init__.py  # stub (Lenia ⊠_κ stub-LLM)
  tests/
    test_distribution.py        # Distribution Protocol smoke
    test_population.py          # pushforward (deterministic & stochastic) on both measure types
    test_substrate_compose.py   # free vs kappa-coupled associativity (up to canonical iso)
    test_variation_compose.py   # diamond_rho: trivial rho recovers tensor product
    test_emergence.py           # EI(uniform)=0; EI(deterministic permutation)=log|X|; CE on a 4-state toy
    test_pipeline.py            # end-to-end tick on a tiny 2-state substrate
    test_typing.py              # asserts no @beartype reachable from run() after first tick
    test_conformance.py         # SystemSpec.from_system(...).is_conformant() on the toy system
```

## Core typing strategy

- **Protocols, not ABCs.** Every slot is a `@runtime_checkable Protocol` so users can write a class that just *has the methods* without inheriting. Matches the paper's "scaffold + components" framing.
- **PEP 695 generics with English type parameter names.** `class Substrate[State, DynamicsParam](Protocol): ...`, `Variation[State, Params]`, `Distribution[State]`, `Population[State]`, `Entity[State]`. The single-letter paper symbols (`X`, `Θ`, `P`) appear in `# paper: ...` sibling comments.
- **`jaxtyping` for tensor-shape annotations** on all array params (`Float[Array, "N D"]`, `Int[Array, "N"]`).
- **`beartype` runtime checks at factory boundaries only**: `SubstrateAgnosticSystem.__init__`, `compose_coupled(...)`, `lift_variation(...)`. **Never inside `jit`/`vmap`.** Enforced by `tests/test_typing.py` walking the call graph from `run()`.
- **Composed substrates produce nested tuple state spaces** (paper §3.3 proposition: associativity is up to canonical iso). Provide `flatten_state(s: Substrate) → Substrate` helper.

## Module specs (the load-bearing details)

### `distribution.py` — paper: `P(X)`, the codomain of `V`

Per paper §3.4, `V_T(μ;x) = Σ_e w_e · V(state(e), θ_e)` is a **weighted sum of probability measures**. So `V` must return a measure-like object, not just a sampler:

```python
class Distribution[State](Protocol):                     # paper: P(X)
    def sample(self, key: PRNGKey) -> State: ...
    def log_prob(self, state: State) -> Float[Array, ""]: ...      # optional
    def as_weighted_samples(self, key: PRNGKey, n: int) -> WeightedSamples[State]: ...
```

Concrete helpers: `PointMass[State]` (paper: Dirac measure; the deterministic case), `Gaussian` on `R^d`, `Categorical` on a finite alphabet — these are the building blocks the paper's variation operators (§3.4) draw from.

### `population.py` — paper: `M+(X)`, the codomain of `F`

```python
class Population[State](Protocol):                       # paper: μ ∈ M+(X)
    @property
    def total_mass(self) -> Float[Array, ""]: ...
    def pushforward_deterministic(self, dynamics: Callable[[State], State]) -> "Population[State]": ...
    def pushforward_stochastic(self, key: PRNGKey, kernel: Callable[[PRNGKey, State], State]) -> "Population[State]": ...

class WeightedSamples[State](Population[State]):         # explicit-population case
    states: State                                        # leading axis = N (batched pytree)
    weights: Float[Array, "N"]                           # nonneg

class ImplicitInSubstrate[State](Population[State]):
    """Substrate-as-population paradigm (Lenia, NCA, Flow-Lenia): μ is encoded in the state itself; pushforward = identity. Paper §3.1 line 289."""
```

Two pushforward methods, not one — the stochastic case requires a key and changes weight semantics.

### `substrate.py` — must expose `Param(Φ)` to make `⊠_κ` checkable

Paper §3.3 line 401: `κ_{i→j} : X_i → Param(Φ_j)` re-shapes `Φ_j`. So `Substrate` must declare its dynamics parameter space:

```python
class Substrate[State, DynamicsParam](Protocol):         # paper: X = (X, Φ, μ_0)
    dynamics_param_space: type[DynamicsParam]            # paper: Param(Φ)
    default_dynamics_param: DynamicsParam
    population_mode: Literal["explicit", "implicit"]     # paper §3.1 line 289 precondition

    def dynamics(self, key: PRNGKey, param: DynamicsParam, state: State) -> State: ...   # paper: Φ
    def initial_state(self, key: PRNGKey) -> State: ...                                  # paper: x_0
    def initial_population(self, key: PRNGKey) -> Population[State]: ...                 # paper: μ_0
```

Free composition (`compose_substrates_independently`) and coupled composition (`compose_substrates_coupled(a, b, coupling)`) are free functions returning a new `Substrate[tuple[StateA, StateB], tuple[ParamA, ParamB]]`. `Coupling[StateA, StateB, ParamA, ParamB]` is a frozen dataclass with `a_to_b: StateA → ParamB` and `b_to_a: StateB → ParamA` (paper: κ).

### `variation.py`

```python
class Variation[State, Params](Protocol):                # paper: V : X × Θ → P(X)
    def __call__(self, state: State, params: Params) -> Distribution[State]: ...
```

`compose_variation_channels(channel_a, channel_b, channel_coupling)` (paper: `⋄_ρ`): trivial coupling (independent) recovers the tensor product, non-trivial supports gene-culture etc. (paper §3.4).

### `system.py` — orchestration; `build_population_variation` lives here

The construction of `V_T` (paper §3.4 lines 577-603) is a **free function**, not a method — `V` doesn't know about `T`, `T` doesn't know about `V`:

```python
def build_population_variation[State, Params](          # paper: V_T construction
    variation: Variation[State, Params],
    topology: InteractionTopology,
    detect_entities: EntityDetector[State],
    hyperedge_params: Callable[[Sequence[Entity[State]]], Params],   # paper: g, the measurable rule, §3.4 line 588
) -> Callable[[PRNGKey, State, Population[State]], Population[State]]: ...

def build_population_variation_multiplex[State](        # paper §3.7 mixture form
    layers: Sequence[tuple[float, Variation[State, Any], InteractionTopology]],
    detect_entities: EntityDetector[State],
    hyperedge_params: Callable[..., Any],
) -> Callable[[PRNGKey, State, Population[State]], Population[State]]: ...
```

Iteration order is **symbolic data**, with English slot names that the runner interprets:

```python
@dataclass(frozen=True)
class JointState[State]:                                # paper: z ∈ Z = X × M+(X)
    state: State                                        # paper: x
    population: Population[State]                       # paper: μ

SlotName = Literal["dynamics", "variation", "viability"]   # paper: Φ, V, F

@dataclass(frozen=True)
class System[State, DynamicsParam, Params]:             # paper: S = (X, V, F, T, O)
    substrate: Substrate[State, DynamicsParam]
    variation: Variation[State, Params]
    viability: ViabilityFilter[State]
    topology: InteractionTopology
    observer: StatefulObserver[State, Any]
    iteration_order: tuple[SlotName, ...] = ("dynamics", "variation", "viability")    # paper §3.1 default
    detect_entities: EntityDetector[State] | None = None
    hyperedge_params: Callable | None = None

def step(system, joint_state: JointState, key: PRNGKey) -> JointState:
    """Interprets system.iteration_order. Validates well-typedness at construction, not per-tick."""

def run(system, n_ticks: int, key: PRNGKey) -> tuple[Trajectory, ObserverOutputs]: ...
```

### `viability.py`

`F : M+(X) → M+(X)` Protocol. Concrete named formalisms (Markov-blanket, autopoietic, RAF, MCC) are **separate classes** — do **not** ship a unified `ClosureViability` superclass (would prejudge conjecture C1, paper §5.1). Ship an *optional* helper `verify_is_closure_operator(c, partial_order)` that checks extensivity/monotonicity/idempotence (paper lines 263-266) for users who write custom `F`.

### `observer.py`

```python
class StatefulObserver[State, ObserverState](Protocol):  # paper: O_s
    window_length: int                                   # paper: w (§3.5)

    def initial_state(self, key: PRNGKey) -> ObserverState: ...
    def observe(
        self,
        window: WindowedTrajectory[State],
        observer_state: ObserverState,
    ) -> tuple[Float[Array, "k"], ObserverState]: ...    # k = number of observed quantities
```

`WindowedTrajectory` is a fixed-length ring buffer over `JointState`s.

### `emergence.py`

```python
def effective_information(                               # paper: EI(M)
    transition_matrix: Float[Array, "n n"],
    intervention_distribution: Float[Array, "n"] | None = None,    # default = uniform; paper: H_max — "conventional, not unique" §3.6 line 893
) -> Float[Array, ""]: ...

def causal_emergence(                                    # paper: CE(M, Π) = EI(M^Π) - EI(M)
    transition_matrix: Float[Array, "n n"],
    partition: Int[Array, "n"],                          # paper: Π
) -> Float[Array, ""]: ...

def find_emergent_partition_bruteforce(transition_matrix, max_states: int = 10):
    """Returns the partition Π that maximises CE. PERF_FLAG: O(B_n) Bell-number explosion.
    Gated at max_states — raises NotImplementedError beyond it. Paper §3.6 line 894: 'only computable for small |X|'."""

def find_emergent_partition_heuristic(transition_matrix, method: Literal["klein2020"] = "klein2020"):
    """PERF_FLAG: heuristic; does not exhaust the supremum. Paper §3.6 line 894-895."""
```

Φ-ID extension (paper §3.6 line 882): leave a `TODO` referencing Rosas/Mediano 2020/2022. Out of v1 scope.

### `spec.py` — the conformance checklist as data

Paper §4 lines 1297-1321 define an 11-item conformance checklist; line 1346 (item iii) makes conformance a typed property. This is the framework's adoption surface — every paper using the library should be able to paste the report into supplementary materials.

```python
@dataclass(frozen=True)
class SystemSpec:                                        # the 11 conformance items from paper §4
    substrate: SubstrateReport
    entity: EntityReport
    variation: VariationReport
    viability: ViabilityReport
    topology: TopologyReport
    observer: ObserverReport
    descriptor: DescriptorReport
    iteration_order: tuple[SlotName, ...]                # ("dynamics", "variation", "viability") by default
    rng: RNGReport
    complexity: ComplexityReport
    pseudocode: str

    @classmethod
    def from_system(cls, system: System) -> "SystemSpec": ...

    def check_conformance(self) -> "ConformanceReport": ...

@dataclass(frozen=True)
class ConformanceReport:
    items: dict[str, Literal["pass", "fail", "missing"]]
    def is_conformant(self) -> bool: return all(v == "pass" for v in self.items.values())
```

### `perf.py`

```python
PERF_FLAG = "PERF"  # convention: comments are `# PERF[reason]: ...`

def flag_bottleneck(name: str, reason: str, port_target: str = "C++/CUDA") -> None:
    """Emits a structured warning the first time a known-slow path runs. Use sparingly; prefer code comments."""
```

## Build / test / lint setup

- **`pyproject.toml`** — `[build-system]` hatchling, `[project]` deps `jax>=0.4.30`, `jaxtyping>=0.2.30`, `beartype>=0.18`, `[project.optional-dependencies] dev = [pytest, ruff, pyright]`.
- **`uv`** for env + lock (`uv sync`, `uv run pytest`).
- **`ruff`** for lint+format (one config block in pyproject).
- **`pyright`** in basic mode for static checks (PEP 695 generics need it).
- **`pytest`** for tests; the `test_typing.py` walker uses `inspect` to verify no `@beartype` is reachable from `run()` after the first tick.

## Verification plan

1. **Static**: `uv run pyright src/` clean.
2. **Lint**: `uv run ruff check src/ tests/` clean.
3. **Unit tests**: `uv run pytest tests/` — every Protocol has a smoke test; every composition operator has an associativity test; EI has the two canonical cases (uniform → 0, deterministic permutation → log|X|).
4. **End-to-end**: `tests/test_pipeline.py` runs a 10-tick simulation on a 2-state substrate (just enough to exercise the iteration-order interpreter, lifted operators, and observer state).
5. **Typing-on-hot-path**: `tests/test_typing.py` introspects the call graph from `run()` and fails if any reachable function carries `@beartype`/`@jaxtyped`. This is the test that protects the perf claim.
6. **Conformance**: `tests/test_conformance.py` builds the toy system, calls `SystemSpec.from_system(...).check_conformance()`, asserts all 11 items pass.

## Out of scope for v1 (deliberate)

- Φ-ID emergence (paper §3.6 extension) — TODO comment in `emergence.py`.
- Closure-operator unification of viability formalisms — left as conjecture C1 in the paper; the library deliberately does not unify them.
- Ω open-endedness metric and FM-embedding observers — observer-side; ship as user-code patterns once examples exist, not as built-ins.
- Non-trivial example implementations — directories and `__init__.py` exist; bodies are empty per user direction.

## Critical files for implementation

- [docs/emergent_systems.tex](docs/emergent_systems.tex) — the paper, especially §3.1 (framework), §3.4 (V_T construction lines 577-603), §3.2 (entity definition lines 460-495), §3.6 (EI/CE definitions lines 800-895), §4 (the 11-item checklist lines 1297-1321).
- [src/emergent_systems/system.py](src/emergent_systems/system.py) — orchestration, lifted operators, `lift_variation` free function, iteration-order interpreter.
- [src/emergent_systems/distribution.py](src/emergent_systems/distribution.py) and [src/emergent_systems/population.py](src/emergent_systems/population.py) — the `P(X)` vs `M+(X)` split that the paper requires.
- [src/emergent_systems/substrate.py](src/emergent_systems/substrate.py) — must expose `param_space` for `⊠_κ` to be checkable.
- [src/emergent_systems/spec.py](src/emergent_systems/spec.py) — `SystemSpec` is the framework's adoption surface (descriptive, not gating — see divergence note below).

## Divergence from the v1 plan — 2026-05-09

The v1 plan above (and the prose throughout this file) frames `spec.py` as a **conformance** mechanism: an 11-item checklist that papers must pass, with `ConformanceReport` returning `pass/fail/missing` per item. That framing has been retired. The framework's purpose is to **elucidate the structure of any emergent system**, not to certify which systems comply. Conformance is implied by being an emergent system; the slot decomposition is exhibitable by construction.

What changed:

- Paper §sec:checklist → §sec:description ("Implementation Checklist" → "System Description"). The 11 items are split into structural items 1–7 (read off the slot decomposition) and reproducibility metadata 8–11 (specified by the implementer). Iteration order moved from item 8 to item 7; descriptor moved from item 7 to item 8. Cross-references retargeted.
- `spec.py`: `ConformanceReport`, `check_conformance`, `is_conformant`, and the `ConformanceStatus` literal are removed. The new method is `SystemSpec.missing_reproducibility_fields() -> tuple[str, ...]`.

Treat the rest of this plan as a snapshot of the v1 design; the spec-as-gate framing in §`spec.py — the conformance checklist as data` and the surrounding test descriptions are superseded.

## Divergence from the v1 plan — 2026-05-11 (framing pivot, v2 design)

This addendum supersedes the v1 plan above for the components the
framing pivot touches. See [`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) for
the full audit and [`FRAMING_PIVOT_TASKS.md`](FRAMING_PIVOT_TASKS.md)
Part 2 for the corresponding code tasks.

### What changed structurally

The framework is no longer a 5-slot descriptive vocabulary; it is a
4-slot predictive characterisation theorem with an external observer
functor. The change cascades through the code as follows:

- **System tuple is now $(\mathbf{X}, V, F, T)$.** The observer slot
  `O` is removed from `System` and from the iteration. The observer
  becomes a category-theoretic functor $O: \mathbf{Sys} \to \mathbf{Obs}$
  attached at run time, not stored on the system.
- **Iteration rule unchanged.** $\widetilde{S}_F \circ \widetilde{V}_T \circ \widetilde{\Phi}$
  remains the canonical tick.
- **Ambient category committed.** $\mathbf{Sys}$ is the SMC of
  $\mathcal{O}_W$-algebras in $\mathbf{Stoch}$. An interpretive lift
  to a sheaf topos is available via Schultz–Spivak 2019 /
  classifying-topos / substrate-induced-locality, but is not
  foundational.
- **`LifeCat` membership predicate is the vitality profile
  $(k, \boldsymbol{\sigma})$.** Membership requires $k \geq 1$. See
  [`vitality_computation.md`](vitality_computation.md) for the
  algorithm.

### What the v2 code changes need

**`System` dataclass** ([`src/emergent_systems/system.py`](../src/emergent_systems/system.py)):
remove the `observer` field; `run(system, observer, ...)` takes the
observer as an argument. New helper `observe(system, trajectory, observer)`
applies an external observer functor to a trajectory.

**`SystemSpec` split** ([`src/emergent_systems/spec.py`](../src/emergent_systems/spec.py)):
the spec splits into `SystemSpec` (structural items 1–7) +
`ObservationSpec` (observer family, window, state, descriptor
space). The two compose at the call site.

**New module `vitality.py`** ([`src/emergent_systems/vitality.py`](../src/emergent_systems/vitality.py)):
implements the algorithm from [`vitality_computation.md`](vitality_computation.md).
Provides `VitalityProfile`, `compute_vitality_profile`,
`compute_composite_vitality_profile`, `infer_coupling_structure`,
plus comparison machinery (`are_structurally_equivalent`,
`partial_order_compare`, `observer_mediated_compare`,
`compare_systems`) and transition-detection machinery
(`detect_level_transition`, `scan_trajectory_for_transitions`).

**Conditional transfer entropy helper.** Pin one of IDTxl / JIDT /
pyinform in `pyproject.toml`; alternatively, write a
Kraskov-Stögbauer-Grassberger estimator in pure JAX.

**Counterfactual perturbation infrastructure.** Helper for
`has_discriminative_capacity` that runs the system with and without
an injected mutant.

**Substrate-specific entity detectors.** Extend
[`entity.py`](../src/emergent_systems/entity.py) with
connected-component / DBSCAN / syntactic detectors per
[`vitality_computation.md`](vitality_computation.md) §1.2.

**Test fixtures.** Add `tests/test_vitality.py` with fixtures
matching the regression table in
[`vitality_computation.md`](vitality_computation.md) §"Validation":
hurricane → $(0, ())$, converged GA → $(1, (0))$, active Tierra →
$(2, (1, 1))$, etc. Update `tests/test_pipeline.py` and
`tests/test_conformance.py` to construct system and observer
separately.

### What survives unchanged from v1

- The four viability formalisms remain separate (`MarkovBlanketViability`,
  `AutopoieticClosureViability`, `RAFSetViability`,
  `MinimalCriterionViability`). C1' (closure-operator unification)
  is still UNPROVEN; the library deliberately does not unify them.
- `Distribution[State]` / `Population[State]` split is unchanged.
- Performance-flagging discipline (`PERF[...]` comments) is unchanged.
- No `@beartype` / `@jaxtyped` on hot paths (the test-typing
  guard remains).
- The naming convention (English identifiers + `# paper: <symbol>`
  comments) is unchanged.

### What is no longer load-bearing

- The observer-as-slot typing (`Observer` Protocol stays as a
  Protocol, but it is no longer composed *inside* `System`; it is
  consumed *by* `observe()` at the call site).
- The "five-slot model" framing throughout this plan.
- `SystemSpec` as a single document for both structural and
  observation-side data (now split).

The full task breakdown for the v2 code refactor is in
[`FRAMING_PIVOT_TASKS.md`](FRAMING_PIVOT_TASKS.md) Part 2 (`C-1`
through `C-12`).
