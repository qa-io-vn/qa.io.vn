---
description: Build or extend automated Web UI / E2E tests with Playwright — user journeys, Page Object Model, cross-browser, auth state, with a11y and visual hooks. Use for web UI test automation.
argument-hint: "<feature / user journey / page>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Web UI / E2E automation: $ARGUMENTS

**ISTQB process:** Test automation (CT-TAE) at the **system/E2E level** (CTFL §2.2). Reserve UI automation for genuine user journeys (pyramid); push checks to API where possible.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Existing UI framework
```!
echo "--- playwright config ---"; ls -1 playwright.config.* 2>/dev/null
echo "--- pages / e2e ---"; ls -1R tests/pages tests/e2e 2>/dev/null | head -40
```

## Your task

Target from `$ARGUMENTS` (feature / journey / page). Build automated UI tests with Playwright + `tooling.language`.

1. **Select journeys by risk** — automate the critical user journeys (`risk_areas`), not every screen. Verify business logic via API where feasible; keep UI for true end-to-end flows.
2. **Page Object Model** — encapsulate selectors and actions in `tests/pages/`; keep assertions in specs. Reuse/extend existing POMs.
3. **Stable selectors** — `getByRole`/`getByLabel`/`data-testid` only; never CSS/XPath coupled to styling. Agree `data-testid` hooks with devs.
4. **Auth & state** — use `storageState` per role (set up once), seed data via API/factories (`/qa:test-data`); each test owns its data, parallel-safe.
5. **Web-first assertions, no hard waits**; rely on auto-waiting.
6. **Cross-browser** — run across `ci.browsers` (Chromium/Firefox/WebKit); add device viewports where responsive matters (or `/qa:mobile-test`).
7. **Hooks** — add accessibility scans (`/qa:a11y-audit`) and visual snapshots on key pages where enabled.

Place under `tests/e2e/`, run (`npx playwright test tests/e2e/...`), fix failures, and wire smoke journeys into the PR gate (full set nightly). Report the journeys covered and any flakiness (route to `/qa:flaky-hunt`).
