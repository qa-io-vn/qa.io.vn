---
description: Implement or extend automated tests for a feature at the right pyramid level (E2E, API, component, contract). Use when the user wants to write/add tests for a specific feature or story.
argument-hint: "<feature or story description>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Implement tests for: $ARGUMENTS

**ISTQB process:** Test implementation + execution (CTFL v4.0 §1.4) — turn test cases into test procedures/scripts and run them. If test cases don't exist yet, design them first with `/qa:test-design`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Existing framework
```!
echo "--- tests tree ---"; ls -1R tests 2>/dev/null | head -60
echo "--- playwright config? ---"; ls -1 playwright.config.* 2>/dev/null
```

## Your task

Target feature is `$ARGUMENTS`. If empty, ask which feature/story to cover. If `qa.config.yml` or the framework is missing, suggest `/qa:qa-init` / `/qa:scaffold` first.

1. Read the OpenAPI spec at `stack.api_spec_path` (if present) for the endpoints this feature touches.
2. Decide coverage by the **test pyramid** and the feature's risk tier (`risk_areas`):
   - Logic → unit (note for devs if not your layer).
   - Endpoints → **API tests** (happy, negative, boundary, authz/role matrix, schema validation against the spec).
   - UI behavior → **component** tests where possible, **E2E** only for the real user journey.
   - Interface stability → **contract** (Pact) if enabled.
   - Non-functional → flag perf/a11y/security needs if the feature is high/critical risk.
3. Reuse existing fixtures, page objects, and typed API clients — extend, don't duplicate. Follow the conventions already in the repo.
4. Write the tests using stable selectors (`getByRole`/`getByLabel`/`data-testid`), web-first assertions, no hard waits. Each test owns its data via factories.
5. Run the new tests if feasible (`npx playwright test <path>`) and fix failures.

Summarize what you added, at which levels, and any gaps you intentionally left (with reasons).
