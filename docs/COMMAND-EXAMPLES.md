# QA Toolkit — Worked Examples (all 64 commands)

A concrete, copy-pasteable **sample invocation for every command**, plus a **"Correct when"** check that proves it ran right. Every example is anchored to **one consistent sample project** so they chain into a real QA story — if you run them in order against that project, the artifacts reference each other.

> How-to and prerequisites for each command: [COMMAND-GUIDE.md](./COMMAND-GUIDE.md). Syllabus mapping: [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md).

---

## The sample project (used in every example below)

The toolkit ships [`templates/qa.config.example.yml`](../templates/qa.config.example.yml) for **"ShopEase"**, a Web + REST API e-commerce app. The examples assume that config:

| Setting | Value |
|---|---|
| Project | **ShopEase** — React + Node/Express, REST (OpenAPI at `./openapi.yaml`) |
| Web / API base URL | `http://localhost:3000` / `http://localhost:4000` |
| Stack | Playwright+TS · Vitest · K6 · Pact · axe · Semgrep/npm-audit/OWASP-ZAP/gitleaks |
| CI | Jenkins — job `shopease/main` at `https://jenkins.acme.io` |
| Critical risk areas | authentication, authorization, payments, checkout, PII |
| Perf gates | checkout p95 ≤ 500 ms · p99 ≤ 1000 ms · error rate ≤ 1% · 100 rps |
| Paths | docs → `docs/qa/` · tests → `tests/` · reports → `reports/` |
| **Release under test** | **R2.4** — features: *guest checkout*, *saved cards* |

## How to verify a command worked (the proof method)

Each example lists a **✓ Correct when** criterion. In general a command ran correctly when **all** of these hold:

1. **The named artifact exists** at the right path (`docs/qa/…`, `tests/…`, or `reports/…`) — or, for analysis/report commands, a structured report is returned.
2. **It used your config**, not generic defaults — e.g. perf thresholds equal the `gates` values, depth concentrates on `risk_areas.critical`, selectors/stack match `tooling`.
3. **It names the ISTQB technique/activity** it applied (EP, BVA, decision table, risk score, exit criteria…) — traceable, not ad-hoc.
4. **Read-only commands didn't modify code** (`automation-audit`, `static-analysis`, `static-review`, `review-coverage`, `coverage-measure`, and the report/governance commands).
5. **Defects aren't masked** — `fix-*`, `self-heal`, `flaky-hunt` escalate real product bugs via `triage` instead of weakening assertions.

---

## 1. Planning & management

**`/qa:qa-init`**
```text
/qa:qa-init
```
Produces: `./qa.config.yml` after an interactive interview. ✓ **Correct when** the file exists at repo root with your real `project`, `stack`, `tooling`, `gates`, and `risk_areas` filled in.

**`/qa:test-policy`**
```text
/qa:test-policy
```
Produces: `docs/qa/TEST-POLICY.md`. ✓ **Correct when** it states org-level testing objectives/principles above any single project (not a per-release plan).

**`/qa:create-strategy`**
```text
/qa:create-strategy
```
Produces: `docs/qa/TEST-STRATEGY.md`. ✓ **Correct when** the level distribution, tooling, and CI match `qa.config.yml`, and it follows the ISO 29119-3 strategy structure.

**`/qa:create-plan`**
```text
/qa:create-plan R2.4 "guest checkout, saved cards"
```
Produces: `docs/qa/TEST-PLAN-R2.4.md`. ✓ **Correct when** scope = the two features, exit criteria = the `gates` (≥98% pass, block on S1/S2), and it cites the R2.4 risk areas.

**`/qa:risk-assessment`**
```text
/qa:risk-assessment R2.4
```
Produces: `docs/qa/RISK-REGISTER-R2.4.md`. ✓ **Correct when** each risk has a likelihood×impact score and *payments/checkout/auth* land in the top tier with a heavier test response.

**`/qa:estimate`**
```text
/qa:estimate "R2.4 — guest checkout + saved cards"
```
Produces: an effort estimate (report). ✓ **Correct when** it shows both a metrics-based and an expert-based figure with assumptions, not a single guess.

**`/qa:tool-select`**
```text
/qa:tool-select "visual regression testing"
```
Produces: `docs/qa/TOOL-EVALUATION-visual-regression.md`. ✓ **Correct when** it lists candidates with benefits/risks, scoring criteria, and a pilot recommendation.

