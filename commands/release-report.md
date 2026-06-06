---
description: Produce the ISTQB Test Completion Report (test summary) for a release against its exit criteria, with residual risk and a ship/hold recommendation. Use at the end of a release.
argument-hint: "<release-id>"
allowed-tools: Read, Glob, Grep, Bash
---

# Test Completion Report: $ARGUMENTS

**ISTQB process:** Test completion (CTFL v4.0 §1.4; ISO/IEC/IEEE 29119-3 Test Completion Report). Evaluate exit criteria, state residual risk (Principle 1), and capture lessons learned.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Latest results
```!
echo "--- junit / reports ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports 2>/dev/null
echo "--- playwright report ---"; ls -1 playwright-report 2>/dev/null
```

## Your task

Release ID from `$ARGUMENTS`. If empty, ask. Pull the matching `TEST-PLAN-<release>.md` from `paths.docs_dir` if present.

1. Gather available results: pass/fail counts, regression status, K6 p95/error-rate, security findings by severity, a11y violations, and `can-i-deploy` status. Where a result isn't available, mark it clearly as "not run / unknown" — never fabricate numbers.
2. Evaluate against the **exit criteria** built from `gates` (min pass rate, no open `block_on_severity`, perf SLAs, security/a11y blockers, can-i-deploy green).
3. Produce a **Test Completion Report**: test-case results (planned/executed/passed/failed/blocked), pass rate, open defects by severity, regression result, performance, security, accessibility, can-i-deploy, **exit-criteria evaluation** against `gates`, an explicit **residual-risk statement** (never claim defect-free — Principle 1), **lessons learned**, and a clear **Ship / Hold recommendation** justified by the gates.
4. Write it to `<paths.docs_dir>/RELEASE-REPORT-<release>.md` and include the approvals block from the plan.

Be honest about gaps — a "Hold" with reasons is more useful than an unsupported "Ship".
