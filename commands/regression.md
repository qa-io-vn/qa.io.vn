---
description: Select, prioritize, and optimize the regression test set using impact analysis, and write the selection to docs. Use when deciding what to regression-test for a change, or to keep the regression suite lean.
argument-hint: "[change / area / release]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Regression test selection: $ARGUMENTS

**ISTQB process:** Change-related testing — **regression testing** (CTFL v4.0 §2.2.2 test types). Distinguish from **confirmation (re-)testing**: confirmation re-runs the tests that previously failed to verify a fix resolves the defect; **regression** re-runs previously passing tests to detect that the change has not broken existing behavior. This command scopes the regression set only — confirmation testing of the fix itself is handled at execution (`/qa:implement`). Risk-based selection and prioritization approaches verify against the current CTAL-TM syllabus.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Change signals
```!
echo "--- recent changes ---"; (git diff --name-only HEAD~5 2>/dev/null || echo "no git history") | head -30
```

## Your task

**Config guard:** if the config above is `none`, state that `<paths.*>` and `risk_areas` are unresolved and offer to run `/qa:qa-init` before producing a persisted artifact; you may still output an in-chat draft.

**Scope resolution (empty-`$ARGUMENTS` branch):** if `$ARGUMENTS` is empty, ask the user for the change/area/release. If no answer is given, default the scope to the union of (a) the changed files in **Change signals** above and (b) `risk_areas.critical` from config, and state this assumption explicitly in the output.

Then proceed:

1. **Impact analysis** — determine what the change affects directly and indirectly. Trace each changed item to the modules, APIs, data flows, and UI journeys that depend on it (shared modules, contracts, persisted state, cross-cutting concerns). Map every affected area to a `risk_areas` tier. Produce an **impact-analysis table**:

   | Changed item | Directly affected | Indirectly affected (dependency) | `risk_areas` tier | Confidence (high/med/low) |
   |---|---|---|---|---|

   Flag any area where impact is hard to trace (poor coverage or weak traceability) as low-confidence — these expand the regression scope by precaution.

2. **Select a regression strategy** by an explicit rule, not preference:
   - **Retest-all** — only when the change is high-risk AND broad (touches `risk_areas.critical` or shared infrastructure) AND time/budget allows a full run.
   - **Risk-based selective regression** (default) — include all tests covering impacted areas plus all `risk_areas` critical/high areas; exclude unaffected low-risk areas.
   - **Test-case prioritization** — within the selected set, order by: (1) risk tier of the area, (2) proximity to the change, (3) historical defect density / past flakiness. Highest-value tests run first so an early stop still maximizes risk coverage.

   State which strategy you chose and the rule that selected it.

3. **Build the regression-set selection matrix** — one row per candidate test/suite, with explicit columns:

   | Test / suite | Area | `risk_areas` tier | Priority (P1/P2/P3) | Decision (include / defer / retire) | Rationale |
   |---|---|---|---|---|---|

   - **Include** = covers an impacted or critical/high-risk area.
   - **Defer** = unaffected lower-risk area; move to nightly/full rather than PR gate.
   - **Retire** = redundant or obsolete (pesticide paradox — CTFL Principle 5), or coverage better pushed to a cheaper level (e.g., logic in a slow E2E that belongs in `tooling.unit`/`tooling.api`).

4. **Recommend CI placement** — split the included set into a **PR smoke** subset (fast, highest-priority, gates merges) and a **nightly/full** regression run, honoring the relevant `gates` and `tooling.*` toggles in config. State counts for each (e.g., "PR smoke: 14 tests; nightly: 86 tests").

5. **State residual risk** — name what the selected set does NOT cover and why (deferred areas, low-confidence impact, untestable paths), per CTFL Principle 1.

**Output:** a **Regression Test Selection report** — a tailored ISO/IEC/IEEE 29119-3 **Test Design Specification** fragment (test-selection rationale and prioritization), written to `<paths.docs_dir>/REGRESSION-SELECTION-<scope>.md`. It contains the impact-analysis table, the selection matrix, the chosen strategy and its rule, CI placement with counts, and the residual-risk statement. Source/test files are read only — do not modify them.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.docs_dir`, `risk_areas` tiers, `gates`, and `tooling.*` toggles in scope are honored; the output path and CI split derive from config, nothing hardcoded.
- [ ] **Confirmation vs regression kept distinct** — the report scopes regression (previously passing tests) and does not conflate it with confirmation re-testing of the fix.
- [ ] **Traceability intact** — every selected test traces back through its area to a changed item or a `risk_areas` tier; the impact-analysis table has no orphan rows.
- [ ] **Measurable** — output states counts (included / deferred / retired; PR smoke vs nightly) rather than prose claims, and each decision has a stated rule.
- [ ] **Residual risk stated** — what the selected set does NOT cover and why is named (CTFL Principle 1).
- [ ] **Work product named** — output is identified as a 29119-3 Test Design Specification (selection) fragment and written to the correct `<paths.docs_dir>` location.

## Handoffs
- **Impact analysis for a maintenance release** → `/qa:maintenance-test` (which calls this command for selection).
- **Keep the selected suite trustworthy** → `/qa:flaky-hunt` (quarantine/repair flaky regression tests before they gate merges).
- **Audit overall coverage of the selection** → `/qa:review-coverage`.
- **Run the selected set / confirm fixes** → `/qa:implement`.
- **Feed results into the release decision** → `/qa:release-report`.
