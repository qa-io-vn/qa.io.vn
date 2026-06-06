---
description: Quickly add a single focused test case from a plain-English description. Use for one-off "add a test that ..." requests.
argument-hint: "<what the test should verify>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Add a test: $ARGUMENTS

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Add one focused test for: `$ARGUMENTS`. If empty, ask what to verify.

1. Pick the **right level** (unit/API/component/E2E) for what's being verified — don't E2E something an API test proves.
2. Find the matching existing spec file (Grep/Glob) and add the case there; only create a new file if none fits.
3. Reuse fixtures/page objects/api-clients. Stable selectors, web-first assertions, self-owned data, no hard waits.
4. Run just that test and confirm it passes (or report why it fails — which may be a real defect → suggest `/qa:triage`).

Keep it minimal and consistent with surrounding tests.
