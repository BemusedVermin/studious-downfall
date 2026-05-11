DOC_DIR := "docs"
PAPER_NAME := "emergent_systems"

# Use Windows PowerShell on Windows; just falls back to `sh` elsewhere.
# The `[unix]` / `[windows]` recipe attributes below pick the right body per host.
set windows-shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

default:
    just --list

# ---- Python library ---------------------------------------------------------

# Sync the dev environment (jax, jaxtyping, beartype, pytest, ruff, pyright).
install:
    uv sync --extra dev

# Run the full test suite.
test:
    uv run pytest

# Run a single test file or node, e.g. `just test-one tests/test_emergence.py`.
test-one TARGET:
    uv run pytest {{ TARGET }} -v

# Run the suite under coverage; fails if total coverage drops below the threshold.
# `--cov-fail-under=80` is set on the CLI (and not relied on via [tool.coverage.report])
# because pytest-cov's propagation of fail_under from pyproject.toml is version-sensitive.
cov:
    uv run pytest --cov --cov-report=term-missing --cov-report=xml --cov-fail-under=80

# Lint without modifying anything.
lint:
    uv run ruff check src tests

# Auto-fix lint issues that ruff knows how to fix.
fix:
    uv run ruff check src tests --fix

# Format the codebase.
fmt:
    uv run ruff format src tests

# Static type-check.
typecheck:
    uv run pyright src tests

# The full pre-commit gauntlet: lint, typecheck, coverage-gated test. Mirrors CI so a
# `just check`-clean tree won't fail the gate after push.
check: lint typecheck cov

# Remove Python build/cache directories.
[unix]
clean-py:
    -rm -rf .pytest_cache .ruff_cache .pyright dist build .coverage coverage.xml htmlcov
    -find src tests -type d -name __pycache__ -exec rm -rf {} +

# Remove Python build/cache directories.
[windows]
clean-py:
    -Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache, .ruff_cache, .pyright, dist, build, .coverage, coverage.xml, htmlcov
    -Get-ChildItem -Path src, tests -Filter __pycache__ -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# ---- Papers -----------------------------------------------------------------
# `paper`        builds the scaffolding (framework) paper at docs/{{ PAPER_NAME }}.tex.
# `paper-result` builds one per-result paper at docs/papers/<slug>/paper.tex.
# Each paper writes intermediate files and the final PDF into its own directory
# so artefacts from different papers never collide.

# Build the scaffolding (framework) paper.
paper:
    latexmk -pdf -interaction=nonstopmode -outdir={{ DOC_DIR }} {{ DOC_DIR }}/{{ PAPER_NAME }}.tex

# Build a per-result paper, e.g. `just paper-result c1_closure_unification`.
# Fails loudly if the slug doesn't exist.
paper-result SLUG:
    latexmk -pdf -interaction=nonstopmode -outdir={{ DOC_DIR }}/papers/{{ SLUG }} {{ DOC_DIR }}/papers/{{ SLUG }}/paper.tex

# Build the textbook (`book` class; master file at docs/textbook/book.tex).
textbook:
    latexmk -pdf -interaction=nonstopmode -outdir={{ DOC_DIR }}/textbook {{ DOC_DIR }}/textbook/book.tex

# Remove LaTeX build intermediates (`*.log`, `*.aux`, `*.bbl`, etc.) under docs/, leaving
# sources (`*.tex`, `*.bib`, `*.md`) and final `*.pdf` outputs in place. Walks recursively so
# both the scaffolding paper and per-result papers under docs/papers/<slug>/ are covered.
[unix]
clean-paper:
    -find {{ DOC_DIR }} -type f \( -name "*.aux" -o -name "*.bbl" -o -name "*.blg" -o -name "*.fdb_latexmk" -o -name "*.fls" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.nav" -o -name "*.snm" -o -name "*.vrb" -o -name "*.lof" -o -name "*.lot" -o -name "*.bcf" -o -name "*.synctex.gz" -o -name "*.run.xml" \) -delete

# Remove LaTeX build intermediates (Windows variant).
[windows]
clean-paper:
    -Get-ChildItem -Path {{ DOC_DIR }} -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in '.aux','.bbl','.blg','.fdb_latexmk','.fls','.log','.out','.toc','.nav','.snm','.vrb','.lof','.lot','.bcf' -or $_.Name.EndsWith('.synctex.gz') -or $_.Name.EndsWith('.run.xml') } | Remove-Item -Force -ErrorAction SilentlyContinue
