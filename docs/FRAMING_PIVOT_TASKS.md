# Framing-pivot task tracker

This document is the checklist-style task tracker for the framing
pivot decided 2026-05-11. The pivot's full design rationale lives
in [`FRAMING_AUDIT.md`](FRAMING_AUDIT.md); this document is the
*work plan* derived from the audit.

**Strategy.** The pivot's downstream content will be developed as a
**series of focused result papers** under
[`docs/papers/`](papers/), not as a textbook compilation. The
scaffolding paper at
[`docs/emergent_systems.tex`](emergent_systems.tex) is rewritten
once against the new framing; subsequent work (proofs, worked
examples, applications) goes into individual result papers using
the existing [`docs/papers/_template/`](papers/_template/) structure.

**Scope of this document.** Action items only. **No proofs.** All
unproven statements are tracked in Part 4 as UNPROVEN with explicit
notes; this document does **not** attempt to prove any of them.

---

## Part 1 — Scaffolding-paper rewrite (`docs/emergent_systems.tex`)

The single most load-bearing edit pass. Each task targets one
section or theme of the paper.

- [x] **P-1. Abstract & introduction.** *Completed 2026-05-11.*
  Replaced methodology / comparative framing with the predictive-
  thesis framing. S1, N1, CAT1, LE introduced upfront as the
  framework's central conjectures.
- [x] **P-2. System definition (§3.1).** *Completed 2026-05-11.*
  4-tuple $\mathcal{S} = (\mathbf{X}, V, F, T)$ with the observer
  moved out as an external functor.
- [x] **P-3. The independent observer.** *Completed 2026-05-11.*
  Promoted to its own subsection (`\subsection{The independent
  observer functor}\label{sec:observer}`) introducing $O:
  \mathbf{Sys} \to \mathbf{Obs}$. Legacy observer-as-slot
  subsection removed.
- [x] **P-4. The ambient category.** *Completed 2026-05-11.* New
  `\subsection{The ambient category}\label{sec:ambient}` stating
  $\mathbf{Sys}$ is the SMC of $\mathcal{O}_W$-algebras in
  $\mathbf{Stoch}$, with the C-via-lift interpretive layer.
- [x] **P-5. Recursive level definition.** *Completed 2026-05-11.*
  New `\subsection{Recursive level structure}\label{sec:recursive-levels}`
  with base case + induction and the operadic-native
  correspondence.
- [x] **P-6. Formal non-triviality definitions.** *Completed
  2026-05-11.* New `\subsection{Non-triviality}\label{sec:nontriviality}`
  with `def:vnontriv`, `def:fnontriv`, `def:disc-cap`.
- [x] **P-7. Vitality profile and $\mathbf{LifeCat}$ membership.**
  *Completed 2026-05-11.* New `\subsection{Vitality profile and
  $\mathbf{LifeCat}$ membership}\label{sec:vitality}` with
  `def:vitality`, `def:lifecat`, and the worked-profiles table.
- [x] **P-8. Horizontal composition.** *Completed 2026-05-11.* New
  `\subsection{Horizontal composition}\label{sec:horizontal}` with
  the three coupling cases and $\sigma$-uplift discussion, plus
  examples across substrates.
- [x] **P-9. Observer-dependence of decomposition.** *Completed
  2026-05-11.* Subsection inline with the recursive level
  structure (\S\ref{sec:recursive-levels}) — the "Where modeler
  choice still enters" paragraph at the end notes that horizontal
  composition and entity detection both depend on $\pi$.
- [x] **P-10. Cross-system comparison.** *Completed 2026-05-11.*
  New `\subsection{Cross-system comparison}\label{sec:comparison}`
  with the three comparison operations and reporting discipline.
- [x] **P-11. Level Emergence (LE).** *Completed 2026-05-11.* New
  `\subsection{Level emergence}\label{sec:le}` with four
  conditions and the chemistry → cells → organisms → ecosystems
  walkthrough. The LE conjecture is restated in the conjectures
  section.
- [x] **P-12. Worked composite example.** *Completed 2026-05-11.*
  Flow-Lenia + LLM example rewritten with 4-tuple and external
  observer; vitality profile reported as a target outcome.
- [x] **P-13. System Description schema.** *Completed 2026-05-11.*
  Schema split into system description (items 1–7), observation
  record (items 8–9), and reproducibility metadata (items 10–12).
