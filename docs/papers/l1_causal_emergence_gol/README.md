# `l1_causal_emergence_gol/` — UNPROVEN

Skeleton paper targeting **L1 (= renamed OP1)**: causal emergence of a
scaffolded system. The candidate witness is Game of Life under
Markov-blanket viability on bounded-support configurations.

**Status:** UNPROVEN. This directory holds a statement-and-plan
skeleton only; no proof is attempted. Status in
[`RESULTS.md`](../../../RESULTS.md) is `open`.

L1 is the **first concrete result the framework targets**. A positive
proof gives a sufficiency witness for the top-level conjecture
**S1**.

## What to do next

The plan of attack is in `paper.tex` §3, with six UNPROVEN steps.
Discharge them one at a time. Coordinate with the methodology paper
under [`vitality_profile_methodology/`](../vitality_profile_methodology/)
for the computational side of the EI / CE comparisons.

If a step proves obstructed, follow the pivot path in
`paper.tex` §4: switch to one of the alternative candidate systems
(Flow-Lenia + MB, Diff-Logic CA, POET) and update
[`RESULTS.md`](../../../RESULTS.md) with status `mutated`.

## Build

```bash
just paper-result l1_causal_emergence_gol
```

## Cross-references

- Scaffolding paper conjecture statement:
  [`docs/emergent_systems.tex`](../../emergent_systems.tex)
  §`sec:op1`.
- Proof-strategy reading list:
  [`docs/proof_techniques.md`](../../proof_techniques.md) §OP1.
- Top-level task tracking:
  [`docs/FRAMING_PIVOT_TASKS.md`](../../FRAMING_PIVOT_TASKS.md)
  Part 5.
