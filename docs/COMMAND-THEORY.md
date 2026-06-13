# How each command works — mechanics & the theory behind it

This is the **"why it works" reference**. For every `/qa:*` command it states three things:

- **Produces** — the work product it writes (named per **ISO/IEC/IEEE 29119-3** wherever one applies).
- **How it works** — the mechanics: what it reads, the steps it runs, the decision logic.
- **Theory & basis** — the ISTQB concept, test-design technique, principle, and/or ISO standard that justifies the approach, and *why* that grounding makes the output correct.

> Companion docs: [COMMAND-GUIDE.md](./COMMAND-GUIDE.md) (operational how-to) · [COMMAND-EXAMPLES.md](./COMMAND-EXAMPLES.md) (worked outputs) · [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md) (syllabus traceability) · [GLOSSARY.md](./GLOSSARY.md) (terms) · [WORKFLOWS.md](./WORKFLOWS.md) (role playbooks).
>
> **On syllabus citations:** the commands cite ISTQB sections to show their lineage, but ISTQB renumbers between syllabus versions. Each command (and this doc) treats section numbers as *verify-before-quoting*, never as load-bearing. The **concepts** are stable; the **§ numbers** are not. ISTQB® materials are copyrighted by ISTQB; this toolkit implements their concepts, it does not reproduce them.

---

## The shared foundation — the spine every command sits on

Before the per-command detail, here is the theory the *whole* toolkit is built on. Every command is an application of these; the per-command "Theory & basis" sections below only add what is specific to that command.

### 1. The seven ISTQB principles are standing rules, not trivia
They are enforced as guardrails inside the commands:

| Principle | Where it shows up in the commands |
|---|---|
| **1 · Testing shows the presence of defects, not their absence** | Every report states *residual risk*; `release-report`/`go-no-go` never claim "zero bugs"; `fix-*`/`ci` escalate real defects instead of masking them. |
| **2 · Exhaustive testing is impossible** | `combinatorial` (pairwise) and `risk-assessment` (risk-based depth) exist precisely because you must sample intelligently, not test everything. |
| **3 · Early testing (shift-left)** | `static-review`, `static-analysis`, `acceptance`, `test-design` all act *before* execution — the cheapest place to remove a defect. |
| **4 · Defects cluster** | `risk-assessment` concentrates depth on high-risk areas; BVA/EP in `test-cases` target where defects congregate (boundaries). |
| **5 · Tests wear out (pesticide paradox)** | `review-coverage`, `flaky-hunt`, `self-heal` refresh/retire stale tests so the suite keeps finding new defects. |
| **6 · Testing is context-dependent** | The whole design: one `qa.config.yml` per project changes *what* the identical commands do. |
| **7 · Absence-of-errors fallacy** | `usability-test`, `acceptance`, `risk-assessment` validate fitness for real user needs, not just defect counts. |

### 2. The seven test-process activities are the command map
ISTQB's test process (CTFL v4.0 §1.4) is the backbone the catalog is organized around: **planning → monitoring & control → analysis → design → implementation → execution → completion**. Each command implements one (or part) of these activities — which is exactly the grouping used below and in the README.

### 3. Every work product is an ISO/IEC/IEEE 29119-3 artifact
The commands don't invent document shapes — they emit the standard's named work products: Test Strategy, Test Plan, Test Design / Case / Procedure Specifications, Test Data, Test Environment Requirements, Test Execution Log / Results, Incident (Defect) Report, Test Status Report, Test Completion Report. This is what makes the output **auditable and portable** between teams and tools.

### 4. Non-functional quality is measured against ISO/IEC 25010
Performance, security, accessibility, usability, reliability, compatibility, portability and maintainability commands all target the **ISO/IEC 25010** product-quality characteristics, so "quality" is a measurable sub-characteristic with a gate — not an opinion.

### 5. `qa.config.yml` is the single context input
One file holds stack, tooling toggles, CI platform, quality gates/SLAs, risk tiers, environments, and team. Every command **reads it and resolves all tool/path/threshold references from it** — nothing is hardcoded. This is Principle 6 (context-dependence) turned into an engineering mechanism: the commands and templates are identical across projects; only the config differs.

