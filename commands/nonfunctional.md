---
description: Design and (where automatable) run non-functional tests beyond performance/security/a11y — reliability, compatibility, portability, maintainability — against measurable ISO/IEC 25010 sub-characteristics. Produces an ISO/IEC/IEEE 29119-3 Test Design + Test Case Specification.
argument-hint: "<characteristic, e.g. reliability, compatibility, portability, maintainability>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Non-functional testing: $ARGUMENTS

**ISTQB process:** Test analysis & design for **non-functional test types** (CTFL v4.0 §2.2.2 — non-functional testing), elaborated with **CTAL-TTA** non-functional test design (a Specialist syllabus — not CTFL Foundation). Targets **ISO/IEC 25010** product-quality characteristics. Verify any specific section number against the current syllabus before asserting it.

## Project config (read first — do not proceed without it)
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init before designing non-functional tests"
```

## Step 0 — config & argument guards (run before anything else)

1. **Config guard.** If the block above printed `MISSING`, stop and recommend `/qa:qa-init`; do not invent paths, tools, characteristics, or thresholds.
2. **Routing guard.** Resolve the target characteristic from `$ARGUMENTS`, then hand off if a dedicated command owns it — this command covers only the remainder:
   - **performance / performance efficiency** → `/qa:perf-test` (and `/qa:perf-plan` for the workload model). Stop here.
   - **security** → `/qa:security-scan`. Stop here.
   - **usability / accessibility** → `/qa:a11y-audit` (accessibility) or `/qa:usability-test` (usability). Stop here.
   - Otherwise continue: **reliability**, **compatibility**, **portability**, **maintainability**, or **functional suitability** (non-functional aspects).
3. **Argument resolution.** If `$ARGUMENTS` is empty: do not guess. Ask which 25010 characteristic to cover. If the user defers, default to the characteristic most associated with the first item in `risk_areas.critical` from config (the highest-risk area); state that default explicitly and proceed.

## Step 1 — fix the characteristic and its measurable sub-characteristics (ISO/IEC 25010)

Select the row matching `$ARGUMENTS` and enumerate its sub-characteristics with a measurable criterion (a metric + threshold) for each. Source each threshold from `gates` / SLAs in config; if a threshold is absent, state which one is unverified and propose a value to add to `gates` rather than asserting a number.

| 25010 characteristic | Sub-characteristics (measurable criteria to define) | Typical test approach |
|---|---|---|
| **Reliability** | maturity (MTBF / failure rate), availability (uptime %), fault tolerance (degrades, not crashes, under a fault), recoverability (RTO/RPO; recovers after failure) | soak + recovery scenarios; inject dependency timeouts/5xx via mocks; chaos-style fault injection |
| **Compatibility** | co-existence (shares an environment without harm), interoperability (correct exchange with external services / API versions) | run the browser/device/OS matrix from config; contract tests across API versions (`/qa:contract-sync`) |
| **Portability** | adaptability (runs across target environments), installability (install/deploy succeeds), replaceability | install/deploy across environments and configurations; containerization/parameterization checks |
| **Maintainability** | modularity, reusability, analyzability, modifiability, testability of code/testware | static analysis & review of the codebase/testware (`/qa:static-review`, `/qa:static-analysis`); coupling/complexity metrics |

State which sub-characteristics are **in scope** for this run and which are out of scope, with the reason.

## Step 2 — derive test conditions and cases

1. Derive **test conditions** (what to test) from the in-scope sub-characteristics and the test basis, then elaborate **test cases** (preconditions, inputs, expected results, postconditions) with the measurable acceptance criterion attached to each.
2. Trace every case back to its sub-characteristic and acceptance criterion so coverage is reportable per characteristic (no orphan cases).
3. Where a criterion lacks a config threshold, propose the `gates` field to add; do not invent a passing value.

## Step 3 — implement what is automatable

Implement the automatable cases under `<paths.tests_dir>` using the configured tooling only (`<tooling.*>` / `<stack.*>` — never a hardcoded tool name):

- **Compatibility:** drive the browser/device/OS matrix from config (e.g. `ci.browsers`) via the configured e2e tool; do not hardcode the runner.
- **Reliability:** dependency-failure simulations (mocked timeouts/5xx), soak/recovery scenarios.
- **Portability:** scripted install/deploy across the configured environments.
- **Maintainability:** wire the configured static-analysis/metrics tool; this characteristic is largely assessed statically rather than executed.

## Step 4 — run where feasible and report against criteria

Run automatable cases against a **non-production** environment when one is available and the user opts in. Report each result as a number versus its acceptance criterion with explicit pass/fail per sub-characteristic — not prose. State residual risk (what was not exercised and why). Feed gated results into `/qa:status-report` (in-cycle) or `/qa:release-report` (completion); flag any newly discovered quality risk to `/qa:risk-assessment`.

## Work product

This command produces an **ISO/IEC/IEEE 29119-3 Test Design Specification + Test Case Specification** for the chosen ISO/IEC 25010 characteristic — written to `<paths.docs_dir>/NONFUNCTIONAL-<characteristic>.md` — plus any executable **Test Procedures / scripts** under `<paths.tests_dir>`, and **Test Execution Log / Results** when run. It does not produce a performance plan (`/qa:perf-plan`) or security/accessibility findings (`/qa:security-scan`, `/qa:a11y-audit`).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`, `paths.tests_dir`, the browser/device matrix, `tooling.*`, `gates`/SLAs, `risk_areas.critical` for the empty-args default) is honored; no path, tool, browser matrix, or threshold is hardcoded.
- [ ] **Characteristic enumerated** — the targeted ISO/IEC 25010 characteristic and its in-scope sub-characteristics are listed, each with a measurable criterion (metric + threshold sourced from `gates`, or flagged as unverified).
- [ ] **Traceability intact** — the chain test basis → condition → case → coverage item → procedure → result is preserved and bidirectional; every case traces to a sub-characteristic and acceptance criterion; no orphans.
- [ ] **Measurable** — output states results as numbers vs. criteria with pass/fail per sub-characteristic, not prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1): sub-characteristics left out of scope, environment/data-fidelity limits, and that point-in-time results are not exhaustive.
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product (Test Design + Test Case Specification, plus Test Procedures/Execution Log when run) and written to the correct `<paths.docs_dir>` / `<paths.tests_dir>` locations.
