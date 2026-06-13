---
description: Produce an ISTQB Test Status (Progress) Report for an in-flight release — monitoring metrics and control recommendations against the plan. Use during a sprint/release to report testing progress.
argument-hint: "<release-id>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Test Status Report: $ARGUMENTS

**ISTQB process:** Test monitoring & control (CTFL v4.0 §5.3). Distinct from the end-of-test Completion Report.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Current results
```!
echo "--- junit/results ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head
echo "--- report/artifact dirs ---"; ls -1d ./*report* ./reports ./test-results 2>/dev/null
```

## Your task

**Config guard:** if `qa.config.yml` is absent (printed "none" above), state that defaults are assumed and recommend `/qa:qa-init`; otherwise read `paths.*`, `gates`, and `risk_areas` from it and honor them — never hardcode paths, tools, or thresholds.

**Resolve the release (handle empty `$ARGUMENTS`):**
1. If `$ARGUMENTS` is non-empty, use it as the release ID.
2. If `$ARGUMENTS` is empty, ask the user for the release ID. If no answer is given, default the scope to the in-flight work touching `risk_areas.critical` and label the report `STATUS-REPORT-current-<date>`.
3. Pull `TEST-PLAN-<release>.md` from `<paths.docs_dir>` for the plan baseline. If no plan is found, note that progress is reported without a baseline (deviations cannot be computed) and proceed.

**1. Monitor** — gather ISTQB-standard progress metrics from available results. Mark anything unavailable as "unknown / not run"; never fabricate numbers or infer pass rates from absent data.
   - **Test-case progress:** planned / designed / implemented / executed / passed / failed / blocked (counts).
   - **Pass rate:** passed ÷ executed, as a percentage.
   - **Defect metrics:** new / open / closed by severity (aligned to `gates.block_on_severity`); defect density / trend.
   - **Coverage:** of requirements (test basis) and of risk areas (`risk_areas`, critical → high → medium), as a percentage.
   - **Entry/exit-criteria status** against the plan's `gates`.

**2. Control** — for each deviation from plan, recommend a corrective action with a named owner and target date. Decision rules:
   - Blocking defect open at a `gates.block_on_severity` level → control action to triage/fix → route to `/qa:triage`.
   - Coverage of any `risk_areas.critical` area below 100% → action to close the gap, prioritized critical → high.
   - Rising flakiness / unstable suite → route to `/qa:flaky-hunt`.
   - Environment or pipeline blockage → route to `/qa:fix-ci`.

**3. Escalate** — assign an overall status using these thresholds (evaluate top-down; first match wins):
   - **RED (escalate now):** any open defect at a `gates.block_on_severity` level, **OR** pass rate < (`gates.min_pass_rate_pct` − 5), **OR** requirement/risk coverage < 50%.
   - **YELLOW (at risk):** pass rate < `gates.min_pass_rate_pct` (but ≥ threshold − 5), **OR** any `risk_areas.critical` area < 100% covered, **OR** one or more entry/exit `gates` not yet met.
   - **GREEN (on track):** pass rate ≥ `gates.min_pass_rate_pct`, zero open defects at `gates.block_on_severity`, all `risk_areas.critical` covered, and all in-scope `gates` met.
   State the matched color, the rule that triggered it, and the metric values behind it.

**4. Output** — produce a **Test Status (Progress) Report** — the ISO/IEC/IEEE 29119-3 *Test Status Report* work product (no dedicated template; mirror the structure of `templates/completion-report-template.md` for the metrics tables). Include: reporting period, overall RED/YELLOW/GREEN status, progress vs plan, metrics tables (test-case progress, defects by severity, coverage), risks/blockers, and control recommendations with owners and dates. Write to `<paths.docs_dir>/STATUS-REPORT-<release>-<date>.md`.

Be factual and progress-focused — report counts and percentages, not prose claims. This report monitors an in-flight release; for the final ship/hold decision use `/qa:release-report`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.*`, `gates` (`min_pass_rate_pct`, `block_on_severity`), and `risk_areas` are read from `qa.config.yml` and honored; no path, tool, or threshold is hardcoded.
- [ ] **No fabrication** — every metric is sourced from real results or marked "unknown / not run"; pass rate is computed only from actual executed counts (Principle 1).
- [ ] **Measurable** — output states counts and percentages, not prose claims; pass rate, coverage %, and defect counts are explicit.
- [ ] **Status justified** — the RED/YELLOW/GREEN color names the triggering rule and the metric values behind it.
- [ ] **Control actionable** — every deviation has a corrective action with a named owner and date; flakiness/CI/defect items route to the correct sibling command.
- [ ] **Work product named & located** — output is identified as the ISO/IEC/IEEE 29119-3 Test Status Report and written to `<paths.docs_dir>/STATUS-REPORT-<release>-<date>.md`.
