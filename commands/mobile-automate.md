---
description: Build automated mobile tests — native/cross-platform via Appium or a cloud device farm, or responsive mobile-web via Playwright. Use for mobile test automation (iOS/Android apps or mobile web). Writes platform/screen objects and specs under the configured tests dir, plus a device-matrix coverage table.
argument-hint: "<feature / flow> [native|web]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile test automation: $ARGUMENTS

**ISTQB process:** Mobile Application Testing (**CT-MAT**, Specialist stream) executed through Test Automation Engineering (**CT-TAE**) — verify section numbers against the current syllabi. CT-MAT is a Specialist topic, not CTFL Foundation. Mobile automation produces **system-level** tests on device; reserve on-device UI automation for genuine end-to-end flows and push checks down to API/component levels where they can be proven more cheaply (the test pyramid).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Existing mobile framework
```!
echo "--- mobile/e2e config ---"; ls -1 wdio.conf.* appium*.* capabilities.* playwright.config.* 2>/dev/null
echo "--- mobile tests (root from paths.tests_dir) ---"; ls -1R tests 2>/dev/null | grep -i mobile | head -40
```

## Your task

Build or extend automated mobile tests for the target in `$ARGUMENTS`, driven entirely by `qa.config.yml`.

### Step 0 — Guards & inputs (run first)
1. **Config-read guard.** If the config block above printed `MISSING` (no `qa.config.yml`), STOP and tell the user to run `/qa:qa-init` first — do not invent or hardcode `paths.*`, `tooling.*`, `stack.*`, the device matrix, `gates`, or `risk_areas`. If config is present, resolve every `<paths.*>`, `<tooling.*>`, `<stack.*>`, the device matrix, `gates`, and `risk_areas` value used below from it. Never hardcode a path, tool, or device list.
2. **Target argument.** `$ARGUMENTS` names the feature/flow to automate, optionally suffixed with `native` or `web` to force the surface. **If `$ARGUMENTS` is empty:** ask the user which feature/flow (and surface) to automate; if they cannot supply one, default the target to the first item in `risk_areas.critical` from `qa.config.yml` and state that you applied this default.

Treat the flow in `$ARGUMENTS` as the **test basis**. Work the ISTQB chain explicitly — **basis → condition (flow/CT-MAT concern) → case → coverage item → procedure → result (→ defect)** — so traceability survives in the testware and the device-matrix table.

### Step 1 — Route to the mobile surface (decision tree)
Pick exactly one branch using `tooling.mobile` and any `native`/`web` suffix in `$ARGUMENTS`:

1. **`tooling.mobile` is unset / `null` / `none`** → the mobile tool is not yet chosen. STOP and route to **`/qa:tool-select`** to evaluate and record the mobile tool (Appium vs device farm vs responsive-web), then return here. Do not assume a tool.
2. **`tooling.mobile: web_app`** *(or `$ARGUMENTS` ends in `web`, or the product has no native binary)* → **Responsive mobile-web.** This command is for native/cross-platform automation; hand off to **`/qa:mobile-test`** for the responsive concerns (viewports, touch, throttling, device matrix). If you build any responsive specs here, place them under `<paths.tests_dir>/mobile/` and keep `/qa:mobile-test` as the owner.
3. **`tooling.mobile: appium`** *(or a cloud device farm, or `$ARGUMENTS` ends in `native`)* → **Native / cross-platform app (iOS / Android).** Continue with Steps 2–6 below.

State which branch you took and why before proceeding.

### Step 2 — Device strategy (matrix from config)
1. Build the device/OS matrix from `tooling.mobile_device_matrix` in config (e.g. iPhone 14 / Pixel 7); never hardcode a device list. If the matrix is absent, ask the user or route to `/qa:tool-select` to define it — do not guess.
2. For each entry decide **real vs emulated/simulated**: cover the platform versions your users actually run; balance real-device cost (route to a cloud device farm such as BrowserStack / Sauce / Firebase Test Lab where configured) against emulator speed.
3. **Decision rule:** every `risk_areas.critical` flow runs on at least one real device per platform (iOS + Android); lower-risk flows may run emulated only. Record this allocation — it drives the device-matrix table in Step 6.

