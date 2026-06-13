---
description: Analyze Cost of Quality and QA ROI — prevention/appraisal/internal-failure/external-failure costs, cost of poor quality, and automation return on investment for budget justification. Use for QA economics and business cases. Writes COST-OF-QUALITY-<scope>.md.
argument-hint: "[scope / period]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Cost of Quality & QA ROI: $ARGUMENTS

**ISTQB process:** Value of testing, test economics & cost of quality — an **Advanced Test Management** topic (CTAL-TM: cost of quality, ROI of testing, metrics). It draws on the Foundation rationale for testing and the cost-of-defects/shift-left principle (CTFL v4.0 §1 — verify the exact subsection against the current syllabus; do not assert a section number). Cost of Quality is **not** a Foundation §1.2 deliverable — treat it as Specialist/Advanced material. Use strict ISTQB Glossary terms; see `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Repo signals (defect / incident / automation baseline)
```!
echo "--- existing test counts ---"; find . -path ./node_modules -prune -o \( -name "*.spec.*" -o -name "*.test.*" \) -print 2>/dev/null | wc -l
echo "--- recent reports (if any) ---"; ls -1 reports 2>/dev/null | head
echo "--- existing QA docs (defect/status/release inputs) ---"; ls -1 docs/qa 2>/dev/null | head
```

## Your task

If `qa.config.yml` is missing, note that the analysis will not reflect this project's risk tiers, gates, or tooling, and suggest the user run `/qa:qa-init` first. Proceed only with explicit, stated assumptions.

**Scope** comes from `$ARGUMENTS` (a period, release, or program). **If `$ARGUMENTS` is empty:** ask the user for the scope and reporting period; if no answer is given, default scope to the `risk_areas.critical` areas in `qa.config.yml` over the **last release cycle** (`process.release_cadence`) and state this default explicitly in the output assumptions.

Build a Cost of Quality analysis and QA business case. Use real figures only where the team can supply them; otherwise present the model with clearly-labeled `(placeholder)` inputs and ask for them — **never invent costs**. Frame economically for budget holders; avoid false precision — use ranges and state every assumption.

### 1. Assumptions & data completeness (do this first)
List, before any number:
- **Scope & period** in effect (including any empty-input default above).
- **Inputs available vs missing** — for each cost category below, mark the data source as *actual* (from defect/incident/CI data), *estimated* (team-supplied), or `(placeholder)` (no data). A category with no input stays a labeled placeholder; it is never silently zeroed.
- **Rates** — loaded labor cost/day, environment/tooling cost, incident/support cost per event — each *actual* or `(placeholder)`.
- **Confidence** — overall high / medium / low, tied to how much is *actual* vs `(placeholder)`.

### 2. Cost of Quality model (prevention / appraisal / failure)
Categorize and, where data exists, quantify each line as a range. The model: investment in **conformance** (prevention + appraisal) reduces far costlier **non-conformance** (internal + external failure), so total CoQ is minimized off the corners, not at zero spend.
- **Prevention** (conformance) — training, tooling, test design, standards, reviews, `/qa:static-review` of the test basis. Shift-left spend.
- **Appraisal** (conformance) — test execution, automation runs (enabled `tooling.*`), environments (`environments`), audits.
- **Internal failure** (non-conformance) — defects found pre-release: rework + confirmation/regression re-test (`/qa:triage` data).
- **External failure** (non-conformance) — defects escaped to production: incidents, support, reputation, churn. **Usually the most expensive** — weight `risk_areas.critical` escapes heaviest.

### 3. Cost of poor quality (CoPQ)
From defect/incident data over the period, estimate the cost of escaped defects and quality incidents (internal failure + external failure). State the per-event and total ranges and the data source for each.

### 4. Automation ROI & payback
For the automation program (or the candidates from `/qa:automate`): implementation + maintenance cost vs manual-effort saved over time, defects caught earlier, and faster feedback. Compute, each as an explicit figure or `(placeholder)`:
- **One-time cost** — authoring/implementation effort × loaded rate.
- **Recurring cost** — maintenance + per-run cost (CI minutes, flakiness triage).
- **Recurring saving** — manual execution effort avoided per cycle × cycles/period (use `process.release_cadence`).
- **Payback period** = one-time cost ÷ net saving per cycle; **break-even** point in cycles/months. State the cycle assumption explicitly.

### 5. Business case & recommendation
Recommend where to invest — more prevention/appraisal where it measurably cuts failure cost — with expected return; support headcount/tooling/budget asks. Tie each recommendation to a CoQ category and an expected reduction range.

## Output schema — `COST-OF-QUALITY-<scope>.md`

Write the analysis to `<paths.docs_dir>/COST-OF-QUALITY-<scope>.md` (default `docs/qa/`; `<scope>` slugified). This is **not** a dedicated ISO/IEC/IEEE 29119-3 work product; it is a management/economics report that supplies the **test-economics and value-of-testing inputs** to the ISO/IEC/IEEE 29119-3 **Organizational Test Strategy / Test Policy** and **Test Plan** (the "resources/value" rationale). Identify it as such — do not mislabel it as a 29119-3 document. Structure:

1. **Assumptions & data completeness** — scope, period, input availability per category, rates, confidence (from step 1).
2. **Cost of Quality model** — prevention / appraisal / internal-failure / external-failure table, each line a range with its data source label.
3. **Cost of poor quality** — escaped-defect/incident cost over the period.
4. **Automation ROI** — one-time vs recurring cost vs saving, **payback period** and **break-even** (cycle assumption stated).
5. **Business case** — prioritized investment recommendations with expected return ranges.
6. **Residual risk & limitations** — what the figures do NOT capture and why (below).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `risk_areas`, enabled `tooling.*`, `environments`, `process.release_cadence`, `gates`) is honored; nothing hardcoded.
- [ ] **Data completeness labeled** — every cost line is marked *actual* / *estimated* / `(placeholder)`; no placeholder is silently treated as zero; no figure is invented.
- [ ] **Measurable, not false-precise** — costs and ROI are stated as ranges with a stated confidence level; prose claims are backed by a number or labeled as assumptions.
- [ ] **Prevention/appraisal/failure model intact** — all four CoQ categories appear; the conformance-vs-non-conformance trade-off (prevention+appraisal reducing failure cost) is explicit.
- [ ] **Automation payback shown** — automation ROI gives payback period and break-even with the cycle assumption stated, reconciled with `/qa:automate` candidate ROI.
- [ ] **Residual risk stated** — name what the figures do NOT cover and why the model could be wrong (ISTQB Principle 1: testing shows the presence, not the absence, of defects; a cost model is a forecast, not a guarantee). This is an advisory economic estimate, not an audited financial statement — flag it for human/finance review before budget decisions.
- [ ] **Work product named** — output is identified as the test-economics/value-of-testing input to the ISO/IEC/IEEE 29119-3 Organizational Test Strategy / Test Plan (not itself a 29119-3 document) and written to the correct `<paths.docs_dir>` location.

End by pointing to the file. The CoQ figures feed the value/resourcing case in `/qa:create-strategy` and `/qa:quality-report`; the automation payback reconciles with `/qa:automate` and `/qa:automation-strategy`; risk weighting for external-failure cost comes from `/qa:risk-assessment`. Do not modify code or tests — the only file you write is the report.
