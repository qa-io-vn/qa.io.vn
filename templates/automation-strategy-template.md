# Test Automation Strategy / Plan — {{project.name}}

> ISO/IEC/IEEE 29119-3 work product: **Test Automation Strategy / Plan**. ISTQB **Test Automation Engineer (CT-TAE)** generic Test Automation Architecture (**gTAA**). Produced by `/qa:automation-strategy`.
> Long-lived & project-general (the *strategy*); the release-scoped automation backlog lives in the Test Automation Plan (`/qa:automate`). Use strict ISTQB Glossary terminology. Omit any sub-section whose tool is `none` in `tooling`. Prose with tables, not bullet walls.
> Test object: {{project.name}} ({{project.type}}) · Author: {{team.qa_lead}} · Generated: {{date}} · Version/Status: `<fill>`
> **Write to:** `<paths.docs_dir>/automation-strategy.md`. Framework root: `<paths.tests_dir>`. Reports: `<paths.reports_dir>`.

## Document control
Work product ID, version/status, author ({{team.qa_lead}}), approvers ({{team.qa_manager}}, {{team.eng_lead}}), related documents (Organizational Test Strategy at `<paths.docs_dir>/strategy.md`, Test Automation Plan, {{stack.api_spec_path}}), change log.

| Field | Value |
|---|---|
| Work product | Test Automation Strategy / Plan (ISO/IEC/IEEE 29119-3) |
| Version / status | `<fill>` |
| Author | {{team.qa_lead}} |
| Approvers | {{team.qa_manager}} · {{team.eng_lead}} · {{team.product_owner}} |
| Related docs | `<paths.docs_dir>/strategy.md` · Test Automation Plan · {{stack.api_spec_path}} |

## 1. Objectives & scope
- **Objectives:** what automation must achieve for {{project.name}} (regression confidence, fast PR feedback, ROI vs manual cost). Automation is an **investment decision**, not "automate everything" (CT-TAE / CTFL §6).
- **In scope:** only enabled `tooling` types — e2e ({{tooling.e2e}}), unit ({{tooling.unit}}), component ({{tooling.component}}), api ({{tooling.api}}), contract ({{tooling.contract}}), performance ({{tooling.performance}}), accessibility ({{tooling.accessibility}}), visual ({{tooling.visual}}), security ({{tooling.security.sast}}/{{tooling.security.sca}}/{{tooling.security.dast}}/{{tooling.security.secrets}}), mocking ({{tooling.mocking}}), mobile ({{tooling.mobile}}).
- **Out of scope (kept manual):** subjective/usability, exploratory, one-off, volatile UI, human-judgment checks — one-line justification each.
- **Risk focus:** depth concentrated on `risk_areas` (critical → high → medium).

| Objective | Success measure (metric/gate) | Priority |
|---|---|---|
| `<fill>` | e.g. PR gate < N min; pass rate ≥ {{gates.min_pass_rate_pct}}% | `<fill>` |

## 2. gTAA architecture layers (CT-TAE)
Layered generic Test Automation Architecture; each layer isolated so changes localize (maintainability). Built by `/qa:scaffold` under `<paths.tests_dir>`. Framework: Playwright + {{tooling.language}}.

| gTAA layer | Responsibility | Realization in {{project.name}} |
|---|---|---|
| **Test generation** | Derive/parameterize cases (data-driven, partitions/boundaries, models). | Data factories per {{test_data.strategy}}; parameterized specs; cases from {{stack.api_spec_path}}. |
| **Test definition** | Express cases independently of execution tech (Page Objects, API clients, keywords/fixtures, test data). | POM + typed API clients (from {{stack.api_spec_path}}), reusable fixtures, storage-state auth. |
| **Test execution** | Run cases, set up/tear down, capture results. | {{tooling.e2e}} runner + {{tooling.unit}}; browsers {{ci.browsers}}; sharded ×{{ci.shard_count}} in {{ci.platform}}. |
| **Test adaptation** | Connect to SUT via interfaces (UI/API/CLI/service virtualization). | Web ({{stack.base_url_web}}), API ({{stack.base_url_api}}), mocking {{tooling.mocking}} (contract-backed), mobile {{tooling.mobile}}. |

