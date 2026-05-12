# Results tracker

Status of every conjecture and open problem stated in
[`docs/emergent_systems.tex`](docs/emergent_systems.tex) (the scaffolding
paper). The scaffolding paper itself stays clean of status notes — they live
here, alongside links to the per-result proof papers under
[`docs/papers/`](docs/papers/).

When a status changes, update the row **and** the *Last updated* date (UTC,
`YYYY-MM-DD`). When a result paper exists, link the directory under
`docs/papers/<slug>/` (or its built PDF on GitHub Pages once published).

> **Framing pivot 2026-05-11.** The framework underwent a major pivot from
> a descriptive vocabulary to a predictive characterisation theorem. See
> [`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md) and
> [`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md). This tracker
> now lists the new top-level conjectures (S1, N1, CAT1, LE) alongside the
> pivot-renamed existing items (C1' → C1, C2' → C2, C3' → C3, L1 = renamed
> OP1, OP2' → OP2, OP3' → OP3 — the primed names from the audit memo are
> the canonical identifiers going forward but the table below preserves the
> original `Cn` / `OPn` names for backward-compatibility with citations).

## Status vocabulary

| Status        | Meaning |
|---------------|---------|
| `open`        | No serious attempt yet, or attempts have not produced a publishable result. |
| `in-progress` | A result paper exists under `docs/papers/<slug>/` but the proof is incomplete. |
| `proved`      | A result paper establishes the conjecture (or, for an open problem, answers it affirmatively in the sense intended). |
| `disproved`   | A result paper establishes a counterexample or a refutation. |
| `mutated`     | The conjecture was reformulated mid-proof; the row links the new statement (typically a new conjecture id, e.g. `C1'`). |
| `withdrawn`   | A definition change in the scaffolding paper made the conjecture vacuous, redundant, or ill-posed. |

## Top-level conjectures (introduced by the framing pivot)

Source: scaffolding paper §sec:conjectures (post-pivot rewrite); see
[`docs/FRAMING_AUDIT.md`](docs/FRAMING_AUDIT.md) §3 and §5 for full
statements and dependencies.

| ID   | Statement (short)                                                              | Paper § | Status | Result paper | Last updated |
|------|--------------------------------------------------------------------------------|---------|--------|--------------|--------------|
| S1   | Sufficiency: some 4-tuple system + observer has vitality profile $(k,\sigma)$ with $k \geq 1$ | §sec:s1 | in-progress | [`docs/papers/s1_sufficiency/`](docs/papers/s1_sufficiency/) (skeleton) | 2026-05-11 |
| N1   | Necessity: every life-producing pair decomposes as a 4-tuple system in $\mathrm{Alg}(\mathcal{O}_W)$ | §sec:n1 | in-progress | [`docs/papers/n1_necessity/`](docs/papers/n1_necessity/) (skeleton) | 2026-05-11 |
| CAT1 | Characterisation: $\mathbf{LifeCat} \simeq \mathrm{image}(\mathrm{Decomp})$    | §sec:cat1 | in-progress | [`docs/papers/cat1_characterisation/`](docs/papers/cat1_characterisation/) (skeleton) | 2026-05-11 |
| LE   | Level emergence: depth-$k$ system transitions to depth $k+1$ iff four conditions hold | §sec:le | in-progress | [`docs/papers/le_level_emergence/`](docs/papers/le_level_emergence/) (skeleton) | 2026-05-11 |

## Sub-lemma conjectures (pivot-renamed; track under both names)

Source: scaffolding paper §5.1 (pre-pivot `C1`–`C3`; the pivot re-points
them as sub-lemmas of `N1`).

| ID (canonical) | Statement (short)                                  | Paper § | Status | Result paper | Last updated |
|----------------|----------------------------------------------------|---------|--------|--------------|--------------|
| C1             | Closure-operator unification of viability          | §5.1    | in-progress | [`docs/papers/c1_closure_unification/`](docs/papers/c1_closure_unification/) (skeleton) | 2026-05-11 |
| C2             | Hierarchical viability composition                 | §5.1    | in-progress | [`docs/papers/c2_hierarchical_viability/`](docs/papers/c2_hierarchical_viability/) (skeleton) | 2026-05-11 |
| C3             | Observer-relative novelty as divergence-functional | §5.1    | in-progress | [`docs/papers/c3_observer_divergence/`](docs/papers/c3_observer_divergence/) (skeleton) | 2026-05-11 |

C1', C2', C3' are the pivot-renamed forms of C1, C2, C3 in the post-pivot
notation. The mathematical statements are unchanged; only the framing is
sharper (C3' now reads the observer as the $\mathbf{Sys} \to \mathbf{Obs}$
functor rather than as a slot).

## Open problems (pivot-renamed; track under both names)

Source: scaffolding paper §5.1 (pre-pivot `OP1`–`OP3`). The pivot renames
`OP1` to `L1` and re-points `OP2`/`OP3` as sub-lemmas of `N1`.

| ID (canonical) | Question (short)                                                                       | Paper § | Status | Result paper | Last updated |
|----------------|----------------------------------------------------------------------------------------|---------|--------|--------------|--------------|
| OP1 (= L1)     | Causal emergence of scaffolded systems: $\sup_\Pi \mathrm{CE}(M(\mathcal{S}),\Pi) > 0$ | §5.1    | in-progress | [`docs/papers/l1_causal_emergence_gol/`](docs/papers/l1_causal_emergence_gol/) (skeleton) | 2026-05-11 |
| OP2            | FEP-as-lens scope: substrate–dynamics pairs for which FEP is informative               | §5.1    | in-progress | [`docs/papers/op2_fep_scope/`](docs/papers/op2_fep_scope/) (skeleton) | 2026-05-11 |
| OP3            | Interaction-topology expressiveness: multiplex-with-$\diamond_\rho$ universality       | §5.1    | in-progress | [`docs/papers/op3_topology_universality/`](docs/papers/op3_topology_universality/) (skeleton) | 2026-05-11 |

`L1` is the **first concrete result targeted** by the framework
post-pivot. A positive `L1` result on Game-of-Life-under-Markov-blanket-
viability is a sufficiency witness for `S1`. See proof_techniques.md
§OP1 D for the lowest-hanging-fruit proof sketch.

## Adding a result

1. Copy [`docs/papers/_template/`](docs/papers/_template/) to
   `docs/papers/<id>_<slug>/` and follow that directory's `README.md`.
2. Flip the row above for `<id>` from `open` to `in-progress` and link the
   directory in the *Result paper* column.
3. When the proof lands (or a counterexample is found), update the status
   to `proved` / `disproved` / `mutated` / `withdrawn` and refresh the date.

## Re-syncing this file with the paper

If the scaffolding paper gains, removes, or renumbers a conjecture or open
problem, update this file in the same commit. The source of truth is
`docs/emergent_systems.tex` §sec:conjectures (and the pre-pivot §5.1) —
`RESULTS.md` is the index, not the specification.

The catalogue of result papers to be written is in
[`docs/FRAMING_PIVOT_TASKS.md`](docs/FRAMING_PIVOT_TASKS.md) Part 5.
