---
description: Run static analysis of source code — complexity, control-/data-flow, coding-standard and maintainability metrics — without executing it, and write a static-analysis findings report. Use to assess code quality and find defects early (shift-left). Distinct from reviewing the test basis (/qa:static-review).
argument-hint: "[path / module]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Static analysis

**ISTQB process:** Static analysis — a form of **static testing** in which code is analyzed, not executed (CTFL v4.0 §3.1; verify the exact section against your current syllabus version). The control-flow, data-flow, and complexity techniques applied here are a Technical Test Analyst topic (CTAL-TTA static analysis — Specialist, not Foundation). The source code is the test object; this command analyzes and reports only — it does not modify code.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — paths/tooling/risk_areas will be inferred from the repo; treat the report location and analyzer as unset"
```

## Tooling signals
```!
echo "--- analyzers present in repo ---"; grep -iE "eslint|sonar|semgrep|tsc|pylint|ruff|flake8|checkstyle|spotbugs|pmd|coverage" package.json pyproject.toml pom.xml build.gradle* 2>/dev/null | head
echo "--- sast configured in qa.config.yml ---"; grep -A4 "security:" qa.config.yml 2>/dev/null | grep -E "sast"
```

## Your task

Static analysis examines code structure to find defects and quality issues early (Principle 3, shift-left). Defects cluster in complex units (Principle 4), so prioritize there.

**Step 0 — Read config & set scope.** Read `qa.config.yml` (the block above). If it is absent, infer `paths.*`, `tooling.*`, and `risk_areas` from the repo and state every assumption in the report. Then resolve scope from `$ARGUMENTS`:
- If `$ARGUMENTS` names a **path/module**, analyze that.
- If `$ARGUMENTS` is **empty**, ask the user for a path/module; if no answer is available, default to the source under `risk_areas.critical` (then `risk_areas.high`), and state in the report that scope was defaulted.

**Step 1 — Run the configured analyzer(s).** Run the analyzer declared in config (`<tooling.security.sast>`) plus any linters/type-checkers discovered above (e.g. ESLint, `tsc --noEmit`, Ruff, SonarQube/Semgrep — only those actually present in the repo). If `<tooling.security.sast>` is `none` and no linter is discovered, analyze manually by reading representative source files. Collect findings; do not invent tools that are not configured or installed.

**Step 2 — Code metrics.** For each unit in scope, measure **cyclomatic complexity**, **nesting depth**, **function/file size**, and parameter count. Apply these default thresholds (override with any `gates`/limits in config) and flag any unit that exceeds one:
- cyclomatic complexity > 10 (flag; > 20 = high severity)
- nesting depth > 4
- function length > 60 lines, or file > 400 lines
- parameter count > 5

**Step 3 — Control-flow / data-flow concerns.** Where the analyzers surface them: unreachable/dead code, infinite loops, uninitialized-before-use or unused variables (data-flow anomalies), null/undefined-dereference risks, missing returns, and unhandled error paths.

**Step 4 — Coding standards & security patterns.** Report standard violations and security-relevant patterns (injection sinks, unsafe APIs, hardcoded secrets). Route deeper security work to `/qa:security-scan` (shared SAST surface) — do not duplicate its analysis.

**Step 5 — Prioritize & recommend.** Rank findings by severity (critical/high/medium/low) and risk area, weighting toward `risk_areas.critical`/`high`. For each, recommend a concrete refactor that lowers complexity and improves testability.

## Output

Write a **Static Analysis Report** to `<paths.reports_dir>/STATIC-ANALYSIS.md` (fall back to `<paths.docs_dir>` if no reports dir is configured). This is not a dedicated ISO/IEC/IEEE 29119-3 work product; it is a **static-analysis findings record** (the closest 29119-3 analogue is review/static-analysis results), and it scores **ISO/IEC 25010 Maintainability** sub-characteristics (analysability, modifiability, modularity, testability). It must contain:
- **Summary** — scope analyzed, analyzer(s) run, headline metrics (units over each threshold, total findings by severity).
- **Metrics table** — `unit (file:function) | cyclomatic complexity | nesting depth | size | over-threshold? | maintainability risk`.
- **Findings table** — `finding | location (file:line) | type (complexity / control-flow / data-flow / standard / security) | severity | recommendation`. Order critical first; weight toward `risk_areas`.

Read-only with respect to the code under analysis — the report is the only file written; do not modify source. This complements `/qa:static-review` (review of requirements/test basis), `/qa:coverage-measure` (structural coverage of the same code), and `/qa:security-scan` (security SAST); route confirmed defects to `/qa:triage`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.reports_dir`/`docs_dir`, `tooling.security.sast`, `gates`/limits, `risk_areas`) is honored; no path or tool is hardcoded, and depth is weighted toward `risk_areas.critical`/`high` (Principle 4).
- [ ] **Evidence-based** — every finding cites a concrete `file:line` and a measured metric (complexity/nesting/size), not a prose claim; analyzer signals were confirmed by reading the code (false positives discarded).
- [ ] **Measurable** — the report states counts (units over each threshold, findings by severity) and the four metrics per unit rather than narrative.
- [ ] **Read-only honored** — no source code was modified; the report at `<paths.reports_dir>/STATIC-ANALYSIS.md` is the only file written.
- [ ] **Routing complete** — security findings routed to `/qa:security-scan`, coverage to `/qa:coverage-measure`, confirmed defects to `/qa:triage`; no orphaned recommendation.
- [ ] **Residual risk stated** — name what static analysis does NOT cover (it finds defects, not their absence — Principle 1; runtime/behavioral defects need dynamic testing) and the ISO/IEC 25010 maintainability sub-characteristics left at risk.
