---
description: Design testing in production (shift-right) — synthetic monitoring, observability checks, canary/A-B validation, feature-flag and post-deploy smoke testing. Use to verify quality in the live environment safely.
argument-hint: "[feature / journey]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Shift-right / testing in production: $ARGUMENTS

**ISTQB process:** Testing in DevOps — shift-right, continuous testing, monitoring (Quality in DevOps; CTFL v4.0 §2.1 SDLC/DevOps). Complements pre-release (shift-left) testing.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Scope from `$ARGUMENTS` (critical journey/feature, else the core flows). Shift-right validates quality in the real environment, where pre-release testing can't fully reach — done **safely**, read-only, never destructive on production data.

1. **Post-deploy smoke / synthetic monitoring** — scripted checks of critical journeys running continuously against production (read-only, synthetic accounts), alerting on failure. Define the journeys, cadence, and alert thresholds.
2. **Observability-based testing** — define the signals to watch (SLIs: latency, error rate, saturation) and the SLOs that constitute "healthy"; verify logging/metrics/tracing actually expose what's needed to detect issues.
3. **Progressive delivery validation** — canary and **A/B** checks: compare the new version's key metrics against baseline before full rollout; define rollback criteria.
4. **Feature-flag testing** — verify behavior with flags on/off and safe rollback via flag kill-switch.
5. **Production health gates** — post-deploy checks that confirm the release is healthy and the rollback plan works.

Approach: implement synthetic checks with the existing framework (Playwright/K6 against prod-safe endpoints), wire alerting, and document what's monitored. **Never** run load or destructive tests against production; use synthetic data and read-only paths.

Output a shift-right plan to `<paths.docs_dir>/SHIFT-RIGHT-<scope>.md` and any synthetic-check scripts under `paths.tests_dir`. Pair with `/qa:dynamic-analysis` (runtime issues) and `/qa:release-report` (post-deploy verification).