**`/qa:process-improvement`**
```text
/qa:process-improvement "flaky pipeline + escaped checkout defects"
```
Produces: `docs/qa/PROCESS-IMPROVEMENT-<date>.md`. ✓ **Correct when** it assesses maturity (TMMi/IDEAL-style) and gives prioritized, owned improvement actions.

## 2. Governance

**`/qa:quality-report`**
```text
/qa:quality-report "Q2-2026"
```
Produces: `docs/qa/QUALITY-REPORT-Q2-2026.md`. ✓ **Correct when** it trends escaped defects, coverage, pass rate, MTTR, automation %, flaky rate across releases.

**`/qa:team-plan`**
```text
/qa:team-plan "Q3-2026"
```
Produces: `docs/qa/TEAM-PLAN-Q3-2026.md`. ✓ **Correct when** it maps staffing/skills to the upcoming backlog and flags gaps + a training plan.

**`/qa:go-no-go`**
```text
/qa:go-no-go R2.4
```
Produces: `docs/qa/GO-NO-GO-R2.4.md`. ✓ **Correct when** it consolidates the signals into a single ship/hold decision against the `gates`, with residual risk and sign-off lines.

**`/qa:cost-of-quality`**
```text
/qa:cost-of-quality "2026 automation programme"
```
Produces: `docs/qa/COST-OF-QUALITY-2026-automation-programme.md`. ✓ **Correct when** it splits prevention/appraisal/failure costs and shows automation ROI/payback.

**`/qa:audit-prep`**
```text
/qa:audit-prep "ISO-29119"
```
Produces: `docs/qa/AUDIT-READINESS-ISO-29119.md`. ✓ **Correct when** it assembles a traceability + evidence pack and flags conformance gaps.

## 3. Static testing, analysis & design

**`/qa:static-review`**
```text
/qa:static-review "docs/stories/guest-checkout.md" walkthrough
```
Produces: a review-findings report. ✓ **Correct when** it lists testability issues/ambiguities in the story (the test basis) — *before* any tests are written.

**`/qa:static-analysis`**
```text
/qa:static-analysis src/checkout
```
Produces: a static-analysis report. ✓ **Correct when** it reports cyclomatic complexity/maintainability per unit and modifies no files.

**`/qa:automation-audit`**
```text
/qa:automation-audit tests
```
Produces: `docs/qa/AUTOMATION-AUDIT.md`. ✓ **Correct when** it scores Architecture/SOLID/Design-quality/Anti-patterns/Pyramid/CI (1–5), cites `file:line` evidence, and changes no code.

**`/qa:test-cases`**
```text
/qa:test-cases "As a guest I can check out with a saved card"
```
Produces: `docs/qa/TEST-CASES-guest-checkout.md` (+ CSV on request). ✓ **Correct when** each case names its technique (EP/BVA/decision table) and includes negative + boundary cases, not just happy path.

**`/qa:test-design`**
```text
/qa:test-design "checkout payment"
```
Produces: `docs/qa/TEST-DESIGN-checkout-payment.md`. ✓ **Correct when** it derives test conditions → cases with coverage items and labeled techniques.

**`/qa:combinatorial`**
```text
/qa:combinatorial "checkout: 3 payment methods × 2 shipping × 4 countries"
```
Produces: `docs/qa/COMBINATORIAL-checkout.md`. ✓ **Correct when** it gives a pairwise/classification-tree set that's far smaller than the 24 exhaustive combos while covering all pairs.

**`/qa:acceptance`**
```text
/qa:acceptance "Guest checkout with a saved card"
```
Produces: `docs/qa/ACCEPTANCE-guest-checkout.md`. ✓ **Correct when** it has Given/When/Then scenarios agreed as the acceptance criteria (ATDD).

**`/qa:mbt`**
```text
/qa:mbt "order lifecycle: cart → placed → paid → shipped → delivered"
```
Produces: `docs/qa/MBT-order-lifecycle.md`. ✓ **Correct when** it models the states/transitions and derives cases by a stated coverage criterion.

**`/qa:exploratory`**
```text
/qa:exploratory "payments"
```
Produces: `docs/qa/EXPLORATORY-payments.md`. ✓ **Correct when** it gives time-boxed charters (mission, areas, ideas) for a `risk_areas.critical` area.

**`/qa:review-coverage`**
```text
/qa:review-coverage checkout
```
Produces: a prioritized gap report. ✓ **Correct when** it names specific untested conditions/endpoints for checkout and ranks them by risk.

## 4. Test levels & change-related

