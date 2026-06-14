# ISTQB Compliance & Standards Mapping

This toolkit is built to follow the **ISTQB®** (International Software Testing Qualifications Board) framework strictly, aligned to the **Certified Tester Foundation Level (CTFL) syllabus v4.0**, the relevant **Advanced / Agile / Specialist** syllabi, the **ISTQB Glossary**, and the test-documentation structure of **ISO/IEC/IEEE 29119-3**.

This document is the authoritative map: it shows exactly how every command, template, and convention traces to an ISTQB concept, so an auditor or a certified tester can verify conformance.

> **Note on sources.** ISTQB syllabi and the Glossary are copyrighted by ISTQB. This toolkit does not reproduce them; it implements their concepts and uses their terminology. Read the official documents at the links in [References](#references).

---

## 1. ISTQB streams covered

The ISTQB portfolio is organized into **Core**, **Agile**, and **Specialist** streams across the **Foundation, Advanced, Specialist, and Expert** levels. This toolkit operationalizes the streams relevant to a Web + API product:

| Stream / syllabus | ISTQB code | How the toolkit applies it |
|---|---|---|
| Foundation Level | CTFL v4.0 | The backbone — principles, test process, levels, types, techniques, documentation, tools. Embedded in every command and the `qa-context` skill. |
| Agile Tester | CTFL-AT | Agile lifecycle mapping, testing quadrants, ATDD, risk-based testing in iterations. See `create-strategy`, `create-plan`. |
| Advanced Test Manager | CTAL-TM | Test strategy, planning, risk management, monitoring & control, estimation, completion, metrics. See `create-strategy`, `risk-assessment`, `status-report`, `release-report`. |
| Advanced Test Analyst | CTAL-TA | Black-box test design techniques, quality characteristics. See `test-design`. |
| Advanced Technical Test Analyst | CTAL-TTA | White-box techniques, static analysis, non-functional. See `test-design`, `static-review`, `perf-test`, `security-scan`. |
| Test Automation Engineering | CT-TAE | Test automation architecture (gTAA), maintainability, reporting. See `scaffold`, `implement`, `flaky-hunt`. |
| Performance Testing | CT-PT | Load/stress/spike/soak, workload modeling, thresholds. See `perf-test`. |
| Security Testing | CT-SEC | Security risk assessment, OWASP-aligned testing. See `security-scan`. |
| Acceptance Testing | CT-AcT | ATDD, acceptance criteria, BDD. See `create-plan`, `test-design`. |
| Usability/Accessibility | CT-UT / a11y | WCAG-aligned accessibility evaluation. See `a11y-audit`. |
| Quality in DevOps | — | CI/CD quality gates, shift-left/right, pipeline testing, testing in production. See `scaffold`, `fix-ci`, `shift-right`. |

---

## 2. The seven ISTQB testing principles — how the toolkit enforces each

(CTFL v4.0 §1.3.) These are standing rules in the `qa-context` skill, so they apply across all work.

| # | Principle | How the toolkit honors it |
|---|---|---|
| 1 | **Testing shows the presence of defects, not their absence** | Reports and the Test Completion Report state residual risk; no command claims "defect-free." Exit evaluation is risk-based, never "proven correct." |
| 2 | **Exhaustive testing is impossible** | `test-design` uses formal techniques (EP, BVA, decision tables) and `risk-assessment` to focus effort instead of brute force. The pyramid pushes coverage to the cheapest effective level. |
| 3 | **Early testing saves time and money (shift-left)** | Static testing (`static-review`) of the test basis, ATDD acceptance criteria at refinement, and tests authored alongside development. Strategy maps testing onto every agile ceremony. |
| 4 | **Defects cluster together** | `risk-assessment` and `review-coverage` direct deeper coverage to high-risk/defect-dense areas (`risk_areas` in config). |
| 5 | **Beware of the pesticide paradox** | `review-coverage` and `flaky-hunt` prompt refreshing/retiring stale tests; `test-design` adds new conditions as the product evolves. |
| 6 | **Testing is context-dependent** | Everything is driven by `qa.config.yml` — risk tiers, domain, criticality, and enabled tooling change what and how much is tested. |
| 7 | **Absence-of-errors is a fallacy** | Validation against user needs (acceptance testing, a11y, usability) is first-class, not just defect-fixing. The Completion Report evaluates fitness for purpose, not just pass counts. |

---

## 3. The ISTQB test process — seven activities mapped to commands

(CTFL v4.0 §1.4.) The ISTQB test process consists of seven activities with defined **work products (testware)**. Every command implements one or more activities and produces the corresponding testware.

| ISTQB activity | Purpose | Toolkit command(s) | Work products (testware) produced |
|---|---|---|---|
| **Test planning** | Define objectives, scope, approach, resources, schedule | `create-strategy`, `create-plan`, `risk-assessment`, `qa-init` | Organizational Test Strategy, Test Plan, product-risk register, quality gates |
| **Test monitoring & control** | Compare progress to plan, take corrective action | `status-report` | Test Status (Progress) Report, control actions |
| **Test analysis** | Analyze the **test basis** to determine **test conditions** ("what to test") | `test-design` (analysis phase), `review-coverage` | Prioritized test conditions, traceability test basis→conditions, basis defects |
| **Test design** | Derive **test cases** and coverage items from test conditions using techniques ("how to test") | `test-design` | Test cases (high/low level), coverage items, test data requirements, test environment requirements |
| **Test implementation** | Create/organize **test procedures**, scripts, suites, data, environment | `scaffold`, `implement`, `add-test`, `test-data` | Test procedures, automated test scripts, test suites, test data, test harness/fixtures, configured test environment |
| **Test execution** | Run tests, compare actual vs expected, log results | `implement` (run), `perf-test`, `a11y-audit`, `contract-sync`, `security-scan`, `fix-ci` | Test execution logs/results, test reports, defect (incident) reports |
| **Test completion** | Collate results, finalize testware, report, capture lessons | `release-report`, `triage` | Test Completion Report, finalized testware, change requests, lessons learned |

**Tailoring (CTFL §1.4):** the process is tailored per iteration. In agile, activities run continuously each sprint rather than as phases — the `create-strategy` output documents this tailoring explicitly.

---

## 4. Test levels (CTFL v4.0 §2.2)

ISTQB defines test levels; the toolkit maps them to concrete tooling via config.

| ISTQB test level | Toolkit realization |
|---|---|
| **Component (unit) testing** | `unit-test` — isolation, test doubles, statement/branch coverage (`tooling.unit`). |
| **Component integration testing** | `integration-test`, `api-automate`; contract tests (Pact, `contract-sync`) verify component interfaces. |
| **System testing** | `web-automate` end-to-end across the integrated Web + API system; non-functional system testing (`perf-test`, `security-scan`, `a11y-audit`). |
| **System integration testing** | `integration-test` across external services using service virtualization / mocking, backed by contract testing. |
| **Acceptance testing** | `acceptance` — ATDD/UAT from acceptance criteria. Includes UAT, operational acceptance, contractual/regulatory, alpha/beta as applicable. |
| **Maintenance testing** (§2.3) | `maintenance-test` — modification / migration / retirement + impact analysis. |

---

## 5. Test types (CTFL v4.0 §2.2.2) and quality characteristics (ISO/IEC 25010)

| ISTQB test type | Toolkit command(s) | ISO 25010 characteristic |
|---|---|---|
| **Functional** | `implement`, `add-test`, `test-design` | Functional suitability |
| **Non-functional — performance** | `perf-test` (K6) | Performance efficiency |
| **Non-functional — security** | `security-scan` | Security |
| **Non-functional — accessibility/usability** | `a11y-audit` | Usability (WCAG) |
| **Non-functional — reliability** | `perf-test` (soak), `flaky-hunt` | Reliability |
| **Non-functional — compatibility** | cross-browser projects in `scaffold` | Compatibility/portability |
| **White-box (structural)** | `test-design` (statement/branch coverage), `static-review` | — |
| **Change-related — confirmation testing** | `triage`/`implement` (re-test fixed defects) | — |
| **Change-related — regression testing** | full regression suites in `scaffold`/CI; `review-coverage` | — |

---

## 6. Test design techniques (CTFL v4.0 §4) — implemented by `test-design`

| Category | Techniques | Applied in |
|---|---|---|
| **Black-box (§4.2)** | Equivalence Partitioning, Boundary Value Analysis (2-value & 3-value), Decision Table testing, State Transition testing | `test-cases` / `test-design` derive cases for API params, forms, business rules, state machines |
| **White-box (§4.3)** | Statement testing/coverage, Branch testing/coverage | `coverage-measure`, `static-review` for structural coverage |
| **Experience-based (§4.4)** | Error Guessing, Exploratory testing, Checklist-Based testing | `exploratory`, `test-cases` (negatives) |
| **Collaboration-based (§4.5)** | Collaborative user story writing, Writing acceptance criteria, ATDD | `acceptance`, `create-plan` (Given/When/Then) |
| **Advanced (CTAL-TA, not CTFL v4.0)** | Pairwise/combinatorial (classification tree), Use-case testing | Available in `test-cases`/`test-design`, explicitly labeled as Advanced |

> **v4.0 strictness note:** CTFL v4.0 §4.2 black-box techniques are exactly the four listed. **Use-case testing and pairwise/combinatorial were removed from Foundation in v4.0** (they are CTAL Test Analyst topics). The toolkit never attributes them to Foundation; when used they are labeled Advanced. White-box in v4.0 is Statement and **Branch** testing (v3.1's "Decision testing" was renamed/changed).

Each derived test case records its **technique** and the **coverage items** it exercises, so coverage is measurable per ISTQB.

---

## 7. Static testing (CTFL v4.0 §3) — `static-review`

ISTQB requires static testing (reviews and static analysis) of the **test basis** — requirements, user stories, the OpenAPI spec — before dynamic testing. `static-review` performs review of the test basis for testability, consistency, completeness, and ambiguity, and runs static analysis (SAST/linting), producing review findings. This realizes Principle 3 (early testing).

Review types supported: informal review, walkthrough, technical review, and inspection — selectable by formality in the command.

---

## 8. Risk-based testing (CTFL v4.0 §5.2; CTAL-TM) — `risk-assessment`

ISTQB risk-based testing drives effort by **risk level = likelihood × impact**. The toolkit:

- Identifies **product risks** (quality risks) and **project risks**.
- Scores each (likelihood 1–5 × impact 1–5) and assigns a risk level.
- Allocates test depth, technique rigor, and level by risk (mirrored in `risk_areas` of `qa.config.yml`).
- Feeds risk into the Test Plan, exit evaluation, and the Completion Report's residual-risk statement.

The output is the **Product Risk Register** (ISO/IEC/IEEE 29119-3 work product; see §11).

---

## 9. Test monitoring, control & metrics (CTFL v4.0 §5.3) — `status-report`

ISTQB distinguishes **monitoring** (gathering data), **control** (corrective action), and reporting. `status-report` produces a **Test Status (Progress) Report** with ISTQB-standard metrics: test-case progress (planned/executed/passed/failed/blocked), defect metrics, coverage (requirements/risk), and entry/exit-criteria status — distinct from the end-of-test **Completion Report**.

---

## 10. Defect management (CTFL v4.0 §5.5) — `triage`

`triage` follows the ISTQB defect (incident) lifecycle and produces a **defect report** with the fields ISTQB specifies (identifier, summary, test object/environment, steps, expected vs actual, severity, priority, status, references). It distinguishes **severity** (impact on the system) from **priority** (urgency to fix), per ISTQB.

---

## 11. Test documentation — ISO/IEC/IEEE 29119-3 alignment

ISTQB references the ISO/IEC/IEEE 29119 standard for documentation. The toolkit's artifacts map to 29119-3 work products (the **Organizational Test Policy** sits above them under **ISO/IEC/IEEE 29119-2**, with the Organizational Test Strategy and Test Plans below it):

| ISO/IEC/IEEE 29119 work product | Toolkit artifact (template) | Produced by |
|---|---|---|
| Organizational Test Policy (ISO/IEC/IEEE **29119-2**) | `TEST-POLICY.md` (`policy-template.md`) | `test-policy` |
| Organizational Test Strategy | `TEST-STRATEGY.md` (`strategy-template.md`) | `create-strategy` |
| Test Automation Strategy / Test Automation Plan | automation strategy/plan doc (`automation-strategy-template.md`, `automation-plan-template.md`) | `automation-strategy` |
| Test Plan | `TEST-PLAN-<release>.md` (`plan-template.md`) | `create-plan` |
| Product Risk Register | risk register (`risk-register-template.md`) | `risk-assessment` |
| Test Design Specification | test-conditions + design output | `test-design` |
| Test Case Specification | test cases (repo + plan §cases, `test-case-template.md`) | `test-design`, `implement` |
| Test Procedure Specification | executable specs/scripts | `implement`, `scaffold` |
| Test Data / Environment Requirements | factories, fixtures, env config (`test-data-template.md`, `test-environment-template.md`) | `test-data`, `test-env`, `scaffold` |
| Test Execution Log / Test Results | CI reports (JUnit/HTML/K6) | `implement`, CI |
| Production Verification Report (shift-right / testing in production) | `production-verification-<scope>.md` (`shift-right-template.md`) | `shift-right` |
| Test Status Report | `STATUS-REPORT-*.md` | `status-report` |
| Test Completion Report | `RELEASE-REPORT-<release>.md` (`completion-report-template.md`) | `release-report` |
| Incident (Defect) Report | defect report (`defect-report-template.md`) | `triage` |

Legacy IEEE 829 users: the Test Plan and Completion Report follow the equivalent 829 structure where teams still require it.

---

## 12. Traceability (CTFL v4.0 §1.4.4)

ISTQB requires **bidirectional traceability** from the test basis through to results. The toolkit maintains this chain and every command preserves it:

```
Test basis (requirement / user story / OpenAPI)
   → Test condition            (test-design, analysis)
      → Test case + coverage item   (test-design)
         → Test procedure / script    (implement)
            → Test execution result     (execution)
               → Defect report            (triage)
```

`review-coverage` audits this chain for gaps; the Test Plan and Completion Report report coverage against it.

---

## 13. Command → ISTQB concept matrix (quick reference)

| Command | ISTQB process activity | Key syllabus reference |
|---|---|---|
| `qa-init` | Test planning (context establishment) | CTFL §1.4, §5.1 |
| `test-policy` | Organizational Test Policy (governance) | ISO/IEC/IEEE 29119-2; CTAL-TM / Test Management (Expert) |
| `create-strategy` | Test planning (org test strategy) | CTFL §5.1; CTAL-TM |
| `create-plan` | Test planning (test plan) | CTFL §5.1; ISO 29119-3 |
| `automation-strategy` | Test automation strategy/plan (gTAA) | CT-TAE; Test Automation Strategy (Specialist) |
| `tool-select` | Test tool selection & evaluation | CT-TAE; Test Automation Strategy (Specialist); CTFL §6 (generic tool support) |
| `cost-of-quality` | Value of testing, test economics & cost of quality | CTAL-TM (cost of quality, ROI, metrics) |
| `risk-assessment` | Risk-based testing | CTFL §5.2; CTAL-TM |
| `static-review` | Static testing | CTFL §3 |
| `test-design` | Test analysis + design + techniques | CTFL §1.4, §4 |
| `acceptance` | Collaboration-based design (ATDD) + acceptance testing | CTFL §4.5 (ATDD technique); CT-AcT (acceptance-testing forms, distinct from §4.5); CTFL §2.2 (level) |
| `scaffold` | Test implementation (test env/automation) | CTFL §1.4, §6; CT-TAE |
| `implement` | Test implementation + execution | CTFL §1.4 |
| `add-test` | Test design + implementation | CTFL §4 |
| `test-data` | Test implementation (test data) | CTFL §1.4 |
| `perf-test` | Non-functional (performance) testing | CT-PT |
| `a11y-audit` | Non-functional (usability/accessibility) | CT-UT / WCAG |
| `contract-sync` | Integration testing | CTFL §2.2 |
| `security-scan` | Non-functional (security) testing | CT-SEC; OWASP / ASVS; ISO/IEC 25010 Security |
| `shift-right` | Testing in production (shift-right) | Quality in DevOps (Specialist); ISO/IEC/IEEE 29119-3 Production Verification Report |
| `ci` | Build-wide CI triage + confirmation testing + defect management | CTFL §1.4, §5.5, §6; DevOps |
| `fix-ci` | Test execution / test environment mgmt | CTFL §6; DevOps |
| `flaky-hunt` | Test automation maintenance & reliability | CT-TAE; CTFL §6 |
| `review-pr` | Static review of a change + impact analysis + risk-based selection | CTFL §3, §2.3, §5.2 |
| `commit` | Confirmation testing + traceability of a change | CTFL §1.4, §1.4.4; Glossary (confirmation testing) |
| `open-pr` | Change-level test reporting (completion-style summary) | CTFL §1.4, §5.3; ISO 29119-3 |
| `merge-gate` | Exit-criteria evaluation at change scope (go/no-go) | CTFL §5.3; CTAL-TM |
| `automation-audit` | Static testing of testware + automation architecture assessment | CTFL §3.1; CT-TAE; ISO/IEC 25010 |
| `review-coverage` | Test monitoring (coverage) + analysis | CTFL §5.3 |
| `status-report` | Test monitoring & control | CTFL §5.3 |
| `triage` | Defect management | CTFL §5.5 |
| `release-report` | Test completion | CTFL §1.4; ISO 29119-3 |

---

## 14. Full ISTQB syllabus → command coverage

This matrix shows that **every applicable ISTQB syllabus has at least one command**, so a tester can perform the full body of knowledge through the agent. Domain-gated syllabi (Automotive, Finance, Gambling, Gaming) are out of scope for a general Web + API product and are marked extensible.

| ISTQB syllabus | Stream / level | Covered by command(s) |
|---|---|---|
| Foundation Level (CTFL v4.0) | Core / Foundation | All commands; principles & process embedded in `qa-context` |
| Advanced Test Manager (CTAL-TM) | Core / Advanced | `test-policy`, `create-strategy`, `create-plan`, `risk-assessment`, `estimate`, `cost-of-quality`, `status-report`, `release-report`, `process-improvement` |
| Advanced Test Analyst (CTAL-TA) | Core / Advanced | `test-design`, `exploratory`, `acceptance`, `usability-test` |
| Advanced Technical Test Analyst (CTAL-TTA) | Core / Advanced | `test-design` (white-box), `coverage-measure`, `static-review`, `nonfunctional`, `perf-test`, `security-scan` |
| Improving the Test Process (Expert) | Expert | `process-improvement` |
| Test Management (Expert) | Expert | `test-policy`, `estimate`, `process-improvement`, `status-report` |
| Agile Tester (CTFL-AT) | Agile / Foundation | `create-strategy` (agile mapping), `acceptance`, `exploratory`, `create-plan` |
| Agile Technical Tester (CT-ATT) | Agile | `implement`, `scaffold`, `test-data`, `fix-ci` |
| Agile Test Leadership at Scale | Agile | `test-policy`, `process-improvement` |
| Test Automation Engineering (CT-TAE) | Specialist | `automate`, `automation-strategy` (gTAA), `automation-audit` (gTAA/SOLID assessment), `api-automate`, `web-automate`, `mobile-automate`, `scaffold`, `implement`, `flaky-hunt`, `tool-select`, `test-env` |
| Test Automation Strategy | Specialist | `automation-strategy`, `tool-select` |
| Performance Testing (CT-PT) | Specialist | `perf-plan` (planning/workload model), `perf-test` (scripting/execution) |
| Security Testing (CT-SEC) | Specialist | `security-scan` |
| Security Test Engineer | Specialist | `security-scan` |
| Acceptance Testing (CT-AcT) | Specialist | `acceptance` |
| Usability Testing (CT-UT) | Specialist | `usability-test`, `a11y-audit` |
| AI Testing (CT-AI) | Specialist | `ai-test` |
| Testing with Generative AI (CT-GenAI) | Specialist | `genai-assist` |
| Model-Based Testing (CT-MBT) | Specialist | `mbt` |
| Mobile Application Testing (CT-MAT) | Specialist | `mobile-automate` (native/cross-platform via Appium/device farm), `mobile-test` (responsive web) |
| Quality in DevOps | Specialist | `scaffold` (CI), `ci`, `fix-ci`, `fix-jenkins`, `review-pr`, `commit`, `open-pr`, `merge-gate`, `coverage-measure`, `shift-right` |
| Accessibility | Specialist | `a11y-audit` |
| Automotive / Finance / Gambling / Game | Specialist (domain) | *Extensible — add a command + config domain if the product is in this domain.* |
| Glossary / learning | — | `istqb-coach` (on-demand reference for any concept) |

> **Completeness:** for a topic-by-topic walk of every CTFL chapter and Advanced/Specialist syllabus against commands (the gap analysis), see [`ISTQB-COVERAGE.md`](./ISTQB-COVERAGE.md).

### Complete command catalog (64) by ISTQB activity

- **Test planning & management:** `qa-init`, `test-policy`, `create-strategy`, `create-plan`, `risk-assessment`, `estimate`, `tool-select`, `process-improvement`
- **QA management & governance:** `quality-report`, `team-plan`, `go-no-go`, `cost-of-quality`, `audit-prep`
- **Static testing & analysis:** `static-review`, `static-analysis`, `automation-audit`
- **Test analysis & design:** `test-cases`, `test-design`, `combinatorial`, `acceptance`, `mbt`, `exploratory`, `review-coverage`
- **Test levels & change-related:** `unit-test`, `integration-test`, `maintenance-test`, `regression`
- **Dynamic analysis & production:** `dynamic-analysis`, `shift-right`
- **Test implementation & automation:** `scaffold`, `automate`, `automation-strategy`, `api-automate`, `web-automate`, `mobile-automate`, `scan-ui`, `implement`, `add-test`, `test-data`, `test-env`
- **Test automation maintenance:** `self-heal`, `flaky-hunt`, `fix-jenkins`
- **Performance:** `perf-plan`, `perf-test`
- **Test execution (functional & non-functional):** `perf-test`, `a11y-audit`, `usability-test`, `nonfunctional`, `security-scan`, `contract-sync`, `mobile-test`, `ai-test`, `regression`, `ci`, `fix-ci`, `fix-jenkins`, `flaky-hunt`
- **Version control & PR quality:** `review-pr`, `commit`, `open-pr`, `merge-gate`
- **Monitoring, control & completion:** `status-report`, `coverage-measure`, `triage`, `release-report`
- **AI-assisted & reference:** `genai-assist`, `istqb-coach`

---

## References

- ISTQB Certified Tester Foundation Level Syllabus v4.0 — https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/
- ISTQB Certification portfolio (Core / Agile / Specialist) — https://istqb.org/certifications/
- ISTQB Glossary of testing terms — https://astqb.org/resources/glossary-of-software-testing-terms/
- ISO/IEC/IEEE 29119 (Software testing standard, Part 3: Test documentation)
- ISO/IEC 25010 (Product quality characteristics)

*The seven principles, the seven test-process activities, and the terminology used here are ISTQB concepts. © ISTQB for the syllabi and glossary; this document is an implementation map, not a copy.*
