# Textbook drafts

A short-form ("essential knowledge"-style) book introducing artificial life, emergence, novelty, and the five-slot decomposition. Audience: readers who want to make their own artificial-life systems and have a working command of probability, dynamical systems, and Python.

## Status

Draft. All nine main chapters and the math primer appendix have first-pass drafts ([preface.tex](preface.tex), [ch01](ch01-what-is-artificial-life.tex)–[ch09](ch09-frontiers.tex), [math-primer.tex](math-primer.tex)). The chapter order is fixed; the prose will be revised in place.

## Chapters

1. What is artificial life? — [ch01-what-is-artificial-life.tex](ch01-what-is-artificial-life.tex)
2. What is life? — [ch02-what-is-life.tex](ch02-what-is-life.tex)
3. Emergence and novelty — [ch03-emergence-and-novelty.tex](ch03-emergence-and-novelty.tex)
4. The five-slot lens — [ch04-five-slot-lens.tex](ch04-five-slot-lens.tex)
5. Substrate and variation — [ch05-substrate-and-variation.tex](ch05-substrate-and-variation.tex)
6. Viability — [ch06-viability.tex](ch06-viability.tex)
7. Topology and observers — [ch07-topology-and-observers.tex](ch07-topology-and-observers.tex)
8. Composition and measurement — [ch08-composition-and-measurement.tex](ch08-composition-and-measurement.tex)
9. Frontiers — [ch09-frontiers.tex](ch09-frontiers.tex)

## Appendix

- Math primer (order theory, measure theory, information theory, category theory) — [math-primer.tex](math-primer.tex)

## Format

LaTeX, `book` class. The master file is [book.tex](book.tex); chapters live in per-file `\input` includes (`preface.tex`, `chNN-slug.tex`). The preamble matches the scaffolding paper's conventions (utf8/T1, microtype, amsmath stack, hidelinks hyperref, 1in geometry).

## Build

From the repo root:

```bash
just textbook
```

This runs `latexmk -pdf` against [book.tex](book.tex) into this directory, mirroring the pattern used by `just paper` for the scaffolding paper. The shared `just clean-paper` recipe also cleans intermediates here.

## Relationship to the rest of this repo

- The paper at [../emergent_systems.tex](../emergent_systems.tex) is the formal reference; the textbook is the readable companion.
- Worked examples will eventually map to notebooks in [../../src/emergent_systems/examples/](../../src/emergent_systems/examples/) (currently stubs).
- Open problems and conjectures are tracked in [../../RESULTS.md](../../RESULTS.md); the textbook cites that file rather than duplicating it.