## 3. Test-level split & pyramid rationale
Prefer the **lowest** level that can verify the check (lower complexity, lower maintenance, faster feedback). Reserve UI E2E for genuine end-to-end journeys. Map levels to enabled `tooling`.

| Level | Tooling | Target share | Rationale (what belongs here) |
|---|---|---|---|
| Component / unit | {{tooling.unit}} · {{tooling.component}} | `<fill>`% | Fast, deterministic logic/contracts of units. |
| Integration / API / contract | {{tooling.api}} · {{tooling.contract}} | `<fill>`% | Service behavior, schema/contract vs {{stack.api_spec_path}}. |
| System / E2E (UI) | {{tooling.e2e}} | `<fill>`% | Critical user journeys only (`risk_areas.critical`). |
| Non-functional | {{tooling.performance}} · {{tooling.accessibility}} · {{tooling.visual}} | `<fill>`% | Perf vs `gates.performance`; a11y vs {{gates.accessibility_standard}}. |

**Pyramid rationale:** wide base, narrow top — push checks down to API/integration to cut flakiness and cost; depth is risk-led by `risk_areas`.

## 4. Tool selection & justification
Only tools enabled in `tooling`. Classify each (CTFL §6) and state benefits *and* risks/costs.

| Capability | Tool (`tooling.*`) | Why selected | Benefit | Risk / cost |
|---|---|---|---|---|
| E2E | {{tooling.e2e}} | `<fill>` | web-first assertions, cross-browser | UI volatility |
| Unit | {{tooling.unit}} | `<fill>` | fast feedback | — |
| Component | {{tooling.component}} | `<fill>` | isolate UI units | — |
| API | {{tooling.api}} | `<fill>` | deterministic, fast | — |
| Contract | {{tooling.contract}} | broker {{tooling.contract_broker_url}} | catches provider/consumer drift | broker upkeep |
| Performance | {{tooling.performance}} | thresholds `gates.performance` | SLA verification | env fidelity |
| Accessibility | {{tooling.accessibility}} | {{gates.accessibility_standard}} | automated a11y checks | partial coverage |
| Visual | {{tooling.visual}} | `<fill>` | regression of rendering | snapshot churn |
| Security | {{tooling.security.sast}} / {{tooling.security.sca}} / {{tooling.security.dast}} / {{tooling.security.secrets}} | OWASP-aligned, CT-SEC | shift-left findings | false positives |
| Mocking / virtualization | {{tooling.mocking}} | contract-backed | isolate unstable deps | mock drift |
| Mobile | {{tooling.mobile}} | matrix {{tooling.mobile_device_matrix}} | device coverage | farm cost |

## 5. CI/CD integration ({{ci.platform}})
- **Pipelines:** fast PR gate → nightly (broad) → pre-release (perf/security on `staging`). Image {{ci.agents_docker_image}}; sharded ×{{ci.shard_count}}; browsers {{ci.browsers}}.
- **Entry → exit gates** (from `gates`): pass rate ≥ {{gates.min_pass_rate_pct}}%; block on severity {{gates.block_on_severity}}; a11y block {{gates.a11y_block_on}}; security block {{gates.security_block_on}}; perf {{gates.performance}}. `can-i-deploy` green before release.
- **Secrets:** from {{test_data.secrets_store}} / env — never committed (e.g. JENKINS_USER, JENKINS_API_TOKEN).
- **Artifacts:** traces, videos, reports → `<paths.reports_dir>`.

| Stage | Trigger | Suites | Gate |
|---|---|---|---|
| PR gate | per-PR | unit + API + smoke E2E | block on {{gates.block_on_severity}} |
| Nightly | schedule | full regression, {{ci.browsers}} | pass ≥ {{gates.min_pass_rate_pct}}% |
| Pre-release | pre-deploy | perf {{tooling.performance}}, security | `gates.performance` / {{gates.security_block_on}} |

## 6. Test environment & data approach
- **Environments:** from `environments` (ci ephemeral PR gate → qa integration → staging pre-release/perf/security).
- **Test data:** strategy {{test_data.strategy}}, seeded via {{test_data.seed_via}}; **{{test_data.sensitive_data_rule}}**; secrets in {{test_data.secrets_store}}.
- **Isolation:** each test builds/tears down its own state (factories), no shared mutable fixtures; mocking {{tooling.mocking}} for unstable third parties (contract-backed).

