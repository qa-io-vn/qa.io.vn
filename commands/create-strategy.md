---
description: Generate or refresh the program-wide Test Strategy document from qa.config.yml. Use when the user wants a test strategy, QA approach, or testing strategy doc.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Create / refresh the Organizational Test Strategy

**ISTQB process:** Test planning — Organizational Test Strategy (CTFL v4.0 §5.1; ISO/IEC/IEEE 29119-3). Follow ISTQB terminology and the seven principles; see `docs/ISTQB-COMPLIANCE.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init`.

1. Read the ISTQB/ISO-29119-aligned structure at `${CLAUDE_PLUGIN_ROOT}/templates/strategy-template.md`. Use strict ISTQB Glossary terms (test object, test basis, test condition, test case, coverage item, test level, test type, entry/exit criteria).
2. Produce a complete **Test Strategy** tailored to this project's config: reflect its stack, the enabled `tooling` (omit sections for tools set to `none`), the `ci.platform`, the `gates` thresholds, and the `risk_areas`.
3. Cover, at minimum: objectives & principles, testing in the agile lifecycle, the test pyramid, risk-based testing, a coverage matrix, the core Playwright+TS approach, API testing, plus a section per enabled specialized type (contract, performance, accessibility, visual, security, mocking), test data, environments, CI integration for the configured platform, entry/exit criteria & DoD, defect management, metrics, roles, tooling summary, risks, and a phased roadmap.
4. Write to `<paths.docs_dir>/TEST-STRATEGY.md` (default `docs/qa/TEST-STRATEGY.md`). Create the directory if needed.
5. Write in prose with tables where they aid clarity. The strategy is long-lived — keep it project-general, not release-specific. Reference, don't duplicate, the per-release plan.

End by telling the user where the file is and suggesting `/qa:scaffold` and `/qa:create-plan`.
