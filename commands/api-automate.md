---
description: Build or extend automated API tests (REST) from the OpenAPI spec — schema validation, CRUD, auth/role matrix, negative & boundary, data-driven. Use for API test automation.
argument-hint: "<endpoint / resource / feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# API test automation: $ARGUMENTS

**ISTQB process:** Test automation (CT-TAE) at the **integration/API test level** (CTFL §2.2). Black-box techniques (CTFL §4.2) applied to API inputs.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## API contract
```!
echo "--- OpenAPI ($(ls openapi.* swagger.* 2>/dev/null)) ---"; sed -n '1,120p' openapi.yaml openapi.json swagger.* 2>/dev/null | head -120
echo "--- existing api tests ---"; ls -1 tests/api 2>/dev/null
```

## Your task

Target from `$ARGUMENTS` (endpoint/resource/feature). The OpenAPI spec (`stack.api_spec_path`) is the test basis. Build automated API tests using Playwright's `request` context (`tooling.api`) with typed clients.

Cover, per endpoint, applying ISTQB techniques:
1. **Happy path** — valid requests (EP valid partitions) → correct status, body, headers.
2. **Negative & boundary** — invalid payloads, missing/extra fields, wrong types, malformed JSON, oversized inputs (EP invalid + BVA on numeric/length limits) → correct 4xx + error envelope.
3. **Authorization (decision table / role matrix)** — unauthenticated, wrong-role, expired/tampered token → 401/403; check IDOR/BOLA (one user can't access another's resource).
4. **Schema validation** — assert every response against the OpenAPI schema so drift is caught automatically.
5. **State & side effects** — verify via follow-up GET / DB; idempotency of repeated POST/PUT/DELETE.
6. **Pagination, filtering, sorting; error contract; status codes & headers (CORS, caching, rate-limit).**

Engineering: **data-driven** the repeated partitions/boundaries; typed clients generated/derived from the spec; reuse fixtures and seeding (`/qa:test-data`); synthetic data only. Keep tests independent and parallel-safe. Tag by resource and risk for CI selection.

Place under `tests/api/`, run them (`npx playwright test tests/api/...`), fix failures, and wire into the PR gate. For consumer/provider **contract** testing use `/qa:contract-sync`; for load use `/qa:perf-test`. Report coverage of endpoints and the techniques applied.