- [x] **P-14. Conjectures section.** *Completed 2026-05-11.* New
  top-level conjectures S1, N1, CAT1, LE added; existing C1, C2,
  C3, OP1 (= L1), OP2, OP3 re-pointed as sub-lemmas.
- [x] **P-15. Scope and Commitments.** *Completed 2026-05-11.*
  Framework now commits on agency (highest non-zero $\sigma_i$);
  "stays open on" replaces "stays neutral on" with a precise list.
- [x] **P-16. Results section.** *Completed 2026-05-11.* Updated
  stub: empty until L1 lands; result papers are the
  developmental venue.
- [x] **P-17. Limitations / submission positioning.** *Completed
  2026-05-11.* Updated to reflect characterisation theorem with
  staged proof obligations; framework positioned as a theory,
  not a methodology.
- [ ] **P-18. Build & lint.** Run `just paper` to rebuild the PDF;
  verify no LaTeX errors, no undefined citations, no overfull
  boxes. **Deferred:** the local LaTeX toolchain is not
  accessible from this session; the build step should be run
  manually at the next opportunity.

---

## Part 2 — Code refactor (`src/emergent_systems/` + `tests/`)

The Python scaffold needs to follow the type-level changes in
the paper.

- [ ] **C-1. `System` dataclass.** Remove the `observer` field
  from `src/emergent_systems/system.py`. The system tuple is now
  $(\mathbf{X}, V, F, T)$ at the type level.
- [ ] **C-2. `run` / `step` signatures.** `run(system, observer,
  ...)` takes the observer as an argument, not an attribute. The
  observer is composed with the system at the call site.
- [ ] **C-3. `observe` helper.** New module-level function
  `observe(system, trajectory, observer)` that applies an external
  observer functor to a system's trajectory and returns observation
  records.
- [ ] **C-4. `SystemSpec` split.** `spec.py` now produces two
  objects: `SystemSpec` (structural items 1–7 from the paper's
  §4) and `ObservationSpec` (observer family, window length,
  state variables, archive details). The two are composed at the
  call site.
- [ ] **C-5. `vitality.py` module.** New module implementing the
  algorithm of [`vitality_computation.md`](vitality_computation.md).
  Provides `VitalityProfile`, `compute_vitality_profile`,
  `compute_composite_vitality_profile`,
  `infer_coupling_structure`, plus the comparison machinery
  (`are_structurally_equivalent`, `partial_order_compare`,
  `observer_mediated_compare`, `compare_systems`) and the
  transition-detection machinery (`detect_level_transition`,
  `scan_trajectory_for_transitions`).
- [ ] **C-6. Conditional transfer entropy helper.** Either wrap
  IDTxl, JIDT, or pyinform (pick one; pin in `pyproject.toml`)
  or write a Kraskov-Stögbauer-Grassberger estimator in pure JAX
  if the dependency cost is too high.
- [ ] **C-7. Counterfactual perturbation infrastructure.** Helper
  for `has_discriminative_capacity` that runs the system with and
  without an injected mutant. Needed for the sharp version of the
  discriminative-capacity test.
- [ ] **C-8. Substrate-specific entity detectors.** Extend
  `entity.py` with the connected-component / DBSCAN / syntactic
  detectors named in `vitality_computation.md` §1.2.
- [ ] **C-9. Tests.** Update `tests/test_pipeline.py` and
  `tests/test_conformance.py` to construct system and observer
  separately. New test module `tests/test_vitality.py` for the
  vitality-profile computation, with fixtures matching the
  regression table in `vitality_computation.md` §"Validation".
- [ ] **C-10. Example stubs.** Update `examples/gol`,
  `examples/lenia`, `examples/boids`, `examples/coupled_lenia_stub`
  to construct system and observer separately, and to include
  fixtures for computing vitality profiles.
- [ ] **C-11. Typing & lint.** Run `just check` after the refactor;
  verify pyright passes, ruff is clean, coverage stays above 80%.
- [ ] **C-12. `pyproject.toml`.** Add the transfer-entropy
  dependency. Pin version.

---

## Part 3 — Tracker and documentation updates

Smaller files but each is load-bearing for someone navigating the
project.

- [x] **T-1. `RESULTS.md`.** *Completed 2026-05-11.* Added rows
  for S1, N1, CAT1, LE; pivot note at top; OP1 → L1 rename
  recorded; dates refreshed.
- [x] **T-2. `IMPLEMENTATION_PLAN.md`.** *Completed 2026-05-11.*
  v2 design pivot addendum appended at the bottom; pre-pivot
  sections preserved as v1 historical record.
