# QA Toolkit

A reusable, **ISTQB-aligned QA toolkit** for Web + REST API projects, packaged as a Claude Code plugin. Install it once, then drive your whole testing workflow with `/qa:*` slash commands in **any** repository. The only thing that changes between projects is a single config file: **`qa.config.yml`**.

Core stack the toolkit assumes (all configurable): **Playwright + TypeScript** for functional/E2E/API, **K6** for performance, **Pact** for contract testing, **axe** for accessibility, **OWASP ZAP / SCA / secret scanning** for security, and **Jenkins** (or GitHub Actions / GitLab / Azure) for CI.

## Standards compliance

The toolkit follows the **ISTQB®** framework strictly — **Certified Tester Foundation Level (CTFL) v4.0**, plus relevant Advanced/Agile/Specialist syllabi (Test Manager, Agile Tester, Test Automation Engineer, Performance, Security, Accessibility) — and the **ISO/IEC/IEEE 29119-3** test-documentation standard. The commands implement the seven ISTQB **test-process activities** (planning, monitoring & control, analysis, design, implementation, execution, completion), use the seven **testing principles** as standing rules, apply ISTQB **test design techniques** (EP, BVA, decision tables, state transition, ATDD), and use **ISTQB Glossary** terminology throughout. Full traceability: [`docs/ISTQB-COMPLIANCE.md`](docs/ISTQB-COMPLIANCE.md) maps every command to its syllabus reference; [`docs/GLOSSARY.md`](docs/GLOSSARY.md) defines the terms.

> ISTQB syllabi and the Glossary are copyrighted by ISTQB. This toolkit implements their concepts and terminology; it does not reproduce the documents.

---

## The idea in one picture

```
  qa-toolkit (this repo, on GitHub)        Your project A          Your project B
  ┌──────────────────────────────┐                ┌───────────────┐       ┌───────────────┐
  │ commands/  (59 /qa:* commands)│   install once │ qa.config.yml │       │ qa.config.yml │
  │ skills/    (auto context)     │ ─────────────► │  (the only    │  ...  │  (different   │
  │ templates/ (strategy & plan)  │   via /plugin  │   per-project │       │   values)     │
  └──────────────────────────────┘                │   file)       │       │               │
        identical everywhere                       └───────────────┘       └───────────────┘
```

Commands + templates are identical across every project. `qa.config.yml` supplies the project-specific values (stack, tooling toggles, CI platform, quality-gate thresholds, risk areas, team). Update one repo here → every project gets the improvement.

---

## Install

```bash
# 1. Add this repo as a plugin marketplace (once per machine)
/plugin marketplace add qa-io-vn/qa.io.vn

# 2. Install the plugin
/plugin install qa@qa-toolkit
```

> Replace `qa-io-vn/qa.io.vn` with your actual GitHub `owner/repo`. You can also point at a local path during development: `/plugin marketplace add /path/to/qa-toolkit`.

To update later: `/plugin marketplace update qa-toolkit`.

---

## Use it on a project (first time)

```bash
cd your-project

# Generate the single per-project config interactively
/qa:qa-init

# Then build out your QA assets from that config
/qa:create-strategy            # → docs/qa/TEST-STRATEGY.md
/qa:scaffold                   # → Playwright+TS / K6 / Pact framework + Jenkinsfile
/qa:create-plan R2.4 "guest checkout, saved cards"   # → docs/qa/TEST-PLAN-R2.4.md
/qa:implement "guest checkout" # → E2E + API + contract tests for the feature
```

Everything reads `qa.config.yml`, so you never re-specify your stack or thresholds.

---

## Commands (59)

A command for every ISTQB activity, so a tester can run the **entire** workflow through the agent. Grouped by the ISTQB test-process activity each implements. All commands read `qa.config.yml`, respect its `tooling` toggles, and use ISTQB Glossary terminology.

> 🏠 **Start here — the visual guide:** [`docs/index.html`](docs/index.html) — a blog-style home page with the role playbooks, lifecycle map, and full catalog (enable GitHub Pages from `/docs` to host it).
> 🧑‍💼 **Role playbooks:** [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) — how to work as a **Manual Tester, Automation Tester, Performance Tester, Test Leader, or Test Manager**: each role's mission, command loops, and cadence, plus the release-lifecycle map that ties them together.
> 📖 **Full how-to:** [`docs/COMMAND-GUIDE.md`](docs/COMMAND-GUIDE.md) — every command's purpose, prerequisites, output, and next step, plus copy-paste **workflow recipes** and a "which command do I use?" index.
> 🧪 **Worked examples:** [`docs/COMMAND-EXAMPLES.md`](docs/COMMAND-EXAMPLES.md) — a sample invocation for **every** command with a "Correct when" check, all anchored to one consistent sample project.
> 📑 **Command reference + proof:** [`docs/command-reference.html`](docs/command-reference.html) — all 59 commands with a **worked sample output** for each (the actual ISTQB artifact it generates for the ShopEase sample project), a live filter box, and the verify-it-worked checklist. The "show me it works" page.
> Full syllabus→command mapping: [`docs/ISTQB-COMPLIANCE.md`](docs/ISTQB-COMPLIANCE.md).

