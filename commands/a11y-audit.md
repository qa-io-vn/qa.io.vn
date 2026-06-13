---
description: Scaffold or run automated accessibility (axe) checks against the WCAG target in qa.config.yml, then write the Test Execution Log. Use for accessibility audits or to add a11y tests.
argument-hint: "[page name or URL]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Accessibility audit: $ARGUMENTS

**ISTQB process:** Test execution — non-functional **accessibility** testing, mapped to the ISO/IEC 25010 **Usability** characteristic (Accessibility sub-characteristic). Accessibility/usability evaluation is the **CT-UT (Usability Testing) Specialist** stream, not CTFL Foundation; verify exact clauses against the current syllabus before quoting numbers. Non-functional testing as a test type is CTFL v4.0 §2.2.2 (verify section number against the current syllabus).
**Work product:** ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the accessibility scan (violations by severity), plus an **Incident (Defect) Report** for each blocking violation. No dedicated template — follow the closest existing structure (`${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md`) for the per-violation defect entries.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Step 0 — Read config & gate on tooling (do this first)

1. **Config-read guard.** Read `qa.config.yml` from the block above. If it printed `MISSING`, stop and route the user to `/qa:qa-init` — do **not** invent paths, tools, or a WCAG level. Resolve the config-derived inputs in scope: `<tooling.accessibility>` (the a11y tool), `gates.accessibility_standard` (the WCAG target, e.g. `WCAG 2.1 AA`), `gates.a11y_block_on` (severities that fail the build, e.g. `critical`/`serious`), `<paths.tests_dir>` (where a11y tests live), `<paths.docs_dir>` (where the execution log is written), `<paths.reports_dir>` (where raw scan output lands), `<stack.base_url_web>` (target origin), and `risk_areas` (which pages to prioritize). Nothing about paths, tools, or the WCAG level is hardcoded — read the WCAG level from `gates.accessibility_standard`, never assume `WCAG 2.1 AA`.
2. **Accessibility-tooling guard:** if `<tooling.accessibility>` is unset or `none`, state that accessibility testing is **disabled** for this project, offer to enable it (set `tooling.accessibility: axe` in `qa.config.yml`), and stop — do not scaffold scans against a disabled toggle.

## Step 1 — Resolve the target page(s)

Parse `$ARGUMENTS`:
- A **full URL** → use it directly (must be within `<stack.base_url_web>` scope).
- A **page/flow name** → resolve against `<stack.base_url_web>`.
- **Empty `$ARGUMENTS`** → do **not** guess. Default to the pages in `risk_areas.critical` (resolved against `<stack.base_url_web>`), and state explicitly that you defaulted there and why. If `risk_areas.critical` is empty or undefined, ask the user for a page or URL before proceeding.

## Step 2 — Wire the automated scan

1. Ensure `<tooling.accessibility>` (e.g. `@axe-core/playwright` for an axe + Playwright stack) is wired via a **reusable helper** under `<paths.tests_dir>/a11y/`, configured to the `<tooling.e2e>`/`<tooling.language>` already chosen for the project — do not introduce a second runner.
2. Configure the rule set / conformance level from `gates.accessibility_standard` (read the WCAG version and level from config; do not hardcode `WCAG 2.1 AA`).

## Step 3 — Scan the target page(s) in each key state

For each target page from Step 1, add or extend scans across the states that change the DOM/ARIA tree:
1. **Logged out**, **logged in** (drive the saved `storageState` per role where auth applies).
2. **Forms** (empty, focused, and post-submit error states), **modals/dialogs** (open + focus-trapped), and **error/empty states**.
3. Assert each scan against `gates.accessibility_standard`.

## Step 4 — Apply the gate

1. **Fail** the build on any violation whose severity is in `gates.a11y_block_on` (e.g. `critical`/`serious`).
2. Report `moderate`/`minor` violations as a **burndown** (tracked, not build-blocking), with owners/SLAs.
3. **Decision rule:** the page **passes** only when zero violations remain at or above the lowest severity in `gates.a11y_block_on`; otherwise it is **blocked**. Log each blocking violation as an **Incident (Defect) Report** (rule id, WCAG success criterion, element/selector, severity, and the concrete fix) per `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md`.

## Step 5 — Run (or scaffold) & capture results

1. If an environment is reachable, **run** the scan and capture raw tool output under `<paths.reports_dir>`; otherwise scaffold the helper + CI wiring and say the run is deferred.
2. Summarize violations **by severity** with the specific rule, WCAG criterion, element, and fix — as counts, not prose.

## Step 6 — State the manual residual (axe cannot prove conformance)

Automated rules detect only ~30–40% of WCAG issues; an axe pass is **not** WCAG conformance. Explicitly flag the manual checks a tool cannot cover and that require human/assistive-tech evaluation:
- keyboard-only navigation and operability,
- visible focus order and focus indicators,
- screen-reader spot checks (meaningful names, reading order, announcements),
- color-contrast judgment on imagery/states tools miss,
- 200% zoom and reflow,
- meaningful sequence and non-text alternatives.

## Output

Write the **Test Execution Log** to `<paths.docs_dir>/A11Y-RESULTS-<target>.md` (`<target>` slugified from `$ARGUMENTS`, or `critical-risk-areas` when defaulted). It is the ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the accessibility scan. Include:

1. **Scope** — pages and states scanned, WCAG target from `gates.accessibility_standard`, and the `risk_areas` tier of each page.
2. **Violations by severity (counts)** — blocking (in `gates.a11y_block_on`) vs burndown (`moderate`/`minor`), each with rule id, WCAG success criterion, element/selector, and fix.
3. **Gate decision** — pass / blocked per page, with the blocking violations named.
4. **Defect references** — each blocking violation as an Incident (Defect) Report reference.
5. **Manual residual** — the human/assistive-tech checks from Step 6 that remain outstanding.

Then run the Self-check below.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`tooling.accessibility`, `gates.accessibility_standard`, `gates.a11y_block_on`, `paths.tests_dir`, `paths.docs_dir`, `paths.reports_dir`, `stack.base_url_web`, `risk_areas`) is honored; the WCAG level is read from `gates.accessibility_standard`, not hardcoded; the accessibility-tooling guard ran.
- [ ] **Traceability intact** — the chain test basis (WCAG success criteria + `risk_areas` pages) -> condition (page/state) -> case (scan) -> coverage item (rule/criterion) -> result (-> defect for blocking violations) is preserved and bidirectional; no orphan violations.
- [ ] **Measurable** — output states counts (pages/states scanned, violations by severity, blocking vs burndown) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why: automated rules detect only a fraction of WCAG issues; keyboard, focus, screen-reader, contrast judgment, and zoom/reflow need human evaluation (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the accessibility scan and written to `<paths.docs_dir>/A11Y-RESULTS-<target>.md`.

## Handoff

- `/qa:usability-test` — broader ISO/IEC 25010 usability evaluation (heuristics, task scenarios) beyond automated accessibility.
- `/qa:web-automate` — fold the a11y helper into the wider E2E suite; reciprocate the automated a11y scan it wires on key pages.
- `/qa:triage` — file and lifecycle each blocking violation as a defect report.
- `/qa:release-report` — feeds the a11y gate status into the Test Completion Report's exit-criteria evaluation.
