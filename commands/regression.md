---
description: Select, prioritize, and optimize the regression test set using impact analysis. Use when deciding what to regression-test for a change, or to keep the regression suite lean.
argument-hint: "[change / area / release]"
allowed-tools: Read, Glob, Grep, Bash
---

# Regression test selection${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Change-related testing — regression strategy (CTFL v4.0 §2.3.4; CTAL-TM regression approaches).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Change signals
```!
echo "--- recent changes ---"; git diff --name-only HEAD~5 2>/dev/null | head -30 || echo "no git history"
```

## Your task

Change/scope from `$ARGUMENTS` (or infer from recent diffs above).

1. **Impact analysis** — determine what the change affects directly and indirectly (shared modules, APIs, data, UI flows). Map affected areas to `risk_areas`.
2. **Select the regression set** using an ISTQB strategy appropriate to risk/time:
   - **Retest-all** only when risk is high and time allows.
   - **Risk-based selective regression** — prioritize tests covering impacted + high-risk areas.
   - **Test-case prioritization** — order by risk, change proximity, and historical defect density so the most valuable tests run first.
3. **Optimize the suite** — flag redundant/obsolete regression tests for removal (pesticide paradox), and tests better pushed to a lower level.
4. Output: the selected/prioritized regression set (with rationale), what was deprioritized, and a recommended CI placement (PR smoke vs nightly full).

Read-only analysis. Pair with `/qa:flaky-hunt` to keep the suite trustworthy.
