---
description: Deep-dive a web UI to discover all interactive elements — extract stable locators and actions into Page Object files, then generate test cases covering every element, action, and flow. Use to bootstrap or expand UI automation from a running app.
argument-hint: "<url or page/flow> [auth role]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Deep-dive UI scan → page objects → test cases: $ARGUMENTS

**ISTQB process:** Test analysis & design using the **running UI as test basis** (CTFL §1.4, §4) + Page Object Model (CT-TAE). Output: page objects + a covering test suite.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Existing UI assets
```!
echo "--- base url ---"; grep base_url_web qa.config.yml 2>/dev/null
echo "--- pages dir ---"; ls -1 tests/pages 2>/dev/null
echo "--- playwright installed? ---"; ls -1 playwright.config.* 2>/dev/null; npx playwright --version 2>/dev/null || echo "run /qa:scaffold first if missing"
```

## Your task

Target from `$ARGUMENTS` — a URL, or a page/flow name resolved against `stack.base_url_web`. An optional auth role uses the saved `storageState`. Requires the Playwright framework (`/qa:scaffold` if missing) and the app reachable.

### 1. Explore the UI (discover elements)
Write and run a Playwright **exploration script** (under `tests/_scan/`) that navigates to the target and extracts every **interactive element**. For each element capture: tag/type, accessible **role**, accessible **name/label**, `data-testid`, placeholder/text, input type, enabled/required state, and the section it belongs to. Use `page.getByRole`, the accessibility snapshot, and DOM queries. Within scope, follow in-app links to reachable pages of the same flow (bounded — don't crawl the whole internet; stay on `base_url_web`, respect a sensible page limit). Handle auth via `storageState` for the given role. Record dynamic/conditional elements and note auth-gated areas.

### 2. Derive stable locators + actions
For each element choose the **most stable locator** (priority: `data-testid` → `getByRole`+name → `getByLabel` → `getByText`/placeholder; avoid CSS/XPath coupled to styling). Infer the **action(s)**: click (buttons/links), fill (text inputs), select (dropdowns), check/toggle, upload, hover, etc. Where `data-testid` is missing on important controls, list them as a recommended `data-testid` contract for devs.

### 3. Generate / extend Page Object files
Write Page Object classes under `tests/pages/` (one per page/component): locators as properties + typed **action methods** (e.g. `fillEmail(v)`, `submit()`, `gotoX()`). Keep assertions OUT of page objects. Reuse/extend existing POMs rather than duplicating; follow the repo's conventions.

### 4. Generate test cases to cover all of it
Derive **test conditions** from the discovered elements/flows, then generate test cases (use the `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md` structure) covering:
- **Presence & state** — each element renders, correct enabled/disabled/required state.
- **Actions** — each action works and produces the expected result/navigation.
- **Input validation** — for fields, EP/BVA: valid + invalid + boundary (empty, too long, wrong format).
- **Navigation flows** — links/buttons reach the right destination.
- **Negative/error paths** — submit invalid forms, required-field errors.
Map each case to its element/locator for traceability and coverage ("every interactive element has ≥1 case").

> Oracle caveat (ISTQB): the scanner knows *what* exists and *how* to drive it, but not always the *correct business outcome*. For each action, set the expected result from the requirements/acceptance criteria where known; where the intended behavior isn't derivable from the UI alone, mark the expected result **TODO: confirm with requirements** rather than asserting something trivial. Flag these for human/`/qa:test-cases` follow-up so tests verify real behavior, not just "element is clickable."

### 5. Output & wire up
- Page objects under `tests/pages/`.
- Test cases: spec doc at `<paths.docs_dir>/UI-SCAN-<target>.md` and/or runnable Playwright specs under `tests/e2e/` (stable selectors, web-first assertions, no hard waits, data via factories).
- A **coverage summary**: elements discovered, page objects created/updated, cases generated, and any elements left uncovered (with reason). Remove the temporary `tests/_scan/` probe.

Run the generated smoke specs to confirm they execute, then suggest `/qa:web-automate` to deepen journeys and `/qa:self-heal` to keep locators current.
