---
description: Produce an ISTQB Test Status (Progress) Report for an in-flight release — monitoring metrics and control recommendations against the plan. Use during a sprint/release to report testing progress.
argument-hint: "<release-id>"
allowed-tools: Read, Glob, Grep, Bash
---

# Test Status Report: $ARGUMENTS

**ISTQB process:** Test monitoring & control (CTFL v4.0 §5.3). Distinct from the end-of-test Completion Report.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Current results
```!
echo "--- junit/results ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports playwright-report 2>/dev/null
```

## Your task

Release from `$ARGUMENTS`. If empty, ask. Pull `TEST-PLAN-<release>.md` from `paths.docs_dir` for the plan baseline.

1. **Monitor** — gather ISTQB-standard progress metrics from available results (mark anything unavailable as "unknown", never fabricate):
   - **Test-case progress:** planned / designed / implemented / executed / passed / failed / blocked.
   - **Defect metrics:** new/open/closed by severity; defect density / trend.
   - **Coverage:** of requirements (test basis) and of risk (`risk_areas`).
   - **Entry/exit-criteria status** against the plan's `gates`.
2. **Control** — recommend corrective actions for deviations (slipping coverage, blocking defects, environment issues, rising flakiness → `/qa:flaky-hunt`).
3. Output a **Test Status Report** (ISO 29119-3): reporting period, progress vs plan, metrics tables, risks/blockers, and control recommendations with owners. Write to `<paths.docs_dir>/STATUS-REPORT-<release>-<date>.md`.

Be factual and progress-focused. For the final ship/hold decision use `/qa:release-report`.
