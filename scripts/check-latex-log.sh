#!/usr/bin/env bash
# Post-build LaTeX log checker for the `papers` workflow.
#
# Two output formats:
#   --format=actions   (default) — emits ::error::/::warning:: GitHub Actions
#                                  annotations. Exit 1 on hard errors so the
#                                  workflow leg fails. Pair with --strict to
#                                  also fail on soft warnings.
#   --format=markdown            — emits a markdown fragment for use in PR
#                                  comments. Exit 0 unless the log file is
#                                  missing (so the comment job aggregates all
#                                  papers even when one has errors). --strict
#                                  is ignored in this mode.
#
# Hard errors (always counted, both formats):
#   - LaTeX Warning: Reference|Citation ... undefined
#   - LaTeX Warning: Label|Reference ... multiply defined
#   - LaTeX Warning: There were undefined references|citations
#   - LaTeX Warning: Label(s) may have changed     (latexmk did not converge)
#
# Soft warnings (always counted, both formats):
#   - Overfull|Underfull \h|\vbox
#
# Usage:
#   check-latex-log.sh <log_file> <source_path>
#       [--format=actions|markdown] [--strict]
#
# Exit codes:
#   0  clean OR markdown mode (markdown mode never exits non-zero on content)
#   1  actions mode and hard errors found
#      (or, with --strict, actions mode and any warning found)
#   2  usage/setup error (log file missing, bad flag)

set -uo pipefail

format="actions"
strict=0
positional=()
for arg in "$@"; do
  case "$arg" in
    --format=actions|--format=markdown)
      format="${arg#--format=}"
      ;;
    --format=*)
      echo "::error::unknown --format value: ${arg#--format=}" >&2
      exit 2
      ;;
    --strict)
      strict=1
      ;;
    -*)
      echo "::error::unknown flag: $arg" >&2
      exit 2
      ;;
    *)
      positional+=("$arg")
      ;;
  esac
done

if (( ${#positional[@]} != 2 )); then
  echo "usage: $0 <log_file> <source_path> [--format=actions|markdown] [--strict]" >&2
  exit 2
fi

log="${positional[0]}"
src="${positional[1]}"

if [[ ! -f "$log" ]]; then
  if [[ "$format" == "actions" ]]; then
    echo "::error::LaTeX log not found: $log"
  else
    echo "_log not found: \`${log}\`_"
  fi
  exit 2
fi

# --- Parse -----------------------------------------------------------------

declare -a errs=()
declare -a warns=()

while IFS= read -r line; do
  errs+=("${line#LaTeX Warning: }")
done < <(grep -E '^LaTeX Warning: (Reference|Citation) .* undefined' "$log" || true)

while IFS= read -r line; do
  errs+=("${line#LaTeX Warning: }")
done < <(grep -E '^LaTeX Warning: (Label|Reference) .* multiply[- ]defined' "$log" || true)

if grep -qE '^LaTeX Warning: There were undefined (references|citations)' "$log"; then
  errs+=("Undefined references or citations remain after the final compile pass.")
fi

if grep -qE '^LaTeX Warning: Label\(s\) may have changed' "$log"; then
  errs+=("Labels changed on the final pass — latexmk did not converge.")
fi

while IFS= read -r line; do
  warns+=("$line")
done < <(grep -E '^(Overfull|Underfull) \\(h|v)box' "$log" || true)

n_err=${#errs[@]}
n_warn=${#warns[@]}

# --- Emit ------------------------------------------------------------------

case "$format" in
  actions)
    for e in "${errs[@]:-}"; do
      [[ -z "${e:-}" ]] && continue
      echo "::error file=${src}::$e"
    done
    for w in "${warns[@]:-}"; do
      [[ -z "${w:-}" ]] && continue
      echo "::warning file=${src}::$w"
    done
    echo ""
    if (( strict )); then
      mode="strict"
    else
      mode="errors-only"
    fi
    echo "LaTeX log summary for ${src} (${mode}): ${n_err} error(s), ${n_warn} warning(s)."
    if (( n_err > 0 )); then
      exit 1
    fi
    if (( strict && n_warn > 0 )); then
      exit 1
    fi
    ;;

  markdown)
    if (( n_err == 0 && n_warn == 0 )); then
      echo "_No errors or warnings._"
    else
      if (( n_err > 0 )); then
        echo "**Errors:**"
        for e in "${errs[@]}"; do
          echo "- ${e}"
        done
        echo ""
      fi
      if (( n_warn > 0 )); then
        echo "**Warnings:**"
        for w in "${warns[@]}"; do
          # Wrap \hbox / \vbox in backticks so Markdown doesn't eat the backslash.
          escaped="${w//\\/\\\\}"
          echo "- ${escaped}"
        done
        echo ""
      fi
    fi
    ;;
esac

exit 0
