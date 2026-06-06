---
description: Analyze Cost of Quality and QA ROI — prevention/appraisal/failure costs, cost of poor quality, and automation return on investment for budget justification. Use for QA economics and business cases.
argument-hint: "[scope / period]"
allowed-tools: Read, Glob, Grep, Bash
---

# Cost of Quality & QA ROI${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Value of testing & cost of quality (CTAL-TM; CTFL §1.1 value of testing).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Scope from `$ARGUMENTS`. Build a Cost of Quality analysis and QA business case. Use real figures where the team can supply them; otherwise present the model with clearly-labeled placeholders and ask for inputs — don't invent costs.

1. **Cost of Quality model** — categorize and (where data exists) quantify:
   - **Prevention** — training, tooling, test design, standards, reviews.
   - **Appraisal** — test execution, automation runs, environments, audits.
   - **Internal failure** — defects found pre-release (rework, re-test).
   - **External failure** — defects escaped to production (incidents, support, reputation, churn) — usually the most expensive.
   The insight: investment in prevention + appraisal reduces far costlier failure (especially external).
2. **Cost of poor quality** — estimate the cost of escaped defects and quality incidents over the period (from defect/incident data).
3. **Automation ROI** — for the automation program: implementation + maintenance cost vs manual-effort saved over time, defects caught earlier, faster feedback. Show payback period and break-even (ties to `/qa:automate` candidate ROI).
4. **Business case** — recommend where to invest (more prevention/appraisal where it cuts failure cost), with expected return; support headcount/tooling/budget asks.

Output to `<paths.docs_dir>/COST-OF-QUALITY-<scope>.md`: the CoQ breakdown, ROI summary, and recommendations. Read-only. Frame economically for budget holders; avoid false precision — use ranges and state assumptions.
