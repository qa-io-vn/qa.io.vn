---
description: Evaluate and select test tools using the ISTQB tool-selection process (benefits, risks, categories, pilot). Use when choosing a new testing tool or justifying the current toolchain.
argument-hint: "<tool category or need, e.g. 'visual testing', 'API mocking'>"
allowed-tools: Read, Glob, Grep, Bash, WebSearch
---

# Test tool selection: $ARGUMENTS

**ISTQB process:** Test tools (CTFL v4.0 §6; CT-TAE for automation tooling).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Need/category from `$ARGUMENTS`. If empty, ask what capability is needed.

1. **Classify** the need by ISTQB tool category (test management, static analysis, test design/data, test execution/automation, performance, defect management, CI/CD, specialized non-functional).
2. **Define selection criteria**: fit with the existing stack (`stack`, `tooling`, `ci.platform`), language alignment (prefer TS/JS to match the team), integration with CI and reporting, learning curve, licensing/cost, maintenance burden, community/support, and vendor lock-in risk.
3. **Survey candidates** (search the web for current options if helpful) and score them against the criteria in a comparison matrix.
4. **Assess benefits and risks** of introducing the tool, per ISTQB (benefits: repeatability, coverage, efficiency; risks: unrealistic expectations, maintenance, over-reliance, integration cost).
5. **Recommend** one option plus a **pilot/PoC plan** (evaluate on a small scope before rollout) and the success criteria for the pilot.

Output a tool evaluation to `<paths.docs_dir>/TOOL-EVALUATION-<category>.md`. Keep recommendations grounded in this project's actual constraints, not generic.
