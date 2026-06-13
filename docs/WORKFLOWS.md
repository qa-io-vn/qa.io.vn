# Role Playbooks — How to Work the Toolkit by Role

The [COMMAND-GUIDE](./COMMAND-GUIDE.md) tells you what each command does. **This document tells you how to *work*** — as a Manual Tester, Automation Tester, Performance Tester, Test Leader, or Test Manager. Each playbook gives the role's mission, its core command loop, and its daily / per-story / per-release cadence, so one person can carry the entire role through the agent.

You can be **all five roles** — just switch playbooks as the day demands. The roles hand work to each other at well-defined points; the [release lifecycle map](#the-release-lifecycle--all-roles-on-one-timeline) at the end shows the whole picture.

> Every command assumes `qa.config.yml` exists. New project? Run `/qa:qa-init` once first, then come back here.

---

## Contents

1. [🔍 Manual Tester](#-manual-tester)
2. [🤖 Automation Tester](#-automation-tester)
3. [⚡ Performance Tester](#-performance-tester)
4. [🧭 Test Leader](#-test-leader)
5. [📊 Test Manager](#-test-manager)
6. [The release lifecycle — all roles on one timeline](#the-release-lifecycle--all-roles-on-one-timeline)
7. [Cheat sheet — one line per situation](#cheat-sheet--one-line-per-situation)

---

## 🔍 Manual Tester

**Mission:** find defects early and validate the product against real user needs — through static review, designed test cases, and skilled exploration.
**ISTQB home turf:** static testing (§3), test analysis & design (§4), defect management (§5.5), experience-based techniques. CTAL-TA.

### Your core loop (per user story)

```text
/qa:static-review "US-123 guest checkout"   # 1. Review the story BEFORE dev finishes — find requirement defects now
/qa:acceptance "US-123"                     # 2. Agree testable acceptance criteria (ATDD / Gherkin) with the team
/qa:test-cases "US-123"                     # 3. Derive test cases with formal techniques (EP, BVA, decision tables) + CSV export
/qa:test-data order                         # 4. Get the data you need to execute
# ... execute the cases manually against the test environment ...
/qa:exploratory "guest checkout"            # 5. Session-based exploration around the scripted cases (charters, timebox, notes)
/qa:triage "checkout accepts expired card"  # 6. Every real defect → proper ISTQB defect report (severity vs priority)
```

### When the feature is bigger than one story

| Situation | Command |
|---|---|
| The feature has complex business rules / states | `/qa:test-design <feature>` — full conditions + cases, decision tables, state transitions |
| Many parameters combine (filters, options, configs) | `/qa:combinatorial <feature>` — pairwise instead of exhaustive |
| A stateful flow (cart, order lifecycle, auth) | `/qa:mbt <flow>` — model it, derive cases by coverage |
| "Did we miss anything?" | `/qa:review-coverage <area>` — gap analysis vs risk |
| You're unsure which technique applies | `/qa:istqb-coach "when do I use decision tables?"` |

### Your cadence

- **Every story, before dev completes:** `static-review` + `acceptance` (shift-left — this is where you're cheapest to the project).
- **Every story, before execution:** `test-cases` (+ `test-data`).
- **Every story, after scripted execution:** one `exploratory` session on the riskiest angle.
- **Every defect found:** `triage` — never report a bug informally.
- **End of sprint:** hand your stable, repetitive cases to the Automation Tester: `/qa:automate path/to/your-cases.csv` scores them by ROI.

**You hand off to:** Automation Tester (stable manual cases → automation candidates), Test Leader (execution results + defects feed `status-report`).

---

## 🤖 Automation Tester

**Mission:** build and maintain a fast, deterministic, maintainable automation suite at the right pyramid levels — and keep CI green honestly (never masking real defects).
**ISTQB home turf:** CT-TAE (gTAA architecture), test implementation & execution (§1.4), maintainability. CTAL-TTA for white-box.

### One-time setup (per project)

```text
/qa:automation-strategy        # 1. The gTAA architecture: level split, tooling, CI, maintainability targets
/qa:scaffold                   # 2. Build it: Playwright+TS, K6, Pact, axe, CI pipeline — all from qa.config.yml
/qa:test-env staging           # 3. Document/provision the environment the suite runs against
```

### Your core loop (per feature)

```text
/qa:automate "guest checkout"        # 1. WHAT to automate: score priority × complexity, pick candidates by ROI
/qa:implement "guest checkout"       # 2. Build at the right level (API > component > E2E) and run
/qa:test-data order                  # 3. Factories & fixtures so every test owns its data
/qa:api-automate /orders             # 4. Surface deep-dives where needed:
/qa:scan-ui https://app/checkout     #    UI → page objects → covering cases
/qa:web-automate "checkout journey"  #    full E2E for the critical journey
```

### The maintenance loop (this is half the job)

```text
/qa:fix-jenkins                # Red build? Pull failed cases, fix by root cause, re-run locally until green
/qa:fix-ci ci.log              # Any other CI / pasted log
/qa:flaky-hunt                 # Intermittent failures → deterministic fixes, not retries
/qa:self-heal                  # UI changed → repair locators (heals HOW we locate, never WHAT we verify)
/qa:triage "<failure>"         # The failure is a REAL product defect → escalate, leave the test red
```

> **The honesty rule:** `fix-*`, `self-heal`, and `flaky-hunt` fix *test/env/flakiness* causes only. A genuine product defect goes to `triage` and the test keeps asserting correct behavior. A green build you can't trust is worse than a red one.

### Quarterly health check

```text
/qa:automation-audit           # gTAA / SOLID / anti-patterns / pyramid shape — scored report
/qa:coverage-measure           # structural + requirements + risk coverage
/qa:static-analysis tests/     # complexity & maintainability of the testware itself
/qa:review-coverage            # the highest-value missing tests
```

**You receive from:** Manual Tester (`automate` their case CSVs), Test Leader (priorities from the risk register).
**You hand off to:** everyone — your suite is the safety net `regression`, `status-report`, and `go-no-go` read from.

---

## ⚡ Performance Tester

**Mission:** prove the system meets its performance SLAs under realistic and extreme load — and catch degradation before users do.
**ISTQB home turf:** CT-PT — workload modeling, load/stress/spike/soak, threshold-based gates.

### Your core loop (per release or per high-risk area)

```text
/qa:perf-plan checkout              # 1. ALWAYS plan first: objectives, SLAs, operational profile, workload model
/qa:perf-test /api/orders load      # 2. Baseline load test at expected traffic — thresholds from qa.config.yml gates
/qa:perf-test /api/orders stress    # 3. Find the breaking point
/qa:perf-test /api/orders spike     # 4. Survive the flash sale / campaign burst
/qa:perf-test checkout soak         # 5. Hours-long: leaks, degradation, resource exhaustion
/qa:dynamic-analysis checkout       # 6. If soak shows degradation: memory/handle/connection leak analysis
```

> **Never script before planning.** `perf-test` without a `perf-plan` tests a number, not a requirement. The plan defines what "fast enough" means (SLAs), who the virtual users are (operational profile), and the pass/fail thresholds — then `perf-test` enforces them as gates.

### Beyond load

| Situation | Command |
|---|---|
| Reliability / availability / failover questions | `/qa:nonfunctional reliability` |
| Production performance monitoring, canary analysis | `/qa:shift-right "checkout journey"` |
| Perf gates in the pipeline | thresholds live in `qa.config.yml` `gates:` — `scaffold` wires them into CI |
| Results for the release decision | your threshold results feed `/qa:go-no-go` and `/qa:release-report` |

### Your cadence

- **Per release:** re-run the baseline `load` suite against the release candidate; compare to last release.
- **Before high-traffic events:** `spike` + `stress` on the affected journeys.
- **Quarterly:** one `perf-test <flow> soak` + `dynamic-analysis` on the core flow.

**You hand off to:** Test Leader / Manager (threshold pass/fail + capacity headroom → `go-no-go`, `quality-report`).

---

## 🧭 Test Leader

**Mission:** run the testing of a release — decide *where* to test deeply, track progress against the plan, take corrective action, and make the evidence-based ship/hold recommendation.
**ISTQB home turf:** test planning, monitoring & control (§5), risk-based testing (§5.2), completion. CTAL-TM operational level.

### Release kickoff

```text
/qa:risk-assessment R2.4                       # 1. Score product & project risks (likelihood × impact) — this drives EVERYTHING
/qa:estimate "R2.4 scope"                      # 2. Effort estimation (metrics + expert based)
/qa:create-plan R2.4 "guest checkout, saved cards"   # 3. The Test Plan: scope, approach, entry/exit criteria, schedule
```

Then brief the team from the risk register: high-risk areas get `test-design` + `exploratory` depth; low-risk areas get standard `test-cases`.

### Mid-release loop (weekly or per milestone)

```text
/qa:status-report R2.4         # Monitoring: progress vs plan, defect trends, coverage, entry/exit criteria status
                               # Control: the report ends with corrective ACTIONS — reassign, descope, add sessions
/qa:review-coverage            # Where is coverage thin vs the risk register?
/qa:regression "payment refactor"   # A change landed → select & prioritize the regression set
/qa:flaky-hunt                 # Pass-rate noise hides real signal — keep the suite trustworthy
```

### Release endgame

```text
/qa:coverage-measure           # 1. Final coverage vs requirements & risk
/qa:go-no-go R2.4              # 2. The formal gate: all signals consolidated → ship/hold + conditions + sign-off
/qa:release-report R2.4        # 3. Test Completion Report: exit criteria, residual risk, lessons learned
```

> **Severity ≠ priority.** When defects pile up at the gate, `triage` keeps the distinction honest: severity is product impact, priority is fix urgency. A ship decision with three open low-severity defects and a residual-risk statement is ISTQB-correct; "zero bugs" is not a thing (Principle 1).

**You receive from:** everyone (execution results, defects, perf thresholds, coverage).
**You hand off to:** Test Manager (status & completion reports roll up into `quality-report`), the org (`go-no-go` decision).

---

## 📊 Test Manager

**Mission:** own the test *organization* — policy, strategy, people, budget, process maturity, and the quality story told to executives. You work across releases, not inside one.
**ISTQB home turf:** CTAL-TM strategic level, Expert Test Management, Improving the Test Process.

### Foundations (once, then yearly review)

```text
/qa:test-policy                # 1. WHY the org tests — objectives, the top of the document hierarchy
/qa:create-strategy            # 2. HOW this product is tested — levels, types, techniques, automation, environments
/qa:automation-strategy        # 3. The automation program: gTAA, level split, ROI model
/qa:tool-select "API test tool"     # 4. Tooling decisions with criteria, comparison, pilot plan
```

### The management rhythm

| Cadence | Command | What you get |
|---|---|---|
| **Monthly / quarterly** | `/qa:quality-report Q2` | Executive KPI dashboard: escaped defects, coverage, MTTR, automation %, flaky rate — cross-release trends |
| **Quarterly** | `/qa:team-plan 6mo` | Capacity vs backlog, skills matrix, training & onboarding plan |
| **Quarterly** | `/qa:cost-of-quality` | Prevention/appraisal/failure cost split, automation payback, the budget case |
| **Per release** | `/qa:go-no-go <release>` | You're the sign-off on the Test Leader's gate |
| **Half-yearly** | `/qa:process-improvement` | TMMi-based maturity assessment + improvement roadmap |
| **Before audits** | `/qa:audit-prep ISO29119` | Traceability evidence pack, conformance gaps |

### When numbers look wrong

```text
/qa:quality-report             # escaped defects trending up? →
/qa:process-improvement        # find the process root cause (late static testing? thin risk coverage?)
/qa:risk-assessment            # re-aim the effort
/qa:cost-of-quality            # quantify the failure cost to fund the fix
```

**You receive from:** Test Leader (per-release reports), Automation Tester (`automation-audit` health scores).
**You hand off to:** the organization — policy, strategy, budget, and the quality narrative.

---

## The release lifecycle — all roles on one timeline

How the five playbooks interlock across one release. **(M)** Manual, **(A)** Automation, **(P)** Performance, **(L)** Leader, **(TM)** Manager.

```text
PLAN ─────────────────────────────────────────────────────────────────────
  (TM) test-policy / create-strategy        ← standing, reviewed yearly
  (L)  risk-assessment → estimate → create-plan <release>
  (A)  automation-strategy → scaffold       ← once per project
  (P)  perf-plan <high-risk area>

BUILD (per story, repeating all sprint) ──────────────────────────────────
  (M)  static-review → acceptance → test-cases → execute → exploratory
  (A)  automate → implement → api-automate / web-automate / test-data
  (M+A) triage <any real defect>
  (A)  fix-jenkins / fix-ci / flaky-hunt / self-heal   ← keep CI honest

STABILIZE ────────────────────────────────────────────────────────────────
  (L)  status-report (weekly) → control actions
  (L)  regression <changes> · review-coverage
  (P)  perf-test load/stress/spike vs release candidate
  (P)  security-scan · a11y-audit            ← non-functional sweep

SHIP ─────────────────────────────────────────────────────────────────────
  (L)  coverage-measure → go-no-go ← (TM) signs off
  (L)  release-report                ← residual risk, lessons learned

BETWEEN RELEASES ─────────────────────────────────────────────────────────
  (TM) quality-report · team-plan · cost-of-quality · process-improvement
  (A)  automation-audit · static-analysis    ← quarterly health check
  (P)  perf-test soak + dynamic-analysis     ← quarterly
```

---

## Cheat sheet — one line per situation

| You are… | …and you need to | Run |
|---|---|---|
| Anyone | start in a new repo | `/qa:qa-init` → `/qa:scaffold` |
| Anyone | learn/check an ISTQB concept | `/qa:istqb-coach <topic>` |
| Manual | review a story before dev finishes | `/qa:static-review <story>` |
| Manual | turn a requirement into cases | `/qa:test-cases <req>` |
| Manual | explore a risky area | `/qa:exploratory <area>` |
| Manual | report a bug properly | `/qa:triage "<bug>"` |
| Automation | decide what's worth automating | `/qa:automate <cases\|feature>` |
| Automation | build + run tests for a feature | `/qa:implement <feature>` |
| Automation | fix a red Jenkins build | `/qa:fix-jenkins` |
| Automation | kill flaky tests | `/qa:flaky-hunt` |
| Automation | repair tests after a UI change | `/qa:self-heal` |
| Automation | health-check the whole suite | `/qa:automation-audit` |
| Performance | define SLAs & workload first | `/qa:perf-plan <scope>` |
| Performance | run load/stress/spike/soak | `/qa:perf-test <target> <type>` |
| Leader | decide where to test deeply | `/qa:risk-assessment <release>` |
| Leader | write the release test plan | `/qa:create-plan <release> <features>` |
| Leader | report progress + take action | `/qa:status-report <release>` |
| Leader | make the ship/hold call | `/qa:go-no-go <release>` → `/qa:release-report <release>` |
| Manager | report quality to executives | `/qa:quality-report <period>` |
| Manager | plan team capacity & skills | `/qa:team-plan <horizon>` |
| Manager | justify the QA budget | `/qa:cost-of-quality` |
| Manager | improve the process | `/qa:process-improvement` |
| Manager | prepare for an audit | `/qa:audit-prep <standard>` |

---

*Companion docs: [COMMAND-GUIDE.md](./COMMAND-GUIDE.md) (every command's how-to) · [COMMAND-EXAMPLES.md](./COMMAND-EXAMPLES.md) (worked examples) · [ISTQB-COMPLIANCE.md](./ISTQB-COMPLIANCE.md) (standards traceability).*
