---
description: Define and provision a test environment, producing the ISO/IEC/IEEE 29119-3 Test Environment Requirements work product driven by qa.config.yml. Use to set up, document, or verify a test environment (env provisioning, not data factories).
argument-hint: "[environment name, e.g. ci | qa | staging]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test environment provisioning & configuration

**ISTQB process:** Test implementation — set up/configure the **test environment** so testware can execute (CTFL v4.0 §1.4; test-tool/environment management CTFL §6). This is a **Test Automation Engineering (CT-TAE, Specialist)** activity per `docs/ISTQB-COMPLIANCE.md`; treat configuration-management-of-testware details as Advanced/Specialist and **verify any section number against the current syllabus** before asserting one.

**Work product:** ISO/IEC/IEEE 29119-3 **Test Environment Requirements** (per `docs/ISTQB-COMPLIANCE.md` §11) — testware documenting the components, configuration, data state, dependencies/virtualization, and readiness gate for one environment.

**Scope boundary:** this command owns **environment provisioning** (services, versions, config, mocks, readiness). It does **not** build data factories/builders — that is `/qa:test-data`. This command declares the *required baseline data state*; `/qa:test-data` produces the factories that populate it.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING"
```

## Your task

1. **Config guard.** If the block above printed `MISSING`, **stop** and tell the user to run `/qa:qa-init` first. Do not provision against assumptions. Otherwise read `paths.*`, `tooling.*`, `ci.*`, `environments[]`, `risk_areas`, and `test_data.*` from `qa.config.yml` and honor them; never hardcode paths, tools, or URLs.

2. **Resolve the target environment** from `$ARGUMENTS`:
   - If `$ARGUMENTS` names an entry in `environments[]`, use it.
   - If `$ARGUMENTS` is empty: if `environments[]` has exactly one entry, use it; if it has several, ask which one (list them by `name`/`purpose`); if `environments[]` is absent, default to a single `ci` (ephemeral, PR-gate) environment and say so.
   - If `$ARGUMENTS` names an environment not in config, ask whether to add it to `environments[]` before proceeding.

3. **Define Test Environment Requirements** for the resolved environment, following `${CLAUDE_PLUGIN_ROOT}/templates/test-environment-template.md`. Capture, per its sections:
   - **Components/services & pinned versions** (web `<stack.frontend>`, API `<stack.backend>`, datastore, runner `<ci.agents_docker_image>`) with health endpoints.
   - **Configuration**: env vars, base URLs (`<stack.base_url_web>` / `<stack.base_url_api>`), `<stack.api_spec_path>`, feature flags — secrets referenced from `<test_data.secrets_store>`, never inline.
   - **Required baseline data state** only (strategy `<test_data.seed_via>`); the factories themselves are `/qa:test-data`'s output.
   - **External dependencies**: which are real vs **virtualized**, using `<tooling.mocking>`; mocks must be contract-backed against `<stack.api_spec_path>` / `<tooling.contract>`.
   - **Test levels/types supported**: component / integration / system / acceptance, limited to the **enabled** `<tooling.*>` toggles.
   - **Risk coverage**: which `risk_areas` tiers (`critical`/`high`/`medium`) this environment exercises.

4. **Provision / document** the environment so it is **reproducible, isolated, and parallel-safe** (unique per shard/worker so concurrent runs don't collide): produce the setup artifacts (docker-compose, env files, seed hooks, mock servers) under `<paths.tests_dir>`, consistent with `<ci.agents_docker_image>` and the config base URLs. If a target subdirectory does not exist, create it.

5. **Verify readiness.** Run the template's §8 **readiness checklist** (PASS/FAIL): components deployed at pinned versions, health endpoints green, config/flags applied, secrets resolved from `<test_data.secrets_store>`, baseline data seeded, test accounts/roles present, mocks contract-backed, enabled `<tooling.*>` suites can reach targets, connectivity from `<ci.platform>` verified. Run a smoke check where possible. **Gate the environment as READY only if every item is PASS**; otherwise mark NOT READY and list each blocker.

## Output

Write the **Test Environment Requirements** for the resolved environment to `<paths.docs_dir>/environments/<environment.name>.md`, using `${CLAUDE_PLUGIN_ROOT}/templates/test-environment-template.md`. Commit the provisioning artifacts (docker-compose / env / mock config) under `<paths.tests_dir>`. End with a **coverage summary**: N components pinned, M env vars + K flags declared, E external deps (V virtualized), readiness items # PASS / # FAIL, and which `risk_areas` tiers are covered. Never put secret values in the repo — reference `<test_data.secrets_store>` only.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `ci.*`, `environments[]`, `risk_areas`, `test_data.*`) is honored; no hardcoded paths, tools, or URLs.
- [ ] **Boundary respected** — this output declares the *required* data state only; data factories/builders are deferred to `/qa:test-data` (no factories authored here).
- [ ] **Measurable** — output states counts (components, env vars, flags, deps, readiness PASS/FAIL) rather than prose claims.
- [ ] **Readiness gated** — the §8 checklist is executed; the environment is declared READY only if every item is PASS, and each FAIL is listed as a blocker.
- [ ] **Residual risk stated** — name what is NOT covered (e.g. dependencies still real, levels/types not supported by enabled tooling) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Environment Requirements** and written to `<paths.docs_dir>/environments/<environment.name>.md`.

---

## Handoffs

- **`/qa:test-data`** — this command provisions the environment and declares the required baseline data state; hand off to `/qa:test-data` to build the typed factories/builders that populate it (env provisioning here vs data factories there).
- **`/qa:scaffold`** — if no automation framework exists yet under `<paths.tests_dir>`, run `/qa:scaffold` first to set up the runner/fixtures this environment must support.
- **`/qa:fix-ci`** / **`/qa:fix-jenkins`** — for CI-side test-environment failures (runner image, agents, pipeline wiring on `<ci.platform>`), hand off to these.
- **`/qa:implement`** — once the environment is READY, run `/qa:implement` to execute automated tests against it.
