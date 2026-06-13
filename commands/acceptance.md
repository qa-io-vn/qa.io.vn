---
description: Author acceptance criteria and acceptance tests collaboratively using ATDD/BDD (Given/When/Then), and trace each criterion to a scenario. Produces an ISO/IEC/IEEE 29119-3 Test Case Specification (acceptance level). Use to turn a user story into agreed, testable acceptance tests before development.
argument-hint: "<user story or feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Acceptance test design (ATDD/BDD): $ARGUMENTS

**ISTQB process activities:**
- **Collaboration-based test design — ATDD** (CTFL v4.0 §4.5: collaborative user-story writing, writing acceptance criteria, ATDD). This is the *design technique* used to derive the Given/When/Then scenarios.
- **Acceptance testing as a test level** (CTFL v4.0 §2.2) — the forms of acceptance testing (UAT, operational acceptance, contractual/regulatory, alpha/beta) belong to the **Acceptance Testing specialist syllabus (CT-AcT)**, not to CTFL §4.5. Keep the ATDD technique and the acceptance-testing forms distinct; do not tag the CT-AcT forms as Foundation §4.5.

**Work product (ISO/IEC/IEEE 29119-3):** a **Test Case Specification** at the acceptance level — the acceptance criteria (test conditions) plus their Gherkin scenarios (test cases). Follow the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md` where applicable. These scenarios are the story's Definition of "done".

> For broader test-condition/test-case design across a feature (EP, BVA, decision table, state transition), use `/qa:test-design`. To turn agreed scenarios into executable procedures/scripts, hand off to `/qa:implement`. For basis defects (ambiguous/contradictory criteria) route to `/qa:static-review`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Step 0 — Read config & validate input (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed with documented defaults — do **not** invent paths/tools; use only the `<paths.*>`/`<stack.*>`/`<tooling.*>` values the user confirms.
2. Resolve the story/feature from `$ARGUMENTS`:
   - **If `$ARGUMENTS` is non-empty:** that is the story/feature to write acceptance tests for.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user for the user story (title + narrative + any draft criteria). If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** and state explicitly that you defaulted there and why.
3. Confirm the resolved target and the config-derived inputs in scope before writing: `<paths.docs_dir>` (output location), `risk_areas` (which forms/paths to prioritize), enabled `<tooling.*>` (which level each scenario runs at — e.g. `<tooling.e2e>` for UI flows, `<tooling.api>` for service-level criteria; treat a value of `none` as "that level is out of scope"), and `<stack.api_spec_path>` when a criterion maps to an API endpoint. Nothing about paths or tools is hardcoded; everything comes from config.

## Your task

Run the following steps in order. If a step is not applicable to this story, say so explicitly and why.

### 1. Three Amigos perspective (shift-left, CTFL Principle 3)

Consider the business, development, and testing views to surface assumptions, ambiguities, and edge cases **before** coding. List any ambiguity, contradiction, missing rule, or untestable wording as a **static-testing finding** and route it to `/qa:static-review` rather than silently resolving it.

### 2. Write acceptance criteria (the test conditions)

Write each acceptance criterion so it is **specific, measurable, and verifiable** (a deterministic oracle — not "works as expected"). Assign each criterion an ID (`AC-1`, `AC-2`, …) and a **risk level** (Critical/High/Med/Low) from `risk_areas`. Each criterion is a **test condition** for this story.

### 3. Express acceptance tests in Gherkin (the test cases)

For each criterion, write one or more **Given/When/Then** scenarios. Rules:
1. **One observable outcome per scenario** — a failure points to one cause. Keep them business-readable.
2. **Cover, per criterion:** the happy path; at least one alternative/negative path; boundary conditions where a value range applies; and authorization/permission paths where access control is relevant.
3. **Use `Scenario Outline` + `Examples`** when the same When/Then holds across a data set (boundaries, partitions), instead of duplicating scenarios.
4. Give each scenario an ID (`SC-1.1`, `SC-1.2`, …) keyed to its criterion.

### 4. Classify each scenario for automation

For each scenario set:
1. **Test level** — acceptance; and the execution level it will run at (system/E2E vs component-integration/API), chosen from enabled `<tooling.*>`.
2. **Acceptance-testing form (CT-AcT)** — tag which form(s) the criterion validates: **UAT** (user needs), **operational acceptance** (backup/restore, security, maintenance, capacity), **contractual/regulatory**, **alpha/beta** — include only those relevant to this story; omit the rest and say so. Do not label these forms as CTFL §4.5.
3. **Priority** (P1/P2/P3) from the criterion's risk level.

### 5. Maintain traceability

Preserve the bidirectional chain **acceptance criterion (test condition) → scenario (test case) → execution level → (later) procedure/result**. Every criterion has ≥1 scenario; no orphan scenarios; every scenario traces back to exactly one criterion and to the story.

### 6. Output

Produce, at the acceptance level:
1. **Acceptance criteria table** — `AC ID | criterion | risk | acceptance form(s)`.
2. **Scenario specification** — per scenario: `SC ID | traces to AC | level | priority | Given/When/Then (or Scenario Outline + Examples)`.
3. **Coverage Summary (with counts)** — state, as numbers not prose: total criteria; total scenarios; scenarios **by priority** (P1/P2/P3) and **by execution level**; criteria covered by happy/negative/boundary/authorization paths; and acceptance forms exercised.

Write the output to `<paths.docs_dir>/ACCEPTANCE-<story>.md` (or append to the Test Plan's cases section if one exists). If the project uses a BDD runner (declared in `<tooling.*>`), format the Gherkin for that runner; otherwise keep it as the spec that `/qa:implement` turns into procedures/scripts at the configured `<tooling.e2e>`/`<tooling.api>` level. Then run the Self-check below.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`, `risk_areas`, enabled `tooling.*`, `stack.api_spec_path` where used) is honored; no path or tool (no specific runner) is hardcoded.
- [ ] **Traceability intact** — the chain acceptance criterion -> scenario -> execution level (-> procedure -> result) is preserved and bidirectional; every criterion has ≥1 scenario and no scenario is an orphan.
- [ ] **Measurable** — the Coverage Summary states counts/coverage (N criteria, M scenarios by priority/level, path types and acceptance forms covered) rather than prose claims.
- [ ] **Standards separated** — ATDD is cited as the CTFL v4.0 §4.5 collaboration-based technique; the acceptance-testing forms (UAT/operational/contractual/alpha-beta) are attributed to CT-AcT, not to §4.5. Any reference not traceable to the toolkit's compliance docs is softened to "verify against the current syllabus".
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Case Specification (acceptance level)** and written to the correct `<paths.docs_dir>` location.

## Handoff

Offer to implement the highest-priority (P1) scenarios via `/qa:implement` (turns Given/When/Then into test procedures/scripts at the configured level). Do **not** write automation here — this command is acceptance design only. For broader feature design route to `/qa:test-design`; for ambiguous/contradictory criteria route to `/qa:static-review`.
