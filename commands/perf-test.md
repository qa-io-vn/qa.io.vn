---
description: Script (and optionally run) a K6 performance test for an endpoint or journey, with pass/fail thresholds derived from qa.config.yml gates/SLAs. Produces an ISO/IEC/IEEE 29119-3 Test Execution Log. Use for load, stress, spike, or soak testing (CT-PT execution).
argument-hint: "<endpoint or journey> [load|stress|spike|soak]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# K6 performance test: $ARGUMENTS

**ISTQB process:** Test implementation & execution — performance testing (CT-PT, a Specialist syllabus — not CTFL Foundation). Scripts and gates the workload model from `/qa:perf-plan`. Tests **performance efficiency** (and, for soak, **reliability**) per ISO/IEC 25010.

## Project config (read first — do not proceed without it)
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init before scripting"
```

## Step 0 — config & argument guards (run before anything else)

1. **Config guard.** If the block above printed `MISSING`, stop and recommend `/qa:qa-init`; do not invent paths, tools, or thresholds.
2. **Tooling gate.** If `tooling.performance` is not `k6` (e.g. `none` or another tool), tell the user K6 is disabled in config, offer to enable it (`tooling.performance: k6`), and stop until confirmed.
3. **Argument resolution.** Parse `$ARGUMENTS` as `<target> [type]`:
   - `type` defaults to `load` when omitted; valid values are `load | stress | spike | soak`.
   - **If `$ARGUMENTS` is empty:** do not guess. Ask which endpoint or journey to model. If the user defers, default the target to the first item in `risk_areas.critical` from config (the highest-risk area), state that default explicitly, and proceed.
4. **Plan check.** If a `<paths.docs_dir>/PERF-PLAN-*.md` exists, derive the workload model, transaction mix, and acceptance criteria from it; otherwise note that no `/qa:perf-plan` exists and seed targets from `gates.performance` alone.

## Step 1 — build the K6 script

Write the script to `<paths.tests_dir>/performance/` (TypeScript/JS), parameterized by environment and load profile. Select stages by `type`:

| type | stage shape | decision rule |
|---|---|---|
| **load** | ramp to `gates.performance.target_rps`, hold, ramp down | verifies SLAs at expected peak |
| **stress** | ramp **beyond** target until degradation | find the breaking point / capacity ceiling |
| **spike** | sharp VU jump, then observe recovery | resilience to sudden surge |
| **soak** | moderate load held for an extended duration | reliability / memory-leak / resource drift |

Use realistic data, think-times, and the API base URL from config. Model the **journey** (transaction mix from the plan), not a single-endpoint hammer, where relevant.

## Step 2 — encode pass/fail thresholds from config (gates/SLAs)

Derive `options.thresholds{}` **only** from `gates.performance` so a breach **fails the run** (non-zero exit). Do not hardcode numbers — read each from config; the values below are placeholders showing the schema:

```js
export const options = {
  thresholds: {
    // from gates.performance.p95_ms / p99_ms (response-time SLAs)
    http_req_duration: ['p(95)<{{gates.performance.p95_ms}}', 'p(99)<{{gates.performance.p99_ms}}'],
    // from gates.performance.error_rate_max (error-rate ceiling)
    http_req_failed: ['rate<{{gates.performance.error_rate_max}}'],
    // from gates.performance.target_rps (throughput floor)
    http_reqs: ['rate>{{gates.performance.target_rps}}'],
  },
  // per-type stages built in Step 1 (load/stress/spike/soak)
  scenarios: { /* ... */ },
};
```

If a `gates.performance` field is absent, state which SLA is unverified rather than substituting a guessed value.

## Step 3 — wire the runner and output

Add an npm/make script (matching `<tooling.*>` conventions) to run the test and write a JSON summary (`--summary-export`) to `<paths.reports_dir>`. This JSON summary plus the K6 console output **is** the Test Execution Log (see Step 5).

## Step 4 — optional smoke execution

If a non-production target environment is available **and** the user opts in, run a short smoke profile and report p95/p99/error-rate vs. the encoded thresholds, stating pass/fail per threshold. **Never run load tests against production.**

After execution, remind the user to correlate results with server-side APM (`/qa:dynamic-analysis`) to locate the real bottleneck, and to feed gated results into `/qa:status-report` (in-cycle) or `/qa:release-report` (completion).

## Work product

This command produces an **ISO/IEC/IEEE 29119-3 Test Execution Log / Test Results** (the K6 JSON summary under `<paths.reports_dir>`) plus the executable **Test Procedure** (the K6 script under `<paths.tests_dir>/performance/`). It does **not** produce a performance test plan — that is `/qa:perf-plan`'s `PERF-PLAN-<scope>.md`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `tooling.performance`, `gates.performance.*`, `paths.tests_dir`, `paths.reports_dir`, and `risk_areas.critical` (for the empty-args default) are honored; no thresholds, paths, or tools are hardcoded.
- [ ] **Thresholds gate the run** — every `gates.performance` SLA is encoded in `options.thresholds{}` so a breach yields a non-zero exit; any absent SLA is flagged as unverified, not guessed.
- [ ] **Measurable** — execution output states p95/p99/error-rate/throughput as numbers with pass/fail per threshold, not prose.
- [ ] **Traceability intact** — the script traces to the workload model/acceptance criteria in `PERF-PLAN-*.md` (or, absent a plan, to `gates.performance`); the journey reflects the transaction mix.
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Execution Log (JSON summary) under `<paths.reports_dir>`, with the K6 script as the Test Procedure under `<paths.tests_dir>/performance/`.
- [ ] **Residual risk stated** — name what is NOT covered (ISTQB Principle 1): a single load profile is not exhaustive; results depend on environment/data fidelity, are point-in-time, and must be correlated with APM before any go/no-go decision. Load tests were not run against production.
