---
description: Apply Model-Based Testing — build a behavioral model (state machine / state-transition table) and derive test cases from it to a stated coverage criterion (all-states / all-transitions / 0-switch). Produces an ISO/IEC/IEEE 29119-3 Test Design Specification. Use for complex stateful flows where model coverage beats ad-hoc cases.
argument-hint: "<feature / stateful flow>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Model-Based Testing: $ARGUMENTS

**ISTQB process:** Model-Based Testing (CT-MBT Specialist). The model and its coverage criteria are the **state-transition** technique from CTFL v4.0 §4.2 (black-box), applied via an explicit behavioral model.
**Work product:** ISO/IEC/IEEE 29119-3 **Test Design Specification** (the model is the design basis; derived cases form the Test Case Specification). No dedicated template — reuse the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md` for the derived cases.

> For non-stateful design (EP/BVA/decision-table) use `/qa:test-design`; for single-item case generation use `/qa:test-cases`. This command is for stateful flows modeled as state machines.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Step 0 — Read config & validate input (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed with documented defaults — do **not** invent paths/tools; use the `<paths.*>`/`<stack.*>`/`<tooling.*>` values the user confirms.
2. Resolve the target stateful flow from `$ARGUMENTS` (e.g. order lifecycle, payment/3DS, session, subscription states):
   - **If `$ARGUMENTS` is non-empty:** that is the flow to model.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user for the stateful flow. If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** and state explicitly that you defaulted there and why.
3. Confirm the resolved target and the config-derived inputs in scope before modeling: the test basis (user story / requirement / `<stack.api_spec_path>` for stateful endpoints), `<paths.docs_dir>` (output location), and `risk_areas` (drives which coverage criterion to target). Nothing about paths or tools is hardcoded.

## Your task

Run the following steps in order. Do not skip a step; if a step is not applicable, say so explicitly and why.

### 1. Build the model

1. Capture the behavior as a **state-transition model** from the test basis. Define explicitly: the set of **states**, the **events/inputs**, the **transitions** (source state + event → target state), and any **guards/conditions** and **actions/outputs**.
2. Mark the **initial state** and any **final state(s)**.
3. Represent the model in **both** a transition table (`Source state | Event | Guard | Target state | Action/output`) **and** a Mermaid `stateDiagram-v2`, so it is auditable and maintainable.

### 2. Choose the coverage criterion (state which, and why)

Select exactly one target and justify it from `risk_areas`:

- **all-states** — every state is reached at least once (weakest; use only for Low-risk flows).
- **all-transitions (0-switch)** — every valid transition is exercised at least once (default; required for Critical/High-risk flows).
- **all transition-pairs (1-switch)** — every pair of consecutive transitions (use for Critical flows where sequence-dependent defects are plausible).
- **all-paths to a stated bound** — only when explicitly justified; state the bound to avoid path explosion.

Decision rule: if `risk_areas` ranks the flow **Critical/High**, target at least **all-transitions (0-switch)**; for **Med/Low** flows, **all-states** is acceptable. State the chosen criterion explicitly.

### 3. Generate test cases from the model

1. Derive cases to meet the chosen criterion. Each case records: the **path** (ordered states), the **events** triggering each transition, the **guards** satisfied, the **expected state/output** after each step, and **which coverage item(s)** (states/transitions) it contributes.
2. Include **invalid transitions** (negative testing): for representative (state, event) pairs that have no defined transition, the case asserts the event is rejected and the state is unchanged.
3. Number the cases and tag each with the **risk level** (from `risk_areas`) and **priority** (P1/P2/P3).

### 4. Maintain traceability

Preserve the bidirectional chain **test basis → model element (state/transition) → test case → coverage item** (CTFL v4.0 §1.4.4). Every transition in scope of the chosen criterion maps to ≥1 case; no orphan cases; every case traces back to a model element and a basis reference.

### 5. Output

Write the output to `<paths.docs_dir>/MBT-<feature>.md`. Produce, in this order:

1. **Model** — the transition table + Mermaid `stateDiagram-v2`, with states/events/guards/actions and initial/final states.
2. **Coverage criterion** — the chosen criterion and its risk-based justification.
3. **Test Case Specification** — the derived cases: `TC ID | path | events | guards | expected state/output | coverage item(s) | risk | priority`.
4. **Coverage Summary (with counts)** — state, as numbers not prose: total **states** and **states covered**; total **valid transitions** and **transitions covered**; **invalid-transition** cases included; and the **criterion achieved** (e.g. "all-transitions / 0-switch: 14/14 transitions covered").

Then run the Self-check below, and offer to implement the highest-priority cases via `/qa:implement`.

> Keep the model maintainable — it is the single source for regenerating tests when behavior changes (counters the pesticide paradox, CTFL v4.0 Principle 5).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`, `stack.api_spec_path`, `risk_areas`) is honored; no path or tool is hardcoded.
- [ ] **Traceability intact** — the chain test basis -> model element (state/transition) -> case -> coverage item (-> procedure -> result -> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — the Coverage Summary states counts/coverage (states covered, transitions covered, criterion achieved) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (e.g. untested transition-pairs/paths, model assumptions); ISTQB Principle 1 (testing shows the presence, not the absence, of defects) and Principle 2 (exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Design Specification** (model + derived Test Case Specification) and written to the correct `<paths.docs_dir>` location.

## Handoff

Offer to implement the highest-priority (P1) cases via `/qa:implement` (turns model-derived cases into test procedures/scripts). Do **not** write automation here — this command is modeling & design only. For non-stateful design techniques route to `/qa:test-design`; for basis ambiguities found while modeling route to `/qa:static-review`.
