---
description: Estimate testing effort for a release, feature, or backlog using ISTQB estimation techniques (metrics-based and expert-based). Use for test planning, sprint capacity, or sizing a test effort.
argument-hint: "<release / feature / backlog scope>"
allowed-tools: Read, Glob, Grep, Bash
---

# Test estimation: $ARGUMENTS

**ISTQB process:** Test planning — estimation (CTFL v4.0 §5.1.4; CTAL-TM).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Scope from `$ARGUMENTS`. If empty, ask what to estimate.

1. Establish the scope: features/stories, their **risk levels** (`risk_areas`), and which test types/levels apply.
2. Apply both ISTQB estimation approaches and reconcile:
   - **Metrics-based** — use historical data where available (test-cases per story, defects per area, automation effort, execution time). Derive from the repo (existing test counts, CI durations) where possible.
   - **Expert-based** — bottom-up estimate per activity (analysis, design, implementation, execution, completion) and per test type.
3. Factor in: risk (higher risk → more depth), automation vs manual split, environment/data setup, regression scope, and a contingency buffer for uncertainty and flakiness.
4. Output an estimate: effort per activity and test type, total person-days, key assumptions, and confidence/risks to the estimate. Express as a range, not a false-precise single number.

Feed this into `/qa:create-plan` (schedule & resourcing). Read-only.
