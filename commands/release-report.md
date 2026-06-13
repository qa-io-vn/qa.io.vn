---
description: Produce the ISO/IEC/IEEE 29119-3 Test Completion Report for a release — evaluate every quality gate, state residual risk, and give a deterministic Ship/Hold recommendation. Use at the end of a release.
argument-hint: "<release-id>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Test Completion Report: $ARGUMENTS

**ISTQB process:** Test completion / closure (CTFL v4.0 §1.4 — the seventh test-process activity; CTAL-TM Test Closure). **Work product:** ISO/IEC/IEEE 29119-3 **Test Completion Report** (a.k.a. test summary report). Evaluate exit criteria against `gates`, state residual risk (Principle 1 — testing shows the presence, not the absence, of defects), and make a Ship/Hold recommendation. Verify any syllabus section against the current ISTQB syllabus before asserting it.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "NO_CONFIG"
```

## Latest results (discovery — paths are illustrative; bind to config below)
```!
echo "--- junit / xml results ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head
echo "--- report dirs ---"; ls -1 reports 2>/dev/null; ls -1 test-results 2>/dev/null; ls -1 playwright-report 2>/dev/null
echo "--- prior plan / report ---"; ls -1 docs/qa/TEST-PLAN-*.md docs/qa/RELEASE-REPORT-*.md 2>/dev/null
```

## Your task

**Config guard.** If the config block above is `NO_CONFIG`, stop and tell the user to run `/qa:qa-init` first — every threshold, path, and tooling toggle below comes from `qa.config.yml`. Do not hardcode paths, tools, or thresholds; read them from config. The discovery listing above is illustrative only — resolve actual locations from `<paths.reports_dir>` / `<paths.docs_dir>` and the enabled `<tooling.*>`.

**Resolve the release.** Take the release ID from `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask the user for the release ID (do not guess); if they decline, scope the report to the `risk_areas.critical` areas for the most recent build and label it provisional. Pull the matching `TEST-PLAN-<release>.md` from `<paths.docs_dir>` if present — its Definition of Done is the source of the exit criteria.

Work through these steps in order:

1. **Gather results (config-driven, conditional on enabled tooling).** Collect only what the project's `<tooling.*>` toggles enable, from `<paths.reports_dir>`:
   - Test execution counts by level/type (planned / executed / passed / failed / blocked) for each enabled level: `<tooling.unit>`, `<tooling.component>`, `<tooling.api>`, `<tooling.e2e>`, `<tooling.contract>`.
   - Open defects by severity (aligned to `gates.block_on_severity`).
   - Regression result.
   - If `<tooling.performance>` is set: p95 / p99 / error-rate / RPS from the perf run.
   - If any `<tooling.security.*>` is set: findings by severity.
   - If `<tooling.accessibility>` is set: violations by impact.
   - `can-i-deploy` status (e.g. from `<tooling.contract>` broker), if contract testing is enabled.
   For any measure whose tool is `none`/disabled or whose result is missing, mark it **"not run / unknown"** — never fabricate a number. A "not run" on a blocking measure is itself a gate risk.

2. **Evaluate exit criteria against `gates`.** Build the exit-criteria table from the Test Plan's Definition of Done, with each row resolving to **PASS** or **FAIL** by an explicit rule:
   - **Pass rate** — PASS iff overall pass rate ≥ `gates.min_pass_rate_pct`%.
   - **Blocking defects** — PASS iff **zero** open defects at any severity in `gates.block_on_severity`.
   - **Performance** — PASS iff every `gates.performance` SLA is met (checkout p95 ≤ `gates.performance.checkout_p95_ms`, p99 ≤ `gates.performance.p99_ms`, error-rate ≤ `gates.performance.error_rate_pct`%, RPS ≥ `gates.performance.target_rps`). If `<tooling.performance>` is `none`, mark "not run" and treat as a FAIL unless the Test Plan explicitly waives it.
   - **Security** — PASS iff no finding at or above any level in `gates.security_block_on`.
   - **Accessibility** — PASS iff no violation at any impact in `gates.a11y_block_on` (standard `gates.accessibility_standard`).
   - **Coverage** — PASS iff 100% of `risk_areas.critical` and `risk_areas.high` are covered.
   - **can-i-deploy** — PASS iff green.

3. **Produce the Test Completion Report** following `${CLAUDE_PLUGIN_ROOT}/templates/completion-report-template.md`, with: document control + approvals (from `team`), executive summary (counts, not adjectives), §2 exit-criteria evaluation (from step 2), test-execution results table (planned/executed/passed/failed/blocked + pass rate, by enabled level), defect summary by severity, non-functional results vs SLAs (perf / security / a11y rows only for enabled tooling), an explicit **residual-risk statement** (deferred defects, descoped areas, "not run" measures, accepted Low-tier risks — Principle 1, never claim defect-free), **traceability** confirmation (test basis → condition → case → coverage item → procedure → result → defect, no orphans), **lessons learned**, and the Ship/Hold recommendation.

4. **Apply the Ship/Hold decision rule (deterministic).** Recommend **SHIP** only when **all** of: pass rate ≥ `gates.min_pass_rate_pct`%, **zero** open defects at `gates.block_on_severity`, every §5 non-functional row PASS against `gates`, every `risk_areas.critical`/`high` area covered, and `can-i-deploy` green. If **any** of these FAIL → **HOLD** (or SHIP-with-conditions only when the failing gate is explicitly waived in the Test Plan and the accepted residual risk is documented and signed off). For each FAIL, name the exact gate, the current value vs threshold, and the owner who must clear it. A justified "Hold" beats an unsupported "Ship".

5. **Write the report** to `<paths.docs_dir>/RELEASE-REPORT-<release>.md` and include the approvals block from the plan. Reference raw evidence (execution logs in `<paths.reports_dir>`) rather than copying it.

## Routing
- Hand the decision to `/qa:go-no-go` for the cross-functional release record (this report is its primary input).
- In-cycle progress (not the final verdict) belongs in `/qa:status-report`.
- Open defects → `/qa:triage`; flaky-test noise inflating failures → `/qa:flaky-hunt`.
- can-i-deploy / contract status comes from `/qa:contract-sync`; perf from `/qa:perf-test`; a11y from `/qa:a11y-audit`; security from `/qa:security-scan`; maintenance changes from `/qa:maintenance-test`.
- Post-deploy verification of the residual risk → `/qa:shift-right`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`, `team`) is honored; no path, tool, or threshold hardcoded; disabled tooling produces "not run", not a fabricated number.
- [ ] **Gates fully evaluated** — every gate (`min_pass_rate_pct`, `block_on_severity`, `performance`, `security_block_on`, `a11y_block_on`, coverage, `can-i-deploy`) resolves to an explicit PASS/FAIL, and the Ship/Hold recommendation follows the decision rule in step 4 with no FAIL silently ignored.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; every blocking defect traces to a failed result and a risk; no orphans.
- [ ] **Measurable** — output states counts/coverage/pass rates rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why, including "not run" measures and deferred defects (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Completion Report and written to `<paths.docs_dir>/RELEASE-REPORT-<release>.md`.
