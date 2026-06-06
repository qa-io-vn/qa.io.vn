---
description: Prepare for a QA/quality audit — assemble traceability and evidence, check standards conformance (ISTQB / ISO 29119), and flag gaps. Use before an internal/external audit or compliance review.
argument-hint: "[standard / release / scope]"
allowed-tools: Read, Glob, Grep, Bash
---

# Audit & compliance readiness${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test documentation, traceability & conformance (CTFL §5.4; ISO/IEC/IEEE 29119; ISTQB). Assembles the evidence an auditor expects.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Existing QA artifacts
```!
echo "--- docs ---"; ls -1 docs/qa 2>/dev/null
echo "--- standards docs ---"; ls -1 docs/ISTQB-*.md 2>/dev/null
echo "--- tests & reports ---"; ls -1d tests reports 2>/dev/null
```

## Your task

Scope/standard from `$ARGUMENTS` (e.g. ISO 29119, a regulated release). Assemble an audit-readiness pack.

1. **Documentation completeness** — confirm the expected work products exist and are current: Test Policy, Organizational Test Strategy, Test Plan(s), Test Case Specifications, Test Status & Completion Reports, defect records, risk register. Map them to ISO/IEC/IEEE 29119-3 document types (see `docs/ISTQB-COMPLIANCE.md §11`). Flag missing/outdated items.
2. **Traceability evidence** — verify the bidirectional chain is demonstrable: requirement/test basis → test condition → test case → test procedure → execution result → defect. Sample-check it and note breaks (use `/qa:review-coverage`).
3. **Process conformance** — check practice against the claimed standard (ISTQB process activities, ISO 29119 process; see `docs/ISTQB-AUDIT.md` and `ISTQB-COVERAGE.md`). Note conformant areas and gaps.
4. **Evidence of execution** — test results/logs retained, sign-offs recorded (`/qa:go-no-go`, `/qa:release-report`), environment & config management, defect lifecycle records.
5. **Gaps & remediation** — list findings by severity with concrete remediation and owners before the audit.

Output an audit-readiness report to `<paths.docs_dir>/AUDIT-READINESS-<scope>.md`: an evidence index (artifact → location → status), traceability sample, conformance summary, and the gap/remediation list. Read-only — assemble and assess; don't alter records.