**`/qa:unit-test`**
```text
/qa:unit-test "src/pricing/discount.ts"
```
Produces: unit-test design + tests. ✓ **Correct when** it targets statement/branch coverage with test doubles and isolates the unit.

**`/qa:integration-test`**
```text
/qa:integration-test "checkout → payment-gateway"
```
Produces: integration design + tests. ✓ **Correct when** it states an integration strategy (incremental) and uses stubs/drivers for the gateway.

**`/qa:maintenance-test`**
```text
/qa:maintenance-test "migrate payments to Stripe API v2"
```
Produces: `docs/qa/MAINTENANCE-stripe-v2.md`. ✓ **Correct when** it includes impact analysis + a confirmation/regression scope for the change.

**`/qa:dynamic-analysis`**
```text
/qa:dynamic-analysis "cart session handling"
```
Produces: `docs/qa/DYNAMIC-ANALYSIS-cart.md`. ✓ **Correct when** it targets runtime leaks/handle-exhaustion/degradation over time, not static defects.

**`/qa:shift-right`**
```text
/qa:shift-right "checkout"
```
Produces: `docs/qa/SHIFT-RIGHT-checkout.md`. ✓ **Correct when** it defines synthetic monitors, observability checks, and canary/feature-flag validation for production.

**`/qa:regression`**
```text
/qa:regression "saved-cards change"
```
Produces: a selected/prioritized regression set. ✓ **Correct when** it uses impact analysis to include affected areas and trims unrelated tests (pesticide paradox).

## 5. Implementation

**`/qa:scaffold`**
```text
/qa:scaffold
```
Produces: the framework — `playwright.config.ts`, `tests/`, fixtures, K6/Pact/a11y setup, `Jenkinsfile`. ✓ **Correct when** `npx playwright test` runs and the structure matches `tooling`/`ci`.

**`/qa:automate`**
```text
/qa:automate "docs/manual/checkout-cases.csv"
```
Produces: `docs/qa/AUTOMATION-PLAN-checkout.md` + the top tests. ✓ **Correct when** it scores each case by ROI/complexity and automates the high-value ones first.

**`/qa:implement`**
```text
/qa:implement "guest checkout"
```
Produces: tests under `tests/` (run + results). ✓ **Correct when** logic lands at the lowest effective level (API/component) and only the journey is E2E, with web-first assertions.

**`/qa:add-test`**
```text
/qa:add-test "password reset link expires after 30 minutes"
```
Produces: one focused spec. ✓ **Correct when** it adds a single self-validating test with real assertions and owns its data.

**`/qa:test-data`**
```text
/qa:test-data "order"
```
Produces: typed factories/fixtures + seed/cleanup helpers. ✓ **Correct when** data is synthetic-only and each test can build/own its own order (parallel-safe).

**`/qa:test-env`**
```text
/qa:test-env qa
```
Produces: `docs/qa/TEST-ENVIRONMENT.md` + environment setup files (docker-compose/env/seed) under `tests/`. ✓ **Correct when** it documents the `qa` environment (URL, data, config) from the `environments` list.

## 6. Automation by surface

**`/qa:automation-strategy`**
```text
/qa:automation-strategy
```
Produces: `docs/qa/AUTOMATION-STRATEGY.md`. ✓ **Correct when** it defines the gTAA 4 layers, the pyramid split, and maintainability/metrics — program-level, not per-feature.

**`/qa:api-automate`**
```text
/qa:api-automate "/orders"
```
Produces: API tests under `tests/`. ✓ **Correct when** they're generated from `./openapi.yaml` with schema validation, CRUD, an auth/role matrix, and negative/boundary cases.

**`/qa:scan-ui`**
```text
/qa:scan-ui http://localhost:3000/checkout
```
Produces: page objects in `tests/pages/` + `docs/qa/UI-SCAN-checkout.md`. ✓ **Correct when** every interactive element gets a stable locator and ≥1 covering case (temp probe removed).

**`/qa:web-automate`**
```text
/qa:web-automate "guest checkout journey"
```
Produces: E2E tests under `tests/`. ✓ **Correct when** they use POM + auth state, run cross-browser per `ci.browsers`, with no hard waits.

**`/qa:mobile-automate`**
```text
/qa:mobile-automate "checkout" web
```
Produces: responsive mobile-web tests. ✓ **Correct when** they cover the `mobile_device_matrix` (iPhone 14, Pixel 7) viewports/touch.

