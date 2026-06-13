---
description: Quickly add a single focused test case from a plain-English description. Use for one-off "add a test that ..." requests. Selects the ISTQB design technique, then implements and runs one test procedure.
argument-hint: "<what the test should verify>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Add a test: $ARGUMENTS

**ISTQB process:** Test design + implementation (CTFL v4.0 §1.4, §4) — select a design technique for one test condition, then implement and run the resulting test procedure. For a full suite from a requirement use `/qa:test-cases` (design) or `/qa:implement` (multi-level implementation); this command is the single-case fast path.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Existing framework
```!
echo "--- tests tree (root from paths.tests_dir) ---"; ls -1R tests 2>/dev/null | head -60
echo "--- e2e config? ---"; ls -1 playwright.config.* vitest.config.* jest.config.* 2>/dev/null
```

## Your task

Add **one** focused test for the condition described in `$ARGUMENTS`.

**If `$ARGUMENTS` is empty:** ask the user what behavior to verify. If they cannot supply one, default the test condition to the first item in `risk_areas.critical` from `qa.config.yml` and state that you are doing so. If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init` first; if no test framework is present (no config above), suggest `/qa:scaffold` first.

Treat `$ARGUMENTS` as the **test basis** for one **test condition**. Work the ISTQB chain explicitly: **basis → condition → technique → case → coverage item**.

### 1. Pick the test level (apply this rule)
Choose the cheapest effective level for what is being verified — do not E2E what a lower level proves:
- Pure logic / a single function → **unit** (`<tooling.unit>`); if outside your layer, note it for devs.
- A single endpoint's behavior → **API test** (`<tooling.api>`); read the relevant operation in `<stack.api_spec_path>` if present.
- One UI behavior in isolation → **component** (`<tooling.component>`) when available.
- A genuine end-to-end user journey only → **E2E** (`<tooling.e2e>`).
- Interface stability between components → **contract** (`<tooling.contract>`) if enabled.

### 2. Select the ISTQB technique (decision tree — choose ONE, record it)
Classify the condition and pick the matching CTFL v4.0 Chapter 4 technique. Stay strictly within the v4.0 categorization (do not tag Advanced techniques as Foundation):

| If the condition is about… | Technique (CTFL v4.0) | Coverage item to target |
|---|---|---|
| an input/output split into classes processed the same way | **Equivalence Partitioning (§4.2)** — one representative per partition, valid **and** invalid | the chosen partition (valid or invalid) |
| the edges of an ordered partition (limits, min/max, lengths) | **Boundary Value Analysis (§4.2)** — state **2-value** (boundary + nearest neighbour) or **3-value** (boundary ± 1) | the boundary value tested |
| a combination of conditions producing different actions (business rule / authorization) | **Decision Table testing (§4.2)** — one case per rule (column) | the decision-table rule exercised |
| stateful behavior (order/session/payment/account state) | **State Transition testing (§4.2)** — state coverage: all-states / a valid transition (0-switch) / an invalid transition | the transition exercised |
| a likely-defect or edge case from experience (empty/null, oversized, special chars, duplicates, interrupted flow, permissions) | **Error Guessing / Checklist-Based (§4.4)** | the guessed defect scenario |
| code-structure coverage of a unit | **Statement / Branch testing (§4.3)** — unit level only | the statement/branch covered |

If the condition spans several of these, this is no longer a single-case request — design the set with `/qa:test-cases` instead and return. State the technique you picked and why in one line before writing.

### 3. Place the test
1. Search the framework under `<paths.tests_dir>` (Grep/Glob) for an existing spec covering the same feature/level.
2. Add the case to that file if one fits; only create a new file (consistent with the repo's naming/structure) if none does.
3. Reuse existing fixtures, page objects, and typed API clients — extend, never duplicate.

### 4. Write the test (conventions — non-negotiable)
- Stable selectors (`getByRole` / `getByLabel` / `data-testid`), web-first assertions, **no hard waits**.
- The test **owns its data** via factories (`test_data.strategy`); synthetic data only — never real PII (`test_data.sensitive_data_rule`).
- One objective per test (atomic), independent of other tests' order/state, with a clear verifiable expected result (the Then).
- Add a trace comment linking the test back to its condition/basis so traceability survives in the testware.

### 5. Run and confirm
Run **just this test** at the chosen level (e.g. the `<tooling.e2e>` / `<tooling.unit>` runner for the file you touched) and confirm it passes.
- If it fails because the test is wrong → fix the test.
- If it fails because the product is wrong → that is a real defect; do not mask it. Report the expected-vs-actual and hand off to `/qa:triage` to log a defect report.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — level/tooling came from `<tooling.*>`, the file lives under `<paths.tests_dir>`, data follows `test_data.*`; nothing hardcoded.
- [ ] **Technique recorded** — exactly one CTFL v4.0 technique is named for the case, attributed to the correct category (no Advanced technique mislabeled as Foundation; BVA states 2-value vs 3-value).
- [ ] **Traceability intact** — the chain test basis → condition → case → coverage item → procedure → result (→ defect) is preserved and bidirectional; the test carries a trace back to its condition; no orphan.
- [ ] **Measurable** — the summary states the level, technique, coverage item, and pass/fail result, not a prose claim.
- [ ] **Residual risk stated** — name what this single case does NOT cover (ISTQB Principle 1: testing shows the presence, not the absence, of defects); point to `/qa:test-cases` for fuller coverage if warranted.
- [ ] **Work product named** — output is a **Test Procedure / script** (ISO/IEC/IEEE 29119-3 Test Procedure Specification) added under `<paths.tests_dir>`.

End with a one-line summary: level + technique + coverage item, the file touched, pass/fail, and what remains uncovered (and whether to expand via `/qa:test-cases`).
