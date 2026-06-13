#!/usr/bin/env bash
#
# lint-commands.sh — lint QA-toolkit command files for hardcoded paths/tools,
# missing self-checks, missing template references, and frontmatter hygiene.
#
# Usage (from repo root):
#   bash scripts/lint-commands.sh
#
# Exit codes:
#   0  no violations (warnings allowed)
#   1  one or more violations found
#   2  setup error (no commands directory / no files)
#
# Pure bash + grep. No external deps beyond coreutils/grep.

set -u

# --- Locate the repo root and commands dir (works regardless of CWD) ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD_DIR="$REPO_ROOT/commands"

# --- Colors (disabled when not a TTY) -----------------------------------------
if [ -t 1 ]; then
  C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_GRN=$'\033[32m'
  C_DIM=$'\033[2m'; C_BOLD=$'\033[1m'; C_RST=$'\033[0m'
else
  C_RED=''; C_YEL=''; C_GRN=''; C_DIM=''; C_BOLD=''; C_RST=''
fi

if [ ! -d "$CMD_DIR" ]; then
  echo "ERROR: commands directory not found at $CMD_DIR" >&2
  exit 2
fi

shopt -s nullglob
FILES=("$CMD_DIR"/*.md)
shopt -u nullglob
if [ "${#FILES[@]}" -eq 0 ]; then
  echo "ERROR: no command files (*.md) found in $CMD_DIR" >&2
  exit 2
fi

# --- Totals -------------------------------------------------------------------
TOTAL_FILES=0
PASS_FILES=0
TOTAL_VIOLATIONS=0
TOTAL_WARNINGS=0

# Global indexed array reused per file: DISCOVERY[<lineno>]=1 marks lines that
# sit inside a ```! discovery block. Declared here so build_discovery_map's
# reset (DISCOVERY=()) operates on a global, not a function-local copy.
DISCOVERY=()

# --- Helpers ------------------------------------------------------------------

# Emit a violation line and bump the per-file + global counters.
# Args: <line-number-or-dash> <message>
violation() {
  local ln="$1"; shift
  FILE_VIOLATIONS=$((FILE_VIOLATIONS + 1))
  if [ "$ln" = "-" ]; then
    printf '  %sVIOLATION%s %s\n' "$C_RED" "$C_RST" "$*"
  else
    printf '  %sVIOLATION%s L%s: %s\n' "$C_RED" "$C_RST" "$ln" "$*"
  fi
}

# Emit a warning line (does not fail the build).
warning() {
  local ln="$1"; shift
  FILE_WARNINGS=$((FILE_WARNINGS + 1))
  if [ "$ln" = "-" ]; then
    printf '  %sWARN%s      %s\n' "$C_YEL" "$C_RST" "$*"
  else
    printf '  %sWARN%s      L%s: %s\n' "$C_YEL" "$C_RST" "$ln" "$*"
  fi
}

# grep that never aborts the script when there are no matches.
g() { grep "$@" || true; }

# Print "L<n>: <trimmed line>" matches for a fixed-string pattern.
# Args: <file> <fixed-pattern>
matches_fixed() {
  g -nF -- "$2" "$1"
}

# Print matches for an extended-regex pattern.
# Args: <file> <ere-pattern>
matches_ere() {
  g -nE -- "$2" "$1"
}

# Determine, for a given 1-based line number in a file, whether that line sits
# inside a ```! discovery (bash) block. Echoes "yes" or "no".
# We pre-compute the set of in-discovery line numbers per file once.
build_discovery_map() {
  # Populates the global array DISCOVERY[<lineno>]=1 for lines inside ```! ... ```
  local file="$1" n=0 in_disc=0 line
  DISCOVERY=()
  while IFS= read -r line || [ -n "$line" ]; do
    n=$((n + 1))
    if [ "$in_disc" -eq 0 ]; then
      # opening fence of a discovery block: ```!  (allow leading spaces)
      if printf '%s' "$line" | grep -qE '^[[:space:]]*```!'; then
        in_disc=1
        DISCOVERY[$n]=1            # the fence line itself counts as in-block
        continue
      fi
    else
      DISCOVERY[$n]=1
      # closing fence: a line that is exactly ``` (allow leading spaces)
      if printf '%s' "$line" | grep -qE '^[[:space:]]*```[[:space:]]*$'; then
        in_disc=0
      fi
    fi
  done < "$file"
}

in_discovery() {
  # Args: <lineno> -> exit 0 if inside a discovery block
  [ "${DISCOVERY[$1]:-0}" = "1" ]
}

# A hardcoded-token match is NOT a real violation when the line is:
#   (a) inside a ```! discovery block (legitimate footprint scan), or
#   (b) discussing config — it contains a <paths.*>/<tooling.*>/<stack.*>/<ci.*>
#       /<gates*>/<risk_areas*>/<test_data*>/<process*> placeholder, or
#   (c) an anti-hardcoding instruction or a stated default/fallback
#       ("never hardcode `tests/`", "default `docs/qa/`", "resolve from ...").
# Args: <lineno> <line-text> -> exit 0 (excluded) / 1 (real candidate)
line_excluded() {
  local ln="$1" text="$2"
  in_discovery "$ln" && return 0
  printf '%s' "$text" | grep -qiE '<(paths|tooling|stack|ci|gates|risk_areas|test_data|process)[._> ]' && return 0
  printf '%s' "$text" | grep -qiE 'hardcod|no (literal|fixed)|not the literal|resolve from|default|unset|fall ?back|discovery|informational' && return 0
  return 1
}

# --- Main loop ----------------------------------------------------------------
for file in "${FILES[@]}"; do
  TOTAL_FILES=$((TOTAL_FILES + 1))
  base="$(basename "$file")"
  FILE_VIOLATIONS=0
  FILE_WARNINGS=0

  # Pre-compute discovery-block line map for this file.
  # DISCOVERY is a plain indexed array keyed by line number (bash 3.2 friendly);
  # build_discovery_map resets it.
  build_discovery_map "$file"

  printf '%s%s%s\n' "$C_BOLD" "$base" "$C_RST"

  # Whole-file content (for "does it write files?" / heading checks).
  content="$(cat "$file")"

  # Does this command write a work product to a <paths.*> location?
  # Match common write phrasings + the placeholder, OR a direct "to `<paths...".
  WRITES_DOC=0
  if printf '%s' "$content" | grep -qiE '(write|output|produce|save|generate)[^`]*`?<paths\.' \
     || printf '%s' "$content" | grep -qiE 'to `<paths\.'; then
    WRITES_DOC=1
  fi

  # =====================================================================
  # RULE 1 — HARDCODED PATHS / TOOLS
  # =====================================================================

  # 1a. literal docs/qa/  (should be <paths.docs_dir>)
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"; text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    violation "$ln" "hardcoded 'docs/qa/' — use <paths.docs_dir>"
  done < <(matches_fixed "$file" 'docs/qa/')

  # 1b. literal playwright-report  (build artifact dir)
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"; text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    violation "$ln" "hardcoded 'playwright-report' — derive from <tooling.*>/config, don't pin the path"
  done < <(matches_fixed "$file" 'playwright-report')

  # 1c. literal test-results/
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"; text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    violation "$ln" "hardcoded 'test-results/' — derive from config, don't pin the path"
  done < <(matches_fixed "$file" 'test-results/')

  # 1d. unrendered template tokens {{vitest / {{jest
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"; text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    violation "$ln" "tooling token '{{vitest|{{jest' — resolve via <tooling.unit>, not a raw mustache token"
  done < <(matches_ere "$file" '\{\{(vitest|jest)')

  # 1e. 'npx playwright' NOT immediately preceded by a config placeholder.
  #     Allowed form: a <tooling.*>/<stack.*>/<paths.*> placeholder right before it.
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"
    text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    # Allowed if the token immediately before 'npx playwright' is a placeholder,
    # e.g. "<tooling.e2e> npx playwright" or "`<tooling.run>` npx playwright".
    if printf '%s' "$text" | grep -qE '<(tooling|stack|paths)\.[^>]*>`?[[:space:]]*npx playwright'; then
      :   # placeholder-prefixed -> allowed
    else
      violation "$ln" "'npx playwright' is hardcoded — prefix with a <tooling.*> run placeholder"
    fi
  done < <(matches_fixed "$file" 'npx playwright')

  # 1f. bare 'tests/' path that is NOT part of <paths.tests_dir>.
  #     We allow the placeholder <paths.tests_dir>. Flag literal tests/ uses.
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"
    text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    # Strip out the allowed placeholder so it can't trigger the match.
    stripped="${text//<paths.tests_dir>/}"
    # After stripping the placeholder, is there still a bare tests/ token?
    # Require a word boundary so 'subtests/' or 'requests/' don't match, and
    # ignore occurrences that are clearly part of another placeholder token.
    if printf '%s' "$stripped" | grep -qE '(^|[^A-Za-z0-9._/<-])tests/'; then
      violation "$ln" "bare 'tests/' path — use <paths.tests_dir>"
    fi
  done < <(matches_ere "$file" '(^|[^A-Za-z0-9._-])tests/')

  # 1g. openapi.yaml|json allowed ONLY inside a ```! discovery block.
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    ln="${m%%:*}"; text="${m#*:}"
    line_excluded "$ln" "$text" && continue
    violation "$ln" "'openapi.(yaml|json)' outside a \`\`\`! discovery block — use <stack.api_spec_path>"
  done < <(matches_ere "$file" 'openapi\.(yaml|json)')

  # =====================================================================
  # RULE 2 — MISSING SELF-CHECK (only relevant if the file writes a doc)
  # =====================================================================
  if [ "$WRITES_DOC" -eq 1 ]; then
    # Accept any heading level, optional "N." numbering, and the advisory
    # variants used by read-mostly commands (Residual-risk / Quality gate).
    if printf '%s' "$content" | grep -qiE '^#+[[:space:]]*([0-9]+\.[[:space:]]*)?(Self-check|Residual.risk|Quality (gate|check))'; then
      :   # has a self-check / residual-risk heading
    else
      violation "-" "writes a file to <paths.*> but has no '## Self-check' (or Residual-risk) heading"
    fi
  fi

  # =====================================================================
  # RULE 3 — MISSING TEMPLATE REFERENCE (warn, only if it writes a doc)
  # =====================================================================
  if [ "$WRITES_DOC" -eq 1 ]; then
    if printf '%s' "$content" | grep -qF '${CLAUDE_PLUGIN_ROOT}/templates/'; then
      :   # references a template
    else
      warning "-" "produces a work product but does not reference \${CLAUDE_PLUGIN_ROOT}/templates/"
    fi
  fi

  # =====================================================================
  # RULE 4 — FRONTMATTER
  # =====================================================================
  # Extract the frontmatter block (between the first two '---' lines).
  frontmatter="$(awk 'NR==1 && $0=="---"{f=1; next} f && $0=="---"{exit} f{print}' "$file")"

  if [ -z "$frontmatter" ]; then
    violation "-" "missing YAML frontmatter (--- block) at top of file"
  else
    # 4a. description: line required
    if ! printf '%s\n' "$frontmatter" | grep -qE '^description:[[:space:]]*[^[:space:]]'; then
      violation "-" "frontmatter missing a non-empty 'description:' line"
    fi
    # 4b. if it writes files, allowed-tools must include Write
    if [ "$WRITES_DOC" -eq 1 ]; then
      if printf '%s\n' "$frontmatter" | grep -qE '^allowed-tools:.*\bWrite\b'; then
        :
      else
        violation "-" "writes files but 'allowed-tools:' does not include Write"
      fi
    fi
  fi

  # --- per-file summary -------------------------------------------------------
  if [ "$FILE_VIOLATIONS" -eq 0 ]; then
    PASS_FILES=$((PASS_FILES + 1))
    if [ "$FILE_WARNINGS" -eq 0 ]; then
      printf '  %sPASS%s\n' "$C_GRN" "$C_RST"
    else
      printf '  %sPASS%s %s(%d warning(s))%s\n' "$C_GRN" "$C_RST" "$C_DIM" "$FILE_WARNINGS" "$C_RST"
    fi
  else
    printf '  %s%d violation(s)%s%s\n' "$C_RED" "$FILE_VIOLATIONS" "$C_RST" \
      "$( [ "$FILE_WARNINGS" -gt 0 ] && printf ', %d warning(s)' "$FILE_WARNINGS" )"
  fi

  TOTAL_VIOLATIONS=$((TOTAL_VIOLATIONS + FILE_VIOLATIONS))
  TOTAL_WARNINGS=$((TOTAL_WARNINGS + FILE_WARNINGS))
done

# --- Final totals -------------------------------------------------------------
echo
printf '%s%s%s\n' "$C_BOLD" "────────────────────────────────────────────" "$C_RST"
printf '%sTotals:%s %d files scanned, %d passing, %d violation(s), %d warning(s)\n' \
  "$C_BOLD" "$C_RST" "$TOTAL_FILES" "$PASS_FILES" "$TOTAL_VIOLATIONS" "$TOTAL_WARNINGS"

if [ "$TOTAL_VIOLATIONS" -gt 0 ]; then
  exit 1
fi
exit 0
