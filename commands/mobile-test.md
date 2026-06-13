---
description: Test responsive/mobile web behavior using ISTQB CT-MAT concerns — viewports, touch, network conditions, device matrix. Use to cover mobile/responsive quality for a web app; writes responsive specs and emits a Test Execution Report with a device-matrix coverage table.
argument-hint: "[feature / page]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile / responsive web testing: $ARGUMENTS

**ISTQB process:** Mobile Application Testing concerns (**CT-MAT**, Specialist stream), applied to responsive web through Test Execution — verify section numbers against the current CT-MAT syllabus before citing them. CT-MAT is a Specialist topic, not CTFL Foundation. This command exercises the ISO/IEC 25010 characteristics most affected by small-screen/touch/network use: **compatibility/portability** (device & viewport coverage), **usability** (tap targets, readable text), **performance efficiency** (constrained network/render), and **reliability** (interrupts, state preservation).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Existing responsive framework
```!
echo "--- web/responsive config ---"; ls -1 playwright.config.* wdio.conf.* 2>/dev/null
echo "--- responsive tests (root from paths.tests_dir) ---"; ls -1R tests 2>/dev/null | grep -iE "mobile|responsive" | head -40
```

## Your task

Test responsive/mobile-web behavior for the target in `$ARGUMENTS`, driven entirely by `qa.config.yml`.

### Step 0 — Guards & inputs (run first)
1. **Config-read guard.** If the config block above printed `MISSING` (no `qa.config.yml`), STOP and tell the user to run `/qa:qa-init` first — do not invent or hardcode `<paths.*>`, `<tooling.*>`, `<stack.*>`, the device/viewport matrix, `<ci.browsers>`, `gates`, or `risk_areas`. If config is present, resolve every value used below from it. Never hardcode a path, tool, viewport, or device list.
2. **Target argument.** `$ARGUMENTS` names the feature/page to cover. **If `$ARGUMENTS` is empty:** ask the user which feature/page (and which key responsive flows) to test; if they cannot supply one, default the scope to the first item in `risk_areas.critical` from `qa.config.yml` and state that you applied this default.
3. **Surface check.** This command owns **responsive mobile-web** only. If a native/cross-platform app exists, hand off to **`/qa:mobile-automate`** (Appium / cloud device farm); note in the report that native concerns are out of this command's scope.

Treat the feature/page in `$ARGUMENTS` as the **test basis**. Work the ISTQB chain explicitly — **basis → condition (CT-MAT concern) → case → coverage item → procedure → result (→ defect)** — so traceability survives in the testware and the device-matrix table.

### Step 1 — Build the device/viewport matrix (from config)
1. Build the matrix from `<tooling.mobile_device_matrix>` (e.g. iPhone 14 / Pixel 7) plus tablet and desktop widths; never hardcode a device or viewport list. If the matrix is absent, ask the user or route to **`/qa:tool-select`** to define it — do not guess.
2. Use Playwright device descriptors and `<ci.browsers>` for emulation; include **WebKit** for iOS Safari fidelity where listed.
3. **Decision rule:** every `risk_areas.critical` flow runs on at least one mobile viewport, one tablet viewport, and one desktop viewport; lower-risk flows may run on a reduced set. Record this allocation — it drives the device-matrix table in Step 7.

### Step 2 — Viewport & layout
Derive and run conditions across the matrix:
- **No horizontal scroll** at the smallest viewport in the matrix.
- **Reflow** — content reflows without loss of function or content (no overlap, no clipped controls).
- **Tap-target size** — interactive targets meet the minimum size threshold; record actual vs threshold per target.
- **Text legibility** — body text meets the minimum size threshold and is not truncated at small widths.

### Step 3 — Touch & interaction
Tap, swipe, long-press, on-screen-keyboard behavior, focus/scroll on inputs; assert the expected result for each gesture rather than only "no error."

### Step 4 — Network conditions
Behavior on slow / flaky / offline connections (throttling): assert graceful loading states, retry/error states, and data recovery on reconnect.

