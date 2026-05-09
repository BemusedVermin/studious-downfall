# Per-result paper template

A self-contained LaTeX project for **one** result targeting one conjecture or
open problem from the scaffolding paper
([`docs/emergent_systems.tex`](../../emergent_systems.tex)).

## How to use

1. **Copy this directory** to `docs/papers/<id>_<slug>/`, where:
   - `<id>` is the conjecture / open-problem identifier (`c1`, `c2`, `c3`,
     `op1`, `op2`, `op3`) from scaffolding paper §5.1, and
   - `<slug>` is a short ASCII slug describing the angle of attack.

   Example: `docs/papers/c1_closure_unification/`.

2. **Edit `paper.tex`:**
   - Set `\title{...}` and `\author{...}`.
   - In `\section{Statement}`, paste the conjecture / open-problem **verbatim**
     from `docs/emergent_systems.tex` so reviewers can compare without
     cross-referencing.
   - Fill in `\section{Result}`, `\section{Proof}`, and `\section{Discussion}`.

3. **Edit `references.bib`:** the scaffolding-paper entry (`emergent_systems_2026`)
   is pre-populated. Append further entries as the proof requires.

4. **Build:** from the repo root, run `just paper-result <id>_<slug>`. The PDF
   lands at `docs/papers/<id>_<slug>/paper.pdf`.

5. **Update [`RESULTS.md`](../../../RESULTS.md):** flip the row for `<id>` from
   `open` to `in-progress`, and link the new directory in the *Result paper*
   column. When the proof is done (or fails), update status accordingly.

## Conventions

- Use `\documentclass{article}` (kept by the template) — these are short
  focused papers, not chapters of a book.
- Use the scaffolding paper's notation. Don't redefine `\X`, `\Mplus`, `\EI`,
  `\CE`, etc.\ in incompatible ways; if you need them, copy the relevant
  `\newcommand`s from the scaffolding paper preamble or extend it.
- Cite the scaffolding paper as `\cite{emergent_systems_2026}` for every
  appeal to a definition or result that lives there. Do **not** restate its
  definitions; that is what the citation is for.
- One result per paper. If the proof needs lemmas, lemmas live in the same
  file. If the proof opens a second independent question, that question gets
  its own `<id>_<slug>/` directory (and its own `RESULTS.md` row).

## What CI will check

The `papers` workflow ([`.github/workflows/papers.yml`](../../../.github/workflows/papers.yml))
auto-discovers any `docs/papers/<slug>/paper.tex` and runs `latexmk`. A new
result paper must compile with no undefined references or citations and no
multiply-defined labels. Overfull/underfull boxes are flagged as warnings;
fix them before merge when feasible.
