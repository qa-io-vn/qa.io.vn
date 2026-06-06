---
description: Run a formal release readiness (go/no-go) review — consolidate all quality signals into a documented ship/hold decision with conditions, residual risk, and stakeholder sign-off. Use at the release gate.
argument-hint: "<release-id>"
allowed-tools: Read, Glob, Grep, Bash
---

# Release go/no-go review: $ARGUMENTS

**ISTQB process:** Release decision against **exit criteria** + risk (CTFL §5.1; CTAL-TM). Consolidates the Test Completion Report into a cross-functional decision; complements `/qa:release-report`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Signals
```!
echo "--- docs ---"; ls -1 docs/qa/RELEASE-REPORT-*.md docs/qa/TEST-PLAN-*.md 2>/dev/null
echo "--- results ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports 2>/dev/null
```

## Your task

Release from `$ARGUMENTS`. If empty, ask. Pull the Test Completion Report (`/qa:release-report`) and Test Plan if present. Produce a **go/no-go decision record** — a governance artifact, not just a test summary.

1. **Consolidate the readiness signals** against the `gates` exit criteria:
   - Test execution: planned/executed/passed, pass rate vs `min_pass_rate_pct`.
   - Open defects by severity; any at `block_on_severity` = blocker.
   - Non-functional gates: performance SLAs, security (high/critical), accessibility (critical/serious).
   - Contract/`can-i-deploy` status; regression result.
   - Residual risk on `risk_areas.critical`.
2. **Readiness scorecard** — each criterion: met / not met / waived, with evidence. RAG-rate overall readiness.
3. **Decision** — **GO**, **NO-GO**, or **GO with conditions** (list the conditions and owners). Be explicit and justify against the criteria; state residual risk plainly (Principle 1 — never "defect-free").
4. **Governance** — rollback plan confirmed, post-deploy verification plan (`/qa:shift-right`), and the **stakeholder sign-off** block (QA Manager, Product Owner, Eng Lead, Release Manager) with any dissent recorded.

Output to `<paths.docs_dir>/GO-NO-GO-<release>.md`. If any blocker is open, default to NO-GO or GO-with-conditions — don't rubber-stamp. Read-only.
