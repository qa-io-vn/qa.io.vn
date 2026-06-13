---
description: Diagnose a failing CI pipeline or test run, classify the cause, and propose or apply a fix without masking product defects. Writes a Confirmation Test Execution Log. Use when the build/pipeline is red, tests fail in CI but pass locally, or the user pastes a CI log.
argument-hint: "[path to log file or pasted error]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fix the failing CI / pipeline

**ISTQB process:** Quality in DevOps — CI/CD pipeline and test-environment management, with **confirmation testing** to verify a fix (CTFL v4.0 §6; DevOps; confirmation testing per the ISTQB Glossary). Fix test/env/pipeline causes without masking product defects. CT-TAE (Test Automation Engineering, Specialist) informs maintainability practices — verify any Specialist references against the current syllabus; this command does not assert a Foundation section it cannot trace.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## CI definition + recent results
```!
echo "--- CI file (discovery) ---"; cat Jenkinsfile 2>/dev/null || cat .github/workflows/*.yml 2>/dev/null || cat .gitlab-ci.yml 2>/dev/null || cat azure-pipelines.yml 2>/dev/null || echo "no CI file found"
echo "--- last reports/results (discovery) ---"; ls -1 reports test-results playwright-report 2>/dev/null; find . -name "*.xml" -path "*results*" 2>/dev/null | head
```

## Your task

> **Config-read guard.** First read `qa.config.yml` above. If it is `none`/missing, ask the user for `ci.platform`, `tooling.e2e`, `paths.reports_dir`, and `risk_areas.critical`, or proceed with explicit, stated assumptions. Resolve every `<tooling.*>` / `<paths.*>` / `<stack.*>` / `<ci.*>` reference below from this config — never hardcode a tool, path, or CI platform. The CI file and reports detected above are a **discovery** step; treat their findings as inputs, not as the configured source of truth.

The user may have passed a log path or error text in `$ARGUMENTS`.

1. **Resolve scope.**
   - If `$ARGUMENTS` is non-empty: read the referenced log file (if a path) or use the pasted text as the failure under analysis.
   - If `$ARGUMENTS` is empty: use the most recent results discovered above (newest JUnit/XML or report under `<paths.reports_dir>`). If none are discoverable, ask the user to paste the CI log or point to a failing run before proceeding — do not guess a failure.

2. **Classify the failure** into exactly one primary category (record it; list secondary contributors if any):
   1. Real product defect — the test correctly asserts behavior the product gets wrong.
   2. Flaky / non-deterministic test.
   3. Environment / config issue (missing service, secret, headless/browser image, unseeded data).
   4. Dependency / version drift (lockfile, `<ci.agents_docker_image>`, `<tooling.e2e>` / browser version mismatch).
   5. Timeout / resource exhaustion.
   6. Pipeline misconfiguration (stage order, caching, shard merge, JUnit/report publishing).

3. **Find the root cause, not the symptom**, applying these decision rules:
   - **Real product defect (Cat. 1)** → do **not** alter the test to make it pass. Leave it asserting correct behavior and **escalate via `/qa:triage`** (severity/priority and defect report). Stop here for the fix; record it in the log as "deferred to /qa:triage".
   - **Flaky (Cat. 2)** → do **not** add blind retries or raise timeouts. Hand off to **`/qa:flaky-hunt`** (quarantine + deterministic fix).
   - **Local-pass / CI-fail (Cat. 3)** → diff the environments: missing services/secrets, headless vs headed `<tooling.e2e>` config, `<ci.agents_docker_image>`, timing/parallelism (`ci.shard_count`), or unseeded `<test_data>`.
   - **Dependency drift (Cat. 4)** → check the lockfile and `<ci.agents_docker_image>` against the `<tooling.e2e>` / browser versions in config.
   - **Pipeline (Cat. 6)** → check stage order, caching, shard merge, and JUnit/report publishing into `<paths.reports_dir>`.

4. **Propose the fix; apply it only if safe and in-scope.**
   - In-scope, low-risk edits (test, fixture, `<tooling.*>` config, CI definition under `<ci.platform>`) → apply directly.
   - Risky or out-of-scope changes (touching product code, secrets, infra) → explain and **ask before applying**. Product-code defects route to `/qa:triage`, never patched here.

5. **Run confirmation testing.** Re-run the previously failing test(s) with the configured `<tooling.e2e>` runner to confirm the fix resolves the failure and introduces no new ones. If the environment cannot reproduce CI, state that explicitly and describe how to verify in `<ci.platform>`.

## Output — Confirmation Test Execution Log (ISO/IEC/IEEE 29119-3)

Produce a **Test Execution Log / Test Results** work product (ISO/IEC/IEEE 29119-3) scoped to this confirmation run, and **write it to `<paths.reports_dir>/CI-FIX-LOG-<date>.md`**. Include:
- **Failure under analysis** — source (`$ARGUMENTS` or discovered run), CI platform (`<ci.platform>`).
- **Classification** — primary category (1–6) and rationale; secondary contributors.
- **Root cause** — the underlying cause, not the symptom.
- **Change made / proposed** — exact files/config touched, or "deferred to /qa:triage" for product defects.
- **Confirmation result** — counts of tests re-run / passed / failed / still-failing, and how to verify in `<ci.platform>`.
- **Routing** — any handoff issued (`/qa:triage` for defects, `/qa:flaky-hunt` for flakiness).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `ci.platform`, `<tooling.e2e>`, `<paths.reports_dir>`, `<ci.agents_docker_image>`, `gates`, and `risk_areas` in scope are honored; nothing hardcoded.
- [ ] **No defect masked** — no real product defect was hidden by a test/timeout/retry change; any Cat. 1 finding is routed to `/qa:triage` with the test left asserting correct behavior (ISTQB Principle 1).
- [ ] **Confirmation evidence** — the log states counts (re-run / passed / failed / still-failing), not prose claims; unreproducible cases are flagged with a CI verification path.
- [ ] **Routing reciprocated** — flakiness → `/qa:flaky-hunt`, product defects → `/qa:triage`; handoffs recorded in the log.
- [ ] **Work product named** — output is identified as a Test Execution Log / Test Results (ISO/IEC/IEEE 29119-3) and written to `<paths.reports_dir>/CI-FIX-LOG-<date>.md`.

Never "fix" a red pipeline by masking a product defect, adding blind retries, or raising timeouts alone.
