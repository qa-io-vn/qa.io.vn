---
description: Generate ISTQB test cases from a requirement, user story, acceptance criteria, OpenAPI endpoint, or a file. Use whenever the user wants to create or derive test cases. Applies ISTQB design techniques and outputs a Test Case Specification.
argument-hint: "<requirement text | story | endpoint | path/to/file>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Create test cases from: $ARGUMENTS

**ISTQB process:** Test analysis → Test design (CTFL v4.0 §1.4, §4). Output = ISO/IEC/IEEE 29119-3 **Test Case Specification**. This is the dedicated case-generation command; for full design context use `/qa:test-design`, and to model stateful flows use `/qa:mbt`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Resolve the test basis (input)
```!
ARG="$ARGUMENTS"
if [ -z "$ARG" ]; then echo "NO INPUT — ask the user for a requirement, story, endpoint, or file."; \
elif [ -f "$ARG" ]; then echo "--- file: $ARG ---"; cat "$ARG"; \
else echo "--- inline requirement / story / endpoint ---"; echo "$ARG"; fi
echo "--- OpenAPI spec (for endpoint inputs) ---"; sed -n '1,80p' openapi.yaml openapi.json swagger.* 2>/dev/null | head -80
```

## Your task

The **test basis** is whatever was passed in `$ARGUMENTS` — pasted requirement text, a user story / acceptance criteria, an API endpoint (look it up in the OpenAPI spec), or a file path (read above).

**If `$ARGUMENTS` is empty:** ask the user for a requirement, story, endpoint, or file. If they cannot supply one, default the test basis to the first item in `risk_areas.critical` from `qa.config.yml` and state that you are doing so. If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init` first.

Work strictly through the ISTQB analysis→design flow. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md` for the exact output structure and fields.

### 1. Test analysis — derive test conditions
Read the test basis and list **test conditions** (what to test): each function, rule, input, state, error path, and relevant non-functional aspect. Flag any ambiguity, gap, or untestable wording as a basis issue (suggest `/qa:static-review`). Tag each condition with a **risk level** using `risk_areas`.

### 2. Technique selection — pick the right ISTQB technique per condition
Use the **CTFL v4.0 Chapter 4** techniques and record which one each case uses. Stay strictly within the v4.0 categorization:

**Black-box test techniques (CTFL v4.0 §4.2) — the four, for requirement-derived cases:**
- **Equivalence Partitioning (EP)** — partition each input/output into classes processed the same way; design at least one case per partition, covering **valid and invalid** partitions. One representative value per partition.
- **Boundary Value Analysis (BVA)** — exercise the boundaries of ordered equivalence partitions. State which form you use:
  - **2-value BVA** — the boundary value and its nearest neighbour in the adjacent partition (e.g. for 1..10: {0,1} and {10,11}).
  - **3-value BVA** — the boundary and the values on both sides (e.g. {0,1,2} and {9,10,11}).
- **Decision Table Testing** — for combinations of conditions and their resulting actions (ideal for business rules and authorization); derive at least one case per decision-table **rule (column)**.
- **State Transition Testing** — for stateful behaviour (order/session/payment/account states). State the coverage targeted: **all states**, **all valid transitions (0-switch)**, or include **invalid transitions**. Cover valid and, per risk, invalid transitions.

**White-box test techniques (CTFL v4.0 §4.3)** — only when source code is in scope: **Statement testing/coverage** and **Branch testing/coverage**. Requirement-derived cases are usually black-box; note structural-coverage needs and defer to `/qa:coverage-measure`.

**Experience-based test techniques (CTFL v4.0 §4.4)** — to find what formal techniques miss: **Error Guessing**, **Exploratory testing** (see `/qa:exploratory`), and **Checklist-Based testing** (empty/null, oversized input, special characters, duplicates, concurrency, interrupted flows, permissions).

**Collaboration-based approaches (CTFL v4.0 §4.5)** — express acceptance-criteria cases via **ATDD** in Given/When/Then (see `/qa:acceptance`).

> **Advanced techniques (NOT CTFL v4.0 — CTAL Test Analyst):** pairwise/combinatorial (classification tree) and use-case testing. Use them only when genuinely needed (e.g. many combining parameters) and label them explicitly as Advanced, not Foundation, so the technique attribution stays accurate.

### 3. Test design — write the cases
For each condition, generate cases covering: **positive (happy path), negative, boundary, error handling, and authorization** as applicable. For each case fill all template fields: ID, title, traces-to (condition + requirement), level, type, technique, **coverage item**, priority, detail, preconditions, test data, steps (Given/When), expected result (Then).

**Priority — map each case's risk tier to a priority (apply this rule exactly):**
Match each condition's `risk_areas` tier (from step 1) to a priority band:

| `risk_areas` tier | Priority |
|---|---|
| `critical` | **P1** |
| `high` | **P1–P2** (P1 for the primary/positive path, P2 for secondary negatives) |
| `medium` | **P2–P3** |
| `low` | **P3** |

A condition that does not match any configured `risk_areas` tier defaults to **medium → P2–P3**; note it as unclassified so the user can confirm the tier.

**Detail level — risk-based mix (per the answers baked into this toolkit):**
- **Critical / High** risk → **low-level (concrete)**: exact preconditions, specific test data, step-by-step actions, exact expected results — directly executable/automatable.
- **Medium / Low** risk → **high-level (logical)**: state the condition and expected behavior; defer concrete data to execution.

### 4. Quality checks (apply before finalizing)
- Each case is **atomic** (one objective), **independent** (no reliance on another case's state/order), and has a **clear, verifiable expected result**.
- **Coverage:** every input has valid + invalid partitions (EP); each ordered partition's boundaries are tested per the chosen BVA form (2-value or 3-value); every business rule has a decision-table row; every state has its valid + (per risk) invalid transitions; negative and authorization paths exist for risky areas.
- **Traceability:** every requirement/condition maps to ≥1 case; no orphan cases. Use synthetic data only — never real PII.
- **Priorities** follow the `risk_areas`→priority mapping in step 3 (critical→P1, high→P1–P2, medium→P2–P3, low→P3); no case is left without a priority.

### 5. Self-check (run before writing the output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.docs_dir` is the write target, every condition's tier comes from `qa.config.yml` `risk_areas`, and any `tooling.*`/`stack.*` discovery used was config-driven; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis → condition → case → coverage item is preserved and bidirectional; every condition has ≥1 case and every case traces back to a condition + requirement; no orphans.
- [ ] **Measurable** — the coverage summary states counts (N conditions, M cases by priority/level/type) and coverage achieved, not prose claims.
- [ ] **Priorities mapped** — every case carries a priority derived from the step-3 `risk_areas`→priority rule; unclassified conditions are flagged.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as an ISO/IEC/IEEE 29119-3 **Test Case Specification** and written to the correct `<paths.docs_dir>` location.

### 6. Output
Write a **Test Case Specification** (ISO/IEC/IEEE 29119-3 work product) to `<paths.docs_dir>/TEST-CASES-<item>.md` using the template: test-conditions table, the test-case table, and a **coverage summary** (techniques applied, coverage achieved, counts by priority/level/type, traceability confirmation).

Also offer (don't auto-create unless asked):
- a **generic CSV** export (`TEST-CASES-<item>.csv`, tool-neutral columns: ID, Title, Traces, Level, Type, Technique, Priority, Preconditions, Test Data, Steps, Expected) for importing into a test management tool, and
- handing the P1 cases to `/qa:implement` to turn them into automated test procedures/scripts.

End with a one-line summary: N conditions → M cases (by priority), techniques used, basis gaps found, and the residual risk (what is not covered and why).