**Test planning & management** (CTFL §5 · CTAL-TM · Expert)

| Command | What it does |
|---|---|
| `/qa:qa-init` | Interview you and generate the per-project `qa.config.yml`. Start here. |
| `/qa:test-policy` | Author the **Organizational Test Policy** (top of the doc hierarchy). |
| `/qa:create-strategy` | Generate the **Organizational Test Strategy** (ISO 29119-3). |
| `/qa:create-plan <release> [features]` | Generate a release/sprint **Test Plan** (ISO 29119-3). |
| `/qa:risk-assessment [scope]` | Risk-based testing — score product/project risks (likelihood×impact). |
| `/qa:estimate <scope>` | Test effort **estimation** (metrics- & expert-based). |
| `/qa:tool-select <need>` | Evaluate & select a test **tool** (criteria, comparison, pilot). |
| `/qa:process-improvement` | Test process maturity assessment & improvement (TMMi/IDEAL). |
| `/qa:quality-report [period]` | Cross-release **quality KPI dashboard / executive report** (escaped defects, coverage, MTTR, automation %). |
| `/qa:team-plan [horizon]` | **Team capacity & skills** — staffing vs backlog, skills matrix, training/onboarding. |
| `/qa:go-no-go <release>` | Formal **release readiness** gate — consolidated ship/hold decision with sign-off. |
| `/qa:cost-of-quality [scope]` | **Cost of Quality & QA ROI** — prevention/appraisal/failure costs, automation payback, budget case. |
| `/qa:audit-prep [standard]` | **Audit & compliance readiness** — traceability + evidence pack, ISO 29119/ISTQB conformance. |

**Static testing · analysis · design** (CTFL §3–4 · CTAL-TA/TTA)

| Command | What it does |
|---|---|
| `/qa:static-review <story\|spec>` | Static testing — review the test basis + static analysis (shift-left). |
| `/qa:test-cases <requirement>` | **Generate test cases** from a requirement/story/endpoint/file — ISTQB techniques, risk-based detail, Test Case Spec (+ CSV on request). |
| `/qa:test-design <feature>` | Broader test analysis & design context for a feature (conditions + cases). |
| `/qa:combinatorial <feature>` | **Pairwise / classification-tree** design for multi-parameter features (Advanced/CTAL-TA). |
| `/qa:acceptance <story>` | ATDD/BDD acceptance criteria & Gherkin scenarios. |
| `/qa:mbt <flow>` | **Model-Based Testing** — model a stateful flow, derive cases by coverage. |
| `/qa:exploratory <area>` | Session-based **exploratory** testing charters (experience-based). |
| `/qa:static-analysis [path]` | **Static analysis** of code — complexity, control/data flow, maintainability metrics. |
| `/qa:automation-audit [path]` | **Audit an existing automation project** — gTAA architecture, **SOLID** & clean-code, test-case/design quality, anti-patterns, pyramid; scored health report + prioritized fixes. |
| `/qa:review-coverage [area]` | Audit coverage & traceability; recommend missing tests. |

**Test levels & change-related** (CTFL §2.2, §2.3)

| Command | What it does |
|---|---|
| `/qa:unit-test <module>` | **Component (unit)** testing — isolation, test doubles, statement/branch coverage. |
| `/qa:integration-test <interface>` | **Integration** testing — component & system integration, incremental strategy, stubs/drivers. |
| `/qa:maintenance-test <change>` | **Maintenance** testing — modification / migration / retirement + impact analysis. |
| `/qa:dynamic-analysis <flow>` | **Dynamic analysis** — runtime memory/resource leaks, degradation over time. |
| `/qa:shift-right [journey]` | **Testing in production** — synthetic monitoring, observability, canary/A-B, feature flags. |

**Test implementation** (CTFL §1.4 · CT-TAE)

| Command | What it does |
|---|---|
| `/qa:scaffold` | Set up the automation architecture (Playwright, K6, Pact, CI pipeline). |
| `/qa:automate <cases\|requirement>` | **Full automation pipeline** — score priority & complexity, select candidates by ROI, design automated cases, plan, and implement the top ones (CT-TAE). |
| `/qa:implement <feature>` | Turn test cases into procedures/scripts at the right level and run them (generic engine). |
| `/qa:add-test <description>` | Add a single focused test case. |
| `/qa:test-data <entity>` | Generate typed data factories, fixtures, seeding helpers. |
| `/qa:test-env [name]` | Provision the test environment & manage testware configuration. |

**Test automation by surface** (CT-TAE · CT-PT · CT-MAT) — the *how* for each surface; `automate` decides *what*, these build it.

