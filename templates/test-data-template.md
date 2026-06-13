# Test Data / Environment Requirements — {{item}}

> ISO/IEC/IEEE 29119-3 **Test Data Requirements** + **Test Environment Requirements** work product. Produced by `/qa:test-data`.
> Test basis: {{source}} · Generated: {{date}} · Author: {{author}}
> Written to `<paths.tests_dir>/data/` (factories) and recorded in `<paths.docs_dir>`. Strategy follows `test_data.strategy`; seed via `test_data.seed_via`; secrets from `test_data.secrets_store`. Synthetic-only — never real PII (`test_data.sensitive_data_rule`).

## 1. Entity / domain

The data entities under management and their relationships — the domain model the factories build against.

| Entity | Purpose | Key attributes | Relationships / dependencies | Owning area (`risk_areas`) |
|---|---|---|---|---|
| `<EntityName>` | … | id, … | belongs-to `<…>`, requires `<…>` | critical / high / medium |

- **Domain notes:** invariants, required-before-create order, uniqueness constraints.
- **Source of truth:** {{stack.api_spec_path}} (schema) where applicable.

## 2. Factory / builder directory tree & API

Factories/builders live under `<paths.tests_dir>/data/` and build entities for `<tooling.e2e>` (+ `<tooling.api>`) tests in `<tooling.language>`.

### Directory tree

```
<paths.tests_dir>/data/
├── factories/
│   ├── <entity>.factory.<ext>      # build/create <Entity>
│   └── index.<ext>                 # registry / barrel
├── builders/
│   └── <entity>.builder.<ext>      # fluent overrides
├── seed/
│   └── seed.<ext>                  # seeding orchestration
└── README.md
```

### API (signatures)

| Factory / builder | Signature | Builds | Persisted via |
|---|---|---|---|
| `<entity>Factory.build` | `build(overrides?: Partial<Entity>): Entity` | in-memory entity | none |
| `<entity>Factory.create` | `create(overrides?: Partial<Entity>): Promise<Entity>` | persisted entity | `test_data.seed_via` (api / db) |
| `<Entity>Builder` | `.with<Attr>(v).build()` / `.create()` | customized entity | as above |

### In-test example

```ts
// <paths.tests_dir>/<feature>.spec.<ext>
const user = await userFactory.create({ role: 'standard' });   // synthetic, persisted
const order = await new OrderBuilder()
  .withCustomer(user)
  .withStatus('pending')
  .create();
// ... exercise SUT against `order` ...
```

## 3. Data lifecycle

### Seeding strategy
- **Strategy:** `test_data.strategy` (factories / fixtures / db-seed).
- **Seed channel:** `test_data.seed_via` (api / db / both) — prefer API seeding so data respects domain invariants.
- **Scope:** per-test (isolated) vs. per-suite (shared reference data) — state which and why.
- **Determinism:** seeded values are reproducible; unique fields namespaced per run (e.g. run-id suffix) to avoid collisions across CI shards (`ci.shard_count`).

### Teardown / cleanup pairing
Every `create` is paired with a teardown so tests leave no residue (independence + repeatability).

| Created entity | Created in | Cleaned up in | Mechanism |
|---|---|---|---|
| `<Entity>` | factory `create` | `afterEach` / `afterAll` | delete via API / db rollback / transaction |

- **Pairing rule:** track created IDs and tear down in reverse dependency order.
- **Environment reset:** which `environments` entry is reset between runs and how (ephemeral `ci` vs. shared `qa`/`staging`).

## 4. Sensitive-data handling

- **Synthetic / anonymized only:** all data is generated or anonymized — `test_data.sensitive_data_rule` (synthetic-only — never real PII). No production data copied into tests.
- **No PII:** no real names, emails, payment details, or regulated identifiers. Use deterministic fake generators within synthetic ranges.
- **Secrets store:** credentials/tokens come from `test_data.secrets_store` (jenkins-credentials / vault / env) — never hardcoded in factories or committed. Surface to tests via environment at runtime only.
- **Masking:** any value that resembles sensitive data is masked in logs/reports (`<paths.reports_dir>`).

## 5. Traceability table

Links each factory back to the test conditions it enables and the test cases that consume it (bidirectional: condition ↔ data ↔ case).

| Factory / builder | Test conditions supported | Test cases using it |
|---|---|---|
| `<entity>Factory` | TCond-01, TCond-… | TC-{{item}}-001, TC-… |
| `<Entity>Builder` | TCond-… | TC-… |

- No factory exists without a condition it serves; no in-scope condition lacks a data source (see §6).

## 6. Coverage summary

- **Factories / builders:** **N** total (`<N>` factories, `<N>` builders).
- **Conditions covered:** **M** test conditions have a backing data source.
- **Conditions WITHOUT data (residual gap):** list each in-scope condition that has **no** factory yet, with reason and plan.

| Test condition | Risk (`risk_areas`) | Data status | Reason / plan if missing |
|---|---|---|---|
| TCond-… | critical / high | covered by `<factory>` | — |
| TCond-… | medium | **NO DATA** | … (e.g. needs db-seed fixture next sprint) |

- **Coverage:** M of (M + gaps) in-scope conditions have data = **`<pct>`%**.

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISO/IEC/IEEE 29119-3 (Test Data Requirements & Test Environment Requirements) and ISTQB CTFL v4.0. See `docs/ISTQB-COMPLIANCE.md`.*
