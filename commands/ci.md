---
description: Autonomous red-build workflow — pull the latest CI build's failures (any platform), triage every failure into buckets, fix the test/environment/flake causes and confirm each locally, harden fixed tests to green ×3, escalate real product defects without masking them, and write a Test Execution Log. Use after a red build to triage and fix the whole build end-to-end. Pass 'x' or 'full' for the extended mandatory-stability + full-suite gate.
argument-hint: "['x' or 'full' for the extended stability + full-suite gate] [build/run URL | build number | 'last']"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Triage & fix the red build end-to-end — pull, classify, fix, harden, report

**ISTQB process:** Quality in DevOps — CI/CD triage with **confirmation testing**, plus **defect management** (CTFL v4.0 §1.4 test process; §2.2 change-related test types; §5.5 defect management; §6 test tools / Quality-in-DevOps — verify the section numbers against the current syllabus). Take a red build to green by fixing the test / environment / flake causes and **confirming each fix locally**, while real product defects are escalated, never masked (Principle 1: testing shows the presence of defects, not their absence). CT-TAE (Test Automation Engineering, Specialist) informs the maintainability/stability practices — verify any Specialist reference against the current syllabus.

> **Positioning — this is the build-wide orchestrator.** For a single pasted log or one pipeline failure use `/qa:fix-ci`; for a Jenkins-only pull-and-fix use `/qa:fix-jenkins`. This command pulls the **whole** failing build on **any** CI platform, triages **every** failure into a bucket, fixes the fixable ones, and adds a **stability-hardening gate (green ×3)** on top — then optionally verifies the full suite.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Latest CI build — failures (discovery)
```!
ARG="$ARGUMENTS"
# Strip a leading mode token (x|full) so it is never mistaken for a build reference.
BUILD=$(echo "$ARG" | sed -E 's/^[[:space:]]*(x|full)([[:space:]]+|$)//I')
PLATFORM=$(grep -E '^\s*platform:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*platform:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
echo "--- CI platform (config): ${PLATFORM:-unknown} · build ref: ${BUILD:-last} ---"
case "$PLATFORM" in
  jenkins)
    URL=$(grep -E '^\s*jenkins_url:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*jenkins_url:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
    JOB=$(grep -E '^\s*jenkins_job:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*jenkins_job:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
    JOBPATH=$(echo "$JOB" | sed 's#/#/job/#g')
    AUTH=""; [ -n "$JENKINS_USER" ] && [ -n "$JENKINS_API_TOKEN" ] && AUTH="-u $JENKINS_USER:$JENKINS_API_TOKEN"
    TREE="suites[cases[className,name,status,errorDetails,errorStackTrace]]"
    REF="$BUILD"; echo "$REF" | grep -qE '^[0-9]+$' || REF="lastCompletedBuild"
    if echo "$BUILD" | grep -qE '^https?://'; then
      curl -s $AUTH "${BUILD%/}/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
    elif [ -n "$URL" ] && [ -n "$JOB" ] && [ -n "$AUTH" ]; then
      curl -s $AUTH "$URL/job/$JOBPATH/$REF/testReport/api/json?tree=$TREE" | head -c 12000 || echo "fetch failed"
    else
      echo "Jenkins not auto-reachable (need jenkins_url + jenkins_job in config and JENKINS_USER/JENKINS_API_TOKEN in env, or pass a build URL)."
    fi
    ;;
  github-actions)
    if command -v gh >/dev/null 2>&1; then
      echo "--- latest failed GitHub Actions run (gh) ---"
      gh run list --status failure --limit 1 2>/dev/null || echo "gh run list failed (auth?)"
      RID=$(gh run list --status failure --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null)
      [ -n "$RID" ] && gh run view "$RID" --log-failed 2>/dev/null | head -c 12000
    else
      echo "gh CLI not found — authenticate gh, or pass a run URL, or use the local artifacts below."
    fi
    ;;
  *)
    echo "Platform '${PLATFORM:-unset}' has no auto-pull here — pass a build/run reference, or use the local result artifacts below."
    ;;
esac
REPORTS=$(grep -E '^\s*reports_dir:' qa.config.yml 2>/dev/null | head -1 | sed -E 's/.*reports_dir:[[:space:]]*//; s/[[:space:]]*#.*$//; s/"//g; s/[[:space:]]*$//')
echo "--- local result artifacts (discovery fallback) ---"; find . -name "*.xml" -path "*result*" 2>/dev/null | head; ls -1 "${REPORTS:-reports}" 2>/dev/null
echo "--- already-documented defects / known issues (do NOT re-fix these) ---"; ls -1 "${REPORTS:-reports}/defects" 2>/dev/null | head
```

