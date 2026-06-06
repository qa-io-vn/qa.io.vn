---
description: Plan performance testing per ISTQB CT-PT — objectives, SLAs, operational profiles, workload model, system/data needs, test types, entry/exit. Produces a performance test plan that feeds /qa:perf-test. Use before scripting load tests.
argument-hint: "[release / system area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Performance test plan${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Performance Testing planning (CT-PT). Precedes scripting/execution in `/qa:perf-test`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Your task

Scope from `$ARGUMENTS` (release or system area). If `tooling.performance` is `none`, note it and offer to enable. Produce a CT-PT performance test plan:

1. **Objectives** — what questions the testing answers (capacity, responsiveness under load, stability over time, scalability, resource usage).
2. **Performance acceptance criteria / SLAs** — response-time targets (p95/p99), throughput (target RPS), error-rate ceiling, resource limits. Seed from `gates.performance`; refine with Product/SRE.
3. **Operational profiles & workload model** — identify the key user types and **transaction mix**, expected and peak volumes, concurrency, think-times, data volumes, and arrival patterns. Model realistic load, not single-endpoint hammering.
4. **Performance test types to run** — choose from load, stress, spike, soak/endurance, capacity/scalability — and why each, per risk.
5. **System & data requirements** — a production-like environment (never prod), production-scale data, monitoring/APM in place to find bottlenecks (not just symptoms).
6. **Performance risks** — likely bottlenecks (DB, external calls, caching, N+1), and which workload targets them.
7. **Entry/exit criteria & schedule** — when perf testing runs (nightly/pre-release), and what result gates the release (SLA breach = fail).
8. **Metrics & reporting** — what to capture and trend over releases.

Write the plan to `<paths.docs_dir>/PERF-PLAN-<scope>.md`. Then `/qa:perf-test <endpoint|journey>` scripts and runs each modeled scenario with thresholds derived from this plan.
