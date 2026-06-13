# QA Toolkit — Full Command Guideline

The complete operating manual for all **60 `/qa:*` commands**. For each command you get: what it does, **when** to use it, what it **needs** (prerequisites), what it **outputs**, and what to run **next**. It also gives ready-made **workflow recipes** and a **"which command do I use?"** index.

- New here? Read [§1 How the toolkit works](#1-how-the-toolkit-works) → [§2 Quick-start recipes](#2-quick-start-workflow-recipes), then dip into the [§4 command reference](#4-command-reference) as needed.
- Want a copy-paste **sample invocation for every command** (with a "Correct when" check)? See [COMMAND-EXAMPLES.md](./COMMAND-EXAMPLES.md).
- One-line summaries and the syllabus map live in the [README](../README.md) and [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md). This guide is the *how-to*.

---

## 1. How the toolkit works

**One config drives everything.** Every command reads `qa.config.yml` at your project root — stack, tooling toggles, CI platform, quality gates/SLAs, risk areas, environments, paths, team. You maintain that one file; the commands are identical across all projects.

**The golden rule:** run **`/qa:qa-init` first** in any new project to generate `qa.config.yml`. Without it, most commands will prompt you to create it.

**Standing conventions every command honors:**
- **Tooling toggles** — a command skips a tool that's disabled in `qa.config.yml` (e.g. no Pact → `contract-sync` is a no-op).
- **Paths** — generated docs go to `paths.docs_dir`, testware to `paths.tests_dir`, reports to `paths.reports_dir`.
- **Quality gates** — `gates` thresholds are the **exit criteria**; results are always expressed with residual risk (never "defect-free").
- **Stable selectors & data ownership** — `getByRole`/`getByLabel`/`data-testid`, web-first assertions, no hard waits; each test owns its data via factories; synthetic data only, secrets from `test_data.secrets_store`.
- **ISTQB process** — each command states which of the seven activities it performs (planning → monitoring & control → analysis → design → implementation → execution → completion).

**Prerequisites you provide outside the config (only where noted):**
- **Running app + `stack.base_url_web`** for `scan-ui`, `web-automate`, `a11y-audit`, `shift-right`.
- **OpenAPI/Swagger spec** for `api-automate`.
- **Framework present** (run `/qa:scaffold` once) before commands that *run* tests: `implement`, `web-automate`, `api-automate`, `scan-ui`, `perf-test`, `add-test`.
- **Env vars** `JENKINS_USER` + `JENKINS_API_TOKEN` (and `ci.jenkins_url`/`ci.jenkins_job` in config) for `fix-jenkins`.

**Legend** — **Needs:** assumes `qa.config.yml` exists unless stated; only *extra* prerequisites are listed. **Output:** `→ docs` means a document under `paths.docs_dir`; `→ tests` means code under `paths.tests_dir`; `→ report` means an in-chat summary.

---

## 2. Quick-start workflow recipes

Copy-paste sequences for the common situations. Each step links to the detailed entry in §4.

### A. Brand-new project (greenfield)
```text
/qa:qa-init                      # 1. generate qa.config.yml (interview)
/qa:test-policy                  # 2. (optional) org-level policy
/qa:create-strategy              # 3. program test strategy
/qa:automation-strategy          # 4. automation architecture (gTAA)
/qa:scaffold                     # 5. build the framework (Playwright/K6/Pact/CI)
/qa:risk-assessment              # 6. score product/project risk
/qa:create-plan R1 "feat a,b"    # 7. release test plan
/qa:implement "feature a"        # 8. write + run tests for the feature
```

### B. Per-release / per-sprint loop
```text
/qa:risk-assessment <release>    # what's risky this release
/qa:create-plan <release> <feats>
/qa:test-cases <requirement>     # design cases (repeat per story)
/qa:implement <feature>          # automate + run
/qa:regression <change>          # pick the regression set
/qa:status-report <release>      # mid-release monitoring & control
/qa:go-no-go <release>           # release gate
/qa:release-report <release>     # completion report after ship
```

### C. Turn manual test cases into automation
```text
/qa:automate path/to/manual-cases.csv   # score ROI, pick candidates, plan
/qa:implement "<top candidate>"          # build the selected tests
/qa:test-data <entity>                    # data factories the tests need
```

### D. Bootstrap automation from a live UI
```text
/qa:scaffold                     # if no framework yet
/qa:scan-ui https://app/login    # discover elements → page objects → cases
/qa:web-automate "checkout"      # deepen into full journeys
/qa:self-heal                    # keep locators current later
```

### E. A red build came in
```text
/qa:ci                           # whole build: pull, bucket every failure, fix + confirm, harden ×3
/qa:ci x                         # …then verify the full suite locally (extended gate)
# or target one thing:
/qa:fix-jenkins <build-url>      # pull failed cases, fix, re-run locally (Jenkins)
/qa:fix-ci ci.log                # diagnose + fix a single pipeline / pasted log (any CI)
/qa:flaky-hunt                   # if failures are intermittent
/qa:triage "<failure>"           # if it's a real product defect
```

### F. Inherited / unknown automation project (health check)
```text
/qa:automation-audit             # score architecture, SOLID, design quality, anti-patterns
/qa:review-coverage              # where coverage is thin
/qa:static-analysis              # source complexity/maintainability metrics
/qa:automation-strategy          # define the target architecture to refactor toward
```

### G. Non-functional sweep on a high-risk area
```text
/qa:perf-plan <area>  →  /qa:perf-test <endpoint>
/qa:security-scan
/qa:a11y-audit <page>
/qa:nonfunctional reliability
```

---

## 3. The command map (all 60 at a glance)

| Phase | Commands |
|---|---|
| **Planning & management** | `qa-init` · `test-policy` · `create-strategy` · `create-plan` · `risk-assessment` · `estimate` · `tool-select` · `process-improvement` |
| **Governance** | `quality-report` · `team-plan` · `go-no-go` · `cost-of-quality` · `audit-prep` |
| **Static testing, analysis & design** | `static-review` · `static-analysis` · `automation-audit` · `test-cases` · `test-design` · `combinatorial` · `acceptance` · `mbt` · `exploratory` · `review-coverage` |
| **Test levels & change-related** | `unit-test` · `integration-test` · `maintenance-test` · `dynamic-analysis` · `shift-right` · `regression` |
| **Implementation** | `scaffold` · `automate` · `implement` · `add-test` · `test-data` · `test-env` |
| **Automation by surface** | `automation-strategy` · `api-automate` · `scan-ui` · `web-automate` · `mobile-automate` · `perf-plan` |
| **Execution (non-functional)** | `perf-test` · `a11y-audit` · `usability-test` · `nonfunctional` · `security-scan` · `contract-sync` · `mobile-test` · `ai-test` |
| **Maintenance, CI & flakiness** | `ci` · `fix-ci` · `fix-jenkins` · `flaky-hunt` · `self-heal` |
| **Monitoring, control & completion** | `status-report` · `coverage-measure` · `triage` · `release-report` |
| **AI-assisted & reference** | `genai-assist` · `istqb-coach` |

---

## 4. Command reference

### 4.1 Planning & management

**`/qa:qa-init`** — Interview you and generate the per-project `qa.config.yml`.
- **When:** first thing in any new project; re-run to refresh config.
- **Needs:** nothing (it creates the config).
- **Output:** `./qa.config.yml`.
- **Then:** `create-strategy`, `scaffold`.

**`/qa:test-policy`** — Author the **Organizational Test Policy** (why/how the org tests, above any project).
- **When:** establishing org-wide QA governance.
- **Output:** `→ docs/TEST-POLICY.md`.
- **Then:** `create-strategy`.

**`/qa:create-strategy`** — Generate/refresh the program-wide **Test Strategy** (ISO 29119-3).
- **When:** you need the overall QA approach for the product.
- **Output:** `→ docs/TEST-STRATEGY.md`.
- **Then:** `automation-strategy`, `create-plan`.

**`/qa:create-plan <release-id> [features]`** — Release/sprint **Test Plan** from config + release + feature list.
- **When:** planning a specific release or sprint.
- **Output:** `→ docs/TEST-PLAN-<release-id>.md`.
- **Then:** `test-cases`, `implement`, `status-report`.

**`/qa:risk-assessment [release|area]`** — Score product & project risks (likelihood × impact) and derive the test response.
- **When:** start of a release, or to prioritize where to test deeply (Principle 4).
- **Output:** `→ docs/RISK-REGISTER-<scope>.md`.
- **Then:** `create-plan`, `review-coverage`, `test-design`.

**`/qa:estimate <scope>`** — Test effort **estimation** (metrics-based + expert-based).
- **When:** sizing a test effort, sprint capacity.
- **Output:** `→ report`.
- **Then:** `team-plan`, `create-plan`.

**`/qa:tool-select <need>`** — Evaluate & select a tool (benefits/risks, categories, pilot). *Uses web search.*
- **When:** choosing a new testing tool or justifying the toolchain.
- **Output:** `→ docs/TOOL-EVALUATION-<category>.md`.

**`/qa:process-improvement [focus]`** — Test process maturity assessment & improvement (TMMi/IDEAL).
- **When:** retrospectives, audits, or when escaped defects/flakiness/slow pipelines signal process pain.
- **Output:** `→ docs/PROCESS-IMPROVEMENT-<date>.md`.

### 4.2 Governance

**`/qa:quality-report [period]`** — Cross-release **quality KPI dashboard / exec report** (escaped defects, coverage, pass rate, MTTR, automation %, flaky rate).
- **When:** management/stakeholder reporting.
- **Output:** `→ docs/QUALITY-REPORT-<period>.md`.

**`/qa:team-plan [horizon]`** — QA **capacity & skills** — staffing vs backlog, skills matrix, training/onboarding.
- **When:** resourcing decisions, team development.
- **Output:** `→ docs/TEAM-PLAN-<horizon>.md`.

**`/qa:go-no-go <release-id>`** — Formal **release readiness gate**: consolidate all signals into a ship/hold decision with conditions, residual risk, sign-off.
- **When:** the release gate.
- **Needs:** quality signals exist (tests run, reports). Pairs with `status-report`/`coverage-measure`.
- **Output:** `→ docs/GO-NO-GO-<release>.md`.
- **Then:** `release-report`.

**`/qa:cost-of-quality [scope]`** — **CoQ & QA ROI** — prevention/appraisal/failure costs, automation payback, budget case.
- **When:** QA economics, business cases.
- **Output:** `→ docs/COST-OF-QUALITY-<scope>.md`.

**`/qa:audit-prep [standard]`** — **Audit/compliance readiness** — traceability + evidence pack, ISO 29119/ISTQB conformance, gaps.
- **When:** before an internal/external audit.
- **Output:** `→ docs/AUDIT-READINESS-<scope>.md`.

### 4.3 Static testing, analysis & design

**`/qa:static-review <story|spec|file> [review-type]`** — ISTQB **static testing**: review the test basis (requirements, stories, OpenAPI) for testability & defects (shift-left).
- **When:** before writing tests for a story/spec.
- **Output:** `→ report` (review findings).
- **Then:** `test-cases`, `test-design`.

**`/qa:static-analysis [path]`** — **Static analysis** of source code — complexity, control/data flow, coding-standard & maintainability metrics (no execution).
- **When:** assess code quality / find defect-prone units early.
- **Output:** `→ report`.

**`/qa:automation-audit [path]`** — **Audit an existing automation project**: gTAA architecture, **SOLID** & clean-code, test-case/design quality, anti-patterns, pyramid; scored health report + prioritized fixes. *Read-only.*
- **When:** onboarding/inheriting a suite, or a periodic health check.
- **Output:** `→ docs/AUTOMATION-AUDIT.md`.
- **Then:** routes findings to `static-analysis`, `review-coverage`, `automation-strategy`, `self-heal`, `flaky-hunt`.

**`/qa:test-cases <requirement|story|endpoint|file>`** — **Generate ISTQB test cases** with design techniques; outputs a Test Case Specification (+ CSV on request).
- **When:** whenever you need to derive concrete test cases.
- **Output:** `→ docs/TEST-CASES-<item>.md`.
- **Then:** `implement`, `automate`.

**`/qa:test-design <feature|story|endpoint>`** — Derive **test conditions + cases** using EP, BVA, decision table, state transition, ATDD (broader analysis context than `test-cases`).
- **When:** designing the test approach for a feature.
- **Output:** `→ docs/TEST-DESIGN-<item>.md`.

**`/qa:combinatorial <feature>`** — **Pairwise / classification-tree / orthogonal-array** design for multi-parameter features.
- **When:** several inputs/options combine and exhaustive testing is infeasible.
- **Output:** `→ docs/COMBINATORIAL-<feature>.md`.

**`/qa:acceptance <story>`** — **ATDD/BDD** acceptance criteria & Gherkin scenarios, collaboratively.
- **When:** turning a story into agreed, testable criteria before dev.
- **Output:** `→ docs/ACCEPTANCE-<story>.md`.

**`/qa:mbt <stateful flow>`** — **Model-Based Testing**: build a behavioral model (state machine) and derive cases by coverage.
- **When:** complex stateful flows where model coverage beats ad-hoc cases.
- **Output:** `→ docs/MBT-<feature>.md`.

**`/qa:exploratory <area>`** — Session-based **exploratory** testing charters (experience-based).
- **When:** high-risk or newly changed areas; complement to scripted tests.
- **Output:** `→ docs/EXPLORATORY-<feature>.md`.

**`/qa:review-coverage [area]`** — Audit **coverage gaps** vs strategy & risk; recommend the highest-value missing tests; check traceability.
- **When:** "what's under-tested?"
- **Output:** `→ report` (prioritized gap table).
- **Then:** `implement`, `test-cases`.

### 4.4 Test levels & change-related

**`/qa:unit-test <module>`** — **Component (unit)** testing — isolation, test doubles, statement/branch coverage at the lowest level.
- **Output:** `→ design + tests`.

**`/qa:integration-test <interface>`** — **Integration** testing — component & system integration, incremental vs big-bang strategy, stubs/drivers.
- **Output:** `→ design + tests`.

**`/qa:maintenance-test <change>`** — **Maintenance** testing — modification/migration/retirement + impact analysis.
- **When:** patches, upgrades, data migrations, decommissioning.
- **Output:** `→ docs/MAINTENANCE-<scope>.md`.

**`/qa:dynamic-analysis <flow>`** — **Dynamic analysis** — runtime memory/resource leaks, handle exhaustion, degradation over time.
- **When:** faults that only surface at runtime.
- **Output:** `→ docs/DYNAMIC-ANALYSIS-<scope>.md`.

**`/qa:shift-right [journey]`** — **Testing in production** — synthetic monitoring, observability, canary/A-B, feature flags, post-deploy smoke.
- **Needs:** live environment access.
- **Output:** `→ docs/SHIFT-RIGHT-<scope>.md`.

**`/qa:regression [change]`** — **Select & prioritize** the regression set via impact analysis; keep the suite lean.
- **When:** deciding what to regression-test for a change.
- **Output:** `→ report` (selected/prioritized set).

### 4.5 Implementation

**`/qa:scaffold`** — Build the **automation framework** — Playwright+TS structure, fixtures, config, plus K6/Pact/a11y/CI per config.
- **When:** first-time setup of testing in a project.
- **Output:** `→ framework files + Jenkinsfile/CI`.
- **Then:** `implement`, `web-automate`, `api-automate`.

**`/qa:automate <manual cases|requirement|feature>`** — Full **automation pipeline**: score priority & complexity, select candidates by ROI, design automated cases, plan, implement the top ones.
- **When:** deciding *what* to automate; converting manual → automated.
- **Output:** `→ docs/AUTOMATION-PLAN-<item>.md` + tests.
- **Then:** `implement` for remaining candidates.

**`/qa:implement <feature|story>`** — Turn cases into **tests at the right pyramid level** (E2E/API/component/contract) and run them. The generic engine.
- **Needs:** framework (`scaffold`).
- **Output:** `→ tests` (run + results).
- **Then:** `regression`, `status-report`.

**`/qa:add-test <description>`** — Add a **single focused** test from a plain-English description.
- **When:** one-off "add a test that…".
- **Output:** `→ tests` (one case).

**`/qa:test-data <entity>`** — Generate typed **data factories**, builders, fixtures, seeding/cleanup helpers.
- **When:** tests need data setup.
- **Output:** `→ tests` (factories/fixtures).

**`/qa:test-env [name]`** — Provision/document the **test environment** & testware configuration management.
- **Output:** environment definition (docker-compose/env/seed) `→ tests` + `→ docs/TEST-ENVIRONMENT.md`.

### 4.6 Automation by surface
> `automate` decides *what* to automate; these build the *how* for each surface.

**`/qa:automation-strategy`** — Program-level **Test Automation Strategy & gTAA** — approaches, level split, tool fit, CI, maintainability, metrics, ROI.
- **When:** set or review the overall automation architecture.
- **Output:** `→ docs/AUTOMATION-STRATEGY.md`.

**`/qa:api-automate <resource>`** — **API** test automation from OpenAPI — schema, CRUD, auth/role matrix, negative/boundary, data-driven.
- **Needs:** OpenAPI/Swagger spec; framework.
- **Output:** `→ tests` (API).

**`/qa:scan-ui <url|flow> [auth role]`** — Deep-dive a UI: discover every interactive element → **page objects** → covering test cases.
- **Needs:** running app + `base_url_web`; Playwright (`scaffold`).
- **Output:** page objects under `tests/pages/` + `→ docs/UI-SCAN-<target>.md`.
- **Then:** `web-automate`, `self-heal`.

**`/qa:web-automate <journey>`** — **Web UI / E2E** automation — POM, critical journeys, cross-browser, auth state, a11y/visual hooks.
- **Needs:** framework; running app for execution.
- **Output:** `→ tests` (E2E).

**`/qa:mobile-automate <flow> [native|web]`** — **Mobile** automation — native/cross-platform (Appium/device farm) or responsive mobile-web (Playwright).
- **Needs (native):** Appium/device farm config.
- **Output:** `→ tests` (mobile).

**`/qa:perf-plan [scope]`** — **Performance test planning** — objectives, SLAs, operational profiles, workload model. Feeds `perf-test`.
- **Output:** `→ docs/PERF-PLAN-<scope>.md`.
- **Then:** `perf-test`.

### 4.7 Execution — non-functional

**`/qa:perf-test <endpoint|journey> [load|stress|spike|soak]`** — Generate (and optionally run) a **K6** test with thresholds from config.
- **Needs:** K6 (`scaffold`); ideally a `perf-plan`.
- **Output:** `→ tests` (K6 script) + run results.

**`/qa:a11y-audit [page]`** — **Accessibility** checks (axe) vs the WCAG target.
- **Needs:** axe enabled; page/URL reachable.
- **Output:** `→ a11y tests + report`.

**`/qa:usability-test <flow>`** — **Usability/UX** evaluation (heuristics, task scenarios) — distinct from a11y.
- **Output:** `→ docs/USABILITY-<feature>.md`.

**`/qa:nonfunctional <characteristic>`** — **Reliability, compatibility, portability, maintainability** (ISO/IEC 25010).
- **Output:** `→ docs/NONFUNCTIONAL-<characteristic>.md`.

**`/qa:security-scan [sast|sca|dast|secrets|all]`** — Security **baseline** — SAST, SCA, DAST (OWASP ZAP), secret scan, per config.
- **Needs:** the relevant scanners enabled in `tooling.security`.
- **Output:** `→ config/run + report`.

**`/qa:contract-sync [consumer|provider|can-i-deploy]`** — **Pact** contracts + `can-i-deploy`.
- **Needs:** Pact enabled.
- **Output:** `→ contracts + report`.

**`/qa:mobile-test [page]`** — Responsive/**mobile-web** testing — viewports, touch, network, device matrix.
- **Output:** `→ tests/report`.

**`/qa:ai-test <feature>`** — Test **AI/ML** components (CT-AI) — data quality, model metrics, bias/fairness, robustness, explainability, drift.
- **When:** the SUT includes AI/ML features.
- **Output:** `→ docs/AI-TEST-<feature>.md` + automatable metric/data checks `→ tests`.

### 4.8 Maintenance, CI & flakiness

**`/qa:ci ['x'|'full'] [build]`** — **End-to-end red-build orchestrator** (any CI). Pulls the **whole** failing build, buckets **every** failure (test defect / product defect / env / flaky), fixes the fixable ones, **confirms each locally**, and **hardens to green ×3**; real product defects are escalated via `triage`, never masked. `x`/`full` adds a mandatory-stability + full-suite local gate.
- **When:** a build went red and you want the whole build triaged in one pass — not just one log.
- **Needs:** `ci.platform` (+ `ci.jenkins_url`/`ci.jenkins_job` & `JENKINS_USER`/`JENKINS_API_TOKEN`, or `gh` for GitHub Actions) — or a build URL — or local JUnit artifacts.
- **vs.** `fix-ci` (one pasted log/pipeline) and `fix-jenkins` (Jenkins-only pull); `ci` is the build-wide superset that adds the stability gate.
- **Output:** `→ fixes + local confirm + green-×3 + Test Execution Log`; defects `→ triage`.

**`/qa:fix-ci [log]`** — Diagnose & fix a failing **pipeline/test run** (any CI). Classifies root cause, applies safe fixes, reproduces locally.
- **When:** build red, or local-pass/CI-fail; paste a log path.
- **Output:** `→ fix + report`.

**`/qa:fix-jenkins [build URL|job path]`** — Pull the **latest Jenkins build's failed cases**, fix each by root cause, **re-run only those locally until green**; escalate real defects via `triage` (never mask).
- **Needs:** `ci.jenkins_url` + `ci.jenkins_job` in config and `JENKINS_USER`/`JENKINS_API_TOKEN` env — or pass a build URL — or local JUnit artifacts.
- **Output:** `→ fixes + local run + report`.

**`/qa:flaky-hunt [path|N runs]`** — Find **flaky** tests, quarantine, and propose **deterministic** fixes (not blind retries).
- **Output:** `→ quarantine + fixes`.

**`/qa:self-heal [area]`** — **Maintain & auto-heal** the suite — repair broken locators after UI changes, prune/refactor, re-run to confirm. Heals *how we locate*, never *what we verify*.
- **Needs:** running app (for DOM probe) for high-confidence heals.
- **Output:** `→ healed code + report`.

### 4.9 Monitoring, control & completion

**`/qa:status-report <release-id>`** — ISTQB **Test Status (Progress) Report** — monitoring metrics + control actions mid-release.
- **Output:** `→ docs/STATUS-REPORT-<release>-<date>.md`.

**`/qa:coverage-measure [scope]`** — Measure **structural / requirements / risk coverage** and locate holes.
- **Output:** `→ report`.

**`/qa:triage <failure|bug>`** — Defect management — classify **severity vs priority**, draft a clear ISTQB defect report.
- **When:** a test fails for a real reason, or a bug is reported.
- **Output:** `→ defect report`.

**`/qa:release-report <release-id>`** — ISTQB **Test Completion Report** — exit criteria, residual risk, ship/hold.
- **When:** end of a release.
- **Output:** `→ docs/RELEASE-REPORT-<release>.md`.

### 4.10 AI-assisted & reference

**`/qa:genai-assist <task>`** — Use **GenAI** to accelerate testing (ideas, data, case drafting) with CT-GenAI safeguards (human oversight, privacy).
- **Output:** varies by task.

**`/qa:istqb-coach <topic>`** — On-demand **ISTQB reference & coach** — explain/apply any concept, route you to the right command. *Uses web search.*
- **When:** learn a technique, check a definition, or "how do I test X the ISTQB way?"
- **Output:** `→ explanation + command routing`.

---

## 5. "Which command do I use?" index

| I want to… | Command |
|---|---|
| Set up QA in a new repo | `qa-init` → `scaffold` |
| Write the test strategy / plan | `create-strategy` / `create-plan` |
| Decide where to test deeply | `risk-assessment` |
| Turn a requirement into test cases | `test-cases` (or `test-design` for the approach) |
| Cover a many-parameter feature efficiently | `combinatorial` |
| Agree acceptance criteria with the team | `acceptance` |
| Explore a risky/changed area | `exploratory` |
| Automate a feature's tests | `implement` (or `automate` to choose ROI candidates) |
| Build tests from a live UI | `scan-ui` → `web-automate` |
| Automate API tests from OpenAPI | `api-automate` |
| Add one quick test | `add-test` |
| Set up test data | `test-data` |
| Load/stress test | `perf-plan` → `perf-test` |
| Check accessibility | `a11y-audit` |
| Run security checks | `security-scan` |
| See what's under-tested | `review-coverage` / `coverage-measure` |
| Assess an inherited automation suite (architecture/SOLID) | `automation-audit` |
| Check source code quality | `static-analysis` |
| Triage & fix a whole red build (any CI), end-to-end | `ci` |
| Fix a red Jenkins build | `fix-jenkins` |
| Fix any red pipeline / pasted log | `fix-ci` |
| Deal with intermittent failures | `flaky-hunt` |
| Repair tests after a UI change | `self-heal` |
| File a bug properly | `triage` |
| Pick the regression set for a change | `regression` |
| Report progress mid-release | `status-report` |
| Make the ship/hold call | `go-no-go` → `release-report` |
| Report quality to management | `quality-report` |
| Prep for an audit | `audit-prep` |
| Learn an ISTQB concept | `istqb-coach` |

---

## 6. Outputs map (where things land)

- **Documents** → `paths.docs_dir` (default `docs/qa/`): strategies, plans, registers, design specs, audits, reports.
- **Testware** → `paths.tests_dir` (default `tests/`): specs, page objects (`tests/pages/`), API clients, data factories, K6 scripts, Pact contracts.
- **Reports/artifacts** → `paths.reports_dir` (default `reports/`): run results, coverage, JUnit XML, HTML reports.
- **The config** → `./qa.config.yml` (project root). Maintained by `qa-init`; never hardcode what it already defines.

---

## 7. Tips & gotchas

- **Run `qa-init` first.** Almost every command degrades to "create `qa.config.yml` first" without it.
- **Respect tooling toggles.** If Pact/K6/security scanners are off in config, the matching commands intentionally do little — flip the toggle (or `tool-select` first).
- **Read-only vs writing.** `automation-audit`, `static-analysis`, `static-review`, `review-coverage`, `coverage-measure`, `estimate`, and the governance/report commands **analyze and report** — they don't modify code. Implementation/automation commands write tests; the doc commands write to `paths.docs_dir`.
- **Never mask defects.** `fix-jenkins`, `fix-ci`, `self-heal`, and `flaky-hunt` fix *test/flaky/env* causes; a genuine product defect is escalated via `triage`, with the test left asserting correct behavior.
- **Jenkins auth via env only.** `fix-jenkins` reads `JENKINS_USER`/`JENKINS_API_TOKEN` from the environment — never store tokens in `qa.config.yml`.
- **Improve once, benefit everywhere.** Because commands are shared, edit `commands/<name>.md` or `templates/` in this toolkit to change behavior across all your projects; keep project-specific values in each repo's `qa.config.yml`.

---

*Generated for QA Toolkit v3.9.0 — 60 commands. Full syllabus traceability: [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md) · terminology: [GLOSSARY.md](./GLOSSARY.md).*
