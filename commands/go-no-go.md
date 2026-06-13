---
description: Run a formal release readiness (go/no-go) review — consolidate all quality signals into a documented ship/hold decision with conditions, residual risk, and stakeholder sign-off. Use at the release gate.
argument-hint: "<release-id>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Release go/no-go review: $ARGUMENTS

**ISTQB process:** Release decision against **exit criteria** + residual risk — test monitoring, control & exit-criteria evaluation (CTFL v4.0 §5.3; CTAL-TM release-decision practice). This is a cross-functional **governance decision record** built on top of the ISO/IEC/IEEE 29119-3 **Test Completion Report** (`/qa:release-report`) and **Test Status Report** (`/qa:status-report`); it does not replace them. Verify any section number against the current syllabus before quoting it externally.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Signals (discovery)
```!
echo "--- decision inputs (release report / test plan) ---"; find . \( -name "RELEASE-REPORT-*.md" -o -name "STATUS-REPORT-*.md" -o -name "TEST-PLAN-*.md" \) 2>/dev/null | head
echo "--- results ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1d ./*report* ./reports ./test-results 2>/dev/null
```

## Your task

Produce a **go/no-go decision record** — a governance artifact, not just a test summary. Be explicit, measurable, and traceable; never rubber-stamp.

**Config guard:** if `qa.config.yml` printed "none" above, state that defaults are assumed, recommend `/qa:qa-init`, and proceed with conservative gate thresholds. Otherwise read `paths.*`, `gates`, `tooling.*` toggles, and `risk_areas` from it and honor them — never hardcode paths, tools, or thresholds.

**Resolve the release (handle empty `$ARGUMENTS`):**
1. If `$ARGUMENTS` is non-empty, use it as the release ID.
2. If `$ARGUMENTS` is empty, ask the user for the release ID. If no answer is given, default the scope to the in-flight work touching `risk_areas.critical`, label the record `GO-NO-GO-current-<date>`, and state this assumption at the top of the record.

**Consolidate inputs (do not re-derive — pull from the sibling reports):**
3. Read the matching `RELEASE-REPORT-<release>.md` (Test Completion Report, from `/qa:release-report`) and, if present, the latest `STATUS-REPORT-<release>.md` (from `/qa:status-report`) and `TEST-PLAN-<release>.md` from `<paths.docs_dir>`. If a report is missing, record it as a gap and treat its gates as **not met / unknown** — never fabricate numbers.

**Evaluate each gate against `gates` exit criteria. Use this deterministic decision table — each criterion is `met` / `not met` / `waived` (waived requires a named approver + reason):**

| # | Gate criterion | Source | Decision rule |
|---|---|---|---|
| G1 | Test execution & pass rate | release/status report | `met` if pass rate ≥ `gates.min_pass_rate_pct` and 0 blocked-must-run cases; else `not met` |
| G2 | Open defects by severity | triage / release report | `met` if 0 open defects at `gates.block_on_severity` or above; any such open defect → `not met` (blocker) |
| G3 | Performance SLAs | `<paths.reports_dir>` / release report | `met` if p95/error-rate within `gates` perf thresholds; missing run → `not met / unknown` |
| G4 | Security | release report | `met` if 0 high/critical findings (per `gates`); else `not met` |
| G5 | Accessibility | release report | `met` if 0 critical/serious violations (per `gates`); else `not met` |
| G6 | Contract / `can-i-deploy` | broker / release report | `met` only if green; red or unknown → `not met` |
| G7 | Regression | release report / CI | `met` if regression suite passed at required scope; else `not met` |
| G8 | Residual risk on `risk_areas.critical` | risk register | `met` if accepted with documented mitigation/owner; otherwise `not met` |

4. **Readiness scorecard** — render the table above with the actual met/not-met/waived state, the measured value, and the evidence source for each gate. Report counts, not prose claims.
5. **Aggregate decision rule (deterministic):**
   - **NO-GO** if any gate marked a **blocker** is `not met` (default blockers: G2, G6; plus any gate listed under `gates.block_on_severity`/critical config).
   - **GO with conditions** if all blocker gates are `met` but one or more non-blocker gates are `not met` or `waived` — list each condition, its owner, and its due date.
   - **GO** only if every in-scope gate is `met` (or `waived` with a recorded approver + reason).
   - When in doubt, default to the more conservative outcome. State residual risk plainly (Principle 1 — never "defect-free").
6. **Governance block:** confirm the rollback plan, the post-deploy verification plan (`/qa:shift-right`), and a **stakeholder sign-off** table (QA Manager, Product Owner, Eng Lead, Release Manager) with name, role, decision (approve/dissent), and date. Record any dissent verbatim.

**Output:** a Release Go/No-Go Decision Record — a governance extension of the ISO/IEC/IEEE 29119-3 **Test Completion Report** (no dedicated 29119-3 template; see `/qa:release-report` for the closest work product). Write it to `<paths.docs_dir>/GO-NO-GO-<release>.md`. Modify nothing except this decision record.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; no paths, tools, or thresholds are hardcoded.
- [ ] **Traceability intact** — each gate row links back to its evidence source (release report / status report / risk register); no decision asserted without a cited signal, and "unknown" sources are flagged rather than assumed met.
- [ ] **Measurable** — the scorecard states counts/values per gate (pass rate, open-blocker count, p95, finding counts) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why, and the accepted risk on `risk_areas.critical` with owner (ISTQB Principle 1 — never "defect-free").
- [ ] **Decision rule applied** — the GO / GO-with-conditions / NO-GO outcome follows the aggregate rule in step 5; any blocker `not met` forces NO-GO (or GO-with-conditions), never a rubber-stamp.
- [ ] **Work product named** — output is identified as the Release Go/No-Go Decision Record (governance extension of the 29119-3 Test Completion Report) and written to `<paths.docs_dir>/GO-NO-GO-<release>.md`.
