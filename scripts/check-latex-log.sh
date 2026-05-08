#!/usr/bin/env bash
# Post-build LaTeX log checker for the `papers` workflow.
#
# Emits GitHub Actions annotations:
#   ::error::   undefined references/citations, multiply-defined labels,
#               label-convergence failure  -> exit 1, fails the workflow leg
#   ::warning:: Overfull/Underfull h/vbox  -> visible in the PR UI, does not fail
#
# Usage:
#   check-latex-log.sh <log_file> <source_path_for_annotations>
#
# Exit codes:
#   0  clean (annotations may still have been emitted as warnings)
#   1  hard error: undefined refs/cites/labels or convergence failure
#   2  usage/setup error (log file missing)
#
# Note: not using `set -e` because `grep` returns 1 on no-match, which is the
# desired clean state. We use `|| true` on each grep instead.

set -uo pipefail

log="${1:?usage: $0 <log_file> <source_path>}"
src="${2:?usage: $0 <log_file> <source_path>}"

if [[ ! -f "$log" ]]; then
  echo "::error::LaTeX log not found: $log"
  exit 2
fi

errors=0
warnings=0

emit_error() {
  echo "::error file=${src}::$1"
  errors=$((errors + 1))
}

emit_warning() {
  echo "::warning file=${src}::$1"
  warnings=$((warnings + 1))
}

# --- Hard failures ----------------------------------------------------------

# Per-occurrence undefined reference/citation.
while IFS= read -r line; do
  emit_error "${line#LaTeX Warning: }"
done < <(grep -E '^LaTeX Warning: (Reference|Citation) .* undefined' "$log" || true)

# Multiply-defined labels (silent corruption risk: cross-refs go to wrong target).
while IFS= read -r line; do
  emit_error "${line#LaTeX Warning: }"
done < <(grep -E '^LaTeX Warning: (Label|Reference) .* multiply[- ]defined' "$log" || true)

# Summary line confirming undefined items remain after the final pass.
if grep -qE '^LaTeX Warning: There were undefined (references|citations)' "$log"; then
  emit_error "Undefined references or citations remain after the final compile pass."
fi

# Label-convergence failure: latexmk should rerun until labels stabilise. If the
# final pass still reports this, the run did not converge (cyclic dependency or
# pass-cap reached).
if grep -qE '^LaTeX Warning: Label\(s\) may have changed' "$log"; then
  emit_error "Labels changed on the final pass — latexmk did not converge."
fi

# --- Soft warnings ----------------------------------------------------------

# Overfull/Underfull h/vbox — cosmetic, surfaced as warnings.
while IFS= read -r line; do
  emit_warning "$line"
done < <(grep -E '^(Overfull|Underfull) \\(h|v)box' "$log" || true)

# --- Summary ----------------------------------------------------------------

echo ""
echo "LaTeX log summary for ${src}: ${errors} error(s), ${warnings} warning(s)."

if (( errors > 0 )); then
  exit 1
fi
exit 0
