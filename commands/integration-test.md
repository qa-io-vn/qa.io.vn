---
description: Design integration testing — component integration and system integration, with an integration strategy (incremental vs big-bang), test doubles, and an interface coverage table. Produces an ISO/IEC/IEEE 29119-3 Test Design Specification for the interfaces under test. Use to test interactions between components or systems.
argument-hint: "<components / systems / interface>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Integration testing: $ARGUMENTS

**ISTQB process:** Component integration & system integration testing — test levels (CTFL v4.0 §2.2.1).
**Work product:** ISO/IEC/IEEE 29119-3 **Test Design Specification** scoped to the interfaces under test (the integration test design), with an explicit integration strategy and test-double plan.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Step 0 — Read config & validate input (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed only with documented defaults the user confirms — do **not** invent paths/tools. Resolve the config-derived inputs in scope: `<paths.docs_dir>` (output location), `<paths.tests_dir>` (where integration tests live), `<tooling.mocking>` (service virtualization / test doubles for externals), `<tooling.contract>` (contract backstop), `environments` (which environments host the integrated systems), and `risk_areas` (prioritization). Nothing about paths or tools is hardcoded; everything comes from config.
2. Resolve the integration target from `$ARGUMENTS` (which components / systems / interface to integrate):
   - **If `$ARGUMENTS` is non-empty:** that is the integration target.
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user which components/systems/interface to integrate. If the user declines or cannot specify, **default to the first area listed in `risk_areas.critical`** and state explicitly that you defaulted there and why.
3. Confirm the resolved target and decide which integration **level** applies before designing (a target may involve both).

## Step 1 — Classify the integration level

Distinguish the two ISTQB integration levels and tag each interface in scope to one:

1. **Component integration testing** — interactions and interfaces **between integrated components** of the system (e.g. service ↔ repository, module ↔ module). Focus on the interfaces and the data passed, not the components' internal logic.
2. **System integration testing** — interactions between the system and **other systems / external services** (payment, email, third-party APIs). Use service virtualization / mocking (`<tooling.mocking>`) for unstable or costly externals, backed by contract testing (`/qa:contract-sync`) so virtualized interfaces cannot silently drift from reality.

## Step 2 — Choose the integration strategy (state which and why)

1. Prefer an **incremental** strategy (top-down, bottom-up, or functional/feature-based) over **big-bang**, so that when an integration fault occurs it is localized to the most recently added interface.
2. Decision rule:
   - **Top-down** when high-level control/orchestration is stable first — replace not-yet-integrated callees with **stubs**.
   - **Bottom-up** when low-level components/externals are ready first — drive them with **drivers**.
   - **Functional/feature** when integrating a vertical slice end-to-end is the priority.
   - Use **big-bang** only when the system is tiny or all components are already available and stable; state the localization cost you are accepting.
3. Record the chosen strategy, the integration order, and the **stubs/drivers/mocks** each step requires.

## Step 3 — Derive interface conditions & cases

For each interface in scope:

1. Identify the **interface contract**: the data shape, the success path, and the failure modes. Cover, at minimum: correct data passed and returned, **error propagation**, **timeout / unavailability of the other side**, **sequencing/ordering**, and **transaction / rollback** behaviour.
2. Apply CTFL v4.0 §4.2 black-box techniques to the interface inputs: **Equivalence Partitioning** (valid + invalid partitions), **Boundary Value Analysis** (state 2-value or 3-value), and **Decision Table** where the interface behaviour depends on input combinations. Integration points are where defects cluster (Principle 4) — explicitly cover negative and failure paths.
3. Decide the **test double** per dependency: stub (canned responses), mock (verifies interactions), fake (working lightweight impl), or a real instance. For externals, prefer virtualization via `<tooling.mocking>` and note the contract backstop.

## Step 4 — Build the interface coverage table

Produce a table with one row per interface/condition:

| interface | condition | technique | test double | coverage |
|---|---|---|---|---|

- **interface** — the component↔component or system↔external boundary.
- **condition** — the specific interaction tested (e.g. "timeout on payment gateway → order rolled back").
- **technique** — EP / BVA (2- or 3-value) / decision table / error guessing.
- **test double** — stub / driver / mock / fake / real (and virtualized-via-`<tooling.mocking>` vs hit-for-real).
- **coverage** — which interface contract element this row exercises (data / error / timeout / sequencing / transaction).

## Step 5 — Implement & run (where feasible)

1. Implement at the API/integration level where possible (Playwright `request`, or route to `/qa:api-automate`); place tests under `<paths.tests_dir>` per project convention.
2. Keep tests **independent and parallel-safe**: no shared mutable state, explicit setup/teardown, deterministic doubles.
3. Run them against the appropriate entry from `environments`, and report **interface coverage** as counts.

## Output

Write the integration test design to `<paths.docs_dir>/INTEGRATION-TEST-<target>.md` (`<target>` slugified from `$ARGUMENTS`). It is the ISO/IEC/IEEE 29119-3 **Test Design Specification** for the interfaces under test. Include:

1. **Scope & level** — the integration target and which interfaces are component-integration vs system-integration.
2. **Integration strategy** — chosen strategy, integration order, and the stubs/drivers/mocks per step.
3. **Interface coverage table** — the table from Step 4.
4. **Virtualization vs real** — which externals are virtualized via `<tooling.mocking>` and which are hit for real, plus the `/qa:contract-sync` backstop for any mocked interface.
5. **Coverage summary (counts)** — interfaces in scope, conditions covered, and conditions deferred, as numbers not prose.

Then run the Self-check below.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`, `paths.tests_dir`, `tooling.mocking`, `tooling.contract`, `environments`, `risk_areas`) is honored; no path or tool is hardcoded.
- [ ] **Traceability intact** — the chain test basis -> interface condition -> case -> coverage item (-> procedure -> result -> defect) is preserved and bidirectional; no orphan interfaces or cases.
- [ ] **Measurable** — the coverage summary and table state counts (interfaces in scope, conditions covered/deferred, which are virtualized vs real) rather than prose claims.
- [ ] **Residual risk stated** — name the interfaces, failure modes, or externals NOT covered (and any reliance on test doubles that could drift) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Design Specification** for the interfaces under test and written to `<paths.docs_dir>/INTEGRATION-TEST-<target>.md`.

## Handoff

- Implement the highest-priority interface cases via `/qa:api-automate` (API-level) or `/qa:implement`.
- Back any virtualized/mocked external interface with `/qa:contract-sync` so the doubles cannot drift from the provider.
- For the lowest level (single component in isolation) use `/qa:unit-test`; for full end-to-end across the integrated system use `/qa:web-automate`.
- Route basis ambiguities (unclear interface contracts) to `/qa:static-review`.
