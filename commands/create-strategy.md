---
description: Generate or refresh the program-wide Test Strategy document from qa.config.yml. Use when the user wants a test strategy, QA approach, or testing strategy doc.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Create / refresh the Organizational Test Strategy

**ISTQB process:** Test planning — **Organizational Test Strategy** (CTFL §5.1; CTAL-TM; agile mapping per CTFL-AT; verify each section reference against the current syllabus). **Work product:** the ISO/IEC/IEEE 29119-3 **Organizational Test Strategy**. Use strict ISTQB terminology and the seven principles; see `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md`.

Hierarchy: **Test Policy → Organizational Test Strategy (this command) → Test Plan**.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

1. **Config guard.** If the block above printed `MISSING` (no `qa.config.yml`), stop and tell the user to run `/qa:qa-init` first. Do not proceed. Otherwise, parse the config and treat its fields as the single source of truth — read `<paths.docs_dir>`, `<tooling.*>`, `<stack.*>`, `ci.platform`, `ci.browsers`, `gates`, `risk_areas`, `test_data`, `environments`, `team`, and `process.*`. Never hardcode paths, tools, or thresholds.

2. **Arguments.** This command takes no arguments. If `$ARGUMENTS` is non-empty, treat it as an optional scope hint (e.g. a subsystem name) and note it in the scope section; otherwise produce the full org-wide strategy. If config has no `risk_areas`, default the risk tiers to `risk_areas.critical` and state that the rest are unscoped.

3. **Read the template.** Use the ISTQB/ISO-29119-aligned structure at `${CLAUDE_PLUGIN_ROOT}/templates/strategy-template.md`. Follow its section order. Use strict ISTQB Glossary terms (test object, test basis, test condition, test case, coverage item, test level, test type, entry/exit criteria).

4. **Tailor to config (decision rules).** Produce a complete **Organizational Test Strategy** that reflects this project's config:
   - For every `tooling.*` toggle: include its section only when the value is **not** `none`/empty; omit (do not stub) sections for disabled tools, and list omitted types under "Out of scope" with the reason "`tooling.<x>` disabled".
   - Carry `gates` thresholds (coverage, performance, `gates.accessibility_standard`) verbatim into the entry/exit-criteria and metrics sections.
   - Map test levels/types to the configured stack via `<stack.*>`, `<tooling.unit>`, `<tooling.performance>`, `<tooling.accessibility>`, `<tooling.security>`, `<tooling.contract>`, `<tooling.mocking>`; CI integration for `ci.platform` and `ci.browsers`.
   - Derive risk tiers and test depth from `risk_areas` (risk level = likelihood × impact).

5. **Cover, at minimum:** scope & objectives; quality policy & the seven ISTQB principles; test approach (agile lifecycle tailoring: planning → monitoring & control → analysis → design → implementation → execution → completion, run continuously per iteration); test levels (CTFL §2.2); test types (CTFL §2.3 / ISO/IEC 25010); test design techniques (CTFL §4; label any pairwise/use-case techniques as Advanced/CTAL-TA, never Foundation); static testing (CTFL §3); test automation architecture (CT-TAE) for Playwright + `<tooling.language>`; risk-based testing (CTFL §5.2; CTAL-TM); a coverage matrix; a section per enabled specialized type (contract, performance, accessibility, visual, security, mocking); test data & environments; CI integration; entry/exit criteria & DoD; defect management; metrics; roles (RACI from `team`); tooling summary; risks; and a phased roadmap.

6. **Write the work product.** Write the **Organizational Test Strategy** (the ISO/IEC/IEEE 29119-3 work product) to `<paths.docs_dir>/TEST-STRATEGY.md` (default `docs/qa/TEST-STRATEGY.md` only if `paths.docs_dir` is unset). Create the directory if needed. Write in prose with tables where they aid clarity. Keep it long-lived and project-general, not release-specific — reference, don't duplicate, the per-release Test Plan.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, every `tooling.*` toggle, `ci.platform`/`ci.browsers`, `gates`, `risk_areas`, `team`, `test_data`, `environments`, `process.*`) is honored; each `tooling.*` set to `none` has its section omitted and listed as out of scope; nothing hardcoded.
- [ ] **Gates carried verbatim** — `gates` thresholds (coverage, performance, `gates.accessibility_standard`) appear unchanged in the entry/exit-criteria and metrics sections.
- [ ] **Risk tiers honored** — every `risk_areas` tier maps to a stated test depth/level; if `risk_areas` was empty, the `risk_areas.critical` default and the unscoped remainder are stated explicitly.
- [ ] **Traceability intact** — the strategy defines the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) as bidirectional, with no orphan levels/types.
- [ ] **Measurable** — entry/exit criteria and metrics state counts/coverage thresholds rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why, including any disabled tooling and unscoped risk tiers (CTFL Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Organizational Test Strategy** and written to the correct `<paths.docs_dir>` location.

End by telling the user the file location, then route: **up** to `/qa:test-policy` (the org Test Policy this strategy serves) and **down** to `/qa:create-plan` (a release-scoped Test Plan deriving from this strategy) and `/qa:scaffold` (to stand up the automation architecture this strategy defines).
