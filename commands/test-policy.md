---
description: Create or refresh the Organizational Test Policy — the highest-level statement of testing intent, value, and principles for the organization. States WHY the org tests and WHAT quality means; the HOW lives in the Organizational Test Strategy.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Organizational Test Policy

**Work product:** Organizational Test Policy per **ISO/IEC/IEEE 29119-2** (the highest-level governance document; the Organizational Test Strategy and Test Plans sit below it). Use strict ISTQB terminology and the seven ISTQB principles — verify any specific syllabus section against `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` and `${CLAUDE_PLUGIN_ROOT}/docs/GLOSSARY.md` (test-management concepts trace to the current Advanced Test Manager / Test Management syllabi; verify against the current syllabus rather than asserting a section number).

**Scope boundary:** the Policy says **WHY/WHAT** (intent, value, quality goals, mandated standards, principles). It must **not** define **HOW** — process sequencing, techniques, tooling, environments, and cadence belong to the Organizational Test Strategy (`/qa:create-strategy`).

## Project / org config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

1. **Config guard.** If the block above shows `MISSING`, stop and tell the user to run `/qa:qa-init` first. Otherwise read `qa.config.yml` and bind every `<paths.*>`, `<tooling.*>`, `<gates.*>`, `<risk_areas.*>`, `<team.*>`, and `<stack.*>` reference to its configured value. Never hardcode a path, tool, or threshold.

2. **Scope resolution (empty `$ARGUMENTS`).** This command takes no arguments. The Policy is org-wide and not scoped to a feature, so:
   - If the user supplied a focus (e.g. a product line or regulatory regime), narrow the Policy's *scope* statement (§1) to it.
   - If nothing was supplied, default the scope to the whole organization as described by `project` in config, and anchor depth/quality goals to `<risk_areas.critical>`. Do not block on missing input.

3. **Load the template.** Read the structure at `${CLAUDE_PLUGIN_ROOT}/templates/policy-template.md` and follow its sections in order. Use ISTQB Glossary terms exactly (test object, test basis, test policy, test strategy, quality risk, exit criteria).

4. **Produce the Policy** covering, as intent only (WHY/WHAT — never HOW):
   1. **Purpose & scope** — why the policy exists; which products/teams it governs (from `project`); audience; out-of-scope. State explicitly that HOW lives in the Strategy.
   2. **Test objectives & quality goals** — the organization's test objectives, expressed as **ISO/IEC 25010** quality characteristics, with depth anchored to `<risk_areas.critical>` and success tied to `<gates.*>`.
   3. **The value of testing** — how testing contributes to business goals (confidence, residual-risk reduction, contractual/regulatory needs); value is **measured against `<gates.*>` and coverage, not asserted**.
   4. **Guiding principles** — adherence to the seven ISTQB principles; whole-team quality; risk-based prioritization driven by `<risk_areas.*>`.
   5. **Roles & responsibilities** — accountability for quality (whole-team quality; appropriate tester independence). Reference `<team.*>` for named owners.
   6. **Mandated standards** — the frameworks the org commits to (ISTQB syllabi for terminology/principles, ISO/IEC/IEEE 29119 for process & documentation, ISO/IEC 25010 for the quality model) and what each governs.
   7. **Testware as a controlled asset** — intent for version control, ownership, retention, and bidirectional traceability; testware lives under `<paths.docs_dir>` / `<paths.tests_dir>` / `<paths.reports_dir>`.
   8. **How value is measured** — *what* is measured (intent): exit-criteria conformance via `<gates.min_pass_rate_pct>` / `<gates.block_on_severity>`, requirement & risk coverage, non-functional conformance, and residual risk.
   9. **Review, approval & revision history** — review cycle, approvers (`<team.*>`), change log.

5. **Keep HOW out — delegate it.** If process sequencing, technique selection, tooling, environment, or cadence detail starts to appear, do **not** write it here. State the intent in one line and delegate the detail to the Organizational Test Strategy via `/qa:create-strategy`. Keep the Policy to ~1–2 pages and long-lived (it should rarely change).

6. **Write the artifact** to `<paths.docs_dir>/TEST-POLICY.md` (creating the directory if needed). Write in prose with tables where they aid clarity.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`, `team`) is honored; nothing hardcoded.
- [ ] **Intent only, no HOW** — no process sequencing, techniques, tooling, or cadence detail leaked in; any such content is delegated to `/qa:create-strategy`.
- [ ] **Principles anchored** — the Policy adheres to the **seven ISTQB principles**, and §3/§8 reflect Principle 1 (testing shows the presence, not the absence, of defects) by stating value is measured, not asserted.
- [ ] **Measurable** — quality goals and value are tied to `<gates.*>` and coverage rather than prose claims.
- [ ] **Residual risk stated** — the Policy mandates that residual risk is named explicitly at sign-off, not assumed absent.
- [ ] **Work product named** — output is identified as the **ISO/IEC/IEEE 29119-2 Organizational Test Policy** and written to `<paths.docs_dir>/TEST-POLICY.md`.

End by telling the user where the file is. The Policy is the top of the hierarchy **Policy → Organizational Test Strategy → Test Plan**: hand off **down** to `/qa:create-strategy` (which defines HOW) and note that `/qa:process-improvement` feeds revisions back up into this Policy.
