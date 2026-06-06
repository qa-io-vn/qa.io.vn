---
description: Diagnose a failing CI pipeline or test run and propose or apply a fix. Use when the build/pipeline is red, tests fail in CI but pass locally, or the user pastes a CI log.
argument-hint: "[path to log file or pasted error]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fix the failing CI / pipeline

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## CI definition + recent results
```!
echo "--- CI file ---"; cat Jenkinsfile 2>/dev/null || cat .github/workflows/*.yml 2>/dev/null || cat .gitlab-ci.yml 2>/dev/null || echo "no CI file found"
echo "--- junit/last reports ---"; ls -1 reports test-results 2>/dev/null; find . -name "*.xml" -path "*results*" 2>/dev/null | head
```

## Your task

The user may have passed a log path or error text in `$ARGUMENTS` — read it if so.

1. **Classify the failure**: real product defect, flaky test, environment/config issue, dependency/version drift, timeout/resource, or pipeline misconfiguration.
2. **Find root cause**, not the symptom:
   - Local-pass/CI-fail → look for env differences, missing services/secrets, headless/browser image, timing, parallelism, or unseeded data.
   - Flaky → hand off to the `/qa:flaky-hunt` approach (quarantine + fix); don't just add blind retries.
   - Dependency → check lockfile / `ci.agents_docker_image` / Playwright browser version mismatch.
   - Pipeline → check stage order, caching, shard merge, `junit`/report publishing.
3. Propose the fix clearly; apply it if it's safe and in-scope (edit the test, fixture, config, or `Jenkinsfile`). For risky changes, explain and ask first.
4. If possible, reproduce locally to confirm the fix.

Report: the diagnosis, the root cause, the change made, and how to verify it in CI.
