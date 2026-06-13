# Test Environment Requirements — {{environment.name}}

> ISO/IEC/IEEE 29119-3 **Test Environment Requirements** work product. Produced by `/qa:test-env`.
> Concise & fillable. Pull project-specific values from `qa.config.yml` — do not hardcode. Written to `<paths.docs_dir>/environments/<environment.name>.md`.
> Test object: {{project.name}} · Release: {{release}} · Author: {{author}} · Date: {{date}}

## Document control

| Field | Value |
|---|---|
| **Environment ID** | `ENV-<name>` |
| **Maps to config** | one of `environments[]` in `qa.config.yml` (`<environment.name>` / `<environment.url>`) |
| **Status** | draft · ready · deprecated |
| **Owner / approver** | from `team` (e.g. `<team.eng_lead>`, `<team.qa_lead>`) |
| **Related documents** | Test Plan, Test Strategy, `<stack.api_spec_path>` |
| **Change log** | date · author · change |

## 1. Environment name & purpose

| Field | Value |
|---|---|
| **Name** | `<environment.name>` (e.g. ci / qa / staging) |
| **Purpose** | `<environment.purpose>` (PR gate · integration · pre-release/perf/security) |
| **Test levels supported** | component · integration · system · acceptance |
| **Test types it must support** | only enabled `<tooling.*>` (e2e, api, contract, performance, accessibility, security, visual) |
| **Lifetime** | ephemeral (per-PR) · persistent · on-demand |
| **Risk coverage** | which `risk_areas` (`critical`/`high`/`medium`) this env exercises |

## 2. Components / services & versions

List every deployable unit and its pinned version. Source of truth for "what is under test".

| Component / service | Role | Version / image tag | Source | Health endpoint |
|---|---|---|---|---|
| `<project.name>` web | frontend (`<stack.frontend>`) | `vX.Y.Z` | build artifact / image | `<environment.url>/healthz` |
| `<project.name>` API | backend (`<stack.backend>`) | `vX.Y.Z` | image | `<base_url_api>/health` |
| Database | persistence | engine + version | container / managed | — |
| Cache / queue | infra | version | — | — |
| Test runner image | runs `<tooling.e2e>` | `<ci.agents_docker_image>` | CI | n/a |

## 3. Configuration (env vars, feature flags)

Declare required configuration. Mark secrets as `<from secrets store>` — never inline a value.

**Environment variables**

| Variable | Purpose | Value / source | Secret? |
|---|---|---|---|
| `BASE_URL_WEB` | app under test | `<base_url_web>` | no |
| `BASE_URL_API` | API under test | `<base_url_api>` | no |
| `API_SPEC_PATH` | contract/API source of truth | `<stack.api_spec_path>` | no |
| `DATABASE_URL` | data store connection | `<from <test_data.secrets_store>>` | yes |
| `<CONTRACT_BROKER_URL>` | contract verification (if `<tooling.contract>` ≠ none) | `<tooling.contract_broker_url>` | no |

**Feature flags**

| Flag | State for this env | Rationale |
|---|---|---|
| `<flag-name>` | on / off | match release scope |

## 4. Data state & seeding

Per `test_data` config — synthetic only.

| Field | Value |
|---|---|
| **Strategy** | `<test_data.strategy>` (factories · fixtures · db-seed) |
| **Seed via** | `<test_data.seed_via>` (api · db · both) |
| **Required baseline state** | accounts, catalog, fixtures needed before execution |
| **Sensitive-data rule** | `<test_data.sensitive_data_rule>` — never real PII |
| **Reset / teardown** | how state is reset between runs (truncate · re-seed · ephemeral DB) |
| **Idempotency** | re-seeding is repeatable and isolated per shard/worker |

## 5. Access, credentials & secrets source

Never store secret values here — only their source.

| Field | Value |
|---|---|
| **Access (network)** | URL `<environment.url>` · VPN/allowlist · auth method |
| **Test user accounts** | roles needed (per `risk_areas` authorization), provisioned via `<test_data.seed_via>` |
| **Secrets source** | `<test_data.secrets_store>` (jenkins-credentials · vault · env) |
| **CI auth** | injected by `<ci.platform>` (e.g. `JENKINS_USER` / `JENKINS_API_TOKEN` as env vars) |
| **Rotation / scope** | least-privilege, rotated, env-scoped |

## 6. Provisioning steps

Ordered, repeatable steps to stand the environment up.

1. Provision infra (`<environment.name>`) — ephemeral or target host `<environment.url>`.
2. Deploy components at the versions in §2 (`<ci.agents_docker_image>` for the runner).
3. Inject configuration from §3 and secrets from `<test_data.secrets_store>`.
4. Seed data per §4 (`<test_data.strategy>` / `<test_data.seed_via>`).
5. Stand up mocks / virtual services per §7 (`<tooling.mocking>`).
6. Run the readiness checklist in §8 — gate execution on PASS.

> Automation reference: provisioning lives under `<paths.tests_dir>`; CI runs on `<ci.platform>`.

## 7. External dependencies & service virtualization / mocking

| Dependency | Real or virtualized | Tool / mode | Contract source | Notes |
|---|---|---|---|---|
| Payment gateway | virtualized | `<tooling.mocking>` (playwright-route · msw · prism · wiremock) | `<stack.api_spec_path>` | sandbox only — never live charges |
| 3rd-party API | real / virtualized | `<tooling.mocking>` | `<tooling.contract>` (`<tooling.contract_broker_url>`) | contract-backed |
| Email / notifications | virtualized | mock sink | — | assert-only |

> Mocks must be **contract-backed** (`<tooling.contract>`): the virtual service conforms to `<stack.api_spec_path>` so tests stay traceable to the contract, not to an invented stub.

## 8. Readiness checklist (PASS/FAIL)

Gate test execution on this. Every item must be **PASS** before the env is declared ready.

| # | Check | Expected | Result |
|---|---|---|---|
| 1 | All §2 components deployed at pinned versions | versions match | PASS / FAIL |
| 2 | Health endpoints green | 200 / healthy | PASS / FAIL |
| 3 | §3 config & feature flags applied | matches release scope | PASS / FAIL |
| 4 | Secrets resolved from `<test_data.secrets_store>` | no missing/inline secrets | PASS / FAIL |
| 5 | Baseline data seeded (§4) | synthetic, repeatable | PASS / FAIL |
| 6 | Test accounts/roles present | per `risk_areas` auth needs | PASS / FAIL |
| 7 | Mocks/virtual services up & contract-backed (§7) | conform to `<stack.api_spec_path>` | PASS / FAIL |
| 8 | Enabled `<tooling.*>` suites can reach targets | smoke run green | PASS / FAIL |
| 9 | Connectivity / access verified | reachable from `<ci.platform>` | PASS / FAIL |

**Readiness verdict:** READY (all PASS) / NOT READY (any FAIL — list blockers).

## Coverage & residual summary

- **Components:** N services pinned · **Config:** M env vars + K flags declared.
- **Dependencies:** E external, V virtualized (contract-backed) · **Checks:** total readiness items, # PASS / # FAIL.
- **Risk coverage:** which `risk_areas` tiers this env supports.

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISO/IEC/IEEE 29119-3 (Test Environment Requirements) and ISTQB CTFL v4.0. See `docs/ISTQB-COMPLIANCE.md`.*