## Mode & scope

> **Config-read guard.** Read `qa.config.yml` above first. If it is `none`/missing, tell the user to run `/qa:qa-init`, or proceed with explicit, stated assumptions for `ci.platform`, `<tooling.*>` (the runner), `<paths.reports_dir>`, `gates`, and `risk_areas.*`. Resolve every `<tooling.*>` / `<paths.*>` / `<stack.*>` / `<ci.*>` reference below from this config — **never hardcode** a tool, path, CI platform, or token. The CI/local data above is a **discovery** step; treat it as input, not as the configured source of truth.

Parse `$ARGUMENTS` into a **mode** and an optional **build reference**:

- If the first whitespace-separated token is `x`, `X`, or `full` → **EXTENDED mode = ON**; the build reference is the *second* token (may be empty → latest completed build).
- Otherwise → **EXTENDED mode = OFF** (plain `/qa:ci`); the build reference is the *first* token (may be empty → latest completed build).

Never pass the mode token (`x`/`full`) as a build reference. **Neither mode commits, pushes, or triggers a CI/CD run** — all verification is local-only; the only difference is how thorough that local verification is:

- **OFF** (`/qa:ci`, `/qa:ci 412`): run steps 1–5 and stop. The step-3.5 green-×3 loop is best-effort here.
- **ON** (`/qa:ci x`, `/qa:ci full 412`): run steps 1–5 **and** step 6 (full local-suite verification). In this mode the step-3.5 green-×3 loop is a **hard gate** — no fix is "done" until it passes 3/3 locally.

Track the steps with a TodoWrite list and work through them **in order**.

## Your task

