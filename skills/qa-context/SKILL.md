---
name: qa-context
description: Project QA conventions, ISTQB standards, and configuration. Load automatically whenever the user works on testing, test strategy, test plans, test design, Playwright/K6/Pact tests, CI test failures, defects, or quality gates in a project that has a qa.config.yml file.
user-invocable: false
---

## Project QA configuration

This project may define a `qa.config.yml` at its root — the single source of truth for QA decisions (stack, tooling toggles, CI platform, quality gates/SLAs, risk areas, environments, team).

Current config (empty if not yet created):

```!
cat qa.config.yml 2>/dev/null || echo "NO qa.config.yml FOUND — suggest running /qa:qa-init to create it."
```

## This toolkit follows ISTQB strictly

All QA work here conforms to the **ISTQB CTFL v4.0** framework, relevant Advanced/Agile/Specialist syllabi, the **ISTQB Glossary**, and **ISO/IEC/IEEE 29119-3** documentation. See `docs/ISTQB-COMPLIANCE.md` and `docs/GLOSSARY.md` in the toolkit.

### Use ISTQB terminology (glossary-aligned) — always
test object · test basis · test condition · test case · coverage item · test procedure · test suite · test script · testware · test level (component / integration / system / acceptance) · test type (functional / non-functional / white-box / change-related) · confirmation testing vs regression testing · entry criteria / exit criteria · product risk vs project risk · severity vs priority · test strategy vs test plan · test status report vs test completion report. Do not use casual synonyms when a glossary term exists.

### The seven ISTQB testing principles (standing rules)
1. Testing shows the presence of defects, not their absence — never claim "defect-free"; always state residual risk.
2. Exhaustive testing is impossible — use test techniques + risk to focus, not brute force.
3. Early testing saves time and money — static-test the test basis and write tests alongside development (shift-left).
4. Defects cluster together — concentrate depth on high-risk / defect-dense `risk_areas`.
5. Beware the pesticide paradox — refresh/retire stale tests; add new conditions as the product changes.
6. Testing is context-dependent — let `qa.config.yml` (risk, domain, criticality) drive depth and approach.
7. Absence-of-errors is a fallacy — validate against user needs (acceptance, usability/a11y), not just defect counts.

### The ISTQB test process (drives every command)
Test planning → monitoring & control → analysis (identify test conditions from the test basis) → design (derive test cases + coverage items using techniques) → implementation (procedures, scripts, data, environment) → execution (run, log results) → completion (report, lessons). Each command states which activity it performs and produces the matching testware. In Agile, these run continuously each iteration, not as phases.

### Test design must use ISTQB techniques
Per CTFL v4.0 Chapter 4: black-box (Equivalence Partitioning, Boundary Value Analysis in 2-value/3-value form, Decision Table, State Transition), white-box (statement & branch testing/coverage), experience-based (error guessing, exploratory, checklist), and collaboration-based (ATDD). Use-case and pairwise are Advanced (CTAL-TA), not Foundation — label explicitly if used. Record the technique and coverage items on each derived test case.

### Maintain ISTQB traceability
Keep the bidirectional chain: test basis → test condition → test case + coverage item → test procedure/script → execution result → defect. `review-coverage` audits it; plans and the completion report measure coverage against it.

## Standing engineering conventions
- Treat `qa.config.yml` as authoritative; never hardcode tools, URLs, thresholds, or browsers it already defines. Respect the `tooling` flags — skip disabled tools.
- Apply the test pyramid: push coverage to the lowest effective test level; reserve system-level E2E for `risk_areas.critical` journeys.
- Stable selectors (`getByRole`/`getByLabel`/`data-testid`), web-first assertions, no hard waits. Each test owns its data (factories), parallel-safe.
- Synthetic/anonymized test data only — never real PII. Secrets from `test_data.secrets_store`, never the repo.
- Generated documentation → `paths.docs_dir`; testware → `paths.tests_dir`; reports → `paths.reports_dir`.
- Quality gates in `gates` are the **exit criteria** — use those exact thresholds for "done"/"shippable", and always express results with residual risk.

If `qa.config.yml` is missing, prompt the user to run `/qa:qa-init` before generating project-specific artifacts.
