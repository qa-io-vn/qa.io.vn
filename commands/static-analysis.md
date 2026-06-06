---
description: Run static analysis of source code — complexity, control/data flow, coding-standard and maintainability metrics — without executing it. Use to assess code quality and find defects early. Distinct from reviewing the test basis (/qa:static-review).
argument-hint: "[path / module]"
allowed-tools: Read, Glob, Grep, Bash
---

# Static analysis${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Static analysis (CTFL v4.0 §3.1; CTAL-TTA §3 — control-flow, data-flow, complexity). A form of static testing — code is analyzed, not executed.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Tooling signals
```!
echo "--- linters/analyzers ---"; grep -iE "eslint|sonar|semgrep|tsc|coverage" package.json 2>/dev/null | head
echo "--- sast in config ---"; grep -A4 "security:" qa.config.yml 2>/dev/null | grep sast
```

## Your task

Scope from `$ARGUMENTS` (path/module, else high-risk areas). Static analysis examines code structure to find defects and quality issues early (Principle 3, shift-left):

1. **Run the analyzers** available (`tooling.security.sast`, ESLint, `tsc --noEmit`, SonarQube/Semgrep if present) and collect findings.
2. **Code metrics** — assess **cyclomatic complexity**, nesting depth, function/file size, and maintainability; flag overly complex units (defect-prone, hard to test — defects cluster here).
3. **Control-flow / data-flow concerns** — unreachable code, infinite loops, uninitialized/unused variables, null-dereference risks, missing returns (where analyzers surface them).
4. **Coding standards & security patterns** — violations, injection sinks, unsafe APIs (coordinate with `/qa:security-scan`).
5. **Prioritize** findings by severity and risk area; recommend refactors that improve testability.

Output a static-analysis report: finding | location | type (complexity/flow/standard/security) | severity | recommendation. Read-only — analyze and report; do not modify code. This complements `/qa:static-review` (review of requirements/test basis) and `/qa:coverage-measure` (structural coverage).
