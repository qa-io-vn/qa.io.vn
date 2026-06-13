---
description: Build or extend automated API tests (REST) from the OpenAPI spec — schema validation, CRUD, auth/role matrix, negative & boundary, data-driven. Produces ISO/IEC/IEEE 29119-3 Test Procedure Specifications (automated API scripts) plus a Test Execution Log when run. Use for API test automation.
argument-hint: "<endpoint / resource / feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# API test automation: $ARGUMENTS

**ISTQB process:** Test automation (CT-TAE) applied at the **component integration / API test level** (CTFL v4.0 §2.2.1). Black-box techniques (CTFL v4.0 §4.2) applied to API inputs. The OpenAPI spec is the **test basis**.
**Work product:** ISO/IEC/IEEE 29119-3 **Test Procedure Specification(s)** — the automated API test scripts — plus a **Test Execution Log / Test Results** when executed. (No dedicated template; the closest reference structure is the 29119-3 Test Procedure Specification.)

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## API contract discovery
```!
echo "--- declared spec (from qa.config.yml stack.api_spec_path) ---"; grep -E 'api_spec(_path)?:' qa.config.yml 2>/dev/null
echo "--- spec files found in repo ---"; ls openapi.* swagger.* api-spec.* 2>/dev/null || echo "(none at root — check stack.api_spec_path)"
echo "--- existing api tests (informational — resolve real dir from paths.tests_dir) ---"; ls -1R tests/api 2>/dev/null | head -40
```

## Step 0 — Read config & validate input (do this first)

1. Read `qa.config.yml` from the block above. If it printed `MISSING`, tell the user config is absent, suggest `/qa:qa-init`, and proceed only with documented defaults the user confirms — do **not** invent paths, tools, or a spec location. Resolve the config-derived inputs in scope (nothing about paths/tools is hardcoded; everything comes from config):
   - `<stack.api_spec>` / `<stack.api_spec_path>` — the OpenAPI/Swagger spec that is the **test basis**. If `<stack.api_spec>` is `none` or the path resolves to nothing, stop and route to `/qa:contract-sync` or ask the user for the contract source before designing tests.
   - `<tooling.api>` — the API test driver (e.g. Playwright `request` context); generate/derive typed clients from the spec.
   - `<tooling.language>` — language for the typed clients and specs.
   - `<paths.tests_dir>` — root for automated tests (write API tests under its `api/` subtree per project convention).
   - `<tooling.contract>` and `<tooling.mocking>` — contract backstop and service virtualization for unstable/external dependencies.
   - `<tooling.performance>` — load-test tool for the `/qa:perf-test` handoff.
   - `risk_areas`, `gates`, `environments`, `test_data` — prioritization, error-contract gates, target environment (`base_url_api`), and the synthetic-data rule (`test_data.sensitive_data_rule`).
2. Resolve the automation target from `$ARGUMENTS` (which endpoint / resource / feature):
   - **If `$ARGUMENTS` is non-empty:** that is the target. Map it to the matching path(s)/operation(s) in the spec.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user which endpoint/resource/feature to automate. If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** (typically authentication/authorization) and state explicitly that you defaulted there and why.
3. Confirm the resolved target and the spec operations it maps to before writing any test.

## Step 1 — Derive test conditions per operation (test basis → conditions)

For each in-scope operation (method + path) in the spec, derive conditions covering these categories. Apply ISTQB black-box techniques and record the technique per condition:

