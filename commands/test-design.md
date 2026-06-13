---
description: Derive test conditions and test cases from the test basis using ISTQB test design techniques (EP, BVA, decision table, state transition, ATDD). Produces an ISO/IEC/IEEE 29119-3 Test Design + Test Case Specification. Use to design test cases for a feature, story, or endpoint.
argument-hint: "<feature / story / endpoint>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ISTQB test analysis & design for: $ARGUMENTS

**ISTQB process activities:** Test analysis + Test design (CTFL v4.0 §1.4, §4; black-box design techniques per CTAL-TA where Advanced).
**Work products:** ISO/IEC/IEEE 29119-3 **Test Design Specification** (test conditions) + **Test Case Specification** (test cases). Use the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md`.

> For focused **test case generation** from a single requirement/story/endpoint (with the full Test Case Specification + CSV export), use `/qa:test-cases`. To model stateful flows use `/qa:mbt`. Use this command for broader design context across a feature.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Step 0 — Read config & validate input (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed with documented defaults (do not invent paths/tools — use the `<paths.*>`/`<stack.*>`/`<tooling.*>` values the user confirms).
2. Resolve the design target from `$ARGUMENTS`:
   - **If `$ARGUMENTS` is non-empty:** that is the feature/story/endpoint to design for.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user for the feature/story/endpoint. If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** and state explicitly that you defaulted there and why.
3. Confirm the resolved target and the config-derived inputs in scope before designing: `<stack.api_spec_path>` (test basis for endpoints), `<paths.docs_dir>` (output location), `risk_areas` (prioritization), enabled `<tooling.*>` (informs feasible levels/types). Nothing about paths or tools is hardcoded; everything comes from config.

## Your task

Run the following steps in order. Do not skip a step; if a step is not applicable, say so explicitly and why.

### 1. Test analysis — derive test conditions (what to test)

1. Read the **test basis** for the target: the user story + acceptance criteria, and the OpenAPI spec at `<stack.api_spec_path>` for the relevant endpoints (request/response schemas, status codes, constraints).
2. Identify and list **test conditions** — one per testable aspect: each function, business rule, input field, state, error/negative path, and relevant non-functional aspect (per ISO/IEC 25010).
3. Tag each condition with a **risk level** (Critical/High/Med/Low) using `risk_areas`.
4. Flag any ambiguity, gap, contradiction, or untestable wording in the basis as a **static-testing finding** and suggest `/qa:static-review` (Principle 3, shift-left).

### 2. Test design — derive test cases (how to test)

For each test condition, derive **test cases** using the appropriate technique and record, per case, **which technique** and **which coverage item(s)** it exercises. Apply the **CTFL v4.0 Chapter 4** categorization strictly:

- **Black-box (§4.2):**
  - **Equivalence Partitioning** — at least one case per partition; cover **valid AND invalid** partitions, one representative each.
  - **Boundary Value Analysis** — state which form you use: **2-value** (boundary + adjacent: min, min−1) or **3-value** (min−1, min, min+1). Do not mix forms silently; one case per boundary value selected.
  - **Decision Table** — exactly **one case per rule/column** (cover every rule).
  - **State Transition** — cover **all states**, **all valid transitions (0-switch)**, and representative **invalid transitions**; state which coverage criterion you achieved.
- **White-box (§4.3):** Statement and Branch testing/coverage — only when source is in scope; route structural measurement to `/qa:coverage-measure`.
- **Experience-based (§4.4):** Error Guessing, Exploratory, Checklist-Based — for risk areas and basis gaps; route deeper exploration to `/qa:exploratory`.
- **Collaboration-based (§4.5):** ATDD — acceptance-criteria cases as Given/When/Then.
- **Advanced (CTAL-TA, NOT CTFL v4.0 — label explicitly as Advanced if used):** domain analysis (combine partitions/boundaries across related inputs), defect-based (taxonomy-driven), use-case testing, and pairwise/classification tree (route to `/qa:combinatorial`). Never attribute these to Foundation.

### 3. Classify & prioritize each case

1. Set each case's **test level** (component / component integration / system / system integration / acceptance) and **test type** (functional / non-functional, naming the ISO/IEC 25010 characteristic for non-functional cases).
2. Set **priority** (P1/P2/P3) from the feature's **risk level** (`risk_areas`).
3. Set **detail** risk-based: Critical/High → low-level (concrete data + steps); Med/Low → high-level (logical, data deferred).

### 4. Maintain traceability

Preserve the bidirectional chain **test basis → test condition → test case → coverage item** (CTFL §1.4.4). Every condition has ≥1 case; no orphan cases; every case traces back to a condition and to a basis reference.

### 5. Output

Produce, following the schema in `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md`:

1. **Test Design Specification** — the test-conditions table (TCond ID | condition | traces to | risk).
2. **Test Case Specification** — the case table: `TC ID | title | traces to | level | type | technique | coverage item(s) | priority | detail | preconditions | Given/When/Then | expected result`.
3. **Coverage Summary (with counts)** — state, as numbers not prose:
   - Total **test conditions**, and total **test cases**.
   - Cases **by priority** (P1/P2/P3), **by level**, **by type**.
   - **Techniques applied** and where; **EP** partitions covered (valid + invalid counts), **BVA** form used + boundary values count, **decision-table** rules covered / total rules, **state transitions** covered (states, valid, invalid).

Write the output to `<paths.docs_dir>/TEST-DESIGN-<item>.md` (or append to the relevant Test Plan if one exists). Then run the Quality gate and Self-check below.

## Quality gate (every case must satisfy)

Reject and revise any case that fails these. Confirm all pass before finalizing:

- [ ] **Atomic** — each case verifies one thing; a failure points to one cause.
- [ ] **Independent** — runnable without depending on another case's side effects (or its preconditions are explicit).
- [ ] **Verifiable** — has a concrete, observable expected result (a deterministic oracle), not "works as expected".
- [ ] **Complete coverage** — every equivalence **partition** (valid + invalid), every selected **boundary** value, every decision-table **rule**, and every **state/transition** in scope has ≥1 case; gaps are stated as residual risk.
- [ ] **Technique + coverage item recorded** — each case names its CTFL v4.0 technique and the exact coverage item it exercises; Advanced techniques are labeled CTAL-TA.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`, `stack.api_spec_path`, `risk_areas`, enabled `tooling.*`) is honored; no path or tool is hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item (-> procedure -> result -> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — the Coverage Summary states counts/coverage (N conditions, M cases by priority/level/type, partitions/boundaries/rules/transitions covered) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Design Specification + Test Case Specification** and written to the correct `<paths.docs_dir>` location.

## Handoff

Offer to implement the highest-priority (P1) cases via `/qa:implement` (turns cases into test procedures/scripts). Do **not** write automation here — this command is analysis & design only. For combinatorial explosion route to `/qa:combinatorial`; for basis defects route to `/qa:static-review`.
