---
description: Measure and report test coverage — structural (statement/branch), requirements/test-basis, and risk coverage. Use to quantify how much is actually covered and where the holes are.
argument-hint: "[scope or path]"
allowed-tools: Read, Glob, Grep, Bash
---

# Coverage measurement${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test monitoring — coverage measurement (CTFL v4.0 §4, §5.3; white-box coverage per CTAL-TTA).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Coverage data
```!
echo "--- coverage report ---"; ls -1 coverage 2>/dev/null; cat coverage/coverage-summary.json 2>/dev/null | head -20
echo "--- unit tool ---"; grep -i "coverage\|c8\|nyc\|istanbul" package.json 2>/dev/null | head
```

## Your task

Scope from `$ARGUMENTS`. Distinguish the ISTQB coverage dimensions and report each:

1. **Structural (white-box) coverage** — statement and branch coverage from the unit/component coverage report. Identify under-covered modules, especially in `risk_areas.critical`. Note that 100% is rarely the goal — coverage is a guardrail, not a target to game (Principle: absence-of-errors fallacy).
2. **Test-basis / requirements coverage** — which requirements, user stories, and OpenAPI endpoints have test cases (functional coverage). Use the traceability chain.
3. **Risk coverage** — are all critical/high `risk_areas` covered at the appropriate test levels and types?
4. **Coverage-item coverage** — for designed cases, which coverage items (equivalence partitions, boundaries, decision rules, states) are exercised vs missed.

Output a coverage report: dimension | measured | target | gaps (prioritized by risk). Recommend the highest-value additions and offer `/qa:test-design` / `/qa:implement` to close them. Read-only.
