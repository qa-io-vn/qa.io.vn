---
description: Define the QA metrics program and produce a cross-release quality dashboard / executive report — trends for escaped defects, coverage, pass rate, MTTR, automation %, flaky rate. Use for management/stakeholder quality reporting.
argument-hint: "[period or release range]"
allowed-tools: Read, Glob, Grep, Bash
---

# Quality dashboard / executive report${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test measurement & reporting at the management level (CTAL-TM). Distinct from `/qa:status-report` (single-release progress) — this is the **cross-release quality posture** for leadership.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Available data
```!
echo "--- results history ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports 2>/dev/null
echo "--- coverage ---"; ls -1 coverage 2>/dev/null
```

## Your task

Period/scope from `$ARGUMENTS` (else recent releases). Build a management quality report. Where data isn't available, mark it "not tracked yet" and recommend capturing it — never fabricate numbers.

1. **Define / confirm the KPI set** (ISTQB-aligned, leadership-relevant):
   - **Effectiveness:** Defect Detection Percentage (escaped vs caught pre-prod), escaped defects per release (trend), defect density, defect removal efficiency.
   - **Coverage:** requirements/risk coverage of critical areas, automation coverage %.
   - **Speed/flow:** MTTD & MTTR for defects, pipeline lead time / feedback time, release frequency.
   - **Stability:** pass-rate trend, flaky-test rate / quarantine size.
   - **Risk posture:** open defects by severity, residual risk on critical areas, security/a11y/perf gate status.
2. **Gather & trend** the metrics over the period from CI results, the defect tracker, and coverage; show direction (improving/declining), not just point values.
3. **Interpret for executives** — what the trends mean for quality and release risk, top 3 concerns, and recommended actions (tie to `/qa:process-improvement`). Keep it concise and non-jargon for stakeholders.
4. **Output** a quality report to `<paths.docs_dir>/QUALITY-REPORT-<period>.md` with a summary scorecard (KPI | current | target | trend | RAG status) and short narrative.

Read-only. For a live, auto-refreshing version, this is a good candidate for a dashboard artifact if the team uses one.
