---
description: Maintain and auto-heal the automated test suite — detect broken locators after UI changes, repair them with stable alternatives, prune/refactor obsolete tests, and re-run to confirm. Use when tests break due to UI/DOM changes or for routine suite maintenance.
argument-hint: "[test path / failing area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Self-heal & maintain the test suite

**ISTQB process:** Test automation maintenance (CT-TAE) — keep automated testware effective and current as the test object evolves; counters the pesticide paradox (CTFL v4.0 §1.3, Principle 5 — verify against the current syllabus). Maintainability is an ISO/IEC 25010 quality characteristic of the testware itself.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

**Config-read guard:** if no `qa.config.yml` is found, stop and recommend `/qa:qa-init` before healing — locator strategy, framework (`tooling.e2e`), test root (`<paths.tests_dir>`), report dir (`<paths.reports_dir>`), and the probe target (`<stack.base_url_web>`) all come from config. Do not hardcode any path, tool, or URL.

## Suite signals
```!
echo "--- page objects (under tests root) ---"; ls -1 tests/pages 2>/dev/null | head || echo "(resolve from <paths.tests_dir>)"
echo "--- recent UI changes ---"; git diff --name-only HEAD~10 2>/dev/null | grep -iE "\.(tsx|jsx|vue|html|css)$" | head -20 || echo "no git history"
echo "--- last results ---"; ls -1 playwright-report test-results reports 2>/dev/null || echo "(resolve from <paths.reports_dir>)"
```

> The discovery block above probes common defaults so it works before config is read. Once `qa.config.yml` is loaded, treat **`<paths.tests_dir>`** as the automation/page-object root, **`<paths.reports_dir>`** as the results location, and **`<tooling.e2e>`** as the runner — never the literal `tests/pages`, `playwright-report`, `test-results`, or `npx playwright`.

## Your task

**Scope (resolve `$ARGUMENTS` first):**
- If `$ARGUMENTS` names a path or area, scope to it.
- If `$ARGUMENTS` is **empty**: scope to the tests that currently fail or are impacted by recent UI changes (intersection of the "last results" failures and the "recent UI changes" diff above). If neither signal is available, ask the user for a target rather than scanning the whole suite blind; only fall back to `risk_areas.critical` areas when explicitly told to proceed without a target.

Two jobs: **auto-heal** broken locators, and **maintain** the suite. Run A then B then C in order.

### A. Auto-heal broken locators
1. **Run the in-scope tests** with the configured runner (`<tooling.e2e>`) to see current failures, or read the latest results under `<paths.reports_dir>`. Focus on **locator failures** — element not found, timeout waiting for selector, strict-mode (multiple-match) violations.
2. For each failure, **classify the cause** using these decision rules (apply the first that matches):
   - **Locator drift** — the element still exists but its selector/attribute/DOM position changed → **heal it** (step 3).
   - **Product defect** — the element is genuinely absent because the app is broken (feature regressed, error page, blank render) → do **not** heal it away; escalate via `/qa:triage` and leave the assertion intact.
   - **Flaky/timing** — the element appears late or intermittently (race, animation, network) → do **not** rewrite the locator; stabilize with a web-first assertion and hand off to `/qa:flaky-hunt`.
   - **Intentional removal** — the feature was removed on purpose → prune the test in job B, don't heal.
3. **Heal** by relocating the element via the most **stable strategy available**, in this strict priority order (use the highest tier that resolves to exactly one element): (1) `data-testid`/test attribute → (2) `getByRole` + accessible name → (3) `getByLabel` → (4) `getByText`/placeholder → (5) DOM proximity/anchor. Confirm the new locator resolves to **exactly one** element by inspecting the live DOM (run a small `<tooling.e2e>` probe against `<stack.base_url_web>`). Apply the fix in the **Page Object** under `<paths.tests_dir>` (centralized), never in scattered specs.
4. **Confidence rule** — apply a heal **directly** only when one candidate uniquely matches at tier 1–3 with unchanged semantics. If there are **multiple candidates**, a tier-4/5 match, or any semantic ambiguity, **propose** the change and flag it for human review instead of guessing.

