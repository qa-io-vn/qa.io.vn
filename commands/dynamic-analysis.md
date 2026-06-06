---
description: Plan and run dynamic analysis — detect runtime defects like memory/resource leaks, handle exhaustion, and performance degradation while the system executes. Use to find faults that only appear at runtime.
argument-hint: "<feature / flow / endpoint>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Dynamic analysis: $ARGUMENTS

**ISTQB process:** Dynamic analysis (CTAL-TTA §4) — analyzing the system **while it runs** to find defects that are hard to find statically.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS`. Dynamic analysis observes the running system to surface latent runtime defects:

1. **Memory & resource leaks** — run the target flow repeatedly / under sustained load and watch for growth that never releases: heap/memory, file handles, sockets, DB connections, event listeners. Tie long-duration runs to `/qa:perf-test` (soak) and watch the trend.
2. **Resource exhaustion** — connection-pool/thread-pool saturation, unbounded caches/queues.
3. **Performance degradation over time** — response-time creep during soak (distinct from peak-load behavior).
4. **Wild pointers / unhandled rejections / dangling references** — surfaced via runtime instrumentation, profilers, or leak detectors appropriate to the stack (Node `--inspect`/heap snapshots, clinic.js, OS counters).

Approach:
- Define the scenario and the resource metrics to capture, and a clean baseline.
- Instrument/profile during execution; capture before/after and trend data; correlate with APM if available.
- Report findings with evidence (growth curves, snapshots), suspected root cause, and severity.

Output a dynamic-analysis report to `<paths.docs_dir>/DYNAMIC-ANALYSIS-<scope>.md`. Note where specialist profiling tools or a production-like environment are required. Complements static analysis (`/qa:static-analysis`) and performance testing (`/qa:perf-test`).
