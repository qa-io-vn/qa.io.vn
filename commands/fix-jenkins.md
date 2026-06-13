---
description: Pull the latest Jenkins build's failed test cases, fix each one, then re-run only those cases locally until they all pass. Use to triage and fix a red Jenkins build end-to-end.
argument-hint: "[jenkins build URL | job path]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fix failing Jenkins tests, then verify locally

**ISTQB process:** Test execution + defect management + **confirmation testing** (CTFL v4.0 §1.4 test process; §2.2 change-related test types; §5.5 defect management; §6 test tools / Quality-in-DevOps — verify section numbers against the current syllabus). Re-test fixed cases to confirm resolution — without masking real product defects (Principle 1: testing shows the presence of defects, not their absence).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Pull latest Jenkins results
```!
ARG="$ARGUMENTS"
URL=$(grep -E '^\s*jenkins_url:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*jenkins_url:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
JOB=$(grep -E '^\s*jenkins_job:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*jenkins_job:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
JOBPATH=$(echo "$JOB" | sed 's#/#/job/#g')
AUTH=""; [ -n "$JENKINS_USER" ] && [ -n "$JENKINS_API_TOKEN" ] && AUTH="-u $JENKINS_USER:$JENKINS_API_TOKEN"
TREE="suites[cases[className,name,status,duration,errorDetails,errorStackTrace]]"
if echo "$ARG" | grep -qE '^https?://'; then
  echo "--- testReport from build URL ---"
  curl -s $AUTH "${ARG%/}/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
elif [ -n "$ARG" ] && [ -n "$URL" ] && [ -n "$AUTH" ]; then
  ARGPATH=$(echo "$ARG" | sed 's#/#/job/#g')
  echo "--- testReport from $URL /job/$ARGPATH /lastCompletedBuild ---"
  curl -s $AUTH "$URL/job/$ARGPATH/lastCompletedBuild/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
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
Use the Jenkins data above. Resolve the source by this fixed precedence (stop at the first that yields data):
1. A build URL or job path passed in `$ARGUMENTS`.
2. **If `$ARGUMENTS` is empty:** use the configured `jenkins_url`/`jenkins_job` via the Jenkins REST API (auth from `JENKINS_USER`/`JENKINS_API_TOKEN` env — never hardcode tokens).
3. If neither Jenkins source is reachable: parse local JUnit XML artifacts discovered above (`<paths.*>` test-output / reports location).
4. If nothing is available: ask the user to paste the Jenkins test report — do not guess at failures.

Extract only the cases with status **FAILED** or **REGRESSION** (ignore PASSED/FIXED/SKIPPED). Record the failed set as a numbered list; for each case capture: class/suite, test name, error detail, stack trace. State the count `N` of failed cases pulled — this is the baseline the run in step 4 must clear.

### 2. Diagnose each failure (classify — do NOT blindly make it green)
For every failed case, locate the test in the repo (Grep by title/file) and determine the root cause:
- **Test defect** — wrong selector, bad assertion, outdated expectation, race/timing → fix the test.
- **Flaky / non-deterministic** → stabilize the root cause (auto-waiting/web-first assertions for the configured `<tooling.e2e>`, stable selectors, isolate test data); hand off to `/qa:flaky-hunt`. Do not just add retries.
- **Environment / data / config** — CI-only differences (missing service, seed, secret, browser image, timezone) → fix the setup/fixture.
- **Real product defect** — the application is genuinely wrong. **Do NOT alter the test to hide it.** Raise it via `/qa:triage` (severity vs priority), leave the test asserting correct behavior, and report it as needing a code fix by the team.

> Guardrail: never force a pass by weakening/deleting assertions or skipping a case to go green. A masked defect is worse than a red build.

### 3. Fix
Apply the fix for test/flaky/environment causes (edit the spec, fixture, page object, data factory, or CI config). Keep changes minimal and consistent with existing conventions. Preserve traceability to the requirement/condition.

### 4. Re-run the failed cases locally (confirmation testing)
Run **only the previously-failed set** locally and confirm green — this run is the **confirmation test** that proves each fix resolved the failure:
- Use the configured runner from `<tooling.*>` for the relevant `<stack.*>` (do not assume a tool — read the config). Target the specific failed files/titles only (e.g. pass the spec paths, or filter by test title), never the whole suite.
- Map each failed case (from step 1's numbered set) to its spec/title; run them together so the result is traceable case-by-case.
- Iterate fix → run, capping at **3 attempts per case**. If a case still fails after the cap, stop iterating on it and carry it into step 5 as still-red (do not weaken it to pass).

Record the outcome as a **Test Execution Log / Test Results** work product (ISO/IEC/IEEE 29119-3): for each of the `N` previously-failed cases, its status (PASS/FAIL) after the fix.

### 5. Report
Produce a measurable summary (counts, not prose claims):
- **Pulled:** `N` failed cases.
- **Fixed**, broken down by cause: test defect / flaky / environment-config (give the count for each).
- **Escalated:** real product defects raised via `/qa:triage` as **Incident (Defect) Reports** (ISO/IEC/IEEE 29119-3) — never silenced; the test still asserts correct behavior.
- **Confirmation result:** from step 4's Test Execution Log — how many of the `N` now pass locally.
- **Still red:** list each remaining case and the reason (e.g. unresolved product defect, hit the 3-attempt cap).

Suggest committing the test/fixture/CI-config fixes so the next Jenkins build re-verifies them. **Routing:** `/qa:flaky-hunt` for deep flakiness stabilization; `/qa:triage` for product-defect incident reports; `/qa:fix-ci` for non-Jenkins pipeline failures.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — the runner/files were resolved from `qa.config.yml` (`<tooling.*>`, `<stack.*>`, `<paths.*>`) and `jenkins_url`/`jenkins_job`; no test command, path, or token is hardcoded.
- [ ] **Traceability intact** — every fixed/edited case still traces to its test basis (requirement/condition); assertions were strengthened or left correct, never weakened to go green. No previously-failed case was dropped or skipped to mask a defect.
- [ ] **Measurable** — output states counts: `N` pulled, fixed-by-cause, escalated, confirmed-green, still-red — not prose claims.
- [ ] **Confirmation testing honored** — the local re-run targeted only the previously-failed set and is recorded as a Test Execution Log; real product defects are escalated as Incident (Defect) Reports via `/qa:triage`, not silenced (Principle 1).
- [ ] **Work products named** — the confirmation run is identified as a **Test Execution Log / Test Results** and escalations as **Incident (Defect) Reports** (ISO/IEC/IEEE 29119-3).
