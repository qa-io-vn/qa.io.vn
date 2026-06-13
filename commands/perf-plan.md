---
description: Plan performance testing per ISTQB CT-PT — objectives, SLAs, operational profiles, workload model, system/data needs, test types, entry/exit. Produces a performance test plan that feeds /qa:perf-test. Use before scripting load tests.
argument-hint: "[release / system area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Performance test plan

**ISTQB process:** Performance Testing planning — Performance Testing specialist syllabus (CT-PT). The plan follows the Test Plan structure of ISO/IEC/IEEE 29119-3 and is driven by risk (risk-based testing; CTFL v4.0 §5.2 — verify the section against the current syllabus). It precedes scripting/execution in `/qa:perf-test`. Target quality characteristic: **performance efficiency** (ISO/IEC 25010).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Your task

**Config guard.** If `qa.config.yml` is MISSING above, stop and tell the user to run `/qa:qa-init` first. Otherwise honor it: read `paths.*`, `gates.performance`, `risk_areas` (critical/high/medium), `environments`, `test_data`, and `tooling.performance`; never hardcode project-specific paths, tools, SLAs, or areas.

**Scope resolution (do this first):**
1. If `$ARGUMENTS` is non-empty, the scope is the release or system area named there.
2. If `$ARGUMENTS` is empty, default the scope to the areas in `risk_areas.critical`; state that you defaulted and list which areas were used. (If `risk_areas.critical` is also empty, ask the user for the release or system area and stop.)
3. If `tooling.performance` is `none`, note that performance tooling is disabled in config and offer to enable it before continuing.

Produce a performance test plan (ISO/IEC/IEEE 29119-3 Test Plan, scoped to performance) with these sections, in order:

1. **Objectives** — list the specific questions the testing answers (capacity, responsiveness under load, stability over time, scalability, resource usage). One objective per question; tie each to a `risk_areas` entry or an SLA.
2. **Performance acceptance criteria / SLAs** — carry the `gates.performance` values **verbatim**: response-time targets (`checkout_p95_ms`, `p99_ms`), throughput (`target_rps`), error-rate ceiling (`error_rate_pct`), and any resource limits. State each as a pass/fail rule (e.g. `p95 < checkout_p95_ms` = pass). Refine with Product/SRE only by adding to config, not by overriding it inline.
3. **Operational profile & workload model** — for each key user type, tabulate the **transaction mix** (% of total), expected and peak volumes, concurrency, think-times, data volumes, and arrival pattern. Model realistic mixed load, not single-endpoint hammering. State the assumptions and their source (analytics, SRE, estimate).
4. **Performance test types to run** — select from load, stress, spike, soak/endurance, capacity/scalability. For each selected type give a one-line rule: which `risk_areas` entry or objective justifies it. Mark types **not** run and why.
5. **System & data requirements** — choose the test environment from `environments` (pick the non-prod entry whose `purpose` covers perf, typically `staging`; **never** prod). Require production-scale data per `test_data`, and monitoring/APM to locate bottlenecks (not just symptoms). Name the chosen environment explicitly.
6. **Performance risks & traceability** — list likely bottlenecks (DB, external calls, caching, N+1) as product (quality) risks. For each, record: source `risk_areas` tier, the workload/test type that targets it, and the SLA it threatens. This is the risk-register-to-workload trace; keep it bidirectional (every critical/high `risk_areas` entry maps to at least one modeled scenario, and every scenario traces back to a risk or objective).
7. **Entry & exit criteria** — **Entry:** environment provisioned and production-like, scripts available, monitoring on, baseline captured. **Exit:** every `gates.performance` SLA met (or a waived deviation recorded); any SLA breach = fail/no-go. State each criterion as a checkable condition, not prose.
8. **Schedule** — when perf testing runs (nightly / pre-release) relative to the release in scope.
9. **Metrics & reporting** — list the metrics to capture (p95, p99, error rate, throughput, resource saturation) and how they trend over releases.

Write the plan to `<paths.docs_dir>/PERF-PLAN-<scope>.md` (create the directory if needed). No dedicated perf-plan template exists; mirror the Test Plan structure in `${CLAUDE_PLUGIN_ROOT}/templates/plan-template.md` for document control, scope, and entry/exit sections.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `gates.performance`, `risk_areas`, `environments`, `test_data`, `tooling.performance`) is honored; SLAs are carried verbatim; nothing hardcoded.
- [ ] **Workload model complete** — each key user type has a transaction mix (% summing to ~100), concurrency, think-times, volumes, and arrival pattern, with assumptions and their source stated.
- [ ] **Risk traceability intact** — every critical/high `risk_areas` entry maps to at least one modeled scenario, and every scenario/test type traces back to a risk or objective; bidirectional, no orphans.
- [ ] **Entry/exit measurable** — entry and exit criteria are checkable conditions; every `gates.performance` SLA appears in exit criteria as a pass/fail rule (breach = fail).
- [ ] **Non-prod environment named** — the chosen environment is a specific non-prod entry from `environments`; production is explicitly excluded.
- [ ] **Residual risk stated** — name what this plan does NOT cover and why (e.g. profiles not modeled, load below true peak) — CTFL v4.0 Principle 1: testing shows the presence, not the absence, of defects.
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Plan (performance scope) and written to the correct `<paths.docs_dir>` location.

End by pointing to the file. Then `/qa:perf-test <endpoint|journey>` scripts and runs each modeled scenario with thresholds derived from this plan.
