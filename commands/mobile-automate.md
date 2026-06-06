---
description: Build automated mobile tests — native/cross-platform via Appium or a cloud device farm, or responsive mobile-web via Playwright. Use for mobile test automation (iOS/Android apps or mobile web).
argument-hint: "<feature / flow> [native|web]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile test automation: $ARGUMENTS

**ISTQB process:** Mobile Application Testing (CT-MAT) + Test Automation Engineering (CT-TAE).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Your task

Determine the mobile surface from `$ARGUMENTS` and `tooling.mobile`:

### A. Responsive mobile-web (default for a web app)
If the product is a web app (no native binary), automate with Playwright device emulation — see `/qa:mobile-test` for the responsive concerns (viewports, touch, throttling). Build/extend those specs under `tests/mobile/`.

### B. Native / cross-platform app (iOS / Android)
If there is a native app (`tooling.mobile: appium`):
1. **Tooling** — Appium (with WebdriverIO/Playwright driver) or a cloud **device farm** (BrowserStack/Sauce/Firebase Test Lab). Confirm via `/qa:tool-select` if not set.
2. **Device strategy** — define the device/OS matrix (real vs emulated/simulated); cover the platform versions your users have; balance real-device cost vs emulator speed.
3. **Automate the CT-MAT concerns**:
   - Functional flows via platform locators (accessibility IDs preferred for stability).
   - **Gestures** — tap, swipe, long-press, pinch, scroll.
   - **App lifecycle & interrupts** — background/foreground, rotation, low memory, incoming call/notification, deep links, permissions dialogs.
   - **Network conditions** — offline, slow, transitions; graceful errors and sync.
   - **Platform differences** — iOS vs Android behavior, back button, keyboards.
   - **Installation/upgrade**, and **performance on device** (battery/memory — tie to `/qa:perf-plan`).
4. **Engineering** — page/screen objects per platform, stable accessibility IDs, data-driven, synthetic data, parallel device runs in CI.

Place tests under `tests/mobile/`, run on available devices/emulators, and report device-matrix coverage. Note where real-device testing or manual checks are required beyond what automation covers.