### Step 3 — Automate the CT-MAT concerns
For the flow in scope, derive and automate test conditions for each applicable CT-MAT concern (skip with a stated reason if not applicable):
- **Functional flows** via platform locators — accessibility IDs preferred for stability; never couple to fragile UI hierarchy/XPath.
- **Gestures** — tap, swipe, long-press, pinch, scroll.
- **App lifecycle & interrupts** — background/foreground, rotation, low memory, incoming call/notification, deep links, permissions dialogs.
- **Network conditions** — offline, slow, and transitions; assert graceful errors and data sync.
- **Platform differences** — iOS vs Android behavior, back button, on-screen keyboards.
- **Installation / upgrade**, and **on-device performance** (battery/memory) — hand off the performance objectives/workload model to `/qa:perf-plan` and execution to `/qa:perf-test`.

### Step 4 — Engineering (gTAA, CT-TAE)
1. Page/screen objects **per platform** under `<paths.tests_dir>/mobile/`; keep assertions in the specs, not the screen objects. Grep/Glob for existing screen objects first and extend them — never duplicate.
2. Stable **accessibility IDs** as the primary locator; agree a stable hook with developers where one is missing rather than coupling to markup.
3. **Data-driven & synthetic** — seed each test's data via API/factories per `test_data.strategy` / `test_data.seed_via` (use `/qa:test-data`); synthetic data only, never real PII (`test_data.sensitive_data_rule`). Each test owns its data and is order-independent.
4. **Parallel device runs in CI** on `<tooling.ci.platform>`; treat any flakiness as a test defect and route to `/qa:flaky-hunt`.

### Step 5 — Run & wire in
1. Run the affected specs on the available devices/emulators via the configured runner; fix failures.
   - If a failure is a test defect → fix the test.
   - If a failure is a product defect → do not mask it; report expected-vs-actual and hand off to `/qa:triage` to log a defect (incident) report.
2. Wire critical-flow smoke runs into the PR gate and the full device matrix into the nightly run.

### Step 6 — Device-matrix traceability table
Emit a coverage table so coverage is measurable, not prose. One row per (CT-MAT concern × device) executed:

| Concern (CT-MAT) | Test case | Coverage item | Device (real/emu) | Status | Risk tier |
|---|---|---|---|---|---|
| e.g. Gestures — swipe | TC-… | swipe-to-dismiss | Pixel 7 (real) | Pass | critical |

Every `risk_areas.critical` flow must appear with at least one real-device row per platform. Explicitly list which CT-MAT concerns, devices, or platform versions are **not** covered and why.

## Output & work product
Produce automated mobile tests under `<paths.tests_dir>/mobile/`. The work product is a **Test Procedure / script** (ISO/IEC/IEEE 29119-3 **Test Procedure Specification**) plus the run's **Test Execution Log** (results from the configured runner, written under `<paths.reports_dir>`), accompanied by the device-matrix coverage table above. On-device performance objectives are owned by `/qa:perf-plan` (planning) and `/qa:perf-test` (execution); responsive mobile-web is owned by `/qa:mobile-test`; tool selection by `/qa:tool-select`; this command sits under the program-level Test Automation Strategy (`/qa:automation-strategy`).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — surface routed from `tooling.mobile`, devices from `tooling.mobile_device_matrix`, files under `<paths.tests_dir>/mobile/`, results under `<paths.reports_dir>`, data per `test_data.*`, CI on `<tooling.ci.platform>`; nothing hardcoded (no device list, path, or tool baked in).
- [ ] **Traceability intact** — the chain test basis → condition (flow/CT-MAT concern) → case → coverage item → procedure → result (→ defect) is preserved and bidirectional in the device-matrix table; no orphans.
- [ ] **Measurable** — output states concerns automated, their `risk_areas` tier, and which devices (real/emulated) each ran on via the matrix table, rather than a prose claim; every `risk_areas.critical` flow has a real-device row per platform.
- [ ] **Residual risk stated** — name what is NOT covered (CT-MAT concerns, devices, OS versions left out, manual/real-device checks still required, surface handed to `/qa:mobile-test`) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as a **Test Procedure Specification** (ISO/IEC/IEEE 29119-3) plus **Test Execution Log**, written to `<paths.tests_dir>/mobile/` and `<paths.reports_dir>`.

End with a one-line summary: surface/branch taken, concerns covered (with risk tier), devices run (real/emulated), pass/fail, defects routed to `/qa:triage`, and any flakiness routed to `/qa:flaky-hunt`.
