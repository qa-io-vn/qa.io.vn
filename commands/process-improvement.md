---
description: Assess the test process maturity and recommend improvements using ISTQB/TMMi-style analysis. Use for retrospectives, test process audits, or when escaped defects/flakiness/slow pipelines suggest the process needs work.
argument-hint: "[focus area]"
allowed-tools: Read, Glob, Grep, Bash
---

# Test process improvement${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test process improvement (CTAL-TM; ISTQB Expert "Improving the Test Process"; TMMi / TPI models; IDEAL cycle).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Signals from the repo
```!
echo "--- test counts ---"; find tests -name "*.spec.*" 2>/dev/null | wc -l
echo "--- flaky markers ---"; grep -rl "@flaky\|test.fixme\|skip(" tests 2>/dev/null | wc -l
echo "--- CI file ---"; ls -1 Jenkinsfile .github/workflows/*.yml 2>/dev/null
```

## Your task

1. **Assess** the current test process against the ISTQB test-process activities and good practices. Use a maturity lens (TMMi levels: Initial → Managed → Defined → Measured → Optimization) — identify which practices are in place vs missing (test policy, strategy, planning, risk-based testing, test design techniques, monitoring/metrics, defect management, configuration management, automation maturity, non-functional coverage).
2. **Diagnose** from real signals: escaped-defect trend, flaky-test count, pipeline duration, coverage gaps, missing test types, untracked traceability.
3. **Recommend** improvements with the **IDEAL** structure (Initiating, Diagnosing, Establishing, Acting, Learning): prioritized actions, expected benefit, effort, and owner. Quick wins first, then structural changes.
4. Output a **Test Process Improvement Report** to `<paths.docs_dir>/PROCESS-IMPROVEMENT-<date>.md`.

Read-only analysis. Tie each recommendation to a concrete ISTQB practice and, where possible, a toolkit command that implements it.