### 1. Pull the failing set
Resolve the source by this fixed precedence (stop at the first that yields data):
1. A build/run URL or build number passed in `$ARGUMENTS`.
2. The configured CI (`ci.platform` + `ci.jenkins_url`/`ci.jenkins_job`, or `gh` for `github-actions`) — auth from env (`JENKINS_USER`/`JENKINS_API_TOKEN`, or `gh auth`), **never hardcode tokens**.
3. Local result artifacts discovered above (JUnit/XML under `<paths.reports_dir>` or the runner's output).
4. Nothing reachable → ask the user to paste the failing report or point to a run. **Do not guess at failures.**

Extract only cases that are genuinely **failed** (status FAILED/REGRESSION; ignore PASSED/FIXED/SKIPPED). Where the source distinguishes reruns, count a case as failing only if it **never passed across reruns** — so the set is real, reproducible failures, not flake the rerun already absorbed. Record the failed set as a numbered list; for each capture: class/suite, test name, error detail, stack trace. State the count **`N`** — this is the baseline step 4 must clear, and list the failing cases to the user before starting. If `N = 0`, report "build is green, nothing to fix" and stop.

### 2. Triage each failure into a bucket
For every failed case, locate the test in the repo (Grep by title/file), read its trace, and classify into **exactly one** primary bucket. **First check already-documented issues** — defects under `<paths.reports_dir>/defects/` and any known-flaky/known-infra list — and do **not** re-"fix" a documented product defect or known-infra item:

| Bucket | Signal | Action |
|---|---|---|
| **A — Test defect** | Bad selector/locator, wrong wait, stale hardcoded data, race, assertion-logic error, broke after a UI/contract change | **Fix it** (step 3) |
| **B — Product defect** | App returns 5xx/error, missing/contract-broken behavior — reproducible, and the test correctly asserts the right behavior | **Change no code.** Escalate via `/qa:triage` (step 4) |
| **C — Environment / infra** | Service down, missing seed/secret, browser image, cold-boot/timeout, timezone | Note it; fix only if the fix belongs in the test layer (self-seeding data, resilient wait). Else report as environmental |
| **D — Flaky / non-deterministic** | Passes/fails without a code change; timing-dependent | Stabilize the root cause in step 3.5; hand deep cases to `/qa:flaky-hunt`. **Never** mask with blind retries |

When unsure between **A** and **B**, inspect the **real behavior** before deciding (run the flow / hit the endpoint / view the live UI with whatever the project provides) — do not guess. Record the bucket per case.

### 3. Fix the fixable causes (A + fixable C)
For each, make the **smallest correct change rooted in the trace evidence** (not guesswork), consistent with the repo's existing conventions, and preserve traceability to the requirement/condition. Then **confirm it locally**:
- Use the configured runner from `<tooling.*>` for the relevant `<stack.*>` (read it from config — do not assume a tool), **reruns disabled** so a pass is real, targeting **only** the failed file(s)/title(s), never the whole suite.
- Map each fix to its case from step 1's numbered set so the result is traceable case-by-case.
- Iterate fix → run, capping at **3 attempts per case**. A fix is "done" only when that local run is green; if it still fails after the cap, carry it into step 5 as still-red (never weaken/skip it to go green). Group failures that share one root cause — fix once, verify the group.

> **Guardrail:** never force a pass by weakening/deleting assertions, skipping a case, adding blind retries, or raising timeouts alone. A masked defect is worse than a red build.

### 3.5 Stability hardening (green ×3)
A single green run is not proof of stability. For every Bucket-A / fixable-C / Bucket-D test you touched, run it **3 times back-to-back** with reruns disabled and record pass/fail per iteration. **Triage each iteration's failure by its own trace** — it is often a *different* root cause than the original (e.g. the fix lands but iteration 1 dies in setup = a cold-start flake, not the test logic). Prefer **root-cause hardening over masking**: stable/ scoped selectors, the configured runner's web-first/auto-waiting assertions, isolated test data, resilient (additive, happy-path-unchanged) setup. Never `waitForTimeout`-style sleeps; never raise the rerun count to hide a flake. Re-run the loop after hardening until green ×3.

> In **EXTENDED mode** this 3/3 outcome is a **hard gate**: do not proceed to step 6 until every fixed test is green ×3. In plain mode it is best-effort — but report the honest `n/3` either way. If a cause is genuinely environmental and your hardening is best-effort, say so with the iteration evidence (e.g. "5/6 → 3/3 after the guard; can't guarantee 100% — depends on backend responsiveness").

### 4. Escalate product defects (Bucket B) — never mask
For each confirmed product defect, **change no code** and raise it via **`/qa:triage`**, which writes an ISO/IEC/IEEE 29119-3 **Incident (Defect) Report** using the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md` — with **severity** (impact on the test object) and **priority** (urgency, from the affected `risk_areas` tier) set independently, and the release-blocker flag from `gates.block_on_severity`. Leave the test asserting correct behavior. Note any new product defect as a candidate for the project's known-defect exclusion list (do not edit that list yourself unless asked). Deep/intermittent flakiness → hand off to **`/qa:flaky-hunt`**.

### 5. Report
Print a single summary table back to the user:

| Case | Bucket | Action taken | Local confirm | Stability (3×) |
|---|---|---|---|---|
| … | A/B/C/D | Fixed: <what> / Escalated via /qa:triage / Env | ✅ green / n/a | 3/3 / 2/3 / n/a |

Then state **counts, not prose**: `N` pulled; fixed-by-bucket (A / fixable-C / D); escalated as Incident Reports (B); confirmed-green; green-×3; still-red (list each with its reason). List the files changed so the user can review the diff. **Honesty rule:** if a fix is a symptom-patch rather than a root-cause cure, or a case could not be verified locally (needs the live env / a down service), say so plainly — do not claim green.

**Safety — both modes:** do **not** commit, push, or trigger a CI/CD run unless the user explicitly asks. End by telling them which fixed cases pass locally and are ready to commit / re-run in `<ci.platform>`. In plain mode, **stop here**; in EXTENDED mode, continue to step 6.

### 6. Full local-suite verification (EXTENDED mode only)
**Precondition gate:** do not proceed unless every Bucket-A / fixable-C / D test is green ×3 in step 3.5. Bucket-B product defects and unfixable environmental cases do not block this (they were never expected to pass). Then run the **whole suite locally** with the configured runner, reruns disabled (honest first-pass signal), **excluding the documented known-defect / known-infra cases** so the run isn't polluted by failures already triaged in step 2/4. For each *new* failure the suite surfaces: triage it (step 2 buckets), fix Bucket-A/C/D under the step-3/3.5 rules and harden to green ×3, escalate new Bucket-B defects via `/qa:triage`. Iterate steps 3 → 3.5 → 6 until the only remaining failures are documented known defects. Append a full-suite-result column to the step-5 table and a one-line verdict. **Still no commit, push, or CI/CD trigger** — leave the tree for the user to review.

## Output — Test Execution Log / Test Results (ISO/IEC/IEEE 29119-3)

Produce a **Test Execution Log / Test Results** work product scoped to this triage run and **write it to `<paths.reports_dir>/CI-TRIAGE-LOG-<date>.md`**. Include:
- **Build under analysis** — source (`$ARGUMENTS` / configured CI / local artifacts), `ci.platform`, build/run reference, mode (plain / extended).
- **Failing set** — the `N` pulled cases, each with its bucket (A/B/C/D) and rationale.
- **Fixes** — exact files/config touched per case (or "escalated to /qa:triage" for Bucket B), with root cause (not symptom).
- **Confirmation + stability** — per case: local confirm result and the `n/3` stability outcome; in extended mode, the full-suite result.
- **Escalations** — Bucket-B Incident (Defect) Reports raised via `/qa:triage` (defect IDs).
- **Routing** — handoffs issued (`/qa:flaky-hunt`, `/qa:triage`, `/qa:fix-ci`, `/qa:fix-jenkins`).
- **Residual risk** — still-red cases, best-effort flake hardening, and what was *not* verified.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `ci.platform`, `jenkins_url`/`jenkins_job` (or `gh`), `<tooling.*>` runner, `<paths.reports_dir>`, `gates`, and `risk_areas.*` are read from `qa.config.yml`; no tool, path, CI platform, or token is hardcoded.
- [ ] **No defect masked** — no real product defect was hidden by a test/timeout/retry/assertion change; every Bucket-B finding is escalated via `/qa:triage` as an Incident (Defect) Report with the test left asserting correct behavior (Principle 1).
- [ ] **Confirmation + stability evidence** — each fix was re-run locally on the previously-failed set with reruns disabled; stability is stated as the `n/3` result (not prose), and extended mode reports the green-×3 gate + full-suite outcome.
- [ ] **Measurable** — output states counts (`N` pulled, fixed-by-bucket, escalated, confirmed-green, green-×3, still-red), not prose claims.
- [ ] **Routing reciprocated** — flakiness → `/qa:flaky-hunt`, product defects → `/qa:triage`, single log/pipeline → `/qa:fix-ci`, Jenkins-only pull → `/qa:fix-jenkins`; handoffs recorded in the log.
- [ ] **Safety honored** — no commit, push, or CI/CD trigger was performed unless the user explicitly asked; verification is local-only.
- [ ] **Work product named** — output is identified as a **Test Execution Log / Test Results** (ISO/IEC/IEEE 29119-3) written to `<paths.reports_dir>/CI-TRIAGE-LOG-<date>.md`, with product defects raised as **Incident (Defect) Reports**.

Never "fix" a red build by masking a product defect, weakening assertions, adding blind retries, or raising timeouts alone — and never commit, push, or trigger a CI run unless the user asks.
