---
description: Maintain and auto-heal the automated test suite — detect broken locators after UI changes, repair them with stable alternatives, prune/refactor obsolete tests, and re-run to confirm. Use when tests break due to UI/DOM changes or for routine suite maintenance.
argument-hint: "[test path / failing area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Self-heal & maintain the test suite${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test automation maintenance (CT-TAE) — keep automated testware effective and current as the SUT evolves; counters the pesticide paradox (CTFL §1.3).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Suite signals
```!
echo "--- page objects ---"; ls -1 tests/pages 2>/dev/null | head
echo "--- recent UI changes ---"; git diff --name-only HEAD~10 2>/dev/null | grep -iE "\.(tsx|jsx|vue|html|css)$" | head -20 || echo "no git history"
echo "--- last results ---"; ls -1 playwright-report test-results reports 2>/dev/null
```

## Your task

Scope from `$ARGUMENTS` (a path/area, else the failing/changed areas). Two jobs: **auto-heal** broken locators, and **maintain** the suite.

### A. Auto-heal broken locators
1. **Run the target tests** to see current failures (or read the latest report). Focus on **locator failures** — element not found, timeout waiting for selector, strict-mode violations.
2. For each, **decide why** the locator broke:
   - **Element legitimately moved/renamed** (selector changed, attribute renamed, restructured DOM) → **heal it**.
   - **Element genuinely absent** because the app is broken → this is a **product defect**, NOT a locator problem. Do not heal it away; escalate via `/qa:triage`.
   - **Flaky/timing** (element appears late, race) → stabilize (web-first assertion); see `/qa:flaky-hunt`.
3. **Heal** by finding the element via the most **stable alternative strategy**, in priority order: `data-testid` → `getByRole`+accessible name → `getByLabel` → `getByText`/placeholder → DOM proximity/anchor. Inspect the current DOM (run a small Playwright probe against `base_url_web`) to confirm the new locator resolves to exactly one element. Update the **Page Object** (not scattered specs) so the fix is centralized.
4. **Confidence** — apply high-confidence heals directly; for ambiguous matches (multiple candidates, changed semantics), propose the change and flag for human review rather than guessing.

> Guardrail: never heal by loosening an assertion or pointing at the wrong element to force green. Healing fixes *how we locate*, not *what we verify*. Real product defects are escalated, not silenced.

### B. Maintain the suite
- **Prune** obsolete/duplicate tests and dead page-object methods; remove tests for removed features.
- **Refactor** duplicated locators into shared page objects; replace brittle CSS/XPath with role/testid.
- **Intentional baseline updates** — for visual/snapshot diffs that reflect approved UI changes, update baselines deliberately (`--update-snapshots`) after confirming the change is intended.
- **Pesticide paradox** — flag stale tests that no longer find defects; suggest new conditions (`/qa:test-cases`).
- **Quarantine review** — re-check quarantined `@flaky` tests; fix or retire per SLA.

### C. Verify
Re-run the healed/affected tests **locally** and confirm green. Iterate until the previously-broken (non-defect) tests pass. Report: locators healed (old → new, with confidence), real defects escalated, maintenance actions taken, and the local run result.