| Env (`environments`) | Purpose | Data source | Notes |
|---|---|---|---|
| `<fill>` | `<fill>` | {{test_data.seed_via}} | synthetic-only |

## 7. Reporting & automation metrics (CT-TAE)
Reports → `<paths.reports_dir>`. Track over time; state counts/coverage, not prose.

| Metric (CT-TAE) | Definition | Target / gate |
|---|---|---|
| Automation progress | % of selected candidates automated | `<fill>`% |
| Automated pass rate | passed / executed | ≥ {{gates.min_pass_rate_pct}}% |
| Flaky rate | non-deterministic / total runs | < `<fill>`% |
| Execution time | PR gate / full suite duration | < `<fill>` min |
| Maintenance effort | time spent fixing tests vs SUT defects | trend ↓ |
| Defects found by automation | new defects caught | trend |
| Coverage of `risk_areas` | % critical/high areas with automated checks | `<fill>`% |
| Requirements coverage | conditions/cases traced to basis | 100% of in-scope |

## 8. Maintainability & anti-pattern guards
gTAA-aligned guards so the suite stays cheap to own:
- **Stable selectors** (role/test-id), web-first assertions, **no hard waits** / `sleep`.
- **Page Objects / API clients** isolate the test-definition layer from UI/API churn (one change, one place).
- **Data-driven** parameterization where partitions/boundaries repeat the same logic.
- **No interdependent tests**; isolated, idempotent state per test.
- **Flaky quarantine** policy + root-cause (no blind retries to hide defects).
- **Lowest-level-first**: don't automate at UI what an API check verifies.
- **DRY fixtures**, no copy-paste suites; review automation code like production code.

| Anti-pattern | Guard / policy | Owner |
|---|---|---|
| Hard waits / flakiness | web-first assertions, auto-wait | {{team.qa_lead}} |
| Brittle selectors | test-id strategy | `<fill>` |
| Over-reliance on UI E2E | pyramid level split (§3) | {{team.qa_lead}} |
| Mock drift | contract tests {{tooling.contract}} | `<fill>` |

## 9. Roles & skills
From `team`; whole-team quality; automation code owned, not thrown over the wall.

| Role | Person (`team`) | Automation responsibility | Key skills |
|---|---|---|---|
| QA Manager | {{team.qa_manager}} | strategy sign-off, ROI | governance |
| QA Lead | {{team.qa_lead}} | gTAA design, reviews, metrics | {{tooling.language}}, {{tooling.e2e}} |
| Eng Lead | {{team.eng_lead}} | testability, CI, SUT hooks | {{ci.platform}} |
| Product Owner | {{team.product_owner}} | priority, acceptance criteria | domain |

## 10. Risks & mitigations
Risks to the automation effort (CT-TAE), with owners and mitigations.

| Risk | Likelihood (1–5) | Impact (1–5) | Mitigation | Owner |
|---|---|---|---|---|
| Flaky tests erode trust | `<fill>` | `<fill>` | §8 guards, flaky quarantine + root-cause | {{team.qa_lead}} |
| Maintenance burden > value | `<fill>` | `<fill>` | ROI selection, lowest-level-first | {{team.qa_lead}} |
| Unstable SUT / test data | `<fill>` | `<fill>` | factories, {{tooling.mocking}} (contract-backed) | {{team.eng_lead}} |
| Slow pipeline | `<fill>` | `<fill>` | sharding ×{{ci.shard_count}}, parallelism | {{team.eng_lead}} |
| Mock drift vs real services | `<fill>` | `<fill>` | contract tests {{tooling.contract}} | `<fill>` |
| Skills gap | `<fill>` | `<fill>` | pairing, training (§9) | {{team.qa_manager}} |

**Residual risk:** automation verifies only what is encoded and run; subjective/usability, novel/unseen states, and un-automated `risk_areas` remain covered by exploratory/manual testing (ISTQB Principle 1: testing shows the presence, not the absence, of defects).

---
*References ISTQB CT-TAE (gTAA), CTFL v4.0 §6, and ISO/IEC/IEEE 29119-3. See `docs/ISTQB-COMPLIANCE.md`.*

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.
