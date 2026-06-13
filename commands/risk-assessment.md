---
description: Perform ISTQB risk-based testing analysis — identify and score product and project risks (likelihood x impact), assign a tier, and derive the test response. Produces a Product Risk Register. Use for risk analysis or to prioritize testing.
argument-hint: "[release or area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ISTQB risk assessment for: $ARGUMENTS

**ISTQB process:** Risk-based testing — Product Risk Register (CTFL v4.0 §5.2; CTAL-TM Risk Management; ISO/IEC/IEEE 29119-3). Verify any section number against the current syllabus. Use strict ISTQB terminology and preserve bidirectional traceability (risk → test condition → case → coverage item → procedure → result).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

If `qa.config.yml` is missing above, stop and tell the user to run `/qa:qa-init`. Otherwise honor it: read `paths.*`, `risk_areas` (critical/high/medium), `tooling.*` toggles, and `gates`; never hardcode project-specific paths, tools, or areas.

**Scope resolution (`$ARGUMENTS`):**
1. If `$ARGUMENTS` names a release or area, scope the assessment to it.
2. If `$ARGUMENTS` is empty, default the scope to the areas in `risk_areas.critical`; state that you defaulted and which areas were used.

Then:

1. Read the structure at `${CLAUDE_PLUGIN_ROOT}/templates/risk-register-template.md` and follow it.

2. **Identify risks**, separating two types (per the ISTQB Glossary):
   - **Product (quality) risks** — ways the test object could fail to satisfy a quality characteristic (functional suitability, performance efficiency, security, usability/accessibility, reliability, compatibility — ISO/IEC 25010). Seed from `risk_areas`, prior defects, change-related areas, and the features in scope.
   - **Project risks** — schedule, resources, test environment, dependencies/suppliers, test data.

3. **Assess** each risk: **Likelihood (1–5) × Impact (1–5) = Risk Level (1–25)**. Justify each score in one line. Assign a **tier** using these exact bands:
   - **Low** — Risk Level 1–4
   - **Medium** — Risk Level 5–12
   - **High** — Risk Level 13–15
   - **Critical** — Risk Level 16–25

4. **Derive the test response** per risk by tier (higher risk → earlier, deeper, more independent testing):
   - **Critical/High** → low-level (concrete) cases; component → integration → system → acceptance as the area requires; rigorous techniques (decision table, state transition, BVA 2/3-value, EP); gate the release. Add non-functional checks only for **enabled** `tooling` types and honor `gates` thresholds.
   - **Medium** → high-level (logical) cases at system level; EP / checklist; smoke or spot checks.
   - **Low** → exploratory / regression only.

5. **Assign owners and mitigation triggers.** An **owner is required when Risk Level ≥ 13** (High/Critical) before scope freeze — flag any High/Critical risk without a named owner (drawn from `team`) as a sign-off blocker.

6. **Output the Product Risk Register** following the template: per-risk row (Risk ID | area | description | type | likelihood | impact | risk level | tier | mitigation/test approach | test level & technique | owner | status), sorted by Risk Level descending. Include the **tier summary** (counts per tier, product/project split, owner coverage for ≥ 13). Write to `<paths.docs_dir>/risk-register-<scope>.md`. Reconcile with `risk_areas` in `qa.config.yml` and suggest updates if they diverge. Read-only on product code.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Tiers correct** — every risk has Risk Level = L × I and a tier from the exact bands (Low 1–4 · Medium 5–12 · High 13–15 · Critical 16–25); every risk ≥ 13 has a named owner.
- [ ] **Traceability intact** — the chain risk → test condition → case → coverage item → procedure → result (→ defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts (tier counts, product/project split, owner coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Product Risk Register** and written to the correct `<paths.docs_dir>` location.

Feed the result into `/qa:create-plan` (scope & depth) and exit-criteria thinking; `/qa:estimate` consumes the tiers for depth multipliers; `/qa:status-report` and `/qa:release-report` track and report against these risks and the residual-risk statement.
