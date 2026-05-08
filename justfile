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
    -rm -rf .pytest_cache .ruff_cache .pyright dist build
    -find src tests -type d -name __pycache__ -exec rm -rf {} +

# Remove Python build/cache directories.
[windows]
clean-py:
    -Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache, .ruff_cache, .pyright, dist, build
    -Get-ChildItem -Path src, tests -Filter __pycache__ -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# ---- Paper ------------------------------------------------------------------

paper:
    latexmk -c -pdf -interaction=nonstopmode -outdir={{ DOC_DIR }} {{ PAPER_NAME }}.tex
