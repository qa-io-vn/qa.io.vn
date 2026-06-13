---
description: Estimate testing effort for a release, feature, or backlog using ISTQB estimation techniques (metrics-based and expert-based). Use for test planning, sprint capacity, or sizing a test effort. Writes ESTIMATE-<release>.md.
argument-hint: "<release / feature / backlog scope>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Test estimation: $ARGUMENTS

**ISTQB process:** Test planning — test effort estimation (metrics-based and expert-based). Estimation is an Advanced Test Management topic (CTAL-TM); it supports the Test Plan within the test-planning activity (CTFL v4.0 §5.1 — verify the exact subsection against the current syllabus). Use strict ISTQB Glossary terms; see `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Repo signals (historical baseline for metrics-based estimation)
```!
echo "--- existing test counts ---"; find . -path ./node_modules -prune -o \( -name "*.spec.*" -o -name "*.test.*" \) -print 2>/dev/null | wc -l
echo "--- recent CI durations (if any) ---"; ls -1 reports 2>/dev/null | head
```

## Your task

If `qa.config.yml` is missing, note that estimates will not reflect this project's risk tiers, gates, or tooling, and suggest the user run `/qa:qa-init` first. Proceed only with explicit, stated assumptions.

**Scope** comes from `$ARGUMENTS` (a release ID, feature, or backlog reference). **If `$ARGUMENTS` is empty:** ask the user what to estimate; if no answer is given, default scope to the `risk_areas.critical` areas in `qa.config.yml` and state this default explicitly in the output assumptions.

1. **Establish scope.** List the features/stories in scope. Tag each with a **risk tier** by matching it to `risk_areas` (`critical` / `high` / `medium`; anything unlisted = `low`). Record which **test levels** (component, integration, system, acceptance) and **test types** (functional plus each enabled `tooling.*` non-functional type) apply.
2. **Metrics-based estimate** (use historical data; ISTQB metrics-based approach). Derive ratios from the repo and config where available — test-cases per story, defects per area, automation effort per case, execution time per suite. Use the test counts and CI durations from the signals block above. Where no history exists, mark the figure **(no baseline)** and fall back to the expert-based number for that line.
3. **Expert-based estimate** (bottom-up; ISTQB expert-based approach). For each in-scope item, estimate effort per ISTQB test-process activity — analysis, design, implementation, execution, completion — and per applicable test type. Sum per activity and per type.
4. **Reconcile** the two approaches. Where they diverge by more than ~30%, state why and choose the more defensible figure; carry the spread into the range (step 6).
5. **Apply adjustment factors**, each as an explicit multiplier or added buffer:
   - **Risk** — `critical` tier: add depth (e.g. +50% effort vs `low`); `high`: +25%; `medium`/`low`: baseline. Use the project's own ratios if history justifies different numbers.
   - **Automation vs manual split** — derive from enabled `tooling.*`; automated-suite authoring costs more up-front, less to re-run.
   - **Environment & test-data setup** — from `environments` and `test_data` in config.
   - **Regression scope** — confirmation + regression re-test effort.
   - **Contingency** — add an uncertainty/flakiness buffer (state the %); raise it when `(no baseline)` lines dominate.
6. **Produce the estimate as a range, never a single false-precise number.** Give a low–high band (e.g. ±20–40% by confidence) and a **confidence level** (high / medium / low) tied to how much was metrics-based vs expert-based.

## Output schema — `ESTIMATE-<release>.md`

Write the test estimation report to `<paths.docs_dir>/ESTIMATE-<release>.md` (default `docs/qa/`; `<release>` from scope, slugified). It is the test-effort input to the ISO/IEC/IEEE 29119-3 **Test Plan** (resourcing & schedule); it is not itself a standalone 29119-3 work product. Structure:

1. **Scope & assumptions** — items in scope with risk tier; every assumption listed explicitly (including any empty-input default and `(no baseline)` fallbacks).
2. **Effort breakdown** — table of person-days by ISTQB activity (analysis / design / implementation / execution / completion) × test type.
3. **Method comparison** — metrics-based vs expert-based per line, with the reconciliation note.
4. **Adjustment factors** — risk, automation split, environment/data, regression, contingency — each with its multiplier/buffer.
5. **Total as a range** — low–high person-days, plus a stated **confidence level**.
6. **Risks to the estimate** — what could make it wrong, and the residual-risk note (below).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `risk_areas`, enabled `tooling.*`, `environments`, `test_data`, `gates`) is honored; nothing hardcoded.
- [ ] **Both approaches applied** — metrics-based and expert-based are each present and reconciled; divergences over ~30% are explained.
- [ ] **Measurable** — output states person-days as a low–high range with a confidence level, not prose claims; assumptions are enumerated, not implied.
- [ ] **Residual risk stated** — name what the estimate does NOT cover and why it could be wrong (ISTQB Principle 1: testing shows the presence, not the absence, of defects; an estimate is a forecast, not a guarantee).
- [ ] **Work product named** — output is identified as the test-effort input to the ISO/IEC/IEEE 29119-3 **Test Plan** and written to the correct `<paths.docs_dir>` location.

End by pointing to the file and feeding the result into `/qa:create-plan` (schedule & resourcing). For the risk tiers that drive the depth multipliers, see `/qa:risk-assessment`. Read-only on product code.
