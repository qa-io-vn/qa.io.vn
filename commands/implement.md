---
description: Implement and run automated tests for a feature at the right pyramid level (E2E, API, component, contract). Use when the user wants to write/add and execute tests for a specific feature or story.
argument-hint: "<feature or story description>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Implement tests for: $ARGUMENTS

**ISTQB process:** Test implementation + execution (CTFL v4.0 §1.4) — turn test cases into test procedures/scripts and run them. If test cases don't exist yet, design them first with `/qa:test-design`.

**Work products (ISO/IEC/IEEE 29119-3):** this command produces the **Test Procedure Specification** (executable specs/scripts) and, when tests are run, the **Test Execution Log / Test Results**. Failures that indicate a real defect become **Incident (Defect) Reports** — route those to `/qa:triage`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Existing framework
```!
echo "--- tests tree ---"; ls -1R "$(grep -E '^\s*tests_dir:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*tests_dir:\s*"?([^"#]+)"?.*/\1/' | xargs)" 2>/dev/null | head -60
echo "--- test runner config? ---"; ls -1 playwright.config.* vitest.config.* jest.config.* 2>/dev/null
```

## Your task

**Step 0 — Read config and resolve placeholders.** Parse `qa.config.yml` from the block above. If it printed `MISSING`, stop and tell the user to run `/qa:qa-init` first (do not invent paths/tools). If the framework tree is empty, suggest `/qa:scaffold` before implementing. Resolve these fields and use them throughout — never hardcode a path or tool:
- Runners: `<tooling.e2e>`, `<tooling.api>`, `<tooling.unit>`, `<tooling.component>`, `<tooling.contract>` (treat any value of `none` as "that level is out of scope").
- Locations: `<paths.tests_dir>` (framework root), `<paths.reports_dir>` (where run output lands), `<paths.docs_dir>` (where any spec docs live).
- Spec source: `<stack.api_spec_path>` when `<stack.api_spec>` is `openapi`.
- Risk: `risk_areas` tiers and `gates`.

**Step 1 — Resolve the target.** The target feature is `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask which feature/story to cover; if the user cannot specify, default to the first item in `risk_areas.critical` and state that you did so.

**Step 2 — Read the basis.** If `<stack.api_spec>` is `openapi`, read `<stack.api_spec_path>` for the endpoints this feature touches. Locate existing test cases (from `/qa:test-design` output in `<paths.docs_dir>`); if none exist, design them first with `/qa:test-design` rather than improvising.

**Step 3 — Decide coverage by the test pyramid and risk tier.** Apply these rules in order:
   - **Logic / pure functions** → unit (`<tooling.unit>`); if unit is not your layer, note it for devs.
   - **Endpoints** → API tests (`<tooling.api>`): happy path, negative, boundary, authz/role matrix, and schema validation against `<stack.api_spec_path>`.
   - **UI behavior** → component tests (`<tooling.component>`) where possible; reserve E2E (`<tooling.e2e>`) for the one real user journey that nothing lower can prove.
   - **Interface stability** → contract tests only if `<tooling.contract>` is not `none`.
   - **Non-functional** → if the feature is in `risk_areas.critical` or `risk_areas.high`, flag perf/a11y/security needs and route to `/qa:perf-test`, `/qa:a11y-audit`, or `/qa:security-scan` (do not implement those here).

**Step 4 — Reuse, don't duplicate.** Extend existing fixtures, page objects, and typed API clients under `<paths.tests_dir>`. Follow the conventions already in the repo. Provision data via `/qa:test-data` factories rather than inline literals.

**Step 5 — Write the procedures.** Use stable selectors (`getByRole`/`getByLabel`/`data-testid`), web-first assertions, and no hard waits. Each test owns its data via factories. Keep each test traceable to its source test case (basis -> condition -> case -> procedure).

**Step 6 — Execute.** Run the new tests with the configured runner (e.g. for `<tooling.e2e>`, invoke its test command against the spec under `<paths.tests_dir>`; output lands in `<paths.reports_dir>`). Fix failures that are test defects. If a failure reflects a real product defect, do not mask it — record it as an Incident Report and route to `/qa:triage`.

**Step 7 — Summarize.** State what you added, at which levels, the pass/fail counts from the run, and any gaps you intentionally left (with reasons). For ongoing protection of this feature in CI, route to `/qa:regression`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.tests_dir`, `paths.reports_dir`, `stack.api_spec_path`, `tooling.*` runner toggles, `risk_areas`, `gates`) is honored; no path or tool name is hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> procedure -> result (-> defect) is preserved and bidirectional; every new test maps to a test case and no test is orphaned.
- [ ] **Measurable** — output states counts (tests added per level, pass/fail/skipped from the run) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Procedure Specification** (and **Test Execution Log / Test Results** when run), written under `<paths.tests_dir>` / `<paths.reports_dir>`.

## Handoff

Design gaps route to `/qa:test-design`; missing config/framework route to `/qa:qa-init` / `/qa:scaffold`; test data to `/qa:test-data`; real defects surfaced by a run to `/qa:triage`; CI/regression protection to `/qa:regression`.
