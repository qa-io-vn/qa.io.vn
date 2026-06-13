---
description: Design combinatorial test cases for features with many parameters — pairwise, classification tree, or orthogonal arrays — to get strong coverage with few cases. Use when several inputs/options combine and exhaustive testing is infeasible.
argument-hint: "<feature with multiple parameters>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Combinatorial test design: $ARGUMENTS

**ISTQB process:** Test design (CTFL v4.0 §1.4) using **combinatorial test techniques** — pairwise (all-pairs), classification tree, and orthogonal arrays. These are **Advanced (CTAL Test Analyst)** black-box techniques, NOT CTFL v4.0 Foundation (pairwise/classification tree were removed from Foundation in v4.0 — verify against the current syllabus). Realizes Principle 2 (exhaustive testing is impossible).

**Work product:** ISO/IEC/IEEE 29119-3 **Test Case Specification** (per `docs/ISTQB-COMPLIANCE.md` §11) — a set of test cases plus the coverage items (parameter-value pairs/n-tuples) they exercise. Use the structure and fields in `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

If `qa.config.yml` printed `none`, warn that paths/tooling are unknown and ask the user to run `/qa:qa-init` first, or fall back to documented defaults (`<paths.docs_dir>` = `docs/qa`); do not hardcode tool names beyond config.

**Resolve the target:**
1. If `$ARGUMENTS` names a feature with multiple combining parameters, use it.
2. If `$ARGUMENTS` is empty: ask "Which multi-parameter feature should I design combinatorial cases for?" — and if the user cannot name one, default to the highest-priority entry in `risk_areas.critical` from `qa.config.yml` that has multiple inputs/options. State the assumption explicitly before proceeding.

A combinatorial target is a feature whose behavior depends on **multiple parameters** (e.g. checkout = {payment method × shipping × currency × user tier × coupon}). Exhaustive combinations explode; combinatorial techniques cover the important interactions with far fewer cases.

Work through these steps in order:

1. **Model the parameters.** List each parameter and its values/partitions. Apply Equivalence Partitioning first to reduce each parameter to representative values (one per valid partition; mark invalid values). Record **constraints** — value combinations that cannot co-occur — as explicit exclusion rules. Output a parameter model table: parameter | values (partitions) | invalid values | constraints.
2. **Compute the full Cartesian size** = product of the value counts per parameter. Record this number; it is the baseline for the reduction metric in step 6.
3. **Choose a technique by rule:**
   - **Pairwise (all-pairs), strength = 2 (default):** cover every pair of parameter values at least once. Use unless a higher strength is justified below.
   - **Classification tree:** use when stakeholders need a visual/documented coverage rationale, or parameters are hierarchical.
   - **Orthogonal arrays:** use only when an applicable balanced array exists for the parameter/value counts.
   - **Raise to strength 3 (3-wise) or higher** ONLY for parameters flagged in `risk_areas.critical`/`high` where 3-way interaction failures are credible. State the reason per raised interaction.
4. **Generate the combination set** honoring every constraint from step 1 (exclude invalid pairings; never emit a case that violates a constraint). Present the cases as a table, one row per case, columns = parameters + the derived expected result.
5. **Add boundary/negative cases** that combinatorics alone won't catch — boundary values (2-value or 3-value BVA, state which) and invalid-input cases for high-risk parameters. Label these separately from the combinatorial set.
6. **Traceability & coverage (per case + per set):**
   - **Per-case traceability:** each test case records the technique, the strength, and the specific parameter-value pairs/tuples (coverage items) it covers, and links back to the test condition / test basis item it exercises.
   - **Reduction metric:** report `selected cases / full Cartesian size` (from step 2) as both a count and a percentage (e.g. "23 cases vs 4,320 full Cartesian = 99.5% reduction").
   - **Interaction coverage:** state the achieved coverage (e.g. "100% of valid 2-way pairs; 3-way only for {payment × currency × tier}").

## Output

Write the combinatorial **Test Case Specification** to `<paths.docs_dir>/COMBINATORIAL-<feature>.md`, following `${CLAUDE_PLUGIN_ROOT}/templates/test-case-template.md`, and containing:
- The parameter model table (step 1) and full Cartesian size (step 2).
- The chosen technique and strength with justification (step 3).
- The combinatorial case table (step 4) and the boundary/negative supplement (step 5).
- The per-case traceability table and the reduction + interaction-coverage metrics (step 6).

Then offer to automate the set **data-driven** via `/qa:implement` (UI/system specs) or `/qa:api-automate` (API specs), feeding the case table as parameterized data.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.docs_dir`, `risk_areas`, and any `tooling.*` toggles in scope are honored; no hardcoded paths or tool names.
- [ ] **Traceability intact** — every case links test basis -> condition -> case -> coverage item (the parameter-value pairs/tuples); the chain is bidirectional with no orphan cases or uncovered conditions.
- [ ] **Measurable** — output states the full Cartesian size, the selected-case count, the reduction %, and the achieved interaction (n-way) coverage — not prose claims.
- [ ] **Residual risk stated** — name the interactions NOT covered: at strength 2, no n-way interaction (n≥3) is guaranteed; list any constraint-excluded combinations and any parameters that were partition-reduced (ISTQB Principle 1 — testing shows the presence, not the absence, of defects; Principle 2 — exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Case Specification**, follows the test-case template, and is written to `<paths.docs_dir>/COMBINATORIAL-<feature>.md`.
- [ ] **Technique attribution correct** — pairwise / classification tree / orthogonal arrays are labeled **Advanced (CTAL-TA)**, never CTFL Foundation.

---

## Handoffs

- Upstream: if the test conditions for this feature have not yet been derived, run `/qa:test-design` (or `/qa:test-cases`) first — those own analysis→design; this command specializes in the combinatorial sub-technique for multi-parameter features.
- Downstream: hand the case table to `/qa:implement` (UI/system) or `/qa:api-automate` (API) to drive data-driven automation.