- [x] **T-3. `proof_techniques.md`.** *Completed 2026-05-11.*
  Sixth pillar (categorical decomposition theorems) added; per-
  item reading lists for S1, N1, CAT1, LE added under Part 2.
- [x] **T-4. `CLAUDE.md`.** *Completed 2026-05-11.* "What this
  repo is" updated with pivot note and pointers; architecture
  section retitled to "the four-slot model (v2, post-pivot)";
  load-bearing design decisions item 1 rewritten; spec.py
  description updated; pointers to FRAMING_AUDIT.md and this
  task tracker added.
- [x] **T-5. `README.md` (project root).** *Completed 2026-05-11.*
  v2 pivot tagged at the top; pointer to FRAMING_AUDIT.md; 4-slot
  description with external observer functor.
- [x] **T-6. `docs/papers/README.md`.** *Completed 2026-05-11.*
  Brief section pointing to FRAMING_PIVOT_TASKS.md as the
  catalogue of result papers; naming convention extended to
  include new conjecture prefixes (s, n, cat, le, l).

---

## Part 4 — UNPROVEN items to track

**No proofs in this document.** The following statements are
introduced or restated by the framing pivot. They are tracked here
as UNPROVEN; status updates live in `RESULTS.md`. Each item names
the relevant section of FRAMING_AUDIT.md, names the proof venue
(typically a future result paper), and is explicitly *not* attempted
in this task tracker.

### 4.1 Top-level conjectures (introduced by the framing pivot)

- **S1 (Sufficiency)** — UNPROVEN.
  *Statement*: there exists a 4-tuple system + observer pair
  $(\mathcal{S}, O)$ such that $(\mathcal{S}, O) \in \mathbf{LifeCat}$.
  *Source*: FRAMING_AUDIT §3.1. *Proof venue*: result paper
  `s1_sufficiency/` (to be created). *Note*: subsumed in practice
  by `L1` once that lands — `L1` is a concrete witness for `S1`.

