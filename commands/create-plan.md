---
description: Generate a release or sprint Test Plan from qa.config.yml plus a release name and feature list. Use when the user wants a test plan for a specific release/sprint.
argument-hint: "<release-id> [comma-separated features]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Create a Test Plan for: $ARGUMENTS

**ISTQB process:** Test planning — Test Plan (CTFL v4.0 §5.1; ISO/IEC/IEEE 29119-3). Use strict ISTQB terminology and bidirectional traceability (test basis → condition → case → procedure → result).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

Release / features come from the arguments above (`$ARGUMENTS`): the first token is the release ID (e.g. `R2.4`), the rest is the feature list. If no arguments were given, ask the user for the release ID and features.

If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init`.

1. Read the structure at `${CLAUDE_PLUGIN_ROOT}/templates/plan-template.md`.
2. Produce a complete, release-scoped **Test Plan**:
   - Document control + change log.
   - Scope: features in/out (tag each with a risk tier using `risk_areas`), test types in scope (only enabled `tooling`), regression scope.
   - Test approach per type for THIS release.
   - Entry/exit criteria using the exact `gates` thresholds from config.
   - Environments (from config) and test-data plan (`test_data`).
   - Schedule mapped to `process.sprint_length_weeks` and cadence.
   - A representative set of sample test cases (Given/When/Then) for the listed features — cover happy path, negative, authz, and any non-functional checks relevant to the feature's risk tier.
   - Risk register (Impact×Likelihood), RACI from `team`, defect rules, a test-summary-report template, and an approvals block.
3. Keep it specific to this release — link to `TEST-STRATEGY.md` for the general approach instead of repeating it.
4. Write the **Test Plan** (the ISO/IEC/IEEE 29119-3 Test Plan work product) to `<paths.docs_dir>/TEST-PLAN-<release-id>.md`. Create the directory if needed.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`, `team`, `test_data`, `process.sprint_length_weeks`) is honored; nothing hardcoded.
- [ ] **Every feature covered** — each feature in scope has at least one test case; no feature is listed without a corresponding case.
- [ ] **Acceptance criteria mapped** — each acceptance criterion is traced test basis -> condition -> case; the chain (-> procedure -> result -> defect) is preserved, bidirectional, and free of orphans.
- [ ] **Measurable** — coverage is stated as counts/percentages (e.g. N conditions, M cases by priority, % of features with ≥1 case) rather than prose claims.
- [ ] **Residual risk stated** — include a **Residual Risk** section naming what is NOT covered and why (CTFL v4.0 Principle 1: testing shows the presence, not the absence, of defects; §1.4.4).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Plan** work product, with the `gates` thresholds carried verbatim into its exit criteria, and written to the correct `<paths.docs_dir>` location.

End by pointing to the file and suggesting `/qa:implement <feature>` to start automating.
