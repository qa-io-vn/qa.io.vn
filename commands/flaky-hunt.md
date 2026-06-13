---
description: Find flaky/non-deterministic tests, quarantine them against an SLA, fix the root cause, and write a Flaky-Hunt report. Use when tests intermittently fail or the user mentions flakiness.
argument-hint: "[test path or N runs]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Hunt flaky tests

**ISTQB process:** Test automation maintenance & reliability (CT-TAE — a Specialist topic; verify against the current syllabus) — eliminate false alarms so failures reliably signal defects. This targets the **reliability** quality characteristic (ISO/IEC 25010) of the test suite, and counters the pesticide paradox (CTFL v4.0 Principle 5 — verify the principle number against the current syllabus).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Your task

Build or extend the flaky-test hunt for the target in `$ARGUMENTS`.

**Config-read guard.** If `qa.config.yml` is `none` above, stop and tell the user to run `/qa:qa-init` first — do not hardcode paths, tools, or thresholds. Read the test runner from `<tooling.e2e>` (and `<tooling.unit>` for component-level flakiness) and the language from `<tooling.language>`; read suite locations from `<paths.tests_dir>`, result/report locations from `<paths.reports_dir>`, and the flaky/quarantine SLA from `gates` / `process.*` (fall back to the defaults in step 4 only if those fields are absent, and say so). Never hardcode `tests/`, `playwright-report`, `test-results`, or `npx playwright`.

**If `$ARGUMENTS` is empty:** ask the user for a test path or a run count `N`. If they cannot supply one, default the scope to the suites covering `risk_areas.critical` from `qa.config.yml` (highest-risk first) and state that you are doing so.

Treat each suspect test as the unit of work and preserve traceability — keep the chain **test basis → condition → case → procedure → result (→ defect)** intact; quarantining or fixing a test must not orphan its conditions.

### 1. Identify flakiness sources (static scan)
Scan the in-scope suites under `<paths.tests_dir>` with Grep for these anti-patterns and record each hit with file:line:
- hard sleeps / fixed waits (`waitForTimeout`, `sleep`, fixed `setTimeout` in tests);
- CSS/XPath selectors coupled to styling/markup (vs role/label/test-id);
- tests depending on execution order or shared mutable state;
- unmocked time, randomness, or network (real clock / live endpoints);
- race conditions (assert-before-ready);
- tests that only pass because retries are enabled.

### 2. Confirm non-determinism (dynamic check, decision rule)
Run each suspect test repeatedly with the configured runner to measure a **flake rate** = failed runs ÷ total runs over `N` runs (default `N = 10` if the user gave none).
- Invoke the runner from `<tooling.e2e>` / `<tooling.unit>` with its repeat mechanism (e.g. for a Playwright-class runner, `--repeat-each=N`; for a Jest/Vitest-class runner, the equivalent repeat flag) — derive the flag from the configured tool, do not assume `npx playwright`.
- Classify each test: **deterministic** (0% over `N`) → out of scope; **flaky** (0% < rate < 100%) → step 3; **consistently failing** (100%) → not flaky, treat as a normal failure and route to `/qa:fix-ci` or `/qa:triage`.

### 3. Resolve each confirmed flaky test (root cause, not symptom)
For each flaky test, in order:
1. **Triage the cause** — decide whether the intermittency is in the **test/environment** or the **product**:
   - **Product defect** (a genuine app race condition, timing bug, or non-determinism in the SUT) → do **not** stabilize the test around it. Leave the test asserting correct behavior and escalate via `/qa:triage` (Incident Report). Stop here for this test.
   - **Test/environment** → continue to fix it below.
2. **Quarantine** — tag it (`@flaky` / `test.fixme` per the configured runner) so it is excluded from the blocking gate but still runs visibly. Record it in the report (step 5). Set a fix SLA per step 4.
3. **Fix the cause** — replace hard waits with web-first / auto-waiting assertions; swap brittle CSS/XPath for role/label/`data-testid` locators; isolate test data and make each test own its state (use `/qa:test-data`); mock time/randomness/network; remove order dependence. If the break is a locator that legitimately moved (not timing), hand off to `/qa:self-heal`.
4. **Verify** — re-run the fixed test `N` times; it leaves quarantine only at 0% flake over `N`. Never "fix" flakiness by adding retries or increasing timeouts alone.

### 4. Apply the quarantine SLA (decision rule)
Use the SLA from `gates` / `process.*`; if absent, use these defaults and state that they are defaults:
- **Quarantine** any test with flake rate **> 10%** over `N` (or any product-defect-linked intermittency).
- **Escalate** to `/qa:triage` / the suite owner if a critical-path test (`risk_areas.critical`) stays quarantined **> 2 sprints**, or if quarantine size is **growing release over release** (a maintenance-debt signal).
- Each quarantined test gets a **1-sprint default fix SLA** (or the configured value), an owner from `team`, and a tracking note.

### 5. Write the Flaky-Hunt report
Write a **Flaky-Hunt report** to `<paths.reports_dir>/FLAKY-HUNT-<date>.md` with `<date>` as today's date (YYYY-MM-DD). Structure:
- **Scope** — suites/paths scanned (or the `risk_areas.critical` default), `N` runs used.
- **Flaky tests** — a table: test id/path · root-cause category (from step 1) · measured flake rate (x/N) · disposition (quarantined / fixed / escalated as product defect) · fix SLA & owner.
- **Quarantine ledger** — current quarantine size, change vs last report (flag if growing), and any test breaching the > 2-sprint critical SLA.
- **Fixes applied** — old → new for each stabilized test (wait → web-first, selector → role/test-id, etc.).
- **Residual risk** — flaky tests not yet resolved, suites not scanned, and what that leaves unverified.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — runner from `<tooling.e2e>` / `<tooling.unit>`, language from `<tooling.language>`, suites under `<paths.tests_dir>`, report under `<paths.reports_dir>`, SLA/thresholds from `gates` / `process.*` (or stated defaults); nothing hardcoded (`tests/`, `playwright-report`, `test-results`, `npx playwright`, repeat flag).
- [ ] **Traceability intact** — the chain test basis → condition → case → procedure → result (→ defect) survives quarantine/fix; no condition is orphaned; product-defect cases route to `/qa:triage` with the test still asserting correct behavior.
- [ ] **Measurable** — output states per-test flake rates (x/N), quarantine count and its delta, and counts of tests fixed/quarantined/escalated, not prose claims.
- [ ] **Residual risk stated** — name the flaky tests left unresolved and suites not scanned, and why (CTFL v4.0 Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as a **Flaky-Hunt report** (a test-maintenance work product feeding the **Test Execution Log / Test Results** under ISO/IEC/IEEE 29119-3; no dedicated template) and written to `<paths.reports_dir>/FLAKY-HUNT-<date>.md`; quarantine changes are reflected in the affected **Test Procedures / scripts** under `<paths.tests_dir>`.

End with a one-line summary: tests scanned, flaky found, fixed vs quarantined vs escalated to `/qa:triage`, current quarantine size and trend, and any SLA breach.
