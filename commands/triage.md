---
description: Analyze a failing test or defect, classify severity and priority independently, and write a 29119-3 Incident (Defect) Report. Use when a test fails for a real reason or the user reports a bug.
argument-hint: "<failure, error, or bug description>"
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Triage: $ARGUMENTS

**ISTQB process:** Defect management (CTFL v4.0 §5.5 — verify the section against the current syllabus before asserting it). **Work product:** ISO/IEC/IEEE 29119-3 **Incident (Defect) Report**, one report per defect. Use the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md`. Throughout, keep **severity** (impact of the defect on the test object) and **priority** (urgency to fix — a business decision) as two independent fields; never collapse them.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "NO_CONFIG"
```

## Your task

**Config guard.** If the config block above is `NO_CONFIG`, stop and tell the user to run `/qa:qa-init` first — the severity blocker rule (`gates.block_on_severity`), the priority tiers (`risk_areas.*`), and the output path (`<paths.reports_dir>`) all come from `qa.config.yml`. Do not hardcode paths, tools, severities, or thresholds; read them from config.

**Resolve the subject.** Take the failure, stack trace, or bug description from `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask the user for the failure or bug to triage; if they decline, default the scope to the most recent failing result touching a `risk_areas.critical` area and label the report **provisional**.

Work through these steps in order:

1. **Investigate (read-only).** Read the failing test, the related source, and any trace / screenshot / log under `<paths.tests_dir>` and `<paths.reports_dir>`. Classify the root location using this decision rule, in order — stop at the first match:
   - **Test defect** — the test asserts the wrong thing, has a bad selector/locator, or a timing/ordering bug. → Route to `/qa:flaky-hunt` (if intermittent) or `/qa:add-test` (to correct the assertion). Still record an Incident Report only if it masked a real escape.
   - **Environment / infrastructure** — data, network, config, or build issue, not the product. → Note it; do not raise a product defect.
   - **Product defect** — the test object behaves incorrectly against the test basis. → Continue to step 2 and raise the Incident Report.

2. **Assign severity (impact on the test object — independent of urgency).** Use these thresholds; pick the highest that applies:
   - **S1 — Critical:** system down, data loss, security breach, or no workaround.
   - **S2 — Major:** key function broken; workaround painful or none.
   - **S3 — Minor:** function impaired; an acceptable workaround exists.
   - **S4 — Trivial:** cosmetic / low impact (typo, alignment).
   Record the assigned `S_` with a one-line justification stated in terms of impact on the system.

3. **Assign priority (urgency to fix — set independently of severity).** Map from the affected `risk_areas` tier and release timing:
   - Affected area in `risk_areas.critical` (or blocks the release / critical path) → **P1 — Urgent**.
   - Affected area in `risk_areas.high` → **P2 — High** (fix this release).
   - Affected area in `risk_areas.medium` → **P3 — Medium** (fix when capacity allows).
   - Otherwise → **P4 — Low** (backlog).
   A high-severity defect in a never-used feature can be low priority; a low-severity defect on the critical path can be high priority. State severity and priority as two separate fields.

4. **Flag the release blocker.** If the assigned severity is in `gates.block_on_severity` (default `["S1","S2"]` — read the actual list from config), mark the report **RELEASE BLOCKER** and say which gate it trips.

5. **Assign a unique defect ID.** Use `DEF-<item>-<nnn>` where `<item>` is the affected component/area (lowercase, hyphenated) and `<nnn>` is a zero-padded sequence. Scan existing reports in `<paths.reports_dir>/defects/` and take the next free number for that `<item>`; IDs are unique, stable, and never reused.

6. **Write the Incident (Defect) Report** to `<paths.reports_dir>/defects/<defect-id>.md`, using `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md` as the field schema. Populate: defect ID, summary, test object & version, environment (from `environments` — never hardcode URLs), numbered deterministic steps to reproduce, expected vs actual (the deviation), evidence, severity + priority (with justifications), release-blocker flag, suspected root cause/component, and a suggested owner. Use synthetic test data only — never real PII.

7. **Recommend the follow-up.** If it is a real escape, recommend a regression test so it cannot recur — hand off to `/qa:add-test` (new case) or `/qa:implement` (executable spec), and to `/qa:regression` for suite-level protection. If the failure was an intermittent test defect, hand off to `/qa:flaky-hunt`.

Read-only on product code — diagnose and write the report; do not change product code.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.reports_dir`, `gates.block_on_severity`, and `risk_areas.*` are read from `qa.config.yml`; no path, tool, severity, or threshold is hardcoded.
- [ ] **Severity ≠ priority** — both fields are present and set independently; severity is justified by impact on the test object, priority by the affected `risk_areas` tier and release timing.
- [ ] **Traceability intact** — the report links back through result → procedure/script → case → condition → test basis, and (for an escape) names the missing/weak test condition; no orphan.
- [ ] **Measurable** — the report states reproducibility (always / N-of-M / once) and the concrete deviation (status code, value, error), not prose claims.
- [ ] **Residual risk stated** — name what is NOT covered (e.g. defects beyond this one symptom; defect clustering), per ISTQB Principle 1 (testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Incident (Defect) Report** with a unique `DEF-<item>-<nnn>` ID, written to `<paths.reports_dir>/defects/<defect-id>.md`.
