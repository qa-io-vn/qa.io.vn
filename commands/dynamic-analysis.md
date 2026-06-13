---
description: Plan and run dynamic analysis — detect runtime defects like memory/resource leaks, handle exhaustion, and performance degradation while the system executes. Produces an ISO/IEC/IEEE 29119-3 Test Execution Log extended with profiling/leak evidence. Use to find faults that only appear at runtime.
argument-hint: "<feature / flow / endpoint>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Dynamic analysis: $ARGUMENTS

**ISTQB process:** Dynamic analysis — analyzing the system **while it runs** to find defects (memory/resource leaks, handle exhaustion, runtime degradation) that are hard or impossible to find statically. Dynamic analysis is a technical-test-analyst topic (CTAL-TTA stream, a Specialist-track syllabus — **not** CTFL Foundation); verify the exact section against the current syllabus rather than asserting a number. Complements **static analysis** (`/qa:static-analysis`, code without executing) and **performance testing** (`/qa:perf-test`, workload-driven soak/load).

## Project config (read first — do not proceed without it)
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init before analyzing"
```

## Step 0 — config, stack & argument guards (run before anything else)

1. **Config guard.** If the block above printed `MISSING`, stop and recommend `/qa:qa-init`; do not invent paths, tools, load profiles, or thresholds. Otherwise read `paths.*`, `tooling.*`, `gates`, and `risk_areas` and honor them throughout.
2. **Argument resolution.** Resolve the analysis target from `$ARGUMENTS`:
   - **If `$ARGUMENTS` is non-empty:** that flow/endpoint is the target.
   - **If `$ARGUMENTS` is empty:** do not guess. Ask which flow/endpoint to analyze. If the user defers, default the target to the **first item in `risk_areas.critical`** from config (the highest-risk area — e.g. checkout/auth/payments), state that default explicitly, and proceed.
3. **Stack & profiler validation.** Detect the runtime from the codebase (`package.json` / `go.mod` / `*.csproj` / `requirements.txt` / `pom.xml`) and confirm a profiler is available for that stack:
   - Node.js → `node --inspect`, heap snapshots, clinic.js
   - JVM → JProfiler, YourKit
   - Python → py-spy, memory_profiler
   - .NET → dotTrace
   - Go → pprof
   If the required profiler is missing or the stack is unrecognized, **stop and note it**, then offer install guidance (e.g. "Stack detected as Node.js — install clinic.js via `npm install --save-dev @clinic/clinic`, or use `node --inspect` with Chrome DevTools"). The process below (baseline → run under load → snapshot → trend → root-cause) is universal; only the tools vary.
4. **Environment note.** Dynamic analysis requires a production-like environment for valid results. If only a dev environment is available, state this as a fidelity caveat up front (it constrains the residual-risk statement at the end).

## Step 1 — define the scenario (test basis)

State, in writing, before running anything:
- **Target flow(s)/endpoint** (from Step 0).
- **Load profile** — ops/sec / RPS, sourced from `gates.performance` or `risk_areas` in config (or, if a `<paths.docs_dir>/PERF-PLAN-*.md` exists, from its workload model). Do not invent a number.
- **Duration** — run for **at least 8 hours OR at least 500 iterations** under realistic load (whichever the environment allows; record which was used and why).
- **Baseline resource metrics to capture at t=0** — heap/RSS memory, open file handles, sockets, DB-connection-pool usage, thread-pool usage, event-listener count, cache/queue size.

## Step 2 — instrument & validate baseline

5. Wire the stack-specific profiler from Step 0. **Capture the baseline (t=0) snapshot and confirm it succeeds before committing to the full run** — a failed baseline invalidates every later delta.

## Step 3 — execute & capture snapshots

6. Run for the planned duration. Capture a snapshot of every baseline metric at the **25% / 50% / 75% / 100%** marks (heap dumps, connection-pool state, handle/listener counts). This yields **5 datapoints per metric** (baseline + 4), satisfying the ≥3-snapshot gate below.

## Step 4 — analyze, trend & detect leaks

7. For each monitored resource, plot the t=0 → 25 → 50 → 75 → 100% series and apply these explicit decision rules:
   - **Leak candidate:** the resource grows **> 5% from baseline without releasing back** by run-end (monotonic upward trend, not noise).
   - **No leak:** growth ≤ 5%, **or** the resource rises under load and returns toward baseline (expected churn).
   - **Severity** (used in the work product and routing): **low** = < 2% growth; **medium** = 2–5% growth; **high** = > 5% growth **OR** an unbounded/unknown resource **OR** a crash/OOM during the run.
8. Also screen for: connection-pool / thread-pool saturation, unbounded caches/queues, response-time creep over the soak window (degradation distinct from peak-load behavior), and unhandled rejections / dangling references surfaced by the profiler.
9. Correlate the timeline of any flagged growth with APM/logs to isolate a **suspected** root cause, and produce evidence (growth curves, snapshot diffs, dumps).

## Step 5 — quality gate (9 points; do not publish until all pass)

10. Before writing the report, verify every item:
    - [ ] (a) Baseline (t=0) captured and validated.
    - [ ] (b) ≥ 3 snapshots from distinct time intervals (the 25/50/75/100% schedule gives 4 plus baseline).
    - [ ] (c) Each metric shows a clear trend, not noise (monotonic vs. churn distinguished).
    - [ ] (d) Leak verdict applies the explicit > 5%-without-release rule, not intuition.
    - [ ] (e) Root-cause correlation is grounded in logs/APM, not asserted.
    - [ ] (f) Severity justified by **% growth AND business impact** (crash/OOM vs. minor bloat).
    - [ ] (g) Load profile and duration are config/plan-sourced, not invented.
    - [ ] (h) Environment fidelity (prod-like vs. dev) is stated as a caveat.
    - [ ] (i) Residual risk stated: "Inconclusive — further investigation needed" **or** "Strong evidence of leak in [component] — recommend code review/fix."

## Output — work product

Produce an **ISO/IEC/IEEE 29119-3 Test Execution Log**, extended with profiling data and leak analysis (this command does **not** have a dedicated template; for any confirmed-defect narrative, follow the incident-report structure in `templates/defect-report-template.md`). Write it to `<paths.docs_dir>/DYNAMIC-ANALYSIS-<scope>.md` with:

- **Scenario summary** — target, load profile, duration, environment fidelity.
- **Baseline metrics table:**

  `| Metric | Baseline (t=0) | Final | Growth % | Threshold | Severity | Status | Root cause (suspected) |`

- **Time-series trend** per resource (memory / handles / connections / pools / listeners).
- **APM/log correlation** for each flagged metric.
- **Leak severity** per the Step 4 rule (low < 2% / medium 2–5% / high > 5% or unknown/crash).
- **Suspected root-cause analysis** and **residual risk** (from gate item (i)).

**Routing:** if a leak or anomaly is **confirmed** (growth > 5% / high severity), it becomes an incident — route to `/qa:triage` to file the defect report. Tie long-duration / soak runs to `/qa:perf-test` (which routes runtime correlation back here). For static counterparts use `/qa:static-analysis`. Note explicitly where specialist profiling tools or a production-like environment are required.

**Traceability:** record **basis** (soak scenario, e.g. "`/qa:perf-test checkout soak`"), **monitored resources** (coverage items), **result** (leak found / inconclusive), **defect ID** (from `/qa:triage`, if filed), and **status** (open / in-progress / resolved) — keep this chain bidirectional.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `paths.docs_dir` (output location), `tooling.*` (profiler/stack), `gates.performance`/`risk_areas` (load profile and the empty-args default to `risk_areas.critical`) are honored; no paths, load numbers, or thresholds are hardcoded.
- [ ] **Traceability intact** — the chain basis (soak scenario) -> monitored resources (coverage items) -> result -> defect (`/qa:triage`, if filed) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states per-resource Growth % vs. the 5% threshold with a severity and pass/fail status, not prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects): a single soak window is point-in-time, depends on environment/data fidelity, and surfaces only leaks that manifest within the run duration.
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Execution Log (extended with profiling/leak analysis) and written to `<paths.docs_dir>/DYNAMIC-ANALYSIS-<scope>.md`.
