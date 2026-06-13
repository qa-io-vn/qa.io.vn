---
description: Measure and report test coverage — structural (statement/branch), requirements/test-basis, and risk coverage. Quantifies how much is actually covered and where the holes are, against configured gates. Read-only.
argument-hint: "[scope or path]"
allowed-tools: Read, Glob, Grep, Bash
---

# Coverage measurement

**ISTQB process:** Test monitoring — coverage measurement (CTFL v4.0 §5.3, with white-box statement/branch coverage per §4.3; deeper structural analysis is CTAL-TTA — verify any Advanced claim against the current syllabus). Coverage is a monitoring **metric**, not a target to game (Principle 1 / absence-of-errors fallacy).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Coverage data
```!
echo "--- coverage report ---"; ls -1 coverage 2>/dev/null; cat coverage/coverage-summary.json 2>/dev/null | head -20
echo "--- unit/component coverage tool ---"; grep -iE "coverage|c8|nyc|istanbul" package.json 2>/dev/null | head
```

## Your task

**Config-read guard.** Read `qa.config.yml` from the first block. If it printed `none`, tell the user config is missing, recommend `/qa:qa-init`, and proceed only with values the user confirms — do **not** hardcode paths, tools, or thresholds. Otherwise resolve and honor these fields, using them everywhere instead of literals:
- `<paths.tests_dir>` (test locations), `<paths.reports_dir>` (coverage/report artifacts), `<paths.docs_dir>` (test-basis docs).
- `<tooling.unit>` / `<tooling.component>` (the runner that emits structural coverage; treat `none` as "that level is out of scope"), `<stack.api_spec_path>` (endpoint test basis).
- `gates` (coverage thresholds — see step 5), `risk_areas` (critical/high/medium tiers for prioritization).

Never hardcode `coverage/`, `tests/`, `playwright-report`, `test-results`, `npx playwright`, `vitest`/`jest`, or `openapi.yaml` outside the discovery blocks above.

**1. Resolve scope.**
   - If `$ARGUMENTS` names a scope/path, measure within it.
   - **If `$ARGUMENTS` is empty:** ask the user for the scope (module, feature, or path). If the user declines or cannot specify, **default to the areas listed in `risk_areas.critical`**, and state explicitly that you defaulted there and why.

**2. Structural (white-box) coverage — CTFL §4.3.** From the `<tooling.unit>` / `<tooling.component>` coverage artifact under `<paths.reports_dir>` (or the discovery block), report **statement coverage %** and **branch coverage %** overall and per module. Rank under-covered modules, listing those mapped to `risk_areas.critical`/`high` first. State counts (e.g. "X of Y branches, Z uncovered"), not prose. If no coverage artifact exists, say so and report this dimension as "not measured" rather than estimating.

**3. Test-basis / requirements coverage.** Map which requirements, user stories, and `<stack.api_spec_path>` endpoints have at least one test case via the traceability chain (test basis → condition → case). Report **covered / total** as a count and %, and name the specific uncovered requirements/endpoints.

**4. Risk coverage.** For each `risk_areas` tier, report whether every area is covered at the appropriate test levels and types the strategy requires (e.g. critical journeys need layered API + E2E + the required non-functional checks). Report **areas covered / total** per tier; list uncovered critical/high areas explicitly.

**5. Coverage-item coverage.** For designed cases, report which coverage items (equivalence partitions, boundary values, decision-table rules, states/transitions) are exercised vs missed, as counts.

**6. Apply thresholds from gates.** Compare each measured value against the configured target and flag PASS/FAIL:
   - Structural: against `gates.min_coverage_pct` (or the relevant `gates` coverage field). If no coverage gate is configured, state that no threshold exists and report the measured value without a pass/fail verdict — do not invent a number such as 80%.
   - Risk: every `risk_areas.critical` area must be covered (target 100%); any critical area below target is a **FAIL**.
   - State each comparison as `dimension | measured | target (from gates) | PASS/FAIL`.

**7. Output — coverage measurement.** Produce a coverage report as the ISO/IEC/IEEE 29119-3 **Test Status Report** work product (coverage is a monitoring metric; no dedicated template — mirror the coverage section of `templates/completion-report-template.md` if present). Table columns: **dimension | measured | target (gate) | PASS/FAIL | gaps (prioritized by risk)**. Then recommend the highest-value additions (critical-risk gaps first) and offer `/qa:test-design` to design the missing cases and `/qa:implement` to author them; route deeper coverage trend/exit reporting to `/qa:status-report`, and full traceability-chain auditing to `/qa:review-coverage`.

This is **read-only** analysis — do not create or modify any files. Be specific (name the module/endpoint/requirement/file), never generic.

## Self-check (run before finalizing output)

This command is advisory and read-only; do not finalize until every item passes:
- [ ] **Config reflected** — `<paths.*>`, `<tooling.unit>`/`<tooling.component>`, `gates` thresholds, and `risk_areas` are read from `qa.config.yml` and honored; nothing hardcoded (no `coverage/`, `tests/`, `playwright-report`, `npx playwright`, `vitest`/`jest`).
- [ ] **Measurable** — every dimension states counts/percentages and a PASS/FAIL against the configured gate, not prose claims; no threshold is invented when `gates` omits one.
- [ ] **Traceability honored** — requirements/risk coverage is read through the chain test basis → condition → case → coverage item; orphans (tests with no basis, basis with no test) are surfaced.
- [ ] **Residual risk stated** — name what is **not** covered and why; coverage % is a guardrail, never proof of correctness (Principle 1, absence-of-errors fallacy). No file is written; output is advisory only.
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Status Report** (coverage metric) and prioritizes gaps by `risk_areas` tier.