- **N1 (Necessity)** — UNPROVEN.
  *Statement*: every life-producing pair $(\mathcal{S}', O)$ with
  $\mathcal{S}'$ presentable as an $\mathcal{O}_W$-algebra admits
  a slot-preserving morphism from a 4-tuple system that is
  essentially surjective on $O$-observable behaviour. *Source*:
  FRAMING_AUDIT §3.2. *Proof venue*: result paper `n1_necessity/`
  (to be created). *Note*: requires the Decomp functor (also
  UNPROVEN).

- **CAT1 (Characterisation)** — UNPROVEN.
  *Statement*: $\mathbf{LifeCat} \simeq \mathrm{image}(\mathrm{Decomp})$,
  with the vitality-profile equivalence preserved. *Source*:
  FRAMING_AUDIT §3.3. *Proof venue*: result paper `cat1_characterisation/`
  (to be created). *Note*: depends on `S1` and `N1` first.

- **LE (Level Emergence)** — UNPROVEN.
  *Statement*: a system at depth $k$ transitions to depth $k+1$
  over a time window iff its level-$k$ entities satisfy the four
  conditions (persistence, aggregation, group variation, group
  selection) over that window. *Source*: FRAMING_AUDIT §2.6 and
  §5. *Proof venue*: result paper `le_level_emergence/` (to be
  created). *Note*: independent of `S1`/`N1`/`CAT1`; can be
  pursued in parallel.

### 4.2 Existing sub-lemma conjectures (restated by the pivot)

- **C1' (Closure-operator unification of viability)** — UNPROVEN.
  *Source*: paper §5.1 (existing). *Status in RESULTS.md*: open.
  *Note*: restated under the pivot but unchanged in content.
  *Proof venue*: `c1_closure_unification/` (template-ready per
  papers/README.md).

- **C2' (Hierarchical viability composition)** — UNPROVEN.
  *Source*: paper §5.1. *Status*: open.
  *Note*: known partial counterexample (RAFs do not compose
  trivially). The pivot connects this to `LE` (the post-transition
  state of LE's mechanism).
  *Proof venue*: `c2_hierarchical_viability/`.

- **C3' (Observer = $\mathbf{Sys} \to \mathbf{Obs}$ divergence-functional schema)** — UNPROVEN.
  *Source*: paper §5.1.
  *Status*: open.
  *Note*: pivot re-points C3 from "observer families are
  divergence functionals" to "the observer functor is a divergence
  functional." Likely the easiest of the lemmas to prove.
  *Proof venue*: `c3_observer_divergence/`.

- **L1 (= renamed OP1, causal emergence existence)** — UNPROVEN.
  *Source*: paper §5.1 OP1.
  *Status*: open.
  *Note*: the **first concrete result targeted** by the framework.
  Lowest-cost candidate is Game of Life under Markov-blanket
  viability (per proof_techniques.md §OP1 D). A positive `L1`
  gives a sufficiency witness for `S1`.
  *Proof venue*: `op1_causal_emergence_lenia/` or
  `l1_causal_emergence_gol/`.

- **OP2' (FEP scope)** — UNPROVEN.
  *Source*: paper §5.1 OP2.
  *Status*: open.
  *Note*: pivot re-frames as specialisation of `N1` to
  FEP-presentable substrate-dynamics pairs.
  *Proof venue*: `op2_fep_scope/`.

- **OP3' (Operadic universality of multiplex topology)** — UNPROVEN.
  *Source*: paper §5.1 OP3.
  *Status*: open.
  *Note*: pivot connects this directly to `N1`'s decomposition
  functor (both use $\mathcal{O}_W$). Should be coordinated with
  `N1` proof effort.
  *Proof venue*: `op3_topology_universality/`.

### 4.3 New sub-lemmas introduced by the pivot

- **Persistence sub-lemma of LE** — UNPROVEN. Level-$k$ entities
  have lifetimes $\gg$ substrate relaxation time.
- **Aggregation sub-lemma of LE** — UNPROVEN. $\kappa^{(k)}$
  produces persistent multi-entity patterns.
- **Group-variation sub-lemma of LE** — UNPROVEN. $\kappa^{(k)}$
  varies non-trivially across the population of aggregates.
- **Group-selection sub-lemma of LE** — UNPROVEN. Aggregate types
  have measurably different persistence rates.
- **Discriminative-capacity lemma** — UNPROVEN. The level-$k$
  iteration $(V_k, F_k)$ amplifies strictly-fitter mutants when
  they are injected. *Note*: testable computationally per
  `vitality_computation.md` §1.4.
- **$\sigma_1$-witness lemma** — UNPROVEN. There exists a system
  with $\sigma_1 = 1$ (frequency-dependent / coevolutionary
  selection). *Note*: existence is uncontroversial; the lemma is
  the formal verification.

### 4.4 Decomp functor existence

- **Decomp functor existence** — UNPROVEN.
  *Statement*: there is a constructive decomposition functor
  $\mathrm{Decomp} : \mathrm{Alg}(\mathcal{O}_W) \to \mathbf{Sys}^{4\text{-slot}}$
  with proven essential surjectivity onto $O$-observable behaviour.
  *Note*: the load-bearing object for `N1`. Yau 2018 gives the
  finite generator presentation that reduces the proof to checking
  ~8 generators. *Proof venue*: shared with `n1_necessity/`.

### 4.5 Categorical-ambient upgrade questions (deferred decisions)

- **2-categorical upgrade of $\mathbf{Sys}$** — DEFERRED.
  *Note*: needed only if `N1`'s essential surjectivity needs
  first-class treatment via 2-morphisms (Baez–Pollard style).
  Not on the immediate work plan.
- **Double-categorical upgrade for `C2'`** — DEFERRED.
  *Note*: needed only if hierarchical viability composition
  requires both compose-at-boundary and nest-into-larger
  structures (Baez–Courser structured cospans). Not on the
  immediate work plan.
- **Topos foundation alternative** — REJECTED for the foundational
  layer; kept as interpretive lift only.
  *Note*: Q1 resolved 2026-05-11 in favour of Option A with C-via-lift.

---

## Part 5 — Future result papers (the series)

The framing pivot's downstream proofs and worked examples are
developed as **focused result papers** under `docs/papers/`. This
section catalogues the papers to be written; each is independent
in scope and can be developed in parallel where dependencies
permit. None are attempted in this task tracker; each is its own
work item.

For the per-file checklist on creating a new result paper, see
[`docs/papers/_template/README.md`](papers/_template/README.md).

### 5.1 Existence-witness papers

- [x] **`l1_causal_emergence_gol/`** — *Skeleton created
  2026-05-11.* Concrete $L_1$ witness on Game of Life under
  Markov-blanket viability. Status flipped in `RESULTS.md` to
  `in-progress` (skeleton). Proof is UNPROVEN; plan-of-attack in
  `paper.tex` §3.
- [x] **`s1_sufficiency/`** — *Skeleton created 2026-05-11.*
  Subsumed in practice by `L1`. Plan: cite L1's witness as the
  sufficiency proof, or construct an abstract witness.

### 5.2 Necessity / characterisation papers

- [x] **`n1_necessity/`** — *Skeleton created 2026-05-11.* The
  load-bearing object is the $\mathrm{Decomp}$ functor; proof
  reduces to Yau's finite generator presentation. UNPROVEN.
- [x] **`cat1_characterisation/`** — *Skeleton created 2026-05-11.*
  Blocked on S1 and N1; largely a coherence theorem once those
  land.

### 5.3 Conjecture papers

- [x] **`c1_closure_unification/`** — *Skeleton created 2026-05-11.*
  Four sub-cases listed: RAF (citable), autopoietic (citable),
  Markov-blanket (open), MCC (novel). UNPROVEN.
- [x] **`c2_hierarchical_viability/`** — *Skeleton created
  2026-05-11.* Known partial counterexample for RAFs flagged.
  Coordinate with LE. UNPROVEN.
- [x] **`c3_observer_divergence/`** — *Skeleton created 2026-05-11.*
  Plausibly easiest lemma. Reid-Williamson-style unification.
  UNPROVEN.
- [x] **`le_level_emergence/`** — *Skeleton created 2026-05-11.*
  Four sub-lemmas. Maynard Smith & Szathmáry as biological
  precedent. UNPROVEN.

### 5.4 Open-problem papers

- [x] **`op2_fep_scope/`** — *Skeleton created 2026-05-11.* Aguilera
  et al. proof pattern. Hardest open problem. UNPROVEN.
- [x] **`op3_topology_universality/`** — *Skeleton created
  2026-05-11.* Coordinate with `n1_necessity/`. UNPROVEN.

### 5.5 Worked-example / methodology papers

- [x] **`programmatic_life_decomposition/`** — *Skeleton created
  2026-05-11.* Tierra-arms-race fragment, vitality profile
  $(2, (1, 1))$ target. UNPROVEN; depends on N1 + methodology.
- [x] **`cultural_life_decomposition/`** — *Skeleton created
  2026-05-11.* Linguistic-evolution slice, vitality profile
  $(3, (1, 1, 1))$ or deeper target. UNPROVEN; deepest test of
  the predictive thesis.
- [x] **`vitality_profile_methodology/`** — *Skeleton created
  2026-05-11.* Methodology paper for the vitality-profile
  computation algorithm. UNPROVEN; depends on
  `vitality.py` implementation.
- [x] **`horizontal_composition_formalisation/`** — *Skeleton
  created 2026-05-11.* Optional standalone target; may be folded
  into `n1_necessity/`. UNPROVEN.

### 5.6 Ordering and dependencies

Recommended order for the first wave of result papers:

1. `l1_causal_emergence_gol/` — lowest-cost concrete result.
2. `vitality_profile_methodology/` — operationalises the
   measurement; needed for empirical validation of later papers.
3. `c1_closure_unification/` — most mature literature; clear gap.
4. `c3_observer_divergence/` — plausibly easy.
5. `le_level_emergence/` — independent of `S1`/`N1`/`CAT1`;
   structurally clean.
6. `programmatic_life_decomposition/` — worked example for the
   predictive thesis.
7. `c2_hierarchical_viability/` — needs `c1_closure_unification/`
   first.
8. `op3_topology_universality/` — heavier categorical machinery.
9. `n1_necessity/` — long; coordinate with #8.
10. `op2_fep_scope/` — hardest; depends on commitment to what
    "informative FEP" means.
11. `s1_sufficiency/` — subsumed by `L1`; can be written abstractly.
12. `cat1_characterisation/` — last; depends on `S1` and `N1`.
13. `cultural_life_decomposition/` — depends on methodology being
    settled.

The ordering is a recommendation, not a strict dependency graph.
Papers in the same row of the dependency graph can be written in
parallel.

---

## Conventions for using this tracker

- Mark a checkbox as completed when the action has landed and any
  related commit has been pushed.
- For tasks that produce a result paper, set the paper's status
  in `RESULTS.md` to `in-progress` when the directory is created
  and link the directory; set it to `proved` / `disproved` /
  `mutated` / `withdrawn` when the paper concludes.
- Do not delete entries when complete; check them off, so the
  document also serves as a record of what has been done.
- Add new tasks under the appropriate section as the work
  surfaces them.
- For tasks that turn out to be impossible or unnecessary, mark
  them as withdrawn with a brief note rather than deleting them.