### 6. Two distinctions the commands refuse to collapse
- **Severity ≠ Priority** — severity is the defect's *impact on the test object* (a tester's technical judgment); priority is the *urgency to fix* (a business decision). `triage` and every defect report keep them as two independent fields.
- **Confirmation testing ≠ Regression testing** — confirmation re-runs the tests that *failed* to prove a fix worked; regression re-runs tests that *passed* to prove the change broke nothing. `ci`/`fix-*` do confirmation; `regression` scopes regression.

### 7. Bidirectional traceability is preserved end-to-end
Test basis → risk/condition → case → coverage item → procedure → result → defect, and back. Planning, design, monitoring and completion commands all keep this chain intact so nothing is an orphan and coverage is provable.

### 8. Every writing command ends with a self-check
Each command runs a final **Self-check / residual-risk** gate (config reflected · traceability intact · measurable · residual risk stated · work product named) before finalizing. That gate is what turns "an LLM wrote something plausible" into "a standards-conformant work product."

---

## A · Test planning & management
*ISTQB test process: planning (CTFL §5) · CTAL-TM · Expert Test Management.*

### `/qa:qa-init` — generate the per-project config
- **Produces:** `qa.config.yml` (the project test-context configuration that feeds the Organizational Test Strategy and every later artifact).
- **How it works:** detects project signals (package manifest, API spec, CI files, test dirs), interviews you for what it can't infer, runs a pre-write validation (schema match, valid YAML, no invented values, mandatory minimum), then writes the config and emits a readiness checklist.
- **Theory & basis:** realizes the **test-planning** activity's first step — establishing project context (CTFL v4.0 §1.4). The config is the **29119-3 context input** every downstream work product consumes; treating it as the single source enforces Principle 6 (context-dependence).

### `/qa:test-policy` — organizational test policy
- **Produces:** the **Organizational Test Policy** — top of the documentation hierarchy.
- **How it works:** states *why* the organization tests and *what* quality means (objectives, value, principles); deliberately leaves the *how* to the strategy.
- **Theory & basis:** the policy is the highest tier of the ISTQB/29119 document hierarchy (policy → strategy → plan). Separating WHY (policy) from HOW (strategy) is the standard's own layering.

### `/qa:create-strategy` — organizational test strategy
- **Produces:** the ISO/IEC/IEEE 29119-3 **Organizational Test Strategy**.
- **How it works:** generates the program-wide approach from `qa.config.yml` — levels, types, techniques, automation, environments, entry/exit — using strict ISTQB terminology and the seven principles.
- **Theory & basis:** test planning at program scope (CTFL §5.1; CTAL-TM; agile mapping per CTFL-AT). It is product-/org-wide and long-lived, distinct from a release Test Plan.

### `/qa:create-plan <release> [features]` — release/sprint test plan
- **Produces:** a release-scoped ISO/IEC/IEEE 29119-3 **Test Plan**.
- **How it works:** combines the config + a release name + feature list into scope, approach, entry/exit criteria, schedule, and risks, with bidirectional traceability seeded.
- **Theory & basis:** the **Test Plan** work product (CTFL §5.1; 29119-3). A plan is risk- and context-driven, which is why it consumes the risk register and config rather than a fixed template.

