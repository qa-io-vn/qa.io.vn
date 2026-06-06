---
description: Pull the latest Jenkins build's failed test cases, fix each one, then re-run only those cases locally until they all pass. Use to triage and fix a red Jenkins build end-to-end.
argument-hint: "[jenkins build URL | job path]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fix failing Jenkins tests, then verify locally

**ISTQB process:** Test execution + defect management + **confirmation testing** (CTFL v4.0 §1.4, §5.5). Re-test fixed cases to confirm resolution — without masking real product defects.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Pull latest Jenkins results
```!
ARG="$ARGUMENTS"
URL=$(grep -E '^\s*jenkins_url:' qa.config.yml 2>/dev/null | sed 's/.*: *//; s/"//g; s/#.*//; s/ *$//')
JOB=$(grep -E '^\s*jenkins_job:' qa.config.yml 2>/dev/null | sed 's/.*: *//; s/"//g; s/#.*//; s/ *$//')
JOBPATH=$(echo "$JOB" | sed 's#/#/job/#g')
AUTH=""; [ -n "$JENKINS_USER" ] && [ -n "$JENKINS_API_TOKEN" ] && AUTH="-u $JENKINS_USER:$JENKINS_API_TOKEN"
TREE="suites[cases[className,name,status,duration,errorDetails,errorStackTrace]]"
if echo "$ARG" | grep -qE '^https?://'; then
  echo "--- testReport from build URL ---"
  curl -s $AUTH "${ARG%/}/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
elif [ -n "$URL" ] && [ -n "$JOB" ] && [ -n "$AUTH" ]; then
  echo "--- testReport from $URL /job/$JOBPATH /lastCompletedBuild ---"
  curl -s $AUTH "$URL/job/$JOBPATH/lastCompletedBuild/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
else
  echo "Jenkins not auto-reachable (need jenkins_url + jenkins_job in config and JENKINS_USER/JENKINS_API_TOKEN in env, or pass a build URL)."
  echo "--- local JUnit artifacts fallback ---"; find . -name "*.xml" -path "*results*" 2>/dev/null | head; ls -1 reports test-results 2>/dev/null
fi
```

## Your task

Goal: take every test case that **failed in the latest Jenkins build**, fix it, and prove the fix by running **those cases** locally until they all pass.

### 1. Get the failed cases
Use the Jenkins data above. Sources, in order of preference: a build URL passed in `$ARGUMENTS`; the configured `jenkins_url`/`jenkins_job` via the Jenkins REST API (auth from `JENKINS_USER`/`JENKINS_API_TOKEN` env — never hardcode tokens); or local JUnit XML artifacts; or ask the user to paste the report. Extract the cases with status **FAILED** or **REGRESSION** (ignore PASSED/FIXED/SKIPPED). For each: class/suite, test name, error detail, stack trace.

### 2. Diagnose each failure (classify — do NOT blindly make it green)
For every failed case, locate the test in the repo (Grep by title/file) and determine the root cause:
- **Test defect** — wrong selector, bad assertion, outdated expectation, race/timing → fix the test.
- **Flaky / non-deterministic** → stabilize the root cause (web-first assertions, stable selectors, isolate data); see `/qa:flaky-hunt`. Do not just add retries.
- **Environment / data / config** — CI-only differences (missing service, seed, secret, browser image, timezone) → fix the setup/fixture.
- **Real product defect** — the application is genuinely wrong. **Do NOT alter the test to hide it.** Raise it via `/qa:triage` (severity vs priority), leave the test asserting correct behavior, and report it as needing a code fix by the team.

> Guardrail: never force a pass by weakening/deleting assertions or skipping a case to go green. A masked defect is worse than a red build.

### 3. Fix
Apply the fix for test/flaky/environment causes (edit the spec, fixture, page object, data factory, or CI config). Keep changes minimal and consistent with existing conventions. Preserve traceability to the requirement/condition.

### 4. Re-run the failed cases locally (confirmation testing)
Run **only the previously-failed set** locally and confirm green:
- Playwright: `npx playwright test <files>` or target titles with `-g "<title>"`.
- Map each failed case to its spec/title; run them together.
Iterate fix→run until **all previously-failed cases pass** locally (cap retries; if a case still fails after a reasonable attempt, stop and report it).

### 5. Report
Summarize: failed cases pulled (N) → fixed (by cause: test/flaky/env), real product defects escalated to `/qa:triage` (not silenced), and the local run result confirming the fixed set is green. List any still-red cases and why. Suggest committing the fixes so the next Jenkins build verifies them.
