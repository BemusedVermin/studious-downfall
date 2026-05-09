# Results tracker

Status of every conjecture and open problem stated in
[`docs/emergent_systems.tex`](docs/emergent_systems.tex) (the scaffolding
paper). The scaffolding paper itself stays clean of status notes — they live
here, alongside links to the per-result proof papers under
[`docs/papers/`](docs/papers/).

When a status changes, update the row **and** the *Last updated* date (UTC,
`YYYY-MM-DD`). When a result paper exists, link the directory under
`docs/papers/<slug>/` (or its built PDF on GitHub Pages once published).

## Status vocabulary

| Status        | Meaning |
|---------------|---------|
| `open`        | No serious attempt yet, or attempts have not produced a publishable result. |
| `in-progress` | A result paper exists under `docs/papers/<slug>/` but the proof is incomplete. |
| `proved`      | A result paper establishes the conjecture (or, for an open problem, answers it affirmatively in the sense intended). |
| `disproved`   | A result paper establishes a counterexample or a refutation. |
| `mutated`     | The conjecture was reformulated mid-proof; the row links the new statement (typically a new conjecture id, e.g. `C1'`). |
| `withdrawn`   | A definition change in the scaffolding paper made the conjecture vacuous, redundant, or ill-posed. |

## Conjectures

Source: scaffolding paper §5.1, statements `C1`–`C3`.

| ID | Statement (short)                                  | Paper § | Status | Result paper | Last updated |
|----|----------------------------------------------------|---------|--------|--------------|--------------|
| C1 | Closure-operator unification of viability          | §5.1    | open   | —            | 2026-05-08   |
| C2 | Hierarchical viability composition                 | §5.1    | open   | —            | 2026-05-08   |
| C3 | Observer-relative novelty as divergence-functional | §5.1    | open   | —            | 2026-05-08   |

## Open problems

Source: scaffolding paper §5.1, statements `OP1`–`OP3`.

| ID  | Question (short)                                                                       | Paper § | Status | Result paper | Last updated |
|-----|----------------------------------------------------------------------------------------|---------|--------|--------------|--------------|
| OP1 | Causal emergence of scaffolded systems: $\sup_\Pi \mathrm{CE}(M(\mathcal{S}),\Pi) > 0$ | §5.1    | open   | —            | 2026-05-08   |
| OP2 | FEP-as-lens scope: substrate–dynamics pairs for which FEP is informative               | §5.1    | open   | —            | 2026-05-08   |
| OP3 | Interaction-topology expressiveness: multiplex-with-$\diamond_\rho$ universality       | §5.1    | open   | —            | 2026-05-08   |

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
`docs/emergent_systems.tex` §5.1 — `RESULTS.md` is the index, not the
specification.
