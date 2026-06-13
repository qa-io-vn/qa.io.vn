---
description: Define the program-level Test Automation Strategy and architecture (gTAA) — objectives, scope, approaches, tool fit, level distribution, CI, maintainability, metrics, ROI. Use to set or review the overall automation approach (above any single feature or release). Writes the Test Automation Strategy work product.
argument-hint: "(no args — optional: a focus area, e.g. 'API layer' or a risk_areas key)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test Automation Strategy & Architecture

**ISTQB process:** Test Automation Engineering — generic Test Automation Architecture (gTAA) and the program-level Test Automation Strategy (CT-TAE; ISTQB Test Automation Strategy — verify section numbers against the current syllabus). This is the long-lived, program-level **Test Automation Strategy** (organization/product-wide). It is distinct from a release-scoped **Test Automation Plan**, which is produced per feature/release by `/qa:automate`. Sits above per-surface automation (`/qa:api-automate`, `/qa:web-automate`, `/qa:mobile-automate`, `/qa:perf-plan`) and complements the Organizational Test Strategy from `/qa:create-strategy`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Current automation footprint (discovery scan)
```!
echo "--- framework ---"; ls -1 playwright.config.* 2>/dev/null; ls -1 tests 2>/dev/null
echo "--- CI ---"; ls -1 Jenkinsfile .github/workflows/*.yml 2>/dev/null
```

## Your task

Produce the program-level **Test Automation Strategy** for this product (long-lived, automation-specific, above any single feature or release).

### Step 0 — Guards & inputs (run first)
1. **Config guard.** If the config block above printed `MISSING` (no `qa.config.yml`), STOP and route the user to `/qa:qa-init` to establish project context — do not invent `paths.*`, `tooling.*`, `gates`, or `risk_areas`. If config is present, read it and resolve every `<paths.*>`, `<tooling.*>`, `<stack.*>`, `gates`, and `risk_areas` value used below from it; never hardcode a path or tool.
2. **Scope argument.** `$ARGUMENTS` is an optional focus area (e.g. `API layer`, or a `risk_areas` key). If `$ARGUMENTS` is empty, default the depth focus to `risk_areas.critical` and produce the full strategy. If `$ARGUMENTS` names a focus area, still produce the full strategy but concentrate detail there.
3. **Template.** Read `${CLAUDE_PLUGIN_ROOT}/templates/automation-strategy-template.md` and produce its sections in order. Omit any sub-section whose tool is `none`/absent in `tooling`. Automation is an **investment/ROI decision** (CT-TAE) — never "automate everything."

### Step 1 — Objectives & business case
State why automate, the expected ROI, and what automation will and will not do (it complements — does not replace — manual and exploratory testing). Tie each objective to a measurable success criterion (e.g. PR-gate wall-clock target, pass rate ≥ `gates.min_pass_rate_pct`).

### Step 2 — Scope
List the test levels and surfaces in scope (unit, component, integration/API, contract, system/UI-E2E, mobile, performance, accessibility, security) strictly per enabled `<tooling.*>`. State what is explicitly out of scope (kept manual) with a one-line justification each.

### Step 3 — gTAA: generic Test Automation Architecture (CT-TAE)
Define the layered architecture and keep the SUT decoupled from tests via the adaptation layer. Specify each gTAA layer concretely for this product:
1. **Test generation** — how test cases are derived/parameterized (data-driven, partitions/boundaries, models; cases from `<stack.api_spec_path>`).
2. **Test definition** — how tests and test data are specified independently of execution tech (Page Objects, typed API clients, keywords/fixtures, test data).
3. **Test execution** — runners, setup/teardown, logging, reporting, CI (`<tooling.e2e>`/`<tooling.unit>`; results to `<paths.reports_dir>`).
4. **Test adaptation** — interfaces that connect to the SUT (UI/API/CLI drivers, service virtualization/mocking) so changes localize to this layer.

### Step 4 — Automation approaches
Choose and justify one or more, matched to team and stack: data-driven, keyword-driven, behavior-driven (BDD/ATDD), and/or model-based. State the decision rule used for each choice.

### Step 5 — Level distribution (pyramid)
Define a target split across unit / component / API+contract / UI-E2E / non-functional, expressed as approximate percentages. **Decision rule:** assign each check to the lowest level that can verify it; reserve UI-E2E for genuine end-to-end journeys in `risk_areas.critical`. Map every level to its enabled `<tooling.*>`.

### Step 6 — Tooling fit
Confirm each capability maps to an enabled `<tooling.*>`/`<stack.*>` entry; for any gap (capability needed but tool is `none`), do not assume a tool — flag it and route to `/qa:tool-select`.

### Step 7 — CI/CD integration
Define where automation runs (PR gate vs nightly vs pre-release) on `<tooling.ci.platform>`, sharding/parallelism, and reporting destination (`<paths.reports_dir>`). State the gate rule (what blocks a merge/release) referencing `gates`.

### Step 8 — Maintainability strategy
Specify stable-selector policy, reuse via the adaptation layer, no hard waits, the flakiness policy (route ongoing triage to `/qa:flaky-hunt`), and versioning of testware. For an assessment of existing testware quality, route to `/qa:automation-audit`.

### Step 9 — Automation metrics
Define the metric set and its target/threshold for each (cite `gates` where one applies):
1. **Automation coverage** — % of in-scope conditions/journeys automated.
2. **Pass rate** — vs `gates.min_pass_rate_pct`.
3. **Flaky rate** — target ceiling.
4. **Execution time** — PR-gate wall-clock target; nightly duration.
5. **Manual effort saved / ROI** — automated vs manual cost.
6. **Maintenance effort** — testware churn per release.
7. **Defects found by automation** — escape-rate signal.
State the source and cadence for each metric.

### Step 10 — Risks & assumptions
List automation-specific risks (over-reliance, maintenance cost, unstable SUT/data, tool limits, false confidence) with a mitigation for each, and the assumptions the strategy depends on.

## Output & work product
Write the result to `<paths.docs_dir>/automation-strategy.md`. This is the **Test Automation Strategy** work product (ISO/IEC/IEEE 29119-3 test-documentation alignment; gTAA per CT-TAE). It guides every surface command (`/qa:api-automate`, `/qa:web-automate`, `/qa:mobile-automate`, `/qa:perf-plan`), the per-feature/release Test Automation Plan (`/qa:automate`), framework setup (`/qa:scaffold`), and testware assessment (`/qa:automation-audit`).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; no path or tool is hardcoded, and `none`/absent tooling is omitted.
- [ ] **Architecture intact** — all four gTAA layers (generation, definition, execution, adaptation) are defined and the SUT stays decoupled from tests via the adaptation layer; no layer is orphaned.
- [ ] **Measurable** — the strategy states target metrics/thresholds (coverage %, pass rate vs `gates.min_pass_rate_pct`, flaky ceiling, execution-time target, level-split %) rather than prose claims.
- [ ] **Residual risk stated** — name what automation does NOT cover and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects); automation complements, not replaces, manual/exploratory testing.
- [ ] **Work product named** — output is identified as the **Test Automation Strategy** (program-level, distinct from a release-scoped Test Automation Plan) and written to `<paths.docs_dir>/automation-strategy.md`.
