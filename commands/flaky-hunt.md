---
description: Find flaky/non-deterministic tests, quarantine them, and propose deterministic fixes. Use when tests intermittently fail or the user mentions flakiness.
argument-hint: "[test path or N runs]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Hunt flaky tests

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

1. Identify flakiness sources by scanning the suite for anti-patterns: `waitForTimeout`/hard sleeps, CSS/XPath selectors coupled to styling, tests depending on order or shared mutable state, unmocked time/network, race conditions, and reliance on retries to pass. Use Grep.
2. If feasible, run the suspect tests repeatedly to confirm non-determinism:
   `npx playwright test <path> --repeat-each=10` (adjust to the project).
3. For each confirmed flaky test:
   - **Quarantine**: tag it (e.g. `test.fixme` or a `@flaky` tag excluded from the gate) so it stops blocking the pipeline.
   - **Fix the cause**, not the symptom: replace hard waits with web-first assertions, swap brittle selectors for `getByRole`/`data-testid`, isolate data, mock time/network, remove order dependence.
   - Open a tracking note with a 1-sprint fix SLA per the strategy.
4. Report: list of flaky tests, root cause each, fix applied or proposed, and current quarantine size (a quality signal — flag if growing).

Never "fix" flakiness by increasing retries or timeouts alone.
