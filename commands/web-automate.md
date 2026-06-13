---
description: Build or extend automated Web UI / E2E tests at the system level — user journeys, Page Object Model, cross-browser, per-role auth state, with config-gated accessibility and visual hooks. Use for web UI test automation.
argument-hint: "<feature / user journey / page>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Web UI / E2E automation: $ARGUMENTS

**ISTQB process:** Test automation (CT-TAE) producing **system-level / end-to-end** tests (the System test level, CTFL v4.0 §2.2 — verify the section number against the current syllabus). Reserve UI automation for genuine user journeys (the test pyramid); push checks to the API/component level wherever they can be proven more cheaply.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Existing UI framework
```!
echo "--- e2e config ---"; ls -1 playwright.config.* cypress.config.* wdio.conf.* 2>/dev/null
echo "--- pages / e2e (root from paths.tests_dir) ---"; ls -1R tests 2>/dev/null | head -40
```

## Your task

Build or extend automated Web UI / E2E tests for the target in `$ARGUMENTS` using `<tooling.e2e>` + `<tooling.language>`.

**Config-read guard.** If `qa.config.yml` is MISSING above, stop and tell the user to run `/qa:qa-init` first — do not hardcode paths or tools. If no E2E config was found above, suggest `/qa:scaffold` (or `/qa:tool-select` to choose the framework) before continuing. All paths come from `<paths.tests_dir>`, all tooling from `<tooling.*>`, the browser matrix from `<ci.browsers>`; never hardcode `tests/`, `playwright-report`, or `npx playwright`.

**If `$ARGUMENTS` is empty:** ask the user which feature / user journey / page to automate. If they cannot supply one, default the target to the first item in `risk_areas.critical` from `qa.config.yml` and state that you are doing so.

Treat the user journey in `$ARGUMENTS` as the **test basis**. Work the ISTQB chain explicitly — **basis → condition (journey/step) → case → coverage item → procedure → result** — so traceability survives in the testware.

### 1. Select journeys by risk (decision rule)
Automate the **critical** user journeys only — those touching `risk_areas.critical`, then `risk_areas.high`; do not automate every screen.
- For each candidate step, ask: can this be proven at the API (`/qa:api-automate`) or component level instead? If yes, push it down and keep only the true end-to-end flow at the UI level.
- Result: a short list of journeys to automate, each tagged with its `risk_areas` tier.

### 2. Page Object Model
Encapsulate selectors and actions in page objects under `<paths.tests_dir>/pages/`; keep all assertions in the specs, not the page objects. Reuse and extend existing page objects (Grep/Glob first); never duplicate.

### 3. Stable selectors (non-negotiable)
Use role/label/test-id locators only (`getByRole` / `getByLabel` / `data-testid` for the configured framework); never CSS or XPath coupled to styling. Where a stable hook is missing, agree a `data-testid` with developers rather than coupling to markup.

### 4. Auth & state (numbered substeps)
1. Set up authenticated session state **once per role** (e.g. `storageState`) — one stored state per role in `risk_areas`/`team` scope; never log in through the UI inside every test.
2. Seed each test's data via API/factories per `test_data.strategy` and `test_data.seed_via` (use `/qa:test-data`); synthetic data only — never real PII (`test_data.sensitive_data_rule`).
3. Each test **owns its data** and is independent of other tests' order/state, so the suite is parallel-safe.

### 5. Web-first assertions, no hard waits
Rely on the framework's auto-waiting and web-first assertions; never insert fixed `sleep`/timeout waits. Any flakiness is a defect in the test — route to `/qa:flaky-hunt`.

### 6. Cross-browser (numbered substeps)
1. Run the journeys across every engine in `<ci.browsers>` (e.g. Chromium / Firefox / WebKit).
2. Add device viewports where responsive behavior matters; for dedicated responsive/mobile-web coverage hand off to `/qa:mobile-test`.
3. Record which journeys ran on which engines/viewports so coverage is measurable.

### 7. Config-gated hooks
- **Accessibility:** if `<tooling.accessibility>` is set (not `none`), add an automated accessibility scan on key pages against the `gates.accessibility_standard` (WCAG); for a full audit hand off to `/qa:a11y-audit`. Skip if the toggle is `none`.
- **Visual:** if `<tooling.visual>` is set (not `none`), add visual snapshots on key pages; otherwise skip. State explicitly when a hook is skipped because its toggle is off.

### 8. Place, run, and wire in
1. Place specs under `<paths.tests_dir>/e2e/` and page objects under `<paths.tests_dir>/pages/`.
2. Run the affected specs with the `<tooling.e2e>` runner; fix failures.
   - If a failure is a test defect → fix the test.
   - If a failure is a product defect → do not mask it; report expected-vs-actual and hand off to `/qa:triage` to log a defect (incident) report.
3. Wire smoke journeys into the PR gate and the full set into the nightly run.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — framework from `<tooling.e2e>`/`<tooling.language>`, browsers from `<ci.browsers>`, files under `<paths.tests_dir>`, data per `test_data.*`; accessibility/visual hooks honor the `<tooling.accessibility>`/`<tooling.visual>` toggles and `gates.accessibility_standard`; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis → condition (journey/step) → case → coverage item → procedure → result (→ defect) is preserved and bidirectional; each spec carries a trace back to its journey; no orphans.
- [ ] **Measurable** — output states the journeys automated, their `risk_areas` tier, and which browsers/viewports each ran on, rather than a prose claim.
- [ ] **Residual risk stated** — name what is NOT covered (screens left to lower levels, browsers/viewports/hooks skipped and why) before sign-off (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is a **Test Procedure / script** (ISO/IEC/IEEE 29119-3 **Test Procedure Specification**) under `<paths.tests_dir>/e2e/`, plus the run's **Test Execution Log** (results from the `<tooling.e2e>` reporter).

End with a one-line summary: journeys covered (with risk tier), browsers/viewports run, hooks enabled vs skipped, pass/fail, and any flakiness routed to `/qa:flaky-hunt`.
