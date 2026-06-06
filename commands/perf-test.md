---
description: Generate (and optionally run) a K6 performance test for an endpoint or journey, with thresholds from qa.config.yml. Use for load, stress, spike, or soak testing.
argument-hint: "<endpoint or journey> [load|stress|spike|soak]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# K6 performance test: $ARGUMENTS

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

If `tooling.performance` is not `k6`, tell the user it's disabled in config and offer to enable it. Target + type come from `$ARGUMENTS` (default type: load). If empty, ask which endpoint/journey.

1. Build a K6 script under `tests/performance/` (TypeScript/JS), parameterized by environment and load profile:
   - **load**: ramp to `gates.performance.target_rps`, hold, ramp down.
   - **stress**: ramp beyond target until degradation.
   - **spike**: sharp VU jump, observe recovery.
   - **soak**: moderate load for an extended duration.
2. Encode `thresholds{}` from `gates.performance` so a breach **fails the run** (e.g. `http_req_duration: ['p95<500','p99<1000']`, `http_req_failed: ['rate<0.01']`).
3. Use realistic data, think-times, and the API base URL from config. Model the journey, not a single-endpoint hammer, where relevant.
4. Add an npm/make script to run it and output a JSON summary to `paths.reports_dir`.
5. If a target environment is available and the user wants it, run a short smoke profile and report p95/p99/error-rate vs. thresholds. Never run load tests against production.

Remind the user to correlate results with server-side APM to find the real bottleneck.
