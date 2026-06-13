---
description: Define the QA metrics program and produce a cross-release quality dashboard / executive report — trends for escaped defects, coverage, pass rate, MTTR, automation %, flaky rate, each mapped to its ISTQB term and ISO/IEC 25010 characteristic. Use for management/stakeholder quality reporting across releases.
argument-hint: "[period or release range]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Quality dashboard / executive report

**ISTQB process:** Test measurement & test reporting at the management level (CTAL-TM metrics & reporting; CTFL v4.0 §5.3 monitoring & metrics — verify section numbering against the current syllabus). This is the **cross-release quality posture** for leadership, aggregating the per-release reports. Distinct from `/qa:status-report` (single in-flight release — Test Status Report) and `/qa:release-report` (end-of-test Test Completion Report). It does **not** replace those 29119-3 work products; it summarizes their metrics over time.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "NO_CONFIG"
```

## Available data
```!
echo "--- results history ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports 2>/dev/null
echo "--- coverage ---"; ls -1 coverage 2>/dev/null
echo "--- prior reports ---"; ls -1 docs 2>/dev/null | grep -iE "STATUS-REPORT|RELEASE-REPORT|QUALITY-REPORT" 2>/dev/null
```

## Your task

**Config guard (do first).** If the config block printed `NO_CONFIG`, do not assume paths or tools. State that `qa.config.yml` is missing, derive `<paths.docs_dir>` / enabled `<tooling.*>` from what the discovery blocks above actually show, and recommend running `/qa:scaffold` to create the config. Otherwise read `paths.*`, the `tooling.*` toggles, `gates`, and `risk_areas` from it and honor them throughout — never hardcode a path or tool name.

**Scope (do second).** Resolve the reporting period from `$ARGUMENTS`.
- If `$ARGUMENTS` is non-empty, use it verbatim as the period/release range.
- If `$ARGUMENTS` is empty, ask the user for the period. If no answer is available, default to the **last 3 releases** found in the prior-reports / results history above; if none exist, default to `risk_areas.critical` as the reporting lens and state that no historical baseline was found.

Build a management quality report. For each metric, **only gather from tooling enabled in `tooling.*`**; for any metric whose source tool is disabled or whose data is absent, mark it `not run` (tool disabled) or `not tracked yet` (enabled but no data) — never fabricate, interpolate, or carry forward a stale number.

1. **Confirm the KPI set** (ISTQB-aligned, leadership-relevant). Build a mapping table so each KPI is traceable to its ISTQB term and the ISO/IEC 25010 quality characteristic it evidences:

   | Metric (KPI) | ISTQB term | ISO/IEC 25010 characteristic | Source (`tooling.*`) |
   |---|---|---|---|
   | Escaped defects / release; Defect Detection Percentage (DDP) | Defect detection percentage; defect escape | Functional suitability | defect tracker |
   | Defect density; defect removal efficiency (DRE) | Defect density | Functional suitability | defect tracker + scope |
   | Requirements / risk coverage of critical areas | Coverage (test basis & risk) | Functional suitability | coverage / `risk_areas` |
   | Automation coverage % | Test automation coverage | Maintainability (of testware) | CI / `tooling.e2e`,`tooling.unit` |
   | MTTD & MTTR for defects | Mean time to detect / repair | Reliability | defect tracker / CI |
   | Pipeline lead / feedback time; release frequency | Test feedback time | (flow metric — no 25010 char.) | CI |
   | Pass-rate trend | Pass/fail ratio | Reliability | CI results |
   | Flaky-test rate / quarantine size | Test flakiness | Reliability (of testware) | `tooling.e2e` / flaky data |
   | Open defects by severity; residual risk on critical areas | Severity; residual risk | (risk posture — cross-characteristic) | defect tracker / `risk_areas` |
   | Security / a11y / perf gate status | Quality gate / exit criteria | Security; Usability; Performance efficiency | `tooling.security`,`tooling.a11y`,`tooling.perf` |

   (Verify the ISO 25010 characteristic names against the current standard; confirm DDP/DRE definitions against the current syllabus rather than asserting a fixed formula.)

2. **Gather & trend** each enabled metric over the period from CI results, the defect tracker, and coverage. For every metric report **direction** (improving / flat / declining) against the prior period, not just a point value. Apply explicit RAG thresholds, overridden by `gates` where the config defines them:
   - **Red:** metric breaches a `gates` threshold, or escaped defects / flaky rate rose ≥ 20% vs prior period, or pass-rate fell below the gate.
   - **Amber:** within 10% of a `gates` threshold, or a 2-period adverse trend with no breach.
   - **Green:** meets target and trend is flat or improving.
   - If no `gates` value exists for a metric, state the target as `unset` and mark RAG `n/a` rather than inventing a threshold.

3. **Interpret for executives** — what the trends mean for quality and release risk: the **top 3 concerns** (each tied to the metric, its trend, and the affected `risk_areas`), and recommended actions. Route systemic/process gaps to `/qa:process-improvement`; route a current ship/hold decision to `/qa:release-report` and in-flight progress to `/qa:status-report`. Keep the narrative concise and non-jargon for stakeholders.

4. **Output** the report to `<paths.docs_dir>/QUALITY-REPORT-<period>.md` containing: the metric→ISTQB-term→ISO 25010 mapping table from step 1, a summary scorecard (`KPI | current | target | trend | RAG status`), the top-3-concerns narrative, and a **residual-risk note** stating which KPIs were `not run`/`not tracked` and what that blinds the report to (ISTQB Principle 1 — testing shows presence, not absence, of defects).

This command is a management summary, not a 29119-3 testware work product itself — it aggregates the per-release Test Status Reports (`/qa:status-report`) and Test Completion Reports (`/qa:release-report`). Do not modify code or tests — the only file you write is the report. For a live, auto-refreshing view this is a good candidate for a dashboard artifact if the team uses one.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; missing config is flagged, nothing hardcoded.
- [ ] **Enabled-only** — every KPI was gathered solely from enabled `tooling.*` sources; disabled sources are marked `not run` and absent data `not tracked yet`; no number was fabricated or carried forward.
- [ ] **Mapped** — each KPI in the scorecard appears in the metric→ISTQB-term→ISO 25010 mapping table.
- [ ] **Measurable** — output states counts/percentages and trend direction rather than prose claims; RAG status follows the explicit thresholds (or `gates`).
- [ ] **Residual risk stated** — the report names which KPIs are uncovered and what that blinds leadership to (ISTQB Principle 1).
- [ ] **Work product named** — output is identified as a cross-release management quality report (aggregating 29119-3 Test Status / Test Completion Reports) and written to the correct `<paths.docs_dir>` location.
