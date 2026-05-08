DOC_DIR := "docs"
PAPER_NAME := "emergent_systems"

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
clean-py:
    -rm -rf .pytest_cache .ruff_cache .pyright dist build
    -find src tests -type d -name __pycache__ -exec rm -rf {} +

# ---- Paper ------------------------------------------------------------------

paper:
    latexmk -c -pdf -interaction=nonstopmode -outdir={{ DOC_DIR }} {{ PAPER_NAME }}.tex
