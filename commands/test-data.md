---
description: Generate typed test-data factories, builders, fixtures, and seeding/cleanup helpers per qa.config.yml. Use when tests need data setup.
argument-hint: "<entity or domain, e.g. user, order>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test data for: $ARGUMENTS

**ISTQB process:** Test implementation (CTFL v4.0 §1.4) — prepare the test data and testware needed for execution.

**Work product:** ISO/IEC/IEEE 29119-3 **Test Data / Environment Requirements** (per `docs/ISTQB-COMPLIANCE.md`) — testware documenting the data factories/fixtures, seeding/cleanup lifecycle, and traceability to test conditions. Follow the template at `${CLAUDE_PLUGIN_ROOT}/templates/test-data-template.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING"
```

## Your task

**Step 0 — Read config and resolve placeholders.** Parse `qa.config.yml` from the block above. If it printed `MISSING`, stop and tell the user to run `/qa:qa-init` first (do not invent paths/tools). Resolve these fields and use them throughout — never hardcode a path or tool:
- `<paths.tests_dir>`, `<paths.docs_dir>`, `<paths.reports_dir>`
- `<test_data.factories_path or 'data/factories'>`, `<test_data.strategy or 'factories'>`, `<test_data.seed_via or 'api'>`, `<test_data.secrets_store>`, `<test_data.sensitive_data_rule>`
- `<stack.api_spec or 'none'>`, `<stack.api_spec_path>`, `<stack.language>`, `<tooling.e2e>`, `<tooling.api>`
- `<risk_areas.*>` (to tag each entity's owning area)

**Step 1 — Resolve the target entity/domain.** Take the entity from `$ARGUMENTS`. If `$ARGUMENTS` is empty, do NOT guess — follow this decision tree:
1. Ask: "Which entity/domain do you need data for? (e.g. user, order, payment, inventory)"
2. When the user answers, validate it maps to at least one **test condition** (from `/qa:test-design` output in `<paths.docs_dir>`) OR a schema definition in `<stack.api_spec_path>` (when `<stack.api_spec>` is `openapi`).
3. If neither maps — i.e. there is no test condition driving the data need — hand off to `/qa:test-design` first to identify the conditions that require data, then return here.

Do not proceed to Step 2 without a clear entity/domain backed by a condition or schema.

**Step 2 — Build typed factories/builders.** Follow `<test_data.strategy or 'factories'>`: create typed factories/builders under `<paths.tests_dir>/<test_data.factories_path or 'data/factories'>`. If that path does not exist, create it. Each factory MUST:
- produce data valid against the contract — derive shapes from `<stack.api_spec_path>` (OpenAPI) where `<stack.api_spec>` is `openapi`;
- be parallel-safe — generate a unique identifier (UUID or timestamp+run-id suffix) per call so concurrent shards (`ci.shard_count`) never collide;
- be written in `<stack.language>` and match repo conventions already present under `<paths.tests_dir>`.

**Step 3 — Add seeding + paired teardown.** Add seeding helpers using `<test_data.seed_via or 'api'>` (decision rule: prefer `api` — it exercises real paths and respects domain invariants; use `db` only for bulk setup). Every `create` MUST have a matching teardown (`afterEach`/`afterAll`) that removes created records in reverse dependency order, so runs leave no residue and stay independent.

**Step 4 — Enforce sensitive-data rules.** Apply `<test_data.sensitive_data_rule>`: synthetic/anonymized data only, never real PII (no real names, emails, payment details, or regulated identifiers). Pull any credentials/tokens from `<test_data.secrets_store>` at runtime — never hardcode literals in factories or commit them.

**Step 5 — Wire into fixtures.** Wire the factories into the existing fixtures under `<paths.tests_dir>/fixtures/` (for `<tooling.e2e>`/`<tooling.api>`) so specs get data declaratively. If no fixtures directory exists, hand off to `/qa:scaffold` first to set up the framework, then return here.

## Output

Write the **Test Data / Environment Requirements** to `<paths.docs_dir>/TEST-DATA-<entity>.md`, following `${CLAUDE_PLUGIN_ROOT}/templates/test-data-template.md`:
- §1 Entity/domain: model, relationships, owning `<risk_areas.*>`, source of truth (`<stack.api_spec_path>`).
- §2 Factory/builder directory tree + API documentation (signatures, options, in-test example in `<stack.language>`).
- §3 Data lifecycle: seeding strategy (`<test_data.seed_via or 'api'>`) and paired cleanup/teardown pattern.
- §4 Sensitive-data handling: redaction/anonymization rules applied; secrets via `<test_data.secrets_store>`.
- §5 **Traceability table** (bidirectional): factory name | test conditions it supports | test cases using it.
- §6 **Coverage summary** (measurable): N factories created, M test conditions covered, X test cases ready to use them, % coverage, and every in-scope test condition WITHOUT a data factory (residual gaps, with reason/plan).

Commit the implemented factories to `<paths.tests_dir>/<test_data.factories_path or 'data/factories'>`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `test_data.*`, `stack.*`, `tooling.*`, `risk_areas`) is honored; no hardcoded path, tool, or secret.
- [ ] **Secrets & PII clean** — `grep -riE 'api[_-]?key|token|password|secret|auth' <paths.tests_dir>/<test_data.factories_path or 'data/factories'>` finds no literal credentials (all via `<test_data.secrets_store>`); any PII-like value is synthetic/anonymized per `<test_data.sensitive_data_rule>`.
- [ ] **Parallel-safe & paired** — every factory emits a unique identifier per call; every `create`/seed has a matching teardown in reverse dependency order.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure (-> result) is preserved and bidirectional; no factory without a condition, no in-scope condition without a data source.
- [ ] **Measurable** — output states counts/coverage (N factories, M conditions covered, % coverage, gaps) rather than prose claims.
- [ ] **Residual risk stated** — name the in-scope conditions left WITHOUT a data factory and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Data / Environment Requirements** and written to `<paths.docs_dir>/TEST-DATA-<entity>.md`.

---

## Handoffs

- **Inbound — no test conditions yet:** if `$ARGUMENTS`/the chosen entity isn't backed by a test condition, run `/qa:test-design` first to derive the conditions (and their data requirements), then return here. `/qa:test-design` produces the conditions this command builds data for.
- **Sibling — environment vs. data:** if the test environment (services, mock servers, docker-compose, DB state) is not yet set up, run `/qa:test-env` first — that command owns environment provisioning; this command owns the data factories/builders that populate it. `/qa:test-env` reciprocally hands off here for the data.
- **No framework yet:** if no fixtures/framework exists under `<paths.tests_dir>`, run `/qa:scaffold` first, then return here.
- **Outbound — automate:** to turn test cases into automated specs wired to these factories, hand off to `/qa:implement` (which provisions data via these `/qa:test-data` factories rather than inline literals).
