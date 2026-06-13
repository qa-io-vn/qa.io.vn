---
description: Design or review component (unit) testing at the lowest test level — structural coverage targets, isolation, test doubles. Produces component test procedures/scripts (ISO/IEC/IEEE 29119-3 Test Procedure Specification) plus a statement/branch coverage report. Use for unit/component test guidance and coverage at the component level.
argument-hint: "<module / component / file>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Component (unit) testing: $ARGUMENTS

**ISTQB process:** Component testing — the lowest **test level** (CTFL v4.0 §2.2; verify the section against the current syllabus). Cases are derived with black-box techniques (§4.2) plus **white-box** statement and branch coverage (§4.3).
**Work product:** component **test procedures / automated test scripts** (ISO/IEC/IEEE 29119-3 **Test Procedure Specification**) plus a **statement/branch coverage report**. No dedicated template — for any case schema reuse `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md`.

> Component (unit) tests are usually **developer-owned**; this command helps design, review, and strengthen them. For structural-coverage measurement across the whole codebase use `/qa:coverage-measure`; for higher levels use `/qa:integration-test`, `/qa:api-automate`, `/qa:web-automate`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Unit tooling & coverage (discovery)
```!
echo "--- tooling.unit (from qa.config.yml) ---"; grep -iE "^[[:space:]]*unit:" qa.config.yml 2>/dev/null || echo "tooling.unit: not set"
echo "--- coverage support ---"; grep -iE "coverage|c8|nyc|istanbul|--cov|vitest|jest" package.json 2>/dev/null | head
```

## Step 0 — Read config & resolve target (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed with documented defaults — do **not** invent paths/tools; use the `<paths.*>`/`<stack.*>`/`<tooling.*>` values the user confirms.
2. Resolve the **unit runner** from `<tooling.unit>` (read in the discovery block above) — do **not** assume a specific framework. If `<tooling.unit>` is unset, ask the user which runner to use (or infer from `package.json` and confirm). Never hardcode a runner name.
3. Resolve the target from `$ARGUMENTS` (module/component/file):
   - **If `$ARGUMENTS` is non-empty:** that is the component under test.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user for the component. If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** and state explicitly that you defaulted there and why.
4. Confirm the resolved target, the runner (`<tooling.unit>`), the test location convention (`<paths.tests_dir>` / project convention), and `risk_areas` (drives coverage target) before proceeding. Nothing about paths or tools is hardcoded.

## Your task

Run the following steps in order. Do not skip a step; if a step is not applicable, say so explicitly and why.

### 1. Scope (isolation)

Test a single component in **isolation**, using test doubles (stubs/mocks/fakes) for its dependencies. Verify functional behavior, and where relevant non-functional aspects (e.g. resource use) and structure. No real I/O, network, clock, or dependence on other tests.

### 2. Derive cases (techniques)

1. **Black-box** — apply EP and BVA to the component's inputs (state which BVA form, 2-value or 3-value); add decision-table cases where the logic is rule-driven.
2. **White-box (§4.3)** — identify the statements and branches in the component's logic; ensure cases exercise every branch (true/false of each decision), not just the happy path.
3. Include **negative** and error-path cases; assert exceptions/rejections, not just success.

### 3. Coverage target (decision rule)

1. Set the structural-coverage target from `risk_areas`:
   - Component in **`risk_areas.critical`/high** → target **branch coverage** (every decision outcome exercised), and 100% of identified branches in the critical logic unless explicitly waived.
   - **Med/Low** component → **statement coverage** of the changed/added logic is the floor; cover branches where cheap.
2. Honor any `gates`/coverage thresholds in `qa.config.yml` if present.
3. Coverage is a **guardrail, not a vanity metric** — do not game the number; uncovered ≠ tested-and-passing (avoid the absence-of-errors fallacy, CTFL v4.0 Principle 7).

### 4. Quality bar

Each test: fast, isolated, deterministic, asserts **one behavior**; clear arrange/act/assert; descriptive name; no reliance on real I/O or test ordering.

### 5. If reviewing existing unit tests

Identify untested branches, missing negative cases, brittle/over-specified mocks, and over-coupling to internals; recommend concrete additions mapped to the uncovered coverage items.

### 6. Implement, run, measure

1. Place/extend tests at the component's location per `<paths.tests_dir>` / project convention.
2. Run them with the resolved `<tooling.unit>` runner **with coverage enabled**, using the project's configured coverage flag (from the discovery block) — do not hardcode a CLI.
3. Report **counts**: tests added/passing, statements covered (n/total, %), branches covered (n/total, %), and the prioritized list of remaining gaps.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — the unit runner came from `<tooling.unit>`, tests live under `<paths.tests_dir>` / project convention, the coverage target honors `risk_areas`/`gates`; nothing hardcoded (no literal runner name, no fixed CLI).
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item (statement/branch) -> procedure -> result (-> defect) is preserved and bidirectional; every branch in scope maps to ≥1 case; no orphan tests.
- [ ] **Measurable** — output states statement and branch coverage as counts/percentages (n/total) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (untested branches/paths, mocked-away integrations, waived targets); ISTQB Principle 1 (testing shows the presence, not the absence, of defects) and Principle 2 (exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as component **test procedures / scripts** (ISO/IEC/IEEE 29119-3 **Test Procedure Specification**) plus a statement/branch **coverage report**, written under `<paths.tests_dir>` / project convention.

## Handoff

- Untested branches confirmed across the codebase, or a full structural-coverage report → `/qa:coverage-measure`.
- Higher test levels → `/qa:integration-test` (component/system integration), `/qa:api-automate`, `/qa:web-automate`.
- Adding a single targeted test at the right level → `/qa:add-test`. Turning designed cases into running procedures/scripts → `/qa:implement`.
- Test-basis ambiguity found while designing → `/qa:static-review`.
