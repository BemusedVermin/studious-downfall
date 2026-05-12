# `docs/papers/`

Per-result proof papers live here, one self-contained LaTeX project per
subdirectory. The scaffolding paper at
[`docs/emergent_systems.tex`](../emergent_systems.tex) is the framework
reference; everything in this directory **cites** the scaffolding paper rather
than redefining its types or notation.

> **Framing pivot (2026-05-11).** Following the framing pivot documented in
> [`../FRAMING_AUDIT.md`](../FRAMING_AUDIT.md), the downstream expository and
> proof work develops as **a series of focused result papers under this
> directory**, not as a textbook. A previous textbook draft under
> `docs/textbook/` was deleted on 2026-05-11; see `CHANGELOG.md`. The full
> catalogue of result papers to be written — covering both the existing
> conjectures `C1`–`C3` / `OP1`–`OP3` and the new top-level conjectures `S1`,
> `N1`, `CAT1`, `LE`, plus worked-example and methodology papers — is in
> [`../FRAMING_PIVOT_TASKS.md`](../FRAMING_PIVOT_TASKS.md) Part 5.

## Layout

```text
docs/
  emergent_systems.tex           # scaffolding paper (framework reference)
  emergent_systems.bib
  papers/
    README.md                    # this file
    _template/                   # copyable starter for a new result
      paper.tex
      references.bib
      README.md                  # how to copy and rename
    c1_closure_unification/      # example future result (not present yet)
      paper.tex
      references.bib
```

The scaffolding paper stays the single source of truth for definitions,
typing, and conjectures. Each `<slug>/` here addresses **one** conjecture or
open problem (or a closely-related cluster) and produces one PDF.

## Naming convention

Subdirectory names follow `<id>_<short-slug>/`:

- `c<n>_<slug>/` for results addressing Conjecture C\<n\> (e.g.
  `c1_closure_unification/`).
- `op<n>_<slug>/` for results addressing Open Problem OP\<n\> (e.g.
  `op1_causal_emergence_lenia/`).
- `l<n>_<slug>/` for the renamed `L1` (= former `OP1`) and any
  future lemma-level results.
- `s<n>_<slug>/`, `n<n>_<slug>/`, `cat<n>_<slug>/`, `le_<slug>/`
  for the post-pivot top-level conjectures (`S1`, `N1`, `CAT1`,
  `LE` respectively).

The `<id>` prefix matches the conjecture/open-problem identifiers used in the
scaffolding paper and tracked in [`RESULTS.md`](../../RESULTS.md). Use
lowercase ASCII for the slug; underscores between words.

## Starting a new result paper

1. Copy `_template/` to `<id>_<slug>/`.
2. Read [`_template/README.md`](_template/README.md) for the per-file checklist
   (title, abstract, statement, proof, bib).
3. Build with `just paper-result <id>_<slug>` (see below).
4. Update the row for `<id>` in [`RESULTS.md`](../../RESULTS.md): set status
   to `in-progress`, link the new directory.
5. When the proof lands, set status to `proved` (or `disproved` /
   `mutated` / `withdrawn` per the vocabulary in `RESULTS.md`).

## Building

From the repo root:

```bash
just paper                      # builds the scaffolding paper
just paper-result <id>_<slug>   # builds one result paper
```

Both recipes invoke `latexmk` with `-pdf -interaction=nonstopmode` and write
intermediate files plus the final PDF into the paper's own directory so build
artefacts from different papers never collide.

## CI

Every `paper.tex` under `docs/papers/<slug>/` is auto-discovered by the
`papers` workflow ([`.github/workflows/papers.yml`](../../.github/workflows/papers.yml))
and built on every push / PR. Each paper is its own matrix leg so a broken
paper does not mask the others. PDFs are published to GitHub Pages on
push-to-master.

The workflow runs [`scripts/check-latex-log.sh`](../../scripts/check-latex-log.sh)
on each build log; a new result paper must compile with **no undefined
references or citations** and should aim for no overfull/underfull boxes.
