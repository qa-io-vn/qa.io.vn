---
description: Prepare for a QA/quality audit — assemble an evidence pack, sample-check bidirectional traceability, check standards conformance (ISTQB / ISO/IEC/IEEE 29119), and flag gaps. Use before an internal/external audit or compliance review.
argument-hint: "[standard / release / scope]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Audit & compliance readiness

**ISTQB process:** Test documentation, traceability & conformance evidence (CTFL v4.0 §1.4.4 traceability; ISO/IEC/IEEE 29119-3 documentation; ISTQB conformance). Assembles the evidence pack an auditor expects. Verify any section number against the current syllabus before quoting it externally.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Existing QA artifacts
```!
echo "--- standards docs ---"; ls -1 docs/ISTQB-*.md 2>/dev/null
echo "--- repo doc/test dirs (config decides authoritative paths) ---"; ls -1d docs reports tests test results 2>/dev/null
```

## Your task

You are assembling an **audit-readiness evidence pack** for the scope/standard in `$ARGUMENTS` (e.g. `ISO 29119`, a regulated release, or `ISTQB conformance`).

**Config guard:** if `qa.config.yml` printed "none" above, state that defaults are assumed, recommend `/qa:qa-init`, and proceed reading conventional locations conservatively. Otherwise read `paths.*`, `tooling.*` toggles, `gates`, and `risk_areas` from it and honor them — never hardcode paths, tools, or thresholds. Resolve all artifact locations through `<paths.docs_dir>` and `<paths.tests_dir>`; treat anything outside config as a discovery hint only.

**Empty `$ARGUMENTS`:** if no scope/standard is given, ask the user for the target standard and scope. If unanswered, default to an **ISTQB / ISO/IEC/IEEE 29119-3 conformance** audit scoped to `risk_areas.critical` from `qa.config.yml`, and state that default explicitly in the output.

Work through these steps in order. Assemble and assess **without altering existing records** — the only file you write is the readiness report.

1. **Documentation completeness** — confirm the expected work products exist under `<paths.docs_dir>` and are current: Test Policy / Organizational Test Strategy, Test Plan(s), Test Design & Test Case Specifications, Test Procedure Specifications, Test Status & Test Completion Reports, defect (incident) records, and the product-risk register. Map each to its ISO/IEC/IEEE 29119-3 document type (see `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` §11). Record each as **present / present-but-outdated / missing**; "outdated" = last modified before the release/baseline under audit or superseded by a newer artifact.
2. **Traceability evidence** — verify the bidirectional chain is demonstrable end-to-end: test basis (requirement / user story / OpenAPI) → test condition → test case + coverage item → test procedure → execution result → defect (per `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` §12). Sample-check at least one chain per `risk_areas.critical` item (minimum 3 samples, or all if fewer exist). Record each sample as **intact** or as a **break** naming the orphaned link and direction. Hand off the full coverage audit to `/qa:review-coverage`.
3. **Process conformance** — check practice against the claimed standard (ISTQB test-process activities and their testware per `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` §3; ISO/IEC/IEEE 29119 process; the test-case-design conformance precedent in `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-AUDIT.md`). For each in-scope activity record **conformant / partial / non-conformant** with the evidence relied on. Do not assert an ISTQB section number that is not traceable in those docs — soften to "verify against the current syllabus" instead.
4. **Evidence of execution** — confirm test results/logs are retained (from `<paths.tests_dir>` and configured `tooling.*` reporters), sign-offs are recorded (read-only inputs: `/qa:go-no-go` decision records and `/qa:release-report` Test Completion Reports), environment & config management is evidenced, and the defect lifecycle is traceable. Treat each as **evidenced / partial / absent** — never fabricate a result or sign-off; mark unknowns as gaps.
5. **Gaps & remediation** — list every finding with a **severity** (High = blocks audit / mis-attributed standard claim; Medium = present-but-incomplete or outdated; Low = cosmetic/traceable-with-effort), a concrete remediation action, and an owner. Order findings High → Low.

**Output:** an **audit-readiness evidence pack** — an evidence index assembled over the ISO/IEC/IEEE 29119-3 work product set (no dedicated 29119-3 template; the closest reference work product is the Test Completion Report, see `/qa:release-report`). Write it to `<paths.docs_dir>/AUDIT-READINESS-<scope>.md`, containing: (a) an evidence index (artifact → 29119-3 type → location → status), (b) the traceability sample table with intact/break verdicts, (c) the process-conformance summary, and (d) the severity-ordered gap & remediation list with owners. Modify nothing except this readiness report.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; no artifact path, tool, or threshold is hardcoded.
- [ ] **Traceability intact** — each evidence-index row and traceability sample preserves the bidirectional chain test basis → condition → case → coverage item → procedure → result (→ defect); breaks name the orphaned link and direction rather than being silently dropped.
- [ ] **Measurable** — the report states counts (work products present/outdated/missing, samples intact/broken, findings by severity) rather than prose claims.
- [ ] **Standards traceable** — every ISTQB/ISO section cited is traceable to `docs/ISTQB-COMPLIANCE.md` / `docs/ISTQB-AUDIT.md`; otherwise softened to "verify against the current syllabus"; no Specialist topic is mis-tagged as CTFL Foundation.
- [ ] **Residual risk stated** — name what is NOT covered by this readiness pass and why (e.g. unsampled chains, unaudited domains), per ISTQB Principle 1; never imply audit-ready certainty.
- [ ] **Work product named** — output is identified as the audit-readiness evidence pack over the ISO/IEC/IEEE 29119-3 work product set and written to `<paths.docs_dir>/AUDIT-READINESS-<scope>.md`, altering no existing record.
