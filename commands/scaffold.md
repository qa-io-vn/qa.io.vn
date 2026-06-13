---
description: Scaffold the test automation framework — language/framework structure, fixtures, config, plus performance / contract / a11y / CI pipeline per qa.config.yml. Use when setting up test automation in a project for the first time.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Scaffold the test framework

**ISTQB process:** Test implementation (CTFL v4.0 §1.4, §6 · CT-TAE — Specialist) — build the test automation architecture (gTAA) and testware that test implementation and execution run on. Verify any specific syllabus section against the current syllabus before quoting it.

**Work product (ISO/IEC/IEEE 29119-3):** primarily the **Test Procedure Specification** (executable specs/scripts + the harness/fixtures they run on), plus **Test Data and Test Environment Requirements** (factories, fixtures, env/CI config). This command produces the *scaffold* of those work products, not finished test cases — design those with `/qa:test-design` and fill them in with `/qa:implement`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Current repo state
```!
echo "--- root ---"; ls -1 2>/dev/null | head -40
echo "--- package.json (if JS/TS) ---"; cat package.json 2>/dev/null | head -30
echo "--- existing tests dir (best-effort) ---"; ls -1R tests test e2e 2>/dev/null | head -30
```

## Your task

**Step 0 — guards (do these first, in order).**
1. If `qa.config.yml` is missing (the block above printed `MISSING`), **stop** and tell the user to run `/qa:qa-init`. Do not scaffold against assumptions.
2. Read these fields from the config and use them everywhere instead of hardcoded values: `paths.tests_dir`, `paths.reports_dir`, `tooling.language`, `tooling.framework` (the UI/E2E runner), `tooling.unit`, `tooling.mocking`, `tooling.contract`, `tooling.performance`, `tooling.accessibility`, `tooling.security`, `stack.api_spec_path`, `stack.base_url`, `ci.platform`, `ci.browsers`, `ci.shard_count`, `ci.agents_docker_image`, `gates.*`, `risk_areas.*`.
3. For any field that is **empty/unset**, do not invent a value: skip that capability and record it in the final "not scaffolded (and why)" list. Default only where the config defines a default (e.g. tests directory defaults to `<paths.tests_dir>` → `tests/` when unset). When the language/framework toggle is unset, ask the user which to use rather than guessing.
4. **Never overwrite an existing file silently.** Prefer creating missing pieces. If an existing `<paths.tests_dir>` framework or config file is present, list the conflict and **ask before changing it**.

**Step 1 — scaffold only what the config's `tooling` enables**, under `<paths.tests_dir>` (default `tests/`):

1. **`<tooling.framework>` + `<tooling.language>` core**
   - The runner config (e.g. `playwright.config.*` for Playwright) with: one project per browser in `ci.browsers`, an `api` project (no browser), a `setup` project for auth storage-state, `baseURL` from `stack.base_url`, reporters HTML + JUnit + blob written under `<paths.reports_dir>`, trace on first retry, `retries: 2` in CI, full parallelism.
   - Folder structure under `<paths.tests_dir>`: `e2e/`, `api/`, `component/` (if enabled), `a11y/` (if `<tooling.accessibility>`), `visual/` (if enabled), `fixtures/`, `pages/`, `api-clients/`, `data/factories/`, `utils/`, `config/`.
   - A `test-base` fixture file that composes fixtures (auth storage-state, seeded data, typed API client built from `stack.api_spec_path` when present), one sample Page Object, and one sample E2E + one sample API spec wired to `stack.base_url`.
   - Language config (e.g. `tsconfig.json`) and runner scripts in the project manifest (`test`, `test:e2e`, `test:api`, `test:smoke`, `test:report`).
2. **Performance** (if `<tooling.performance>` set): `<paths.tests_dir>/performance/` with a parameterized load script and `thresholds` derived from `gates.performance`.
3. **Contract** (if `<tooling.contract>` set): consumer test skeleton + publish/verify scripts pointing at `contract_broker_url` from config, with a `can-i-deploy` script.
4. **Accessibility** (if `<tooling.accessibility>` set): an a11y + framework helper and a sample scan of one key page.
5. **Visual** (if enabled): a sample screenshot-assertion spec with masking guidance.
6. **Security** (if `<tooling.security>` set): config stubs / scripts for the chosen SAST/SCA/DAST/secret tools.
7. **CI pipeline** for `<ci.platform>`: the platform's pipeline file implementing a fast PR gate (lint, type-check, unit, component, API mocked, contract-consumer, smoke E2E, a11y key pages, visual, SCA/secret, can-i-deploy) and nightly/pre-release stages (full E2E sharded across `ci.shard_count`, performance, DAST, full scans). Use `ci.agents_docker_image` for agents.

**Step 2 — quality rules for every generated file (these are pass/fail, not preferences):**
- Use stable, semantic selectors (role/label/test-id) and fixtures. **No hard waits** — no fixed-duration sleeps/timeouts; rely on the framework's auto-waiting / web-first assertions. Before finalizing, grep the generated tree for hard-wait anti-patterns (e.g. `waitForTimeout`, `sleep(`, `Thread.sleep`, `setTimeout`-based waits) and remove any you introduced.
- Each test owns its data via factories; no shared mutable state between tests.
- No secrets or environment-specific URLs hardcoded — read from config/env.

**Step 3 — post-scaffold validation (do not report success without running this):**
1. Install dependencies if needed and note the exact command for the user.
2. Run the language build / type-check (e.g. `tsc --noEmit` or the project's `build`) and confirm it passes.
3. Run a **framework smoke run** of the sample spec(s) (the runner's list/dry-run plus actually executing the sample smoke test if the environment allows) and confirm the framework loads its config, discovers specs, and the sample passes.
4. If validation fails, fix the scaffold and re-run; only report success once build + smoke pass, or clearly flag what could not be validated and why.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `ci.*`, `gates`, `risk_areas`, `stack.*`) is honored; nothing hardcoded (no fixed paths, tools, URLs, or secrets).
- [ ] **Only-enabled scaffolded** — capabilities whose `tooling.*` toggle is unset were skipped and listed in "not scaffolded (and why)".
- [ ] **No hard waits** — the generated tree contains no fixed-duration waits; auto-waiting / web-first assertions used instead (grep-verified).
- [ ] **Validated** — language build/type-check passes and a framework smoke run discovers and executes the sample spec(s); report the actual result (counts), not a prose claim.
- [ ] **Work product named** — output is identified as the 29119-3 **Test Procedure Specification** scaffold (+ Test Data / Environment Requirements) and written under the correct `<paths.tests_dir>` / `<paths.reports_dir>` locations.
- [ ] **Residual risk stated** — name what is NOT covered (e.g. the scaffold ships sample specs only — it does not constitute real test coverage; risk areas in `risk_areas` still need designed tests) per ISTQB Principle 1 (testing shows the presence of defects, not their absence).

## After scaffolding

List what you created, the exact install/setup commands the user should run, the validation result (build + smoke), and the "not scaffolded (and why)" list. Then hand off:
- `/qa:test-design <feature>` to derive test conditions/cases (the design that the scaffold's procedures will execute).
- `/qa:implement <feature>` to fill the scaffold with real automated tests for a feature.
- `/qa:test-data` / `/qa:test-env` to extend factories/fixtures and environment setup.
- `/qa:flaky-hunt` / `/qa:self-heal` later, for reliability and maintenance of the resulting suite.
