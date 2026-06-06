---
description: Define the program-level Test Automation Strategy and architecture (gTAA) — objectives, scope, approaches, tool fit, level distribution, CI, maintainability, metrics, ROI. Use to set or review the overall automation approach (above any single feature).
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test Automation Strategy & Architecture

**ISTQB process:** Test Automation Engineering — gTAA & automation strategy (CT-TAE; ISTQB Test Automation Strategy). Sits above per-feature `/qa:automate`; complements the overall `/qa:create-strategy`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Current automation footprint
```!
echo "--- framework ---"; ls -1 playwright.config.* 2>/dev/null; ls -1 tests 2>/dev/null
echo "--- CI ---"; ls -1 Jenkinsfile .github/workflows/*.yml 2>/dev/null
```

## Your task

Produce the **Test Automation Strategy** for this product (long-lived, automation-specific):

1. **Objectives & business case** — why automate; expected ROI; what automation will and won't do (it complements, not replaces, manual/exploratory testing).
2. **Scope** — which test levels and surfaces are in scope (API, Web/UI, mobile, performance, contract, a11y, security) per `tooling`.
3. **gTAA — generic test automation architecture** — define the three layers: **test generation/definition** (how tests are specified), **test adaptation** (page objects, API clients, drivers, fixtures, service virtualization), and **test execution** (runners, CI, reporting). Keep the SUT decoupled from tests via the adaptation layer.
4. **Automation approaches** — choose and justify: data-driven, keyword-driven, behavior-driven (BDD/ATDD), and/or model-based — matched to the team and stack.
5. **Level distribution (pyramid)** — target split across unit/API/contract/UI-E2E; default to the lowest effective level for maintainability.
6. **Tooling** — confirm fit with `tooling`/`stack`; note gaps (route to `/qa:tool-select`).
7. **CI/CD integration** — where automation runs (PR gate vs nightly vs pre-release) on `ci.platform`; sharding; reporting.
8. **Maintainability strategy** — stable selectors, reuse, no hard waits, flakiness policy (`/qa:flaky-hunt`), versioning of testware.
9. **Metrics** — automation coverage, pass rate, execution time saved, maintenance effort, defects found by automation.
10. **Risks & assumptions** — over-reliance, maintenance cost, unstable SUT/data, tool limits; mitigations.

Write to `<paths.docs_dir>/AUTOMATION-STRATEGY.md`. This guides every surface command (`api-automate`, `web-automate`, `mobile-automate`, `perf-plan`) and the per-feature `automate` workflow.
