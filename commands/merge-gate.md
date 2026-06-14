---
description: Evaluate a pull request against the project's quality gates — CI/checks status, pass rate, coverage, severity blockers, and security/a11y/perf gates — and produce a documented merge / hold decision with conditions and residual risk. A change-scoped go/no-go. Never merges automatically. Use to decide whether a PR is safe to merge.
argument-hint: "[PR number | PR URL | branch] (optional — defaults to the current branch's PR)"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Merge gate — evaluate a PR against the quality gates

**ISTQB process:** **Exit-criteria evaluation** against the configured `gates` + residual-risk statement → a documented merge decision (CTFL v4.0 §5.3 test monitoring, control & exit criteria; release-decision practice per CTAL-TM — verify section numbers against the current syllabus). This is **go/no-go at PR (change) scope** — it complements, and never replaces, the release-level `/qa:go-no-go` or the ISO/IEC/IEEE 29119-3 **Test Completion Report** (`/qa:release-report`). The decision states residual risk rather than claiming none (Principle 1).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## PR signals (discovery)
```!
ARG="$ARGUMENTS"
if command -v gh >/dev/null 2>&1; then
  if echo "$ARG" | grep -qE '^[0-9]+$|^https?://'; then SEL="$ARG"; else SEL=""; fi
  echo "--- PR summary ---"; gh pr view $SEL --json number,title,state,mergeable,reviewDecision,baseRefName,headRefName,url 2>/dev/null || echo "gh pr view failed (no PR for this branch?)"
  echo "--- checks / CI status ---"; gh pr checks $SEL 2>/dev/null | head -40 || echo "no checks reported"
else
  echo "gh CLI not found — supply CI status / coverage manually, or run from a branch with a PR."
fi
REPORTS=$(grep -E '^\s*reports_dir:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*reports_dir:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
echo "--- local quality signals (discovery) ---"; ls -1 "${REPORTS:-reports}" 2>/dev/null | head; ls -1 "${REPORTS:-reports}/defects" 2>/dev/null | head
```

## Your task

> **Config-read guard.** Read `qa.config.yml` first. If it is `none`/missing, tell the user to run `/qa:qa-init`, or proceed with explicit, stated assumptions. The gate thresholds come **entirely** from `gates` (and `risk_areas.*` for severity mapping); resolve `<paths.reports_dir>` and `<tooling.*>` from config — **never hardcode** a threshold, path, or tool.

Goal: decide whether this PR clears the configured quality gates, and record the decision — **never merge automatically**; this command produces a recommendation/record, the human merges.

1. **Resolve the PR.** A PR number/URL in `$ARGUMENTS`, else the current branch's PR (via `gh`); if none is reachable, ask the user to supply the PR or the signals below.

2. **Gather the signals.** From `gh pr checks`/`gh pr view` and the local reports under `<paths.reports_dir>`: CI/checks status, pass rate, coverage (and delta vs base), open defects by **severity** touching the change, and security / accessibility / performance gate results where available.

3. **Evaluate each configured gate** from `gates`, marking each **PASS / FAIL / N-A** with the evidence:
   - `min_pass_rate_pct` — measured pass rate ≥ threshold.
   - `block_on_severity` — no open defect at a blocking severity (severity is impact on the test object; keep it independent of priority).
   - **coverage** — meets the configured/threshold coverage; flag a negative delta.
   - `security_block_on` / `a11y_block_on` — no findings at/above the blocking level.
   - **performance** SLAs (`gates.performance.*`) — thresholds met where the change touches a measured path.

4. **Decide.** Exactly one verdict, naming the driver:
   - **MERGE** — all applicable gates PASS.
   - **MERGE WITH CONDITIONS** — gates pass but residual risk / follow-ups are noted.
   - **HOLD** — a gate FAILS; name it. Route severity blockers to `/qa:triage`, coverage holes to `/qa:review-coverage`, flakiness to `/qa:flaky-hunt`.

## Output — merge gate decision record

Write the decision to `<paths.reports_dir>/MERGE-GATE-<id>-<date>.md` using `${CLAUDE_PLUGIN_ROOT}/templates/completion-report-template.md` as the field guide (change-scoped). Include:
- **PR identity** — number/branch, base, state.
- **Gate evaluation table** — each `gates` item: threshold · measured · PASS/FAIL/N-A · evidence.
- **Decision** — MERGE / MERGE WITH CONDITIONS / HOLD, naming the driving gate.
- **Conditions** — what must be true to merge (if conditional).
- **Residual risk** — what remains uncovered even if merged (Principle 1).
- **Routing & sign-off** — handoffs issued; a sign-off line (the human approves the merge).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every threshold comes from `gates` (and `risk_areas.*`); `<paths.reports_dir>` / `<tooling.*>` resolved from config; nothing hardcoded.
- [ ] **Every gate evaluated** — each `gates` item is marked PASS/FAIL/N-A **with evidence** (counts, status, %), not prose; missing signals are flagged as N-A, not assumed PASS.
- [ ] **Severity ≠ priority** — blocker evaluation uses severity (impact on the test object); priority is not conflated with it.
- [ ] **Decision traceable** — the verdict names the gate(s) that drive it; residual risk is stated (Principle 1); blockers/coverage/flakiness are routed to `/qa:triage` / `/qa:review-coverage` / `/qa:flaky-hunt`.
- [ ] **No auto-merge** — the command records a recommendation only; it does not merge the PR.
- [ ] **Work product named** — output is a **merge gate decision record** (change-scoped, ISO/IEC/IEEE 29119-3 field guide) at `<paths.reports_dir>/MERGE-GATE-<id>-<date>.md`. For release-scope sign-off, use `/qa:go-no-go`; for the full QA review, `/qa:review-pr`.