**`/qa:perf-plan`**
```text
/qa:perf-plan "checkout"
```
Produces: `docs/qa/PERF-PLAN-checkout.md`. ✓ **Correct when** it sets objectives/SLAs from `gates.performance` and a workload model (operational profile), feeding `perf-test`.

## 7. Execution — non-functional

**`/qa:perf-test`**
```text
/qa:perf-test "/checkout" load
```
Produces: a K6 script (+ optional run). ✓ **Correct when** thresholds = the gates (p95 ≤ 500 ms, p99 ≤ 1000 ms, error ≤ 1%, 100 rps) and it fails the build if breached.

**`/qa:a11y-audit`**
```text
/qa:a11y-audit "/checkout"
```
Produces: axe checks + a report. ✓ **Correct when** it audits against `WCAG 2.1 AA` and blocks on `critical`/`serious` per `gates.a11y_block_on`.

**`/qa:usability-test`**
```text
/qa:usability-test "guest checkout"
```
Produces: `docs/qa/USABILITY-guest-checkout.md`. ✓ **Correct when** it applies usability heuristics + task scenarios (distinct from accessibility).

**`/qa:nonfunctional`**
```text
/qa:nonfunctional reliability
```
Produces: `docs/qa/NONFUNCTIONAL-reliability.md`. ✓ **Correct when** it maps to an ISO/IEC 25010 characteristic with measurable criteria.

**`/qa:security-scan`**
```text
/qa:security-scan all
```
Produces: SAST/SCA/DAST/secret runs + a report. ✓ **Correct when** it uses the configured tools (Semgrep/npm-audit/OWASP-ZAP/gitleaks) and blocks on high/critical per `gates.security_block_on`.

**`/qa:contract-sync`**
```text
/qa:contract-sync can-i-deploy
```
Produces: Pact contracts + a `can-i-deploy` result. ✓ **Correct when** it talks to the configured `contract_broker_url` and gates deploy on verified contracts.

**`/qa:mobile-test`**
```text
/qa:mobile-test "/checkout"
```
Produces: responsive/mobile-web tests. ✓ **Correct when** it covers viewports, touch, and network conditions across the device matrix.

**`/qa:ai-test`**
```text
/qa:ai-test "product recommendations"
```
Produces: `docs/qa/AI-TEST-product-recommendations.md` + automatable metric/data-validation checks under `tests/`. ✓ **Correct when** it covers data quality, model metrics, bias/fairness, robustness, and drift (CT-AI).

## 8. Maintenance, CI & flakiness

**`/qa:ci`**
```text
/qa:ci          # triage the whole latest red build
/qa:ci x        # …then verify the full suite locally (extended gate)
```
Produces: the bucketed failing set (test defect / product defect / env / flaky), root-cause fixes confirmed locally, a green-×3 stability result per fixed case, real defects escalated via `triage`, and a Test Execution Log under `reports/`. ✓ **Correct when** it pulls the **whole** build's failures, fixes only the test/env/flaky ones, reports stability as `n/3` (not prose), escalates product defects instead of masking them, and never commits/triggers CI unless asked. *(Auto-fetch from config: `ci.platform` + `ci.jenkins_url`/`ci.jenkins_job` + `JENKINS_USER`/`JENKINS_API_TOKEN`, or `gh` for GitHub Actions.)*

**`/qa:fix-ci`**
```text
/qa:fix-ci reports/ci-build-482.log
```
Produces: a diagnosis + applied fix. ✓ **Correct when** it finds the root cause (env/flaky/dep/pipeline), fixes it, and explains how to verify — without masking a product defect.

**`/qa:fix-jenkins`**
```text
/qa:fix-jenkins https://jenkins.acme.io/job/shopease/job/main/482/
```
Produces: the failed-case list, fixes, and a local re-run. ✓ **Correct when** it pulls only FAILED/REGRESSION cases, fixes by root cause, re-runs **those** locally to green, and escalates real defects via `triage`. *(Auto-fetch also works from config: `ci.jenkins_url`/`ci.jenkins_job` + `JENKINS_USER`/`JENKINS_API_TOKEN`.)*

**`/qa:flaky-hunt`**
```text
/qa:flaky-hunt "tests/e2e/checkout.spec.ts"
```
Produces: quarantine + deterministic fixes. ✓ **Correct when** it stabilizes the root cause (waits/data/order) rather than adding blind retries.

**`/qa:self-heal`**
```text
/qa:self-heal "tests/pages/CheckoutPage.ts"
```
Produces: healed locators + a report. ✓ **Correct when** it repairs *how we locate* (stable selector) in the page object, never loosens an assertion, and re-runs to confirm.

