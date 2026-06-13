---
description: Deep-dive a web UI to discover all interactive elements — extract stable locators and actions into Page Object files, then generate test cases covering every element, action, and flow. Use to bootstrap or expand UI automation from a running app.
argument-hint: "<url or page/flow> [auth role]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Deep-dive UI scan → page objects → test cases: $ARGUMENTS

**ISTQB process:** Test analysis & design (CTFL v4.0 §1.4, §4) using the **running UI as test basis**, implemented with the **Page Object Model** (CT-TAE — Specialist; verify exact clauses against the current syllabus). Output work products (ISO/IEC/IEEE 29119-3): a **Test Procedure Specification** (page objects + executable specs) and a **Test Case Specification** (the discovered conditions/cases doc).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Existing UI assets
```!
echo "--- base url (stack.base_url_web) ---"; grep base_url_web qa.config.yml 2>/dev/null
echo "--- paths (paths.tests_dir / paths.docs_dir) ---"; grep -E "tests_dir|docs_dir" qa.config.yml 2>/dev/null
echo "--- e2e tooling (tooling.e2e) ---"; grep -E "^\s*e2e:" qa.config.yml 2>/dev/null
echo "--- e2e framework config + pages dir ---"; ls -1 playwright.config.* 2>/dev/null; ls -1R tests 2>/dev/null | head -30
```

## Your task

**Config-read guard.** If `qa.config.yml` is MISSING above, stop and route the user to `/qa:qa-init` — do not hardcode paths or tools. All output paths come from `<paths.*>`, the E2E framework from `<tooling.e2e>`/`<tooling.language>`, the target base from `<stack.base_url_web>`; never hardcode `tests/`, `playwright.config`, `npx playwright`, or `playwright-report`. If no E2E framework config was found above, suggest `/qa:scaffold` (or `/qa:tool-select` to choose one) before continuing, and confirm the app is reachable.

**Resolve the target.** Parse `$ARGUMENTS`:
- **Empty `$ARGUMENTS`** → do not guess. Ask the user for a URL or page/flow name. If they cannot specify one, default to the first area in `risk_areas.critical` and resolve it against `<stack.base_url_web>`; state which default you applied.
- A **full URL** → use it directly (must be within `<stack.base_url_web>` scope; refuse off-origin crawling).
- A **page/flow name** → resolve against `<stack.base_url_web>`.
- A trailing **auth role** token → drive the saved `storageState` for that role; otherwise run unauthenticated.

### 1. Explore the UI (discover elements)
Write and run a temporary `<tooling.e2e>` **exploration script** (under `<paths.tests_dir>/_scan/`) that navigates to the target and extracts every **interactive element**. For each element capture: tag/type, accessible **role**, accessible **name/label**, `data-testid`, placeholder/text, input type, enabled/required state, and the section it belongs to. Use role-based queries (`getByRole`), the accessibility snapshot, and DOM queries. Within scope, follow in-app links to reachable pages of the same flow — **bounded**: stay on `<stack.base_url_web>` origin, and cap at **10 pages per run** unless the user raises the limit; never crawl off-origin. Handle auth via the role's `storageState` when an auth role was given. Record dynamic/conditional elements and note auth-gated areas.

### 2. Derive stable locators + actions
For each element choose the **most stable locator** (priority: `data-testid` → `getByRole`+name → `getByLabel` → `getByText`/placeholder; avoid CSS/XPath coupled to styling). Infer the **action(s)**: click (buttons/links), fill (text inputs), select (dropdowns), check/toggle, upload, hover, etc. Where `data-testid` is missing on important controls, list them as a recommended `data-testid` contract for devs.

### 3. Generate / extend Page Object files
Write Page Object classes under `<paths.tests_dir>/pages/` (one per page/component): locators as properties + typed **action methods** (e.g. `fillEmail(v)`, `submit()`, `gotoX()`). Keep **assertions OUT of page objects** — they live in the specs (SRP, CT-TAE). Grep/Glob first and **reuse/extend existing POMs** rather than duplicating; follow the repo's conventions and `<tooling.language>`.

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
- **Page objects** under `<paths.tests_dir>/pages/` (29119-3 Test Procedure Specification — the page-object layer).
- **Test cases**: the **Test Case Specification** doc at `<paths.docs_dir>/UI-SCAN-<target>.md`, and runnable `<tooling.e2e>` specs under `<paths.tests_dir>/e2e/` (stable role/test-id selectors, web-first assertions, no hard waits, data via `test_data.*` factories) — the 29119-3 Test Procedure Specification.
- A **coverage summary** (measurable, not prose): elements discovered, page objects created/updated, test conditions derived, cases generated by priority, and any elements left **uncovered with reason**. Assert the invariant "every interactive element has ≥1 case" or list the exceptions.
- **Remove the temporary `<paths.tests_dir>/_scan/` probe** before finishing.

Run the generated smoke specs (`<tooling.e2e>` runner) to confirm they execute. Then hand off:
- `/qa:web-automate` to deepen full user journeys into the suite,
- `/qa:test-cases` to set/confirm any **TODO** expected results against requirements,
- `/qa:self-heal` to keep locators current as the UI evolves.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — framework from `<tooling.e2e>`/`<tooling.language>`, target from `<stack.base_url_web>`, page objects/specs under `<paths.tests_dir>`, the cases doc under `<paths.docs_dir>`, data per `test_data.*`; nothing hardcoded (`tests/`, `npx playwright`, `playwright-report` never appear).
- [ ] **Traceability intact** — the chain test basis (running UI) -> condition -> case -> coverage item -> procedure (page object/spec) is preserved and bidirectional; every interactive element maps to ≥1 case and every case maps back to an element/locator; no orphans.
- [ ] **Measurable** — output states counts (elements discovered, conditions, cases by priority, % element coverage) rather than prose claims.
- [ ] **Oracle honesty / residual risk stated** — expected results not derivable from the UI alone are marked **TODO: confirm with requirements**, not asserted; name what is NOT covered (auth-gated areas, dynamic states, off-origin links) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work products (**Test Procedure Specification** = page objects + specs under `<paths.tests_dir>`; **Test Case Specification** = cases doc under `<paths.docs_dir>`); the temporary `_scan/` probe was removed.