### `/qa:risk-assessment [scope]` — product risk register
- **Produces:** a **Product Risk Register**.
- **How it works:** identifies product & project risks, scores each **likelihood × impact**, assigns a tier (critical/high/medium), and derives the test response (depth) per tier.
- **Theory & basis:** **risk-based testing** (CTFL §5.2; CTAL-TM). It operationalizes Principle 2 (can't test everything) and Principle 4 (defects cluster) — depth follows risk, so finite effort lands where failure hurts most.

### `/qa:estimate <scope>` — test effort estimation
- **Produces:** `ESTIMATE-<release>.md`.
- **How it works:** applies **metrics-based** (historical data/velocity) and **expert-based** (informed judgment) estimation to a release/feature/backlog, with assumptions and ranges.
- **Theory & basis:** ISTQB test estimation techniques (CTAL-TM), supporting the Test Plan within the planning activity. Two complementary techniques are used because each corrects the other's bias.

### `/qa:tool-select <need>` — tool evaluation decision record
- **Produces:** a **Tool Evaluation** decision record that feeds the Test Automation Strategy.
- **How it works:** classifies the tool category, builds a weighted criteria matrix, weighs benefits/risks, proposes a pilot/PoC, and recommends — or justifies the status quo.
- **Theory & basis:** the ISTQB **tool-selection process** (CT-TAE / Test Automation Strategy; generic tool support CTFL §6). Framed as an ROI/investment decision so the answer is never "adopt every tool."

### `/qa:process-improvement` — test-process maturity & roadmap
- **Produces:** one advisory improvement report (changes no code/CI).
- **How it works:** assesses maturity through a model lens (e.g. TMMi/TPI) and runs the **IDEAL** cycle (Initiating–Diagnosing–Establishing–Acting–Learning) to recommend prioritized improvements.
- **Theory & basis:** ISTQB Expert **"Improving the Test Process"** + IDEAL, with CTAL-TM metrics as inputs. The maturity model is used only as a diagnostic lens, not a compliance checkbox.

### `/qa:quality-report [period]` — cross-release KPI dashboard
- **Produces:** an executive quality dashboard / report.
- **How it works:** aggregates per-release metrics into trends — escaped defects, coverage, pass rate, MTTR, automation %, flaky rate — each mapped to its ISTQB term and ISO/IEC 25010 characteristic.
- **Theory & basis:** test measurement & reporting at management level (CTAL-TM; CTFL §5.3). It summarizes the 29119-3 per-release reports over time; it does not replace them.

### `/qa:team-plan [horizon]` — capacity & skills plan
- **Produces:** a team plan in the docs dir.
- **How it works:** maps staffing vs upcoming backlog, builds a skills matrix, finds gaps, and proposes training/onboarding.
- **Theory & basis:** test-team management (CTAL-TM / Expert). **Tester independence** (levels of independence) is the Foundation anchor; capacity/skills techniques are complementary management practice.

### `/qa:go-no-go <release>` — release readiness gate
- **Produces:** a governance **ship/hold decision record** with conditions, residual risk, and sign-off.
- **How it works:** consolidates every quality signal (coverage, defects, perf/security gates, exit criteria) into a deterministic recommendation built on top of the Status and Completion reports.
- **Theory & basis:** release decision against **exit criteria** + residual risk (CTFL §5.3; CTAL-TM). It is a cross-functional decision *record* layered over the 29119-3 reports, embodying Principle 1 (ship with stated residual risk, never "zero bugs").

### `/qa:cost-of-quality [scope]` — CoQ & QA ROI
- **Produces:** `COST-OF-QUALITY-<scope>.md`.
- **How it works:** splits cost into prevention / appraisal / internal-failure / external-failure, computes cost of poor quality and automation payback, and builds the budget case.
- **Theory & basis:** value of testing & test economics (CTAL-TM), grounded in the cost-of-defects/shift-left rationale (Principle 3) — defects get exponentially more expensive the later they're caught, which is what funds prevention.

### `/qa:audit-prep [standard]` — audit evidence pack
- **Produces:** an evidence pack + conformance gap list.
- **How it works:** assembles the artifacts an auditor expects, sample-checks **bidirectional traceability**, and flags ISTQB / ISO 29119 conformance gaps.
- **Theory & basis:** test documentation, traceability & conformance evidence (CTFL §1.4.4; 29119-3). Auditability rests on traceability being intact and work products being named to the standard.

---

## B · Static testing, analysis & design
*ISTQB test process: static testing (CTFL §3) · analysis & design (CTFL §4) · CTAL-TA/TTA.*

### `/qa:static-review <story|spec>` — review the test basis
- **Produces:** a **Review Report** (review findings).
- **How it works:** reviews the test basis (requirements/stories/API spec) for testability and defects; routes *source-code* analysis to `static-analysis`.
- **Theory & basis:** **static testing** (CTFL §3). Reviewing the basis realizes Principle 3 (early testing) — a defect found in the requirement never becomes a defect in code.

### `/qa:test-cases <requirement>` — generate test cases
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Case Specification** (+ CSV on request).
- **How it works:** analyzes the basis into test conditions, then applies design techniques to derive cases with risk-based detail and full traceability.
- **Theory & basis:** test analysis → design (CTFL §1.4, §4) using **EP, BVA, decision tables, state transition**. These techniques are how you sample the infinite input space well (Principle 2) and aim at where defects cluster (Principle 4).

### `/qa:test-design <feature>` — conditions + cases for a feature
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Design + Test Case Specification**.
- **How it works:** derives test conditions then cases from the basis across the full technique set (EP, BVA, decision table, state transition, ATDD), giving broader design context than the single-purpose `test-cases`.
- **Theory & basis:** the **test design** activity (CTFL §1.4, §4). Choosing the technique to the structure of the problem (rules → decision tables; states → state transition; ranges → BVA) is the core skill the command encodes.

### `/qa:combinatorial <feature>` — pairwise / classification-tree design
- **Produces:** a combinatorial Test Case set.
- **How it works:** for multi-parameter features, generates **pairwise (all-pairs)**, classification-tree, or orthogonal-array cases to get strong coverage with few tests.
- **Theory & basis:** combinatorial techniques (Advanced/CTAL-TA black-box). A direct realization of Principle 2 — most defects involve one or two factors, so all-pairs coverage catches them without the combinatorial explosion.

### `/qa:acceptance <story>` — ATDD/BDD acceptance tests
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Case Specification** (acceptance level).
- **How it works:** elicits testable acceptance criteria collaboratively and expresses them as **Given/When/Then** scenarios, tracing each criterion to a scenario.
- **Theory & basis:** **ATDD/BDD** (CTFL-AT). Agreeing acceptance tests *before* development is shift-left (Principle 3) and defends against the absence-of-errors fallacy (Principle 7) by validating real user needs.

### `/qa:mbt <flow>` — model-based testing
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Design Specification** derived from a model.
- **How it works:** builds a behavioral model (state machine / state-transition table) and derives cases to a stated coverage criterion (all-states / all-transitions / 0-switch).
- **Theory & basis:** **MBT (CT-MBT)** applying the **state-transition** technique (CTFL §4.2) via an explicit model. Coverage becomes a property of the model, so completeness is provable rather than ad-hoc.

### `/qa:exploratory <area>` — session-based exploratory charters
- **Produces:** exploratory test charters + session sheet (29119-3 testware).
- **How it works:** writes time-boxed **charters**, runs/structures the session, and captures findings in a session sheet.
- **Theory & basis:** **experience-based techniques** — exploratory / checklist / error-guessing (CTFL §4.4) under **session-based test management**. It finds defects scripted cases miss; it complements, never replaces, scripted coverage.

### `/qa:static-analysis [path]` — analyze source without running it
- **Produces:** a static-analysis findings report (modifies no code).
- **How it works:** computes complexity, control-/data-flow, coding-standard and maintainability metrics on the source.
- **Theory & basis:** **static analysis**, a form of static testing where code is analyzed not executed (CTFL §3.1; CTAL-TTA techniques). Shift-left (Principle 3) for code; distinct from reviewing the *basis* (`static-review`).

### `/qa:automation-audit [path]` — audit an inherited automation suite
- **Produces:** a scored health report with prioritized fixes (writes only the report).
- **How it works:** assesses gTAA layering/POM, **SOLID** & clean-code, test-case/design quality, anti-patterns, and pyramid/level distribution — the automation codebase is the test object.
- **Theory & basis:** static testing of **testware** + CT-TAE architecture assessment, scored against **ISO/IEC 25010 maintainability** (modularity, reusability, analysability, modifiability, testability). Reports only — analysis must never mutate the thing it judges.

### `/qa:review-coverage [area]` — coverage & traceability audit
- **Produces:** a coverage-gap + traceability report recommending the highest-value missing tests.
- **How it works:** compares coverage to the strategy and risk areas, verifies the bidirectional chain, and ranks gaps by risk.
- **Theory & basis:** test monitoring (coverage) + analysis (CTFL §5.3; §1.4.4 traceability). Counters the pesticide paradox (Principle 5) by surfacing what the current suite no longer protects.

---

## C · Test levels & change-related testing
*ISTQB test process: test levels (CTFL §2.2) · change-related types (CTFL §2.2.2, §2.3).*

### `/qa:unit-test <module>` — component (unit) testing
- **Produces:** component **Test Procedure Specifications** + a statement/branch coverage report.
- **How it works:** designs/reviews tests at the lowest level — isolation, test doubles, and structural coverage targets.
- **Theory & basis:** the **component test level** (CTFL §2.2). Cases come from black-box techniques (§4.2) *plus* **white-box** statement/branch coverage (§4.3) — the level where white-box coverage is meaningful.

### `/qa:integration-test <interface>` — integration testing
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Design Specification** for the interfaces under test.
- **How it works:** designs **component-integration** and **system-integration** tests, picks a strategy (incremental vs big-bang), defines test doubles (stubs/drivers), and builds an interface-coverage table.
- **Theory & basis:** the integration test levels (CTFL §2.2.1). Interfaces, not units, are the risk surface here; incremental integration localizes the fault when something breaks.

### `/qa:maintenance-test <change>` — maintenance testing
- **Produces:** a maintenance **Test Plan** (29119-3).
- **How it works:** for modifications/migration/retirement, runs **impact analysis** to scope what changed and what it touches, then drives confirmation of the change + regression of impacted areas.
- **Theory & basis:** maintenance testing + impact analysis (CTFL §2.3) driving the two change-related test types (§2.2.2). Impact analysis is what makes regression scoping evidence-based, not "run everything."

### `/qa:dynamic-analysis <flow>` — runtime fault detection
- **Produces:** a 29119-3 **Test Execution Log** extended with profiling/leak evidence.
- **How it works:** exercises the system while watching for memory/resource leaks, handle exhaustion, and runtime degradation over time.
- **Theory & basis:** **dynamic analysis** (CTAL-TTA) — finds faults invisible to static analysis because they only manifest during execution. Complements `static-analysis` (no execution) and `perf-test` (workload-driven).

### `/qa:shift-right [journey]` — testing in production
- **Produces:** a **Production Verification Report**.
- **How it works:** designs synthetic monitoring, observability/SLO checks, canary/A-B validation, and feature-flag/post-deploy smoke tests — safely, in the live environment.
- **Theory & basis:** testing in production / continuous testing (**Quality in DevOps**). It extends coverage to real conditions but explicitly **complements, never replaces** shift-left testing (Principle 3).

---

## D · Test implementation
*ISTQB test process: implementation (CTFL §1.4, §6) · CT-TAE.*

### `/qa:scaffold` — build the automation architecture
- **Produces:** the test-automation framework + CI pipeline (language/framework structure, fixtures, config, perf/contract/a11y per config).
- **How it works:** reads tooling toggles and generates the gTAA structure and testware the rest of the toolkit executes on.
- **Theory & basis:** **test implementation** (CTFL §1.4, §6; CT-TAE) — you cannot implement/execute tests without the testware architecture first. Built from config so the architecture matches the project's actual stack.

### `/qa:automate <cases|requirement>` — full automation pipeline
- **Produces:** a Test Automation Plan + implemented top-ROI cases.
- **How it works:** one pipeline — **assess → select → design → plan → implement**: scores priority × complexity, selects candidates by ROI, designs the automated cases, and builds the top ones.
- **Theory & basis:** CT-TAE + **risk-based prioritization** (CTFL §5.2) + implementation/execution (§1.4). Automating by ROI (not "automate everything") is the economic core of CT-TAE.

### `/qa:implement <feature>` — turn cases into running tests
- **Produces:** executable test procedures/scripts at the right level + a Test Execution Log.
- **How it works:** takes existing cases and implements/runs them at the correct pyramid level (E2E/API/component/contract); if no cases exist, it routes to `test-design` first.
- **Theory & basis:** **test implementation + execution** (CTFL §1.4) — the activity that converts the design (cases) into procedures and actually runs them.

### `/qa:add-test <description>` — single-case fast path
- **Produces:** one implemented and run test procedure.
- **How it works:** picks the right design technique for the single condition, implements it, and runs it.
- **Theory & basis:** design + implementation (CTFL §1.4, §4) compressed to one case — the quick path; `test-cases` (design) and `implement` (multi-level) are the full-suite paths.

### `/qa:test-data <entity>` — data factories & fixtures
- **Produces:** typed factories, builders, fixtures, and seeding/cleanup helpers.
- **How it works:** generates data testware per the configured strategy (factories/fixtures/db-seed), synthetic-only.
- **Theory & basis:** **test implementation** (CTFL §1.4) — preparing test data is implementation testware. Synthetic-only data enforces the privacy rule (no real PII) the toolkit applies everywhere.

### `/qa:test-env [name]` — provision the test environment
- **Produces:** the ISO/IEC/IEEE 29119-3 **Test Environment Requirements** work product.
- **How it works:** defines/provisions the environment and manages testware configuration from `qa.config.yml` (env provisioning, distinct from data factories).
- **Theory & basis:** implementation — environment setup so testware can execute (CTFL §1.4, §6; CT-TAE). Controlled environments make results reproducible and defects diagnosable.

---

## E · Test automation by surface
*The "how" per surface; `automate` decides *what*, these build it. CT-TAE / CT-PT / CT-MAT.*

### `/qa:automation-strategy` — program-level gTAA strategy
- **Produces:** the **Test Automation Strategy** work product.
- **How it works:** defines objectives, scope, approaches, tool fit, level distribution, CI, maintainability, metrics, ROI — above any single feature or release.
- **Theory & basis:** the **generic Test Automation Architecture (gTAA)** + program-level strategy (CT-TAE). Long-lived and org-wide, distinct from the release-scoped Automation Plan from `automate`.

### `/qa:api-automate <resource>` — API tests from OpenAPI
- **Produces:** 29119-3 **Test Procedure Specifications** (API scripts) + a Test Execution Log when run.
- **How it works:** generates schema validation, CRUD, auth/role matrix, negative & boundary, and data-driven tests from the spec.
- **Theory & basis:** automation (CT-TAE) at the **component-integration / API level** (CTFL §2.2.1), with black-box techniques (§4.2) over API inputs; the **OpenAPI spec is the test basis**, so the spec defines correctness.

### `/qa:scan-ui <url/flow>` — discover a UI into page objects
- **Produces:** a **Test Procedure Specification** (page objects + specs) and a **Test Case Specification** (discovered conditions).
- **How it works:** crawls a running UI, extracts stable locators/actions into Page Objects, then generates cases covering every element/action/flow.
- **Theory & basis:** analysis & design using the **running UI as the test basis**, implemented with the **Page Object Model** (CT-TAE). POM is the maintainability pattern that keeps UI tests from rotting (ISO 25010 maintainability).

### `/qa:web-automate <journey>` — system-level E2E
- **Produces:** system-level E2E tests (POM, cross-browser, per-role auth, a11y/visual hooks).
- **How it works:** automates critical user journeys at the system level with config-gated accessibility/visual checks.
- **Theory & basis:** automation (CT-TAE) at the **system test level** (CTFL §2.2). The **test pyramid** governs scope — reserve E2E for genuine journeys; push cheaper checks down to API/component.

### `/qa:mobile-automate <flow>` — mobile automation
- **Produces:** platform/screen objects + specs + a device-matrix coverage table.
- **How it works:** native/cross-platform via Appium or device farm, or responsive mobile-web via Playwright; emits the device matrix it covers.
- **Theory & basis:** **CT-MAT** executed through **CT-TAE**. Mobile UI automation is system-level and expensive, so the pyramid still applies — only genuine end-to-end flows belong on-device.

### `/qa:perf-plan [scope]` — performance test planning
- **Produces:** a performance test plan that feeds `perf-test`.
- **How it works:** defines objectives, SLAs, operational profiles, workload model, system/data needs, test types, and entry/exit — *before* any script.
- **Theory & basis:** **CT-PT** planning, in the 29119-3 Test Plan shape, risk-driven (CTFL §5.2), targeting **performance efficiency** (ISO 25010). Planning first is what turns "a number" into a tested requirement.

---

## F · Test execution — functional & non-functional
*ISTQB test process: execution (CTFL §2.2.2) · CT-PT/SEC/UT/AI/MAT · Quality in DevOps.*

### `/qa:perf-test <endpoint>` — run a K6 performance test
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Execution Log**.
- **How it works:** scripts (and optionally runs) load/stress/spike/soak with **pass/fail thresholds derived from `gates`/SLAs** in the config.
- **Theory & basis:** performance testing execution (CT-PT). Thresholds-as-gates make **performance efficiency** (and, for soak, **reliability**) — ISO 25010 — objectively pass/fail, not subjective.

### `/qa:a11y-audit [page]` — accessibility checks
- **Produces:** a **Test Execution Log** of axe checks vs the WCAG target.
- **How it works:** scaffolds or runs automated accessibility checks against the WCAG standard in config and blocks per the configured a11y severities.
- **Theory & basis:** non-functional accessibility testing, mapped to the **ISO/IEC 25010 Usability** characteristic (accessibility sub-characteristic); evaluation lineage is CT-UT. WCAG provides the external, measurable criterion.

### `/qa:usability-test <flow>` — usability evaluation
- **Produces:** a usability findings document.
- **How it works:** evaluates UX via heuristics and task scenarios against ISO 25010 usability sub-characteristics (distinct from accessibility, which it defers to `a11y-audit`).
- **Theory & basis:** usability evaluation (CT-UT; CTAL-TA quality-characteristic analysis) against **ISO/IEC 25010 usability**. Directly addresses Principle 7 — a defect-free product can still fail its users.

### `/qa:nonfunctional <characteristic>` — reliability/compat/portability/maintainability
- **Produces:** a 29119-3 **Test Design + Test Case Specification**.
- **How it works:** designs (and where automatable runs) tests for the non-functional types beyond perf/security/a11y, against measurable 25010 sub-characteristics.
- **Theory & basis:** non-functional test design (CTFL §2.2.2; CTAL-TTA) targeting **ISO/IEC 25010** product-quality characteristics — each made measurable so it can be gated.

### `/qa:security-scan` — security baseline
- **Produces:** a security baseline run/wiring (SAST, SCA, DAST, secret scan) + log.
- **How it works:** runs the configured security tools, gated by tooling toggles and the configured block-severities, aligned to OWASP Top 10 / ASVS.
- **Theory & basis:** non-functional **security** testing (CT-SEC; OWASP Top 10 / ASVS) mapped to the **ISO/IEC 25010 Security** characteristic (confidentiality, integrity, non-repudiation, accountability, authenticity). OWASP supplies the concrete threat checklist.

### `/qa:contract-sync` — consumer-driven contract testing
- **Produces:** consumer/provider contracts + a `can-i-deploy` gate + Test Execution Log.
- **How it works:** generates/verifies Pact contracts across the web↔API boundary and runs the deploy gate.
- **Theory & basis:** implementation & execution at the **component/system integration** level (CTFL §2.2; CT-TAE). Contracts catch integration breakage *without* a full integrated environment — the cheap place to find interface defects.

### `/qa:mobile-test [page]` — responsive/mobile-web testing
- **Produces:** responsive specs + a Test Execution Report with a device-matrix coverage table.
- **How it works:** exercises viewports, touch, network conditions, and a device matrix.
- **Theory & basis:** CT-MAT concerns applied to responsive web, exercising the **25010 characteristics most affected by small-screen/touch/network**: compatibility/portability, usability, performance efficiency, reliability.

### `/qa:ai-test <feature>` — test AI/ML components
- **Produces:** AI-specific test design/execution evidence.
- **How it works:** tests data quality, ML functional-performance metrics, bias/fairness, robustness, explainability, and drift.
- **Theory & basis:** **CT-AI**, mapping **ISO/IEC 25010** (functional suitability, reliability, performance, security) extended with **AI-specific characteristics** (correctness under non-determinism, adaptability, autonomy, drift resistance, transparency, freedom from unwanted bias). Non-deterministic systems need metric-based, not exact-match, oracles.

### `/qa:regression [change]` — select & prioritize the regression set
- **Produces:** the selected/prioritized regression set written to docs.
- **How it works:** uses **impact analysis** to select and prioritize which previously-passing tests to re-run, and to keep the suite lean.
- **Theory & basis:** change-related **regression testing** (CTFL §2.2.2) — re-running *passing* tests to detect new breakage, explicitly distinct from confirmation testing. Risk-based selection (CTAL-TM) keeps it affordable (Principle 2).

### `/qa:ci ['x'|'full'] [build]` — end-to-end red-build triage
- **Produces:** a 29119-3 **Test Execution Log**; product defects raised as Incident Reports.
- **How it works:** pulls the whole failing build (any platform), buckets every failure (test / product / env / flaky), fixes the fixable causes and **confirms each locally**, hardens fixed tests to **green ×3**, and escalates real product defects; `x`/`full` adds a full-suite gate.
- **Theory & basis:** **Quality in DevOps** + **confirmation testing** + **defect management** (CTFL §1.4, §2.2, §5.5). Honesty rule = Principle 1: a defect is escalated, never masked; a green build you can't trust is worse than a red one.

### `/qa:fix-ci [log]` — diagnose one failing pipeline
- **Produces:** a **Confirmation Test Execution Log**.
- **How it works:** classifies a single failure into one root-cause category (product defect / flaky / env / dependency / timeout / pipeline), applies a safe in-scope fix, and re-runs to confirm.
- **Theory & basis:** CI/CD + **confirmation testing** (CTFL §6; DevOps). Routes product defects to `triage` rather than patching the test — Principle 1 again.

### `/qa:fix-jenkins [build URL|job path]` — Jenkins pull-and-fix
- **Produces:** fixes + a local **Test Execution Log** of the re-run.
- **How it works:** pulls the latest Jenkins build's FAILED/REGRESSION cases, fixes each by root cause, and re-runs **only those** locally until green.
- **Theory & basis:** execution + defect management + confirmation testing (CTFL §1.4, §2.2, §5.5). Re-running only the previously-failed set is confirmation testing by definition.

### `/qa:flaky-hunt [path|N runs]` — kill non-determinism
- **Produces:** a Flaky-Hunt report (quarantine + deterministic fixes).
- **How it works:** finds intermittent tests, quarantines them against an SLA, fixes the **root cause** (waits/data/order), never blind retries.
- **Theory & basis:** test-automation maintenance & reliability (CT-TAE) targeting the suite's **ISO 25010 reliability**, countering the pesticide paradox (Principle 5). A false alarm destroys the signal that a failure means a defect.

### `/qa:self-heal [area]` — repair the suite after UI change
- **Produces:** repaired locators/tests + a confirming re-run.
- **How it works:** detects broken locators after UI/DOM changes, repairs with stable alternatives, prunes/refactors obsolete tests, and re-runs. Heals *how we locate*, never *what we verify*.
- **Theory & basis:** test-automation maintenance (CT-TAE); maintainability is an ISO 25010 property of the testware. Counters the pesticide paradox without weakening assertions.

---

## G · Monitoring, control & completion
*ISTQB test process: monitoring & control (CTFL §5.3) · defect management (§5.5) · completion (§1.4).*

### `/qa:status-report <release>` — test status (progress) report
- **Produces:** an ISO/IEC/IEEE 29119-3 **Test Status (Progress) Report**.
- **How it works:** reports monitoring metrics vs the plan and ends with **control recommendations** (reassign, descope, add sessions).
- **Theory & basis:** test monitoring & control (CTFL §5.3). Monitoring without control is just a dashboard — the report's value is the corrective action it mandates.

### `/qa:coverage-measure [scope]` — measure coverage
- **Produces:** a coverage report (read-only).
- **How it works:** measures structural (statement/branch), requirements/basis, and risk coverage against configured gates and names the holes.
- **Theory & basis:** monitoring — coverage measurement (CTFL §5.3; white-box §4.3). Coverage is a **metric, not a target to game** (Principle 7 — the absence-of-errors fallacy).

### `/qa:triage <failure>` — defect report (severity vs priority)
- **Produces:** a 29119-3 **Incident (Defect) Report**, one per defect.
- **How it works:** investigates the failure, classifies the root location, assigns **severity** and **priority independently**, flags release blockers per `gates.block_on_severity`, and writes the report with a unique ID and full traceability.
- **Theory & basis:** **defect management** (CTFL §5.5). The non-negotiable separation of severity (technical impact) from priority (business urgency) is the heart of the technique — collapsing them loses information leaders need.

### `/qa:release-report <release>` — test completion report
- **Produces:** the ISO/IEC/IEEE 29119-3 **Test Completion Report**.
- **How it works:** evaluates every quality gate against `gates`, states residual risk, and gives a deterministic Ship/Hold recommendation.
- **Theory & basis:** **test completion** — the seventh process activity (CTFL §1.4; CTAL-TM). Residual risk is mandatory (Principle 1): you report what is *not* covered, never "no defects remain."

---

## H · AI-assisted & reference

### `/qa:genai-assist <task>` — GenAI with ISTQB safeguards
- **Produces:** accelerated draft test artifacts (ideas, data, case drafts).
- **How it works:** uses generative AI to speed up test work under two hard safeguards — **mandatory human review** of every output and **privacy protection** (never send real PII/production data/secrets).
- **Theory & basis:** **CT-GenAI**. Every GenAI output is treated as an unverified draft (Principle 1 applied to the AI itself); the human-in-the-loop and privacy rules are the syllabus's non-negotiables.

### `/qa:istqb-coach <topic>` — on-demand ISTQB reference
- **Produces:** an explanation/application of any concept (optionally a concept note).
- **How it works:** explains or applies any ISTQB concept, technique, term, or process, and routes you to the right command to do it.
- **Theory & basis:** the **ISTQB Glossary** + syllabus body of knowledge, made interactive — the in-toolkit teacher that makes the other 59 commands learnable.

---

*Generated for QA Toolkit v3.9.0 — 60 commands. Concepts implement the ISTQB® body of knowledge (CTFL v4.0 + Advanced/Specialist) and ISO/IEC/IEEE 29119-3 / ISO/IEC 25010; section numbers are indicative — verify against the current syllabus before quoting externally. Full traceability: [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md).*
