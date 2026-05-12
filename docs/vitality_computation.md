# Computing the vitality profile $(k, \boldsymbol{\sigma})$

This document specifies an algorithm for computing the vitality
profile of a given `System` instance against a trajectory. It
makes the framework's central predicate of
[`FRAMING_AUDIT.md` §2.3](FRAMING_AUDIT.md) operational and
testable. The spec is detailed enough to implement as a
`vitality.py` module that slots into the existing
[`src/emergent_systems/`](../src/emergent_systems/) scaffold per
[`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md).

The algorithm has two stages. **Stage 1** detects the
search-hierarchy depth $k$ via the recursive level definition.
**Stage 2** measures $\sigma_i \in [0, 1]$ at each level
$1 \leq i \leq k$ via conditional transfer entropy or — in the
expensive but unambiguous variant — counterfactual perturbation.
The two stages are independent and reusable across substrates.

The framework's existing modules already supply most primitives:
[`emergence.py`](../src/emergent_systems/emergence.py) computes
effective information and Hoel causal emergence;
[`entity.py`](../src/emergent_systems/entity.py) validates the
E1/E2/E3 entity conditions; [`viability.py`](../src/emergent_systems/viability.py)
exposes the four named viability formalisms;
[`observer.py`](../src/emergent_systems/observer.py) handles
windowed trajectories. The new `vitality.py` module composes
these primitives plus one new helper (conditional transfer
entropy) into the profile computation.

---

## Stage 1 — Detect $k$ recursively

The recursive level definition of FRAMING_AUDIT.md §2.3 gives the
algorithm directly.

```text
INPUT:  system : System          # 4-tuple (X, V, F, T)
        trajectory : Trajectory  # joint-state sequence (x_t, μ_t)
        max_levels : int         # cap to prevent runaway recursion
        epsilon : float          # E1 closure tolerance

OUTPUT: k : int                  # deepest level reached

# Base case: level 0
if not has_nontrivial_substrate_dynamics(system, trajectory):
    return -1                    # not even level 0; degenerate
level_0_entities := detect_level_0_entities(system, trajectory, epsilon)
if level_0_entities is empty:
    return 0                     # Φ acts but no persistent patterns

# Recursive case
current_entities := level_0_entities
k := 0
for n in 1 .. max_levels:
    V_n, F_n := infer_search_operators_at_level(
        system, current_entities, trajectory, level=n
    )
    if V_n is None or F_n is None:
        break                    # no search at level n; stop
    if not has_discriminative_capacity(V_n, F_n, current_entities,
                                       trajectory):
        break                    # search present but unresponsive; stop
    level_n_entities := detect_persistent_patterns(
        V_n, F_n, current_entities, epsilon
    )
    if level_n_entities is empty:
        break                    # no level-n entities; stop
    current_entities := level_n_entities
    k := n
return k
```

The five helpers are described below; each is implementable from
existing primitives.

### 1.1 `has_nontrivial_substrate_dynamics`

Test whether $\Phi$ explores more than one state. Two
implementations:

- **Cheap.** Count distinct states visited along the trajectory.
  If $\geq 2$, non-trivial. Sufficient for most cases.
- **Sharper.** Compute $\sup_\Pi \mathrm{CE}(M(\mathcal{S}), \Pi) > 0$
  via the existing `emergence.effective_information` and the
  Klein–Hoel spectral partition search. Reuses the existing
  causal-emergence machinery.

The sharper version detects systems whose trajectories visit many
states but whose causal structure is trivial (e.g.\ pure noise on
a large state space). The cheap version misses those.

### 1.2 `detect_level_0_entities`

Find persistent patterns under $\Phi$ alone. Substrate-specific
helpers; the [`entity.py`](../src/emergent_systems/entity.py)
detectors already provide most of these.

| Substrate type           | Detector                                                        |
|--------------------------|-----------------------------------------------------------------|
| Lattice (GoL, Lenia)     | Connected-component clustering above an activity threshold      |
| Particle (Boids)         | DBSCAN / agglomerative clustering on positions                  |
| Graph                    | Community-detection (Louvain, modularity-maximisation)          |
| Discrete programs        | Syntactic entity boundaries (each program = one entity)         |
| Substrate-as-population  | `ImplicitInSubstrate`; level-0 entities = substrate state itself|

For substrates without a natural locality structure, fall back to
the **information-closure search** of paper §3.2 (E1): search over
candidate supporting sets $S$, retain those satisfying the
mutual-information closure condition within tolerance $\epsilon$.
Expensive but well-defined.

A level-0 entity is then validated by:

- It has positive support on at least one trajectory window.
- It satisfies E1 with $V$ as identity (persistence is by $\Phi$,
  not by separate variation).
- It is finite (E2) and admits hierarchical composition (E3).

The existing `Entity` dataclass with its E1/E2/E3 validators in
`entity.py` already does this — the only specialisation needed is
running the E1 check with $V = \mathrm{id}$.

### 1.3 `infer_search_operators_at_level`

Given a set of level-$(n-1)$ entities, look for $(V_n, F_n)$
acting on them. Three sub-tests, formalised per
[`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) §2.3 ("Formal definitions
of non-trivial $V$, non-trivial $F$, and discriminative capacity"):

**$V_n$ non-trivial.** A variation kernel
$V_n : E_{n-1} \times \Theta \to \mathcal{P}(E_{n-1})$ exists and
satisfies: $\exists e \in E_{n-1}, \theta \in \Theta$ such that
$V_n(e, \theta) \neq \delta_e$ (Dirac on $e$). Operationally:
track entities across the trajectory, fit a transition model from
entity to entity. The model is *non-trivial* iff there is some
input entity for which the model assigns positive probability to
at least one output entity different from the input. A stronger
test (*diversifying*): the transition model has positive Shannon
entropy on some input — this filters near-deterministic kernels.

**$F_n$ non-trivial.** A viability filter
$F_n : \mathcal{M}_+(E_{n-1}) \to \mathcal{M}_+(E_{n-1})$ exists
and satisfies: $\exists e_1, e_2 \in E_{n-1}$ such that
$F_n(\delta_{e_1})(\{e_1\}) / F_n(\delta_{e_2})(\{e_2\}) \neq 1$.
Operationally: compute per-entity retention rates over the
trajectory, $r(e) := \mathbb{E}_t [F_n(\delta_e)(\{e\})]$. If the
ratio $r(e_1) / r(e_2)$ deviates from 1 for some entity pair
$(e_1, e_2)$, $F_n$ is non-trivial. This rules out the identity
filter (no death) and the uniform scaling filter (death rate
independent of entity).

**Action is on level-$(n-1)$ entities, not on the underlying
substrate.** This is the crucial check that distinguishes level
$n$ from level $n - 1$. Formally: $V_n$ and $F_n$ must operate on
the descriptor space $Y_{n-1}$ of the level-$(n-1)$ scale
projection $\pi_{n-1}$, not on the substrate state directly. For
implementation, this is a typing check on the operators'
signatures — $V_n$ accepts level-$(n-1)$ entities as input, not
substrate states.

If all three tests pass, return $(V_n, F_n)$. Otherwise return
`None` and the recursion halts.

The framework's existing `Variation` and `ViabilityFilter`
Protocols give the typing structure for this check. The hierarchy
of `V_n, F_n` is the framework-side specialisation of the
hierarchical-viability formalism `F*` of `viability.py`.

### 1.4 `has_discriminative_capacity`

The most expensive helper. Formal definition per
[`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) §2.3: $(V_n, F_n)$ has
discriminative capacity at level $n$ iff, for any candidate entity
$e^* \in E_{n-1}$ that is *strictly fitter* than the current
population under $F_n$ — meaning
$F_n(\delta_{e^*})(\{e^*\}) / F_n(\delta_e)(\{e\}) > 1$ for all
$e$ in the current population — the iteration $V_n \circ F_n$
applied to the population augmented by $\epsilon \delta_{e^*}$
gives $e^*$ a strictly increasing share of the population mass
over time, for all small enough $\epsilon > 0$.

Two implementations.

**Counterfactual perturbation (sharp).** Construct a candidate
$e^*$ verifiably satisfying the strict-fitness inequality (e.g.,
by hand-engineering an entity with retention rate $\geq 1 + \delta$
times the current population's per-entity rate). Inject $e^*$ into
the population at small fraction $\epsilon$. Run the iteration for
a window of length $w$. Check that $e^*$'s population share grows
monotonically. Cost: $2\times$ baseline simulation per perturbation,
times multiple perturbations to control noise. Most reliable.

**Fluctuation-spectrum proxy (cheap).** Compute the power spectrum
of $F_n$-retention rates over a long trajectory window. A system
with discriminative capacity shows characteristic
fluctuation-dissipation behaviour — variance and autocorrelation
regress to a mean (the system is responsive). A system without it
shows persistent drift or random-walk variance (the system is
unresponsive). Borrowed from non-equilibrium statistical mechanics.
Cost: one simulation; no counterfactuals needed.

The cheap test approximates the sharp test under a regularity
assumption: when the system's response to natural fluctuations is
well-behaved (mean-reverting), the response to engineered
perturbations is also well-behaved. The cheap test misses cases
where the natural fluctuations don't probe the discriminative
direction; the sharp test catches all cases by construction.

Combine the two: use the fluctuation-spectrum proxy by default;
run the counterfactual test on borderline cases (systems near the
discriminative-capacity threshold by the cheap test).

### 1.5 `detect_persistent_patterns`

Same as 1.2 but operating on level-$(n-1)$ entities under the
$(V_n, F_n)$-induced dynamic instead of substrate states under
$\Phi$. The E1/E2/E3 validation is identical; only the input
domain changes.

---

## Stage 2 — Measure $\boldsymbol{\sigma}$ at each level

The $\sigma_i$ flag measures whether $F_i$'s behaviour depends on
the system's dynamical state beyond the current population at
level $i$. The natural operational definition is **conditional
transfer entropy**:

$$
\sigma_i \;:=\; \frac{T(\,\mathrm{state}_i^{\,t}\;\to\;F_i^{\,t+1}\;\mid\;\mathrm{population}_i^{\,t}\,)}{T_{\max}}
$$

where $T(X \to Y \mid Z)$ is the conditional transfer entropy
from $X$ to $Y$ given $Z$, and $T_{\max}$ is its theoretical
maximum (the entropy of $Y$ minus the entropy of $Y$ given $Z$
alone). $\sigma_i \in [0, 1]$.

### 2.1 `compute_sigma_at_level`

```text
INPUT:  level_i : int
        F_i : ViabilityFilter
        trajectory : Trajectory
        entities_at_level : sequence of Entity

OUTPUT: sigma_i : float in [0, 1]

F_outputs := compute_F_i_outputs_over_trajectory(F_i, trajectory)
population_state := compute_population_at_level(trajectory, level_i,
                                                entities_at_level)
non_population_state := compute_complement_state(trajectory, level_i,
                                                 population_state)

T_conditional := conditional_transfer_entropy(
    source=non_population_state,
    target=F_outputs,
    condition=population_state,
    history_length=window_length
)

T_max := max_possible_transfer_entropy(F_outputs, non_population_state,
                                       population_state)

return T_conditional / T_max if T_max > 0 else 0.0
```

### 2.2 Existing implementations of transfer entropy

Reuse rather than reimplement. Each gives the same result to
within estimator noise:

- **IDTxl** (Information Dynamics Toolkit, Wollstadt et al.). Most
  mature; supports conditional transfer entropy and PID directly.
- **JIDT** (Java Information Dynamics Toolkit, Lizier). Has Python
  bindings; supports the same primitives.
- **pyinform**. Lightweight; sufficient for small systems.

The `vitality.py` module should wrap one of these (probably IDTxl)
rather than rolling its own. Pin the choice in `pyproject.toml`.

### 2.3 The counterfactual alternative

A sharper but more expensive measurement: hold the current
population at level $i$ fixed, perturb the rest of the system's
state at level $i$ by a measurable amount, and observe the change
in $F_i$'s output distribution.

```text
INPUT:  same as compute_sigma_at_level

OUTPUT: sigma_i : float in [0, 1]

baseline_F := apply_F_i_to_trajectory(F_i, trajectory)
perturbations := generate_state_perturbations(trajectory, level_i,
                                              exclude=population)
F_responses := [apply_F_i_to_perturbed(F_i, trajectory, p)
                for p in perturbations]
divergence := KL_divergence(F_responses, baseline_F)
max_divergence := max_KL_under_full_dependence(F_i, level_i)
return divergence / max_divergence if max_divergence > 0 else 0.0
```

The counterfactual version directly measures dependence and
matches the working definition in FRAMING_AUDIT.md §2.3. The
transfer-entropy version is cheaper but indirect. The two agree to
within estimator noise on standard cases.

---

## Putting it together

```text
def compute_vitality_profile(system, trajectory,
                              max_levels=10, epsilon=0.05):
    # Stage 1
    k = detect_level_k(system, trajectory, max_levels, epsilon)

    # Stage 2
    sigma = []
    current_entities = detect_level_0_entities(system, trajectory, epsilon)
    for i in range(1, k + 1):
        V_i, F_i = infer_search_operators_at_level(
            system, current_entities, trajectory, level=i
        )
        sigma_i = compute_sigma_at_level(i, F_i, trajectory, current_entities)
        sigma.append(sigma_i)
        current_entities = detect_persistent_patterns(
            V_i, F_i, current_entities, epsilon
        )

    return VitalityProfile(k=k, sigma=tuple(sigma))
```

The output is a `VitalityProfile` dataclass:

```python
@dataclass(frozen=True)
class VitalityProfile:
    k: int                    # search-hierarchy depth
    sigma: tuple[float, ...]  # one entry per level 1..k

    def is_alive(self) -> bool:
        """LifeCat membership: k >= 1."""
        return self.k >= 1

    def is_autopoietic_at(self, level: int) -> bool:
        """σ_level approximately 1."""
        return level <= self.k and self.sigma[level - 1] > 0.9
```

For composite systems built via $\boxtimes_\kappa$, the entry
point is `compute_composite_vitality_profile` which dispatches to
Stage 3:

```python
def compute_composite_vitality_profile(
    components: list[System],
    couplings: dict[tuple[int, int], Coupling],
    trajectory: WindowedTrajectory,
    *,
    max_levels: int = 10,
    epsilon: float = 0.05,
) -> VitalityProfile:
    """Compute (k, σ) for S_1 ⊠_κ ... ⊠_κ S_m per §3 of this doc."""
    ...
```

If the coupling structure is not given a priori, an inference
helper `infer_coupling_structure(components, trajectory)` returns
the dict of detected couplings, which can then be passed to
`compute_composite_vitality_profile`.

---

## Stage 3 — Composite systems via $\boxtimes_\kappa$

A horizontally-composed system $\mathcal{S} = \mathcal{S}_1 \boxtimes_\kappa \mathcal{S}_2$
has a vitality profile determined jointly by its component
profiles and the coupling structure $\kappa$. The recursive-level
algorithm in Stage 1 and the $\sigma$-measurement algorithm in
Stage 2 both extend to this case, with one additional measurement:
the **cross-coupling transfer entropy** that quantifies how much
$F_i$ on one side depends on the other side's state.

The composite profile is computed as follows.

```text
INPUT:  components : list of System  # [S_1, S_2, ..., S_m]
        couplings : dict of (i,j) -> Coupling  # the κ structure
        trajectory : Trajectory      # joint trajectory of S_1 ⊠_κ ... ⊠_κ S_m

OUTPUT: composite_profile : VitalityProfile

# Stage 3.1: per-component profiles
component_profiles := [compute_vitality_profile(S_n, project(trajectory, n))
                        for S_n in components]

# Stage 3.2: composite level
k_composite := max(p.k for p in component_profiles)
# Horizontal composition preserves level; the composite reaches the
# deepest level reached by any component.

# Stage 3.3: composite σ at each shared level
sigma_composite := []
for i in 1 .. k_composite:
    component_sigmas := [p.sigma[i-1] for p in component_profiles
                         if p.k >= i]

    # Coupling-induced uplift at level i
    sigma_uplift_i := compute_coupling_uplift(
        components, couplings, trajectory, level=i
    )

    sigma_composite_i := combine_sigmas(component_sigmas, sigma_uplift_i)
    sigma_composite.append(sigma_composite_i)

return VitalityProfile(k=k_composite, sigma=tuple(sigma_composite))
```

The key new helper is `compute_coupling_uplift`.

### 3.1 `compute_coupling_uplift`

For each coupling $\kappa_{(i,j)}$ between components $i$ and $j$
at a shared level $\ell$, compute the transfer entropy from
$\mathcal{S}_j$'s state to $\mathcal{S}_i$'s $F_\ell$ output,
conditional on $\mathcal{S}_i$'s own population:

$$
\Delta_{ij}^{(\ell)} \;:=\; \frac{T(\,\text{state}_j^{\,t} \;\to\; F_i^{\,(\ell),\,t+1} \;\mid\; \text{population}_i^{(\ell),\,t}\,)}{T_{\max}}
$$

This is the cross-coupling analog of the within-system $\sigma_\ell$
measurement of Stage 2. It captures *how much $\mathcal{S}_i$'s
viability at level $\ell$ depends on $\mathcal{S}_j$'s state beyond
$\mathcal{S}_i$'s own population* — the operational definition of
"the coupling manufactures self-reference."

```text
INPUT:  components, couplings, trajectory, level : int

OUTPUT: uplift : float in [0, 1]

uplift_terms := []
for (i, j) in couplings:
    if components[i].profile.k < level: continue
    if components[j].profile.k < level: continue

    F_i_outputs := compute_F_outputs_at_level(components[i], trajectory, level)
    population_i := compute_population_at_level(trajectory, i, level)
    state_j := compute_state_at_level(trajectory, j, level)

    T_cross := conditional_transfer_entropy(
        source=state_j,
        target=F_i_outputs,
        condition=population_i
    )
    T_max := max_possible_transfer_entropy(F_i_outputs, state_j, population_i)
    uplift_terms.append(T_cross / T_max if T_max > 0 else 0)

return aggregate(uplift_terms)
```

The aggregation choice depends on coupling structure: for mutual
coupling, max or geometric mean is appropriate; for one-way
coupling, only the relevant direction contributes.

### 3.2 `combine_sigmas`

Given the component $\sigma$ values at a level and the
coupling-induced uplift, produce the composite $\sigma$. The
natural combination respects the framework's structural commitments:

```text
INPUT:  component_sigmas : list of float
        sigma_uplift : float

OUTPUT: sigma_composite : float in [0, 1]

# The composite σ saturates at 1; horizontal composition can only
# raise σ, not lower it (a self-referential component remains
# self-referential under coupling).
baseline := max(component_sigmas) if component_sigmas else 0
return min(1.0, baseline + sigma_uplift)
```

The formula encodes the three cases from FRAMING_AUDIT.md §2.3:

- *Trivial $\kappa$*: $\text{uplift} = 0$, so composite $\sigma$ equals max of components.
- *One-way coupling*: $\text{uplift}$ is non-zero in one direction only; one component's effective $\sigma$ rises.
- *Mutual coupling*: $\text{uplift}$ is non-zero in both directions; the composite $\sigma$ exceeds either component's. **The self-reference manufactured by the coupling appears here as a positive uplift term.**

### 3.3 Detecting the coupling structure $\kappa$

For a given trajectory, the coupling structure may not be given a
priori — it has to be inferred. The detection algorithm:

```text
INPUT:  components : list of System
        trajectory : Trajectory

OUTPUT: couplings : dict of (i,j) -> Coupling

couplings := {}
for i, j in pairs(components):
    if i == j: continue
    coupling := infer_coupling_from_trajectory(
        components[i], components[j], trajectory
    )
    if coupling.is_non_trivial():
        couplings[(i, j)] = coupling
return couplings
```

The inner helper `infer_coupling_from_trajectory` is essentially
transfer-entropy at the substrate level: measure how much
$\mathcal{S}_j$'s substrate state predicts $\mathcal{S}_i$'s
substrate-update behaviour. If the transfer entropy is above a
threshold, a coupling exists. The framework's existing $\kappa$
data type from the paper (paper §3.3 line 401) provides the typing
for the coupling.

### 3.4 Worked composite computations

| Composite                          | Components                        | Coupling           | Expected composite profile  | Key uplift             |
|------------------------------------|-----------------------------------|--------------------|-----------------------------|------------------------|
| Lichen                             | Alga $(1,(1))$ + fungus $(1,(1))$ | Mutualistic        | $(1,(1))$                   | Uplift saturates at 1  |
| Tierra host-parasite               | Host $(2,(1,0))$ + parasite $(2,(1,0))$ | Mutual exploit | $(2,(1,1))$                 | $\sigma_2$ uplift $= 1^*$ |
| Predator-prey populations          | Predator $(2,(1,0))$ + prey $(2,(1,0))$ | Trophic     | $(2,(1,1))$                 | $\sigma_2$ uplift $= 1^*$ |
| Hybrid LLM-Lenia                   | Lenia $(1,(0))$ + LLM $(1,(1))$   | Observer-feedback  | $(1,(1))$                   | $\sigma_1$ uplift on Lenia side |
| Independent two-organism culture   | Bacterium A $(1,(1))$ + bacterium B $(1,(1))$, no mixing | None | $(1,(1))$ ; trivial composite | Uplift $= 0$ |

The asterisked uplifts are the cases where horizontal composition
*manufactures* self-reference. These are the operationally
interesting cases for ALife — the framework now identifies them
mechanically rather than via informal "coevolution feels open-ended"
judgments.

### 3.5 Composition under $\diamond_\rho$

The variation-channel composition operator $\diamond_\rho$ (paper
§3.4) is a refinement of horizontal composition for the case where
two systems' *variation channels* are coupled (gene-culture
coevolution, niche construction, stigmergic coupling). The
algorithm above subsumes $\diamond_\rho$ as a special case: when
the coupling $\kappa$ acts specifically on the $V$ kernels of the
components, the cross-coupling transfer entropy at the variation
level captures the $\diamond_\rho$ structure. No separate
algorithmic stage is needed.

---

## Stage 4 — Comparing vitality profiles across systems

Two systems with different state spaces and different probability
measures need careful handling when compared. The framework's
three-way comparison machinery (per
[`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) §2.3 "Comparing vitality
profiles across systems with different measures") is implemented
in three corresponding functions.

### 4.1 `are_structurally_equivalent`

The cheapest comparison. Two systems are structurally equivalent
in $\mathbf{LifeCat}$ iff their vitality profiles agree.

```text
INPUT:  profile_1 : VitalityProfile
        profile_2 : VitalityProfile
        sigma_tol : float = 0.05  # estimator tolerance

OUTPUT: equivalent : bool

if profile_1.k != profile_2.k:
    return False
for sigma_a, sigma_b in zip(profile_1.sigma, profile_2.sigma):
    if abs(sigma_a - sigma_b) > sigma_tol:
        return False
return True
```

Estimator tolerance accounts for the fact that $\sigma$ values are
floating-point estimates with finite-trajectory noise. The default
of 0.05 corresponds to typical transfer-entropy estimator
precision on $\geq 10^4$ samples.

### 4.2 `partial_order_compare`

The partial order $(k_1, \boldsymbol{\sigma}_1) \preceq (k_2, \boldsymbol{\sigma}_2)$:
profile 2 dominates profile 1 iff $k_2 \geq k_1$ and componentwise
$\sigma_{2,i} \geq \sigma_{1,i}$ for all $i \leq k_1$.

```text
INPUT:  profile_1, profile_2 : VitalityProfile
        sigma_tol : float = 0.05

OUTPUT: ordering : Ordering   # LT, EQ, GT, or INCOMPARABLE

# Check equality first
if are_structurally_equivalent(profile_1, profile_2, sigma_tol):
    return Ordering.EQ

# Check if profile_2 dominates profile_1
p2_dominates = (
    profile_2.k >= profile_1.k
    and all(profile_2.sigma[i] >= profile_1.sigma[i] - sigma_tol
            for i in range(profile_1.k))
)

# Check the reverse
p1_dominates = (
    profile_1.k >= profile_2.k
    and all(profile_1.sigma[i] >= profile_2.sigma[i] - sigma_tol
            for i in range(profile_2.k))
)

if p2_dominates and not p1_dominates:
    return Ordering.LT  # profile_1 < profile_2
if p1_dominates and not p2_dominates:
    return Ordering.GT  # profile_1 > profile_2
if p1_dominates and p2_dominates:
    return Ordering.EQ  # already caught above; defensive
return Ordering.INCOMPARABLE
```

Most pairs of real-world systems return `INCOMPARABLE`. This is
honest: a strong-autopoiesis-but-shallow system $(1, (1.0))$ is
not orderable against a deep-but-low-self-reference system
$(3, (0.5, 0.5, 0.5))$ under the framework's partial order, and
the function reports that rather than fabricating an ordering.

### 4.3 `observer_mediated_compare`

Quantitative comparison requires a common observer.

```text
INPUT:  system_1 : System
        system_2 : System
        observer : Observer    # must be valid for both systems
        trajectory_1, trajectory_2 : WindowedTrajectory
        comparison_metric : Callable[[Distribution, Distribution], float]
                            # KL, Wasserstein, MMD, etc.

OUTPUT: comparison_result : ComparisonResult
        # contains: divergence value, direction, observer name,
        #           metric name, confidence interval

scores_1 := observer(system_1, trajectory_1)
scores_2 := observer(system_2, trajectory_2)

divergence := comparison_metric(scores_1, scores_2)
direction := infer_direction(scores_1, scores_2)
ci := bootstrap_confidence_interval(scores_1, scores_2, comparison_metric)

return ComparisonResult(
    divergence=divergence,
    direction=direction,
    observer_name=observer.name,
    metric_name=comparison_metric.__name__,
    confidence_interval=ci,
)
```

The returned `ComparisonResult` always carries the observer name
and metric name. This is the framework's reporting-discipline
commitment: a quantitative comparison is meaningful only relative
to a specified observer and metric.

### 4.4 `compare_systems` — the recommended composite call

```text
INPUT:  system_1, system_2 : System
        trajectory_1, trajectory_2 : WindowedTrajectory
        observer : Observer = None   # optional
        comparison_metric : Callable = None  # optional

OUTPUT: full_comparison : SystemComparison
        # contains:
        #   - profile_1, profile_2
        #   - structurally_equivalent : bool
        #   - partial_order : Ordering (LT, EQ, GT, INCOMPARABLE)
        #   - observer_mediated : ComparisonResult | None

profile_1 := compute_vitality_profile(system_1, trajectory_1)
profile_2 := compute_vitality_profile(system_2, trajectory_2)

equivalent := are_structurally_equivalent(profile_1, profile_2)
ordering := partial_order_compare(profile_1, profile_2)

observer_result := None
if observer is not None and comparison_metric is not None:
    observer_result := observer_mediated_compare(
        system_1, system_2, observer,
        trajectory_1, trajectory_2,
        comparison_metric,
    )

return SystemComparison(
    profile_1=profile_1,
    profile_2=profile_2,
    structurally_equivalent=equivalent,
    partial_order=ordering,
    observer_mediated=observer_result,
)
```

This is the recommended entry point for paper-level comparisons —
it always reports the structural profile and partial-order verdict,
and adds the quantitative comparison only when an observer is
specified. Users get the honest answer (structural equivalence and
partial-order incomparability are real verdicts to publish) by
default, and the observer-mediated quantitative comparison only on
explicit request.

---

## Stage 5 — Detecting level transitions (LE)

A level transition is a *dynamical event*: a system's measured
vitality profile depth $k$ increases from $k$ to $k + 1$ over time.
Detecting such events in trajectory data corresponds to testing
LE's four conditions on the level-$k$ entities over a sliding
window. Per [`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) §2.6, the
four conditions are: persistence, aggregation, group variation,
group selection.

### 5.1 `detect_level_transition`

```text
INPUT:  system : System
        trajectory : Trajectory          # long enough to see transitions
        current_level_k : int            # current depth, from Stage 1
        window : (start, end)            # time window to check
        thresholds : LEThresholds        # per-condition cut-offs

OUTPUT: transition_event : LETransitionEvent | None
        # event includes: timestamp, conditions satisfied,
        # resulting new level, confidence

# Get level-k entities at start and end of window
entities_start := detect_entities_at_level(system, trajectory[start], current_level_k)
entities_end := detect_entities_at_level(system, trajectory[end], current_level_k)

# Condition 1: Persistence
persistence_score := measure_entity_lifetime(
    entities_start, entities_end, trajectory[start:end]
) / substrate_relaxation_time(system)
if persistence_score < thresholds.persistence:
    return None

# Condition 2: Aggregation
coupling_kappa := detect_coupling_among_entities(
    entities_start, trajectory[start:end], level=current_level_k
)
aggregation_score := measure_aggregate_persistence(coupling_kappa, trajectory[start:end])
if aggregation_score < thresholds.aggregation:
    return None

# Condition 3: Group variation
aggregate_types := classify_aggregate_types(coupling_kappa, trajectory[start:end])
group_variation_score := shannon_entropy(aggregate_types)
if group_variation_score < thresholds.group_variation:
    return None

# Condition 4: Group selection
persistence_by_type := compute_persistence_by_aggregate_type(
    aggregate_types, trajectory[start:end]
)
group_selection_score := variance(persistence_by_type) / mean(persistence_by_type)
if group_selection_score < thresholds.group_selection:
    return None

# All four conditions met
return LETransitionEvent(
    timestamp_window=(start, end),
    new_level=current_level_k + 1,
    persistence=persistence_score,
    aggregation=aggregation_score,
    group_variation=group_variation_score,
    group_selection=group_selection_score,
)
```

### 5.2 The four condition measurements

Each condition has a natural quantitative measurement:

- **Persistence**: mean lifetime of level-$k$ entities divided
  by substrate relaxation time. Above 1 means entities outlast
  the substrate's natural dynamics.
- **Aggregation**: persistence of multi-entity patterns under
  the detected coupling $\kappa^{(k)}$, normalised to the
  single-entity persistence.
- **Group variation**: Shannon entropy of the distribution over
  aggregate types observed in the window. Higher means more
  diverse aggregates exist.
- **Group selection**: coefficient of variation (variance over
  mean) of persistence rates across aggregate types. Higher
  means more differential persistence.

Each of these is operationalisable from trajectory data using
standard estimators. The framework's existing helpers from
`entity.py`, `population.py`, and the new transfer-entropy
machinery cover the components needed.

### 5.3 `scan_trajectory_for_transitions`

For a long trajectory, find all level-transition events by sliding
the window across.

```text
INPUT:  system : System
        trajectory : Trajectory
        window_size : int
        stride : int

OUTPUT: events : list of LETransitionEvent

events := []
current_level_k := compute_vitality_profile(system, trajectory[0:window_size]).k

for start in range(0, len(trajectory) - window_size, stride):
    window := (start, start + window_size)
    event := detect_level_transition(system, trajectory, current_level_k, window)
    if event is not None:
        events.append(event)
        current_level_k = event.new_level

return events
```

The function returns a chronological list of detected level
transitions, each tagged with the four sub-condition scores. This
is the empirical realisation of LE — a list of structural events
the system underwent during the trajectory.

### 5.4 Validation cases

The implementation should produce these results on canonical fixtures:

| Fixture                                | Expected transitions detected                                     |
|----------------------------------------|-------------------------------------------------------------------|
| Tierra full run (seed → arms race)     | 1 transition at the time the parasite lineage emerges (level 1 → 2) |
| Pure GoL                               | 0 transitions (no V on entities)                                  |
| Hurricane simulation                   | 0 transitions                                                     |
| Origin-of-life chemistry surrogate     | 1 transition at the time stable proto-cells form (level 0 → 1)   |
| Multicellularity simulation            | 1 transition at the time cell-cell adhesion produces persistent colonies (level 1 → 2) |
| Linguistic-evolution simulation        | 1 transition at the time written texts persist independently (level 2 → 3) |
| Standard converged GA                  | 0 transitions (level-1 entities never aggregate)                  |

These fixtures collectively validate LE's necessity direction
(transitions detected coincide with the historical events biology
recognises) and its sufficiency direction (in fixtures where the
four conditions are met, transitions are detected).

### 5.5 Skeleton additions to `vitality.py`

```python
@dataclass(frozen=True)
class LETransitionEvent:
    timestamp_window: tuple[int, int]
    new_level: int
    persistence: float
    aggregation: float
    group_variation: float
    group_selection: float

@dataclass(frozen=True)
class LEThresholds:
    persistence: float = 1.0
    aggregation: float = 0.5
    group_variation: float = 0.5
    group_selection: float = 0.1

def detect_level_transition(
    system: System,
    trajectory: WindowedTrajectory,
    current_level_k: int,
    window: tuple[int, int],
    *,
    thresholds: LEThresholds = LEThresholds(),
) -> LETransitionEvent | None: ...

def scan_trajectory_for_transitions(
    system: System,
    trajectory: WindowedTrajectory,
    *,
    window_size: int = 1000,
    stride: int = 100,
    thresholds: LEThresholds = LEThresholds(),
) -> list[LETransitionEvent]: ...
```

---

### 4.5 Comparison-machinery skeleton for `vitality.py`

```python
# Continuing src/emergent_systems/vitality.py

from enum import Enum
from dataclasses import dataclass
from typing import Callable

class Ordering(Enum):
    LT = "less_than"
    EQ = "equal"
    GT = "greater_than"
    INCOMPARABLE = "incomparable"

@dataclass(frozen=True)
class ComparisonResult:
    divergence: float
    direction: Ordering
    observer_name: str
    metric_name: str
    confidence_interval: tuple[float, float]

@dataclass(frozen=True)
class SystemComparison:
    profile_1: VitalityProfile
    profile_2: VitalityProfile
    structurally_equivalent: bool
    partial_order: Ordering
    observer_mediated: ComparisonResult | None

def are_structurally_equivalent(
    profile_1: VitalityProfile,
    profile_2: VitalityProfile,
    *,
    sigma_tol: float = 0.05,
) -> bool: ...

def partial_order_compare(
    profile_1: VitalityProfile,
    profile_2: VitalityProfile,
    *,
    sigma_tol: float = 0.05,
) -> Ordering: ...

def observer_mediated_compare(
    system_1: System,
    system_2: System,
    observer: Observer,
    trajectory_1: WindowedTrajectory,
    trajectory_2: WindowedTrajectory,
    comparison_metric: Callable[..., float],
) -> ComparisonResult: ...

def compare_systems(
    system_1: System,
    system_2: System,
    trajectory_1: WindowedTrajectory,
    trajectory_2: WindowedTrajectory,
    *,
    observer: Observer | None = None,
    comparison_metric: Callable | None = None,
) -> SystemComparison: ...
```

---

## Validation against the stress-tested cases

The implementation must produce these profiles on the canonical
test cases. The cases serve as regression tests for the
`vitality.py` module.

| System                                | Expected profile           | Test fixture                                            |
|---------------------------------------|----------------------------|---------------------------------------------------------|
| Hurricane / atmospheric simulation    | $(0, ())$                  | Toy 2D pressure-gradient simulation                     |
| Plain Game of Life glider             | $(0, ())$                  | `examples/gol/` with $V = \mathrm{id}$, $F = \mathrm{id}$ |
| Chaotic logistic map                  | $(0, ())$                  | $x_{t+1} = r x_t (1 - x_t)$, $r = 3.9$                  |
| Standard converged GA                 | $(1, (0,))$                | OneMax or sphere function, run past convergence         |
| Frequency-dependent GA                | $(1, (1,))$                | Hawk-Dove dynamics                                      |
| Active Tierra arms race               | $(2, (1, 1))$              | `examples/tierra_stub/` (to be implemented)             |
| Stabilised Tierra                     | $(2, (1, 0))$              | Same fixture, run past arms-race phase                  |
| HeLa cell line (synthetic surrogate)  | $(2, (1, \approx 0.4))$    | Cellular-automaton + lab-perturbation overlay           |
| Lenia with parameter variation        | $(1, (1,))$ or $(2, (1, 1))$ | `examples/lenia/` with QD search loop                 |
| Cultural-evolution simulation         | $(3, (1, 1, 1))$           | Boyd-and-Richerson-style memetic transmission model     |

Composite (horizontally-composed) test cases:

| Composite system                      | Expected profile           | Test fixture                                            |
|---------------------------------------|----------------------------|---------------------------------------------------------|
| Lichen surrogate                      | $(1, (1,))$                | Two coupled chemical-reaction-network cells with mutual metabolite exchange |
| Tierra host-parasite ecology          | $(2, (1, 1,))$             | `examples/tierra_stub/` with parasite lineage           |
| Predator-prey Lotka-Volterra + agent  | $(2, (1, 1,))$             | Coupled population simulator with each species an agent  |
| Independent two-population GA         | $(1, (1,))$                | Two GAs with no information sharing                     |
| Hybrid LLM-Lenia worked example       | $(1, (1,))$ or $(2, (1, 1)) $ | `examples/coupled_lenia_stub/` from paper §3.8       |
| Bilingual community simulator         | $(3, (1, 1, 1))$           | Two coupled memetic-transmission models with code-switching |
| Microbiome-host surrogate             | $(\geq 3, (1, 1, 1, \ldots))$ | Multi-level coupled simulation                       |

The composite fixtures are mostly to be built; the
`coupled_lenia_stub` fixture in the existing scaffold is the
nearest extant analog and can serve as the integration-test seed.

The fixtures in `examples/` are mostly stubs as of v1 of the
scaffold; building them out is the third milestone listed in
[`FRAMING_AUDIT.md`](FRAMING_AUDIT.md) closing recommendation.

---

## Known bottlenecks and approximations

The algorithm is asymptotically correct but has three operational
bottlenecks.

**Entity detection at high levels.** Detecting level-$n$ entities
requires applying E1's information-closure condition to a
descriptor space that gets coarser at each level. For $n \geq 3$,
the descriptor space is small enough that direct mutual-information
estimation works; for $n = 1$ on a large substrate (Flow-Lenia,
foundation-model agent populations), the search over candidate
supporting sets is expensive. Approximation: use substrate-specific
detectors (connected-component, DBSCAN, syntactic boundaries) and
validate E1 post-hoc.

**Discriminative-capacity testing.** Counterfactual perturbation
is the gold standard but doubles simulation cost. For systems
where running one trajectory is already expensive (large Lenia
fields, multi-agent LLM systems), the fluctuation-spectrum proxy
should be used by default and counterfactuals reserved for
borderline cases.

**Transfer-entropy estimation at high levels.** Conditional
transfer entropy with high-dimensional conditioning requires long
time series for reliable estimation. For $k \geq 3$, expect the
window length to scale as $O(\dim(Y_i)^2)$ at each level. Use
kernel-based estimators (Kraskov-Stögbauer-Grassberger) for
high-dimensional case; binning-based estimators for low-dimensional.

For all three, the framework's design is to **bound** these
approximations with explicit uncertainty rather than to claim
exactness. The `VitalityProfile` dataclass should optionally carry
confidence intervals on $\boldsymbol{\sigma}$ derived from the
estimator's variance.

---

## What this enables for the framework

Once `vitality.py` is implemented and validated, three things
become possible.

The framework's central predictions become **reproducible
measurements**. The claim "active Tierra and wild bacteria are at
the same vitality profile" stops being rhetorical and becomes a
specific numerical equality to be checked.

The S1 sufficiency conjecture becomes **immediately testable on
the example systems**. Run the four-tuple system, compute its
profile, verify $k \geq 1$. If yes, sufficiency holds for that
case. The first concrete result of the framework (`L1`, the
renamed `OP1`) is a positive vitality-profile measurement on a
Game-of-Life-under-Markov-blanket-viability fixture.

The framework's **comparison vocabulary** becomes operational.
Two systems can now be compared by their vitality profiles rather
than by informal slot-by-slot description. This is what the paper's
existing "system description schema" of §3.7 promises but does not
yet deliver — the schema becomes well-typed once the vitality
profile is what the description ultimately specifies.

---

## Recommended next step

The natural next step is to implement `vitality.py` as a new
module in [`src/emergent_systems/`](../src/emergent_systems/) and
add corresponding tests under
[`tests/`](../tests/). The skeleton would be:

```python
# src/emergent_systems/vitality.py
"""
Vitality-profile computation for substrate-agnostic emergent systems.

Implements the (k, σ) measurement of FRAMING_AUDIT.md §2.3 and
the algorithm of vitality_computation.md. Composes existing
primitives from emergence.py, entity.py, viability.py, observer.py
plus one new helper (conditional transfer entropy via IDTxl).

Provides both single-system and composite-system entry points,
where the composite case handles horizontal composition via
the framework's existing boxtimes_kappa operator.
"""
from dataclasses import dataclass
from .system import System
from .observer import WindowedTrajectory
from .substrate import Coupling  # paper: κ

@dataclass(frozen=True)
class VitalityProfile:
    k: int
    sigma: tuple[float, ...]
    # ...

def compute_vitality_profile(
    system: System,
    trajectory: WindowedTrajectory,
    *,
    max_levels: int = 10,
    epsilon: float = 0.05,
) -> VitalityProfile:
    """Compute (k, σ) per docs/vitality_computation.md §1–2."""
    ...

def compute_composite_vitality_profile(
    components: list[System],
    couplings: dict[tuple[int, int], Coupling],
    trajectory: WindowedTrajectory,
    *,
    max_levels: int = 10,
    epsilon: float = 0.05,
) -> VitalityProfile:
    """Compute (k, σ) for S_1 ⊠_κ ... ⊠_κ S_m per docs/vitality_computation.md §3."""
    ...

def infer_coupling_structure(
    components: list[System],
    trajectory: WindowedTrajectory,
    *,
    threshold: float = 0.05,
) -> dict[tuple[int, int], Coupling]:
    """Detect the κ structure from a joint trajectory; see §3.3."""
    ...
```

A first-pass implementation of the substrate-specific detectors,
plus the IDTxl integration for transfer entropy, plus the test
fixtures for the canonical cases above, is roughly a
several-day-to-one-week project. Once it lands, the framework has
a self-validating predicate and the central thesis becomes
empirically operational.