| Command | What it does |
|---|---|
| `/qa:automation-strategy` | Program-level **Test Automation Strategy & gTAA architecture** (approaches, level split, CI, maintainability, metrics). |
| `/qa:api-automate <resource>` | **API** test automation from OpenAPI — schema, CRUD, auth/role matrix, negative/boundary, data-driven. |
| `/qa:scan-ui <url/flow>` | **Deep-dive a web UI** — extract all locators & actions into Page Objects, then generate covering test cases. |
| `/qa:web-automate <journey>` | **Web UI / E2E** automation — POM, critical journeys, cross-browser, auth state, a11y/visual hooks. |
| `/qa:mobile-automate <flow>` | **Mobile** automation — native/cross-platform (Appium/device farm) or responsive mobile-web. |
| `/qa:perf-plan [scope]` | **Performance test planning** — objectives, SLAs, operational profiles, workload model (feeds `perf-test`). |

**Test execution — functional & non-functional** (CTFL §2.2.2 · CT-PT/SEC/UT/AI/MAT)

| Command | What it does |
|---|---|
| `/qa:perf-test <endpoint>` | K6 performance test (load/stress/spike/soak) with threshold gates (scripts the `perf-plan`). |
| `/qa:a11y-audit [page]` | axe accessibility checks vs the WCAG target. |
| `/qa:usability-test <flow>` | **Usability** evaluation (heuristics, task scenarios). |
| `/qa:nonfunctional <characteristic>` | Reliability, compatibility, portability, maintainability (ISO 25010). |
| `/qa:security-scan` | Security baseline (SAST, SCA, DAST, secret scan). |
| `/qa:contract-sync` | Pact contracts + `can-i-deploy`. |
| `/qa:mobile-test [page]` | Responsive/mobile-web testing (viewports, touch, network). |
| `/qa:ai-test <feature>` | Test **AI/ML** components (metrics, bias, robustness, drift). |
| `/qa:regression [change]` | Regression test **selection & prioritization** (impact analysis). |
| `/qa:fix-ci [log]` | Diagnose & fix a failing pipeline / test run (any CI). |
| `/qa:fix-jenkins [build URL\|job path]` | Pull the **latest Jenkins build's failed cases**, fix each, re-run them locally until all pass. |
| `/qa:flaky-hunt [path\|N runs]` | Find & fix flaky tests — deterministic fixes, no blind retries (testware maintenance). |
| `/qa:self-heal [area]` | **Maintain & auto-heal** the suite — repair broken locators after UI changes, prune/refactor, re-run to confirm. |

**Monitoring, control & completion** (CTFL §5.3–5.5 · ISO 29119-3)

| Command | What it does |
|---|---|
| `/qa:status-report <release>` | **Test Status (Progress) Report** — metrics + control actions mid-release. |
| `/qa:coverage-measure [scope]` | Measure structural / requirements / risk **coverage**. |
| `/qa:triage <failure>` | Defect management — severity vs priority, ISTQB defect report. |
| `/qa:release-report <release>` | **Test Completion Report** — exit criteria, residual risk, ship/hold. |

**AI-assisted & reference**

| Command | What it does |
|---|---|
| `/qa:genai-assist <task>` | Use GenAI to accelerate testing **with** ISTQB safeguards (human oversight, privacy). |
| `/qa:istqb-coach <topic>` | On-demand ISTQB **reference & coach** — explain/apply any concept, route to the right command. |

---

## The one file that differs per project: `qa.config.yml`

Copy [`templates/qa.config.example.yml`](templates/qa.config.example.yml) to your project root as `qa.config.yml`, or let `/qa:qa-init` generate it. It captures: project + stack, process/cadence, tooling toggles, CI platform, **quality gates/SLAs**, risk areas, environments, test-data rules, and team. Every command reads it — it is the only thing you maintain per project.

---

## Repo layout

```
qa-toolkit/
├── .claude-plugin/
│   ├── plugin.json            # plugin manifest (name: qa)
│   └── marketplace.json       # marketplace manifest (clone & install target)
├── commands/                  # the 59 /qa:* slash commands (one .md each)
├── skills/
│   └── qa-context/SKILL.md    # auto-loads qa.config.yml + ISTQB standing rules
├── templates/
│   ├── qa.config.example.yml  # the per-project config template
│   ├── strategy-template.md   # ISTQB/ISO-29119 Org Test Strategy structure
│   └── plan-template.md       # ISTQB/ISO-29119 Test Plan structure
├── docs/
│   ├── index.html             # blog-style visual guide (GitHub Pages-ready)
│   ├── WORKFLOWS.md           # role playbooks: manual/automation/perf tester, lead, manager
│   ├── COMMAND-GUIDE.md       # full how-to for all 59 commands + workflow recipes
│   ├── COMMAND-EXAMPLES.md    # a worked sample invocation for every command
│   ├── ISTQB-COMPLIANCE.md    # command → ISTQB syllabus traceability map
│   └── GLOSSARY.md            # ISTQB Glossary-aligned terms
└── README.md
```

---

## Customizing the toolkit

Because every project shares these commands, improving the toolkit is centralized:

- **Change how a deliverable looks** → edit the files in `templates/`.
- **Change a workflow** → edit the relevant file in `commands/`.
- **Add a command** → drop a new `commands/<name>.md`; it becomes `/qa:<name>`.
- **Bump the version** in both manifests and run `/plugin marketplace update`.

Keep project-specific values out of the toolkit — they belong in each project's `qa.config.yml`.

---

## License

MIT.