## 9. Version control & PR quality

**`/qa:review-pr`**
```text
/qa:review-pr 482
```
Produces: `reports/PR-REVIEW-482-<date>.md` + a merge verdict. ✓ **Correct when** it maps the diff to `risk_areas`, reports coverage of the change as counts (covered/uncovered files), scopes regression, flags testware issues, files real defects via `triage`, and the merge call names the `gates` item that drives it — without editing the PR's product code.

**`/qa:commit`**
```text
/qa:commit "fix: expired-coupon 500"
```
Produces: a verified commit. ✓ **Correct when** it runs the affected tests/lint *first*, commits only if green, writes a Conventional Commits message tracing to the requirement/defect (`Fixes: DEF-…`), and never pushes — a failing change routes to `triage` instead of being committed.

**`/qa:open-pr`**
```text
/qa:open-pr main
```
Produces: a PR + `reports/PR-<branch>-<date>.md`. ✓ **Correct when** the PR body states what changed, what was tested (coverage delta, regression set) as counts, residual risk, and linked defects — and the PR is opened only on confirmation, never force-pushed.

**`/qa:merge-gate`**
```text
/qa:merge-gate 482
```
Produces: `reports/MERGE-GATE-482-<date>.md`. ✓ **Correct when** every `gates` item is marked PASS/FAIL/N-A with evidence, severity (not priority) drives the blocker check, the verdict names the failing gate, and it records a recommendation rather than auto-merging.

## 10. Monitoring, control & completion

**`/qa:status-report`**
```text
/qa:status-report R2.4
```
Produces: `docs/qa/STATUS-REPORT-R2.4-<date>.md`. ✓ **Correct when** it compares progress to the plan with metrics + control actions (mid-release).

**`/qa:coverage-measure`**
```text
/qa:coverage-measure checkout
```
Produces: a coverage report. ✓ **Correct when** it reports structural + requirements + risk coverage and names the holes.

**`/qa:triage`**
```text
/qa:triage "checkout returns HTTP 500 when applying an expired coupon"
```
Produces: an ISTQB defect report. ✓ **Correct when** it separates **severity** from **priority** and gives clear repro/expected/actual.

**`/qa:release-report`**
```text
/qa:release-report R2.4
```
Produces: `docs/qa/RELEASE-REPORT-R2.4.md`. ✓ **Correct when** it evaluates exit criteria vs `gates`, states residual risk, and gives a ship/hold recommendation.

## 11. AI-assisted & reference

**`/qa:genai-assist`**
```text
/qa:genai-assist "generate test ideas for guest checkout"
```
Produces: GenAI-accelerated output (ideas/data/draft). ✓ **Correct when** it applies CT-GenAI safeguards — human-review prompt, no real PII, output labeled for verification.

**`/qa:istqb-coach`**
```text
/qa:istqb-coach "boundary value analysis"
```
Produces: an explanation + command routing. ✓ **Correct when** it explains BVA (2-/3-value) with an example and points you to `/qa:test-design` to apply it.

---

## End-to-end proof run (the examples as one story)

Run these in order against the ShopEase project to see the artifacts reference each other — that chain *is* the proof the toolkit is internally consistent:

```text
/qa:qa-init                                   # → qa.config.yml
/qa:create-strategy                           # → TEST-STRATEGY.md
/qa:risk-assessment R2.4                      # → RISK-REGISTER-R2.4.md  (payments = top risk)
/qa:create-plan R2.4 "guest checkout, saved cards"   # → TEST-PLAN-R2.4.md  (cites the register)
/qa:test-cases "guest checkout with saved card"      # → TEST-CASES-guest-checkout.md
/qa:scaffold                                  # → framework + Jenkinsfile
/qa:implement "guest checkout"                # → tests/ (run green)
/qa:perf-test "/checkout" load                # → K6 vs p95 500ms gate
/qa:status-report R2.4                        # → STATUS-REPORT-R2.4-<date>.md
/qa:go-no-go R2.4                             # → GO-NO-GO-R2.4.md
/qa:release-report R2.4                       # → RELEASE-REPORT-R2.4.md  (exit criteria vs gates)
```

Each step's output names the prior artifacts and the same `gates`/`risk_areas` values — if any step invents different thresholds or ignores the risk tiers, that's the signal it wasn't driven by `qa.config.yml`.

---

*QA Toolkit v3.10.0 — 64 commands. Examples use the shipped [`qa.config.example.yml`](../templates/qa.config.example.yml).*