1. **Happy path** — valid requests (Equivalence Partitioning, valid partitions) → assert correct status code, response body, and headers against the spec.
2. **Negative & boundary** — invalid payloads, missing/extra fields, wrong types, malformed JSON, oversized inputs (EP invalid partitions + Boundary Value Analysis — state **2-value** or **3-value** — on numeric ranges and string-length limits) → assert correct 4xx status and the documented error envelope.
3. **Authorization (decision table / role matrix)** — unauthenticated, wrong-role, expired/tampered token → 401/403; and an object-level access check (IDOR/BOLA): one user must not access another user's resource. Express the role × resource rules as a decision table.
4. **Schema validation** — assert every response against the OpenAPI schema so contract drift is caught automatically (not just spot-checked fields).
5. **State & side effects** — verify persistence via a follow-up GET (or DB read where allowed); confirm idempotency of repeated POST/PUT/DELETE.
6. **Cross-cutting** — pagination, filtering, sorting; error contract; status codes and headers (CORS, caching, rate-limit) where the spec defines them.

API/integration points are where defects cluster (Principle 4) — negative and authorization paths are mandatory, not optional.

## Step 2 — Engineering rules (determinism & maintainability)

1. **Data-driven** the repeated partitions/boundaries (one parameterized case feeds many EP/BVA rows) rather than copy-paste cases.
2. Use **typed clients generated/derived from the spec** in `<tooling.language>`, so the test code tracks the contract.
3. Reuse fixtures and seeding via `/qa:test-data`; obey `test_data.sensitive_data_rule` — **synthetic data only, never real PII**.
4. Keep every test **independent and parallel-safe**: no shared mutable state, explicit setup/teardown, each test owns and cleans its own data.
5. **Tag** each test by resource and risk tier (from `risk_areas`) so CI can select smoke vs full.
6. Virtualize unstable/external dependencies via `<tooling.mocking>` and back any mocked interface with `/qa:contract-sync` so doubles cannot drift.

## Step 3 — Implement, run & report

1. Place tests under `<paths.tests_dir>` (the `api/` subtree per project convention) — do **not** hardcode a directory; resolve it from config.
2. Run them with the configured `<tooling.api>` driver against the appropriate `environments` entry (`base_url_api`), fix failures, and wire the smoke subset into the PR gate (full set scheduled).
3. Report **coverage as counts**: operations in scope, operations covered, conditions/techniques applied per operation, and operations/conditions deferred — as numbers, not prose.

## Output

The command produces:
1. **ISO/IEC/IEEE 29119-3 Test Procedure Specification(s)** — the automated API test scripts, written under `<paths.tests_dir>` (`api/` subtree).
2. A **Test Execution Log / Test Results** — the run output when tests are executed.
3. A short **coverage summary** (counts) of operations and techniques covered, plus what was deferred.

Then run the Self-check below.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`stack.api_spec`/`stack.api_spec_path`, `paths.tests_dir`, `tooling.api`, `tooling.language`, `tooling.contract`, `tooling.mocking`, `tooling.performance`, `gates`, `risk_areas`, `environments`, `test_data`) is honored; no path, tool, or spec location is hardcoded.
- [ ] **Traceability intact** — the chain test basis (OpenAPI operation) -> test condition -> case -> coverage item -> procedure/script -> result (-> defect) is preserved and bidirectional; no orphan operations or cases.
- [ ] **Measurable** — output states counts/coverage (operations in scope, covered, deferred; techniques applied) rather than prose claims.
- [ ] **Residual risk stated** — name the operations, error paths, or auth scenarios NOT covered (and any reliance on mocks/virtualization that could drift) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as ISO/IEC/IEEE 29119-3 **Test Procedure Specification(s)** (automated API scripts) plus the **Test Execution Log** when run, written to the correct `<paths.tests_dir>` location.

## Handoff

- For consumer/provider **contract** testing (and to back any mocked interface) use `/qa:contract-sync`.
- For **load/performance** of these endpoints use `/qa:perf-test` (with `<tooling.performance>`).
- For broader **component/system integration** design (test doubles, integration strategy, interface coverage) use `/qa:integration-test`.
- For seeding/fixtures use `/qa:test-data`; for full end-to-end across the UI use `/qa:web-automate`.
- Route spec ambiguities or contract gaps (the test basis) to `/qa:static-review`; flaky API tests to `/qa:flaky-hunt`.