### B. Maintain the suite
1. **Prune** obsolete/duplicate tests and dead page-object methods under `<paths.tests_dir>`; remove tests for removed features.
2. **Refactor** duplicated locators into shared page objects; replace brittle CSS/XPath with role/testid (apply the same priority order as step A3).
3. **Intentional baseline updates** — for visual/snapshot diffs that reflect *approved* UI changes (requires `tooling.visual` enabled), regenerate baselines deliberately via the runner's update-snapshots mode **only after** confirming the change is intended. If `tooling.visual` is `none`, skip this step.
4. **Pesticide paradox** — flag stale tests that no longer find defects; suggest new conditions via `/qa:test-cases` (and `/qa:test-design` for the design).
5. **Quarantine review** — re-check quarantined `@flaky` tests; fix or retire per the SLA in the strategy. Hand any still-flaky cases to `/qa:flaky-hunt`.

> Guardrail: never heal by loosening an assertion or pointing at the wrong element to force green. Healing fixes *how we locate*, not *what we verify*. Real product defects are escalated via `/qa:triage`, not silenced.

> Scope note: this command maintains **automated testware**. For maintenance *testing* of the product after a change/migration/retirement (impact analysis on the SUT), use `/qa:maintenance-test`.

### C. Verify & report
1. Re-run the healed/affected tests **locally** with `<tooling.e2e>` and confirm green. Iterate until every previously-broken **non-defect** test passes; record the actual run counts (passed/failed), not a prose claim.
2. **Report** (state counts, not adjectives): locators healed (old → new, strategy tier, confidence), real defects escalated to `/qa:triage`, maintenance actions taken (pruned/refactored/baselines), quarantine size delta, and the local run result.

**Work product:** this command updates **automated test scripts / Test Procedure Specifications** (ISO/IEC/IEEE 29119-3) in place under `<paths.tests_dir>`, plus a short maintenance change log; the run output is a **Test Execution Log / Test Results** under `<paths.reports_dir>`. It maintains testware **maintainability** (ISO/IEC 25010). No dedicated 29119-3 template — it edits existing testware rather than authoring a new document.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.tests_dir`, `paths.reports_dir`, `tooling.e2e`, `tooling.visual`, `stack.base_url_web`, `risk_areas`) is honored; nothing hardcoded (no fixed `tests/pages`, `playwright-report`, `test-results`, `npx playwright`, URLs, or secrets).
- [ ] **Cause classified, not masked** — each touched failure is tagged locator-drift / product-defect / flaky / intentional-removal; defects went to `/qa:triage` and flaky cases to `/qa:flaky-hunt` — none were "healed" by loosening an assertion.
- [ ] **Locator stability** — every new locator uses the highest available strategy tier and resolves to exactly one element (verified against the live DOM); fixes live in the Page Object, not scattered specs.
- [ ] **Traceability intact** — the chain test condition → case → procedure/script → result is preserved; healed scripts still assert the original expected behavior (no orphaned or weakened cases).
- [ ] **Measurable** — output states counts (locators healed, defects escalated, tests pruned, quarantine delta, local pass/fail) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered (e.g. heals verified only against the probed environment; flagged ambiguous heals awaiting human review; stale tests not yet refreshed) per ISTQB Principle 1 (testing shows the presence of defects, not their absence).
- [ ] **Work product named** — output is identified as updated 29119-3 Test Procedure Specifications / scripts + Test Execution Log, written to the correct `<paths.tests_dir>` / `<paths.reports_dir>` locations.

## Hand off

- `/qa:triage` — for any element absence/intermittency traced to a genuine product defect.
- `/qa:flaky-hunt` — for tests that are non-deterministic rather than broken by UI drift.
- `/qa:test-cases` / `/qa:test-design` — to add new conditions where the pesticide paradox left coverage stale.
- `/qa:maintenance-test` — for impact analysis / maintenance testing of the product itself after a change.
