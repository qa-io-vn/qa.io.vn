---
description: Plan maintenance testing for changes to a deployed system — modifications, migration, or retirement — with impact analysis, producing a maintenance Test Plan (ISO/IEC/IEEE 29119-3). Use when testing patches, upgrades, data migrations, or decommissioning.
argument-hint: "<change / migration / retirement scope>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Maintenance testing: $ARGUMENTS

**ISTQB process:** Maintenance testing + impact analysis (CTFL v4.0 §2.3). Drives **confirmation testing** of the change and **regression testing** of impacted areas, both change-related test types (CTFL v4.0 §2.2.2). Verify these section numbers against the current syllabus.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "NO_CONFIG"
```

## Recent changes
```!
(git diff --name-only HEAD~10 2>/dev/null || echo "no git history") | head -30
```

## Your task

Produce a maintenance **Test Plan** (the ISO/IEC/IEEE 29119-3 Test Plan work product, scoped to a maintenance release) and implement/run the confirmation + regression tests it specifies. Follow the steps in order; do not skip the config guard.

### 0. Config guard

1. If the config block above printed `NO_CONFIG` (no `qa.config.yml` found), do **not** assume defaults for paths or tooling. Tell the user the config is missing, suggest `/qa:qa-init`, and proceed only with placeholders left explicit (`<paths.*>`, `<tooling.*>`, `<stack.*>`) so nothing is hardcoded.
2. Otherwise, read `paths.*`, `tooling.*` toggles, `gates`, and `risk_areas` from the config and honor them throughout. Never substitute a hardcoded path, report directory, or runner.

### 1. Resolve scope from `$ARGUMENTS`

1. If `$ARGUMENTS` is non-empty, treat it as the maintenance scope (the change, migration, or retirement under test).
2. If `$ARGUMENTS` is **empty**: first try to infer scope from the "Recent changes" diff above. If the diff is empty or ambiguous, ask the user for the change/migration/retirement scope. Only if the user cannot specify, default the scope to `risk_areas.critical` from config and state this assumption explicitly in the plan.

### 2. Classify the maintenance trigger (decision tree)

Pick exactly one trigger per the rules below (CTFL v4.0 §2.3); if the scope spans more than one, plan each and note the dominant one:

1. **Modification** — IF the change is a planned enhancement, patch, hotfix, emergency fix, or an environment/OS/platform upgrade that keeps the same platform → treat as Modification. Plan: confirmation testing of the changed/new behavior + regression on impacted + high-risk areas.
2. **Migration** — IF the system moves to another platform, OR data is migrated/converted/transformed → treat as Migration. Plan: (a) tests of the migration **process** itself, (b) verification of migrated **data integrity** (counts, referential integrity, transformation correctness), (c) operation of the system on the **new platform**, and (d) **rollback** verification.
3. **Retirement** — IF the system or a component is being decommissioned → treat as Retirement. Plan: data **archiving/migration**, **restore/retrieval** procedures, and continued operation of any **remaining** processes/integrations.

### 3. Impact analysis

1. Determine what the change affects **directly** and **indirectly** (shared modules, APIs, data, UI flows, integrations). Map each affected area to `risk_areas` from config.
2. Delegate regression **selection/prioritization** to `/qa:regression`; record its selected set here as the regression scope.
3. Where impact analysis is hard because traceability is poor or absent, flag that explicitly as a **risk** in the plan (per CTFL §1.4.4 bidirectional traceability) and widen the regression scope accordingly.

### 4. Specify and run the tests

1. **Confirmation testing** — re-test the fixed/changed behavior to confirm the change works (route defect re-test handling through `/qa:triage`). State pass/fail per item.
2. **Regression testing** — run the selected regression set on impacted + high-risk areas so nothing previously working broke. Execute via `<tooling.*>`/`<stack.*>` from config; do not name a runner the config does not enable.
3. For **Migration**, add the data-validation and rollback tests from step 2 of the decision tree.
4. Define **entry/exit criteria** for the maintenance release from `gates`, and state **residual risk** (what is not covered and why — Principle 1).

### 5. Output

1. Read the plan structure at `${CLAUDE_PLUGIN_ROOT}/templates/plan-template.md` and produce its sections, scoped to this maintenance release.
2. Write the plan to `<paths.docs_dir>/MAINTENANCE-<scope>.md`.
3. State **measurable** results: counts of confirmation items (pass/fail), regression cases run by priority, and impacted areas covered vs total — not prose claims.
4. Hand results to `/qa:release-report` for the Test Completion Report.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded (no literal `docs/qa/`, `tests/`, report dirs, or runner names).
- [ ] **Trigger classified** — the maintenance trigger is one of Modification / Migration / Retirement (CTFL §2.3), and the plan matches its required tests.
- [ ] **Impact scope traced 100%** — every area the change affects (direct + indirect) is mapped to `risk_areas` and covered by confirmation or regression; no impacted area is left without a corresponding test, and no test is orphaned from an impacted area. Poor-traceability gaps are flagged as risks.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional (CTFL §1.4.4); no orphans.
- [ ] **Measurable** — output states counts/coverage (confirmation items pass/fail, regression cases by priority, % impacted areas covered) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Plan (maintenance release) and written to `<paths.docs_dir>/MAINTENANCE-<scope>.md`.
