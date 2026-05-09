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

# Run the suite under coverage; fails if total coverage drops below the threshold
# in [tool.coverage.report].fail_under (currently 80%). Writes coverage.xml for CI.
cov:
    uv run pytest --cov --cov-report=term-missing --cov-report=xml

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

# The full pre-commit gauntlet: lint, typecheck, test.
check: lint typecheck test

# Remove Python build/cache directories.
[unix]
clean-py:
    -rm -rf .pytest_cache .ruff_cache .pyright dist build .coverage coverage.xml
    -find src tests -type d -name __pycache__ -exec rm -rf {} +

# Remove Python build/cache directories.
[windows]
clean-py:
    -Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache, .ruff_cache, .pyright, dist, build, .coverage, coverage.xml
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