### Step 5 — Interrupts & state preservation
Orientation change, backgrounding/foregrounding, viewport resize, and **state preservation** across each. Record a PASS/FAIL per interrupt scenario for the state-preservation tally in Step 7.

### Step 6 — Implement & run
1. Implement responsive Playwright projects/specs (device emulation, throttling) under `<paths.tests_dir>/`; Grep/Glob for existing responsive specs first and extend them — never duplicate. Keep assertions in the specs.
2. Seed each test's data per `test_data.strategy` / `test_data.seed_via` (use `/qa:test-data`); synthetic data only, never real PII (`test_data.sensitive_data_rule`).
3. Run the affected specs across the matrix via the configured runner; write results under `<paths.reports_dir>/`. For each failure:
   - test defect → fix the test; if flaky, route to **`/qa:flaky-hunt`**.
   - product defect → do not mask it; report expected-vs-actual and hand off to **`/qa:triage`** to log a defect (incident) report.
4. Hand off mobile payload-weight / render-on-constrained-profile objectives to **`/qa:perf-test`** (execution) and **`/qa:perf-plan`** (workload model) — do not duplicate performance thresholds here.

### Step 7 — Output (Test Execution Report)
Emit the report below so coverage is measurable, not prose:

1. **Device-matrix coverage table** — one row per (CT-MAT concern × device/viewport) executed:

   | Concern (CT-MAT) | Test case | Coverage item | Device / viewport (browser) | Status | Risk tier |
   |---|---|---|---|---|---|
   | e.g. Viewport — no h-scroll | TC-… | smallest-width reflow | iPhone 14 (webkit) | Pass | critical |

   Every `risk_areas.critical` flow must appear with at least one mobile, one tablet, and one desktop row.
2. **Tap-target / text-size results** — per checked element: target, actual size, threshold, PASS/FAIL.
3. **State-preservation tally** — PASS/FAIL count across the interrupt scenarios from Step 5 (orientation, background/foreground, resize).
4. **Discovered defects** — list each with summary, severity, and the `/qa:triage` handoff reference.
5. **Residual risk** — list which CT-MAT concerns, viewports, or browsers are **not** covered and why; note any native-app surface deferred to `/qa:mobile-automate`.

## Output & work product
The work product is a **Test Execution Report** (ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** — the closest 29119-3 work product; no dedicated template), written under `<paths.reports_dir>/`, accompanied by the device-matrix coverage table, tap-target/text-size results, state-preservation tally, and discovered defects. Implemented responsive specs are **Test Procedures / scripts** under `<paths.tests_dir>/`. Native/cross-platform automation is owned by `/qa:mobile-automate`; on-device & payload performance by `/qa:perf-plan` (planning) and `/qa:perf-test` (execution); tool selection by `/qa:tool-select`; defects by `/qa:triage`; flakiness by `/qa:flaky-hunt`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — viewports/devices from `<tooling.mobile_device_matrix>` and `<ci.browsers>`, specs under `<paths.tests_dir>/`, results under `<paths.reports_dir>/`, data per `test_data.*`, prioritization per `risk_areas`; nothing hardcoded (no device, viewport, path, or tool baked in).
- [ ] **Traceability intact** — the chain test basis → condition (CT-MAT concern) → case → coverage item → procedure → result (→ defect) is preserved and bidirectional in the device-matrix table; no orphans.
- [ ] **Measurable** — output states the device-matrix coverage table, tap-target/text-size PASS/FAIL, the state-preservation tally, and discovered defects with severity — counts/coverage, not prose; every `risk_areas.critical` flow has mobile + tablet + desktop rows.
- [ ] **Residual risk stated** — name what is NOT covered (CT-MAT concerns, viewports, browsers, native-app surface deferred to `/qa:mobile-automate`) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as a **Test Execution Report** (ISO/IEC/IEEE 29119-3 Test Execution Log / Test Results) written to `<paths.reports_dir>/`, with responsive specs as Test Procedures under `<paths.tests_dir>/`.

End with a one-line summary: scope/page, concerns covered (with risk tier), viewports run, tap-target/state-preservation pass rate, defects routed to `/qa:triage`, and any native surface deferred to `/qa:mobile-automate`.
