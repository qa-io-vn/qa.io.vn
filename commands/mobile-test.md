---
description: Test responsive/mobile web behavior using ISTQB CT-MAT concerns — viewports, touch, network conditions, device matrix. Use to cover mobile/responsive quality for a web app.
argument-hint: "[feature / page]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile / responsive testing${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Mobile Application Testing concerns (CT-MAT), applied to responsive web.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Scope from `$ARGUMENTS` (else key responsive pages). For a responsive web app (no native app), focus on the applicable CT-MAT concerns:

1. **Viewport & layout** — test across device viewports (mobile/tablet/desktop) using Playwright device descriptors and `ci.browsers` (include WebKit for iOS Safari fidelity). Check reflow, no horizontal scroll, tap-target sizes, and readable text at small widths.
2. **Touch & interaction** — tap, swipe, long-press, on-screen keyboard behavior, focus/scroll on inputs.
3. **Network conditions** — behavior on slow/flaky/offline connections (throttling); graceful loading and error states.
4. **Interrupts & state** — orientation change, backgrounding, resize, and state preservation.
5. **Performance on mobile** — payload weight and render on constrained profiles (tie to `/qa:perf-test`).

Implement responsive Playwright projects/specs (device emulation, throttling) under `paths.tests_dir`, and report findings. If a native mobile app exists, note that real-device/native tooling (Appium/cloud device farm) is needed beyond this command's responsive-web scope.
