---
description: Plan and run session-based exploratory testing with charters. Use for experience-based testing of a feature, especially high-risk or newly changed areas.
argument-hint: "<feature / area to explore>"
allowed-tools: Read, Glob, Grep, Bash
---

# Exploratory testing: $ARGUMENTS

**ISTQB process:** Experience-based test techniques — exploratory / session-based testing (CTFL v4.0 §4.4).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS`. If empty, ask what to explore.

1. **Write test charters** (session-based test management): for the feature, define focused charters — "Explore <area> with <resources> to discover <information>." Time-box each (e.g. 60–90 min).
2. **Guide the exploration** with ISTQB experience-based thinking: error guessing (where defects likely hide), checklist-based heuristics (boundaries, error handling, interruptions, concurrency, data extremes, security/permissions, usability), and tours (feature tour, money/risk tour, configuration tour).
3. Since execution is interactive, produce: the charters, concrete things to try and to watch for, oracles (how to recognize a problem), and a **session sheet template** to record observations, bugs, questions, and coverage.
4. Tie findings back to risk — exploratory complements, not replaces, the scripted coverage. Log defects via `/qa:triage` and convert reproducible escapes into automated regression tests via `/qa:implement`.

Output charters + session sheet to `<paths.docs_dir>/EXPLORATORY-<feature>.md`.
