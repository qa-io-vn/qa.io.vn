---
description: Analyze a failing test or defect, classify severity/priority, and draft a clear bug report. Use when a test fails for a real reason or the user reports a bug.
argument-hint: "<failure, error, or bug description>"
allowed-tools: Read, Glob, Grep, Bash
---

# Triage: $ARGUMENTS

**ISTQB process:** Defect management (CTFL v4.0 §5.5). Produce a defect report with ISTQB fields; distinguish **severity** (impact on the test object) from **priority** (urgency to fix).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Subject from `$ARGUMENTS` (a failure, stack trace, or bug description). If empty, ask for it.

1. **Investigate**: read the failing test, related source, and any trace/screenshot/log. Determine whether it's a real product defect, a test defect, or environment.
2. **Classify**:
   - Severity (technical impact) using the strategy's scale — S1 blocker / S2 critical / S3 major / S4 minor.
   - Priority (business urgency) considering the affected `risk_areas`.
   - Flag if it hits `gates.block_on_severity` (a release blocker).
3. **Draft a bug report**: title, environment, severity/priority, preconditions, steps to reproduce, expected vs. actual, evidence, suspected root cause/component, and a suggested owner.
4. If it's a real escape, recommend a regression test (offer `/qa:implement` / `/qa:add-test`) so it can't recur. If it's a flaky test, point to `/qa:flaky-hunt`.

Read-only — diagnose and draft; don't change product code.
