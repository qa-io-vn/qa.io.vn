---
description: Evaluate usability and user experience (distinct from accessibility) using ISTQB usability-testing methods and heuristics. Use to assess how usable a feature or flow is.
argument-hint: "<feature / flow>"
allowed-tools: Read, Glob, Grep, Bash
---

# Usability evaluation: $ARGUMENTS

**ISTQB process:** Usability testing (CT-UT; ISO/IEC 25010 usability). Complements `/qa:a11y-audit` (accessibility).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS`. If empty, ask which feature/flow.

1. Evaluate against ISO 25010 **usability** sub-characteristics: appropriateness recognizability, learnability, operability, user-error protection, UI aesthetics, accessibility (defer detailed a11y to `/qa:a11y-audit`).
2. Apply **heuristic evaluation** (e.g. Nielsen's heuristics): visibility of system status, match to the real world, user control/freedom, consistency, error prevention, recognition over recall, flexibility, minimalist design, helpful error messages, help/documentation.
3. Define **usability test scenarios / tasks** a real user would perform, with success criteria (task completion, errors, efficiency) — usable for moderated or unmoderated sessions.
4. Review forms/flows for user-error protection and clear, actionable error messaging.
5. Output findings: heuristic violations (severity-rated), task scenarios, and recommendations, to `<paths.docs_dir>/USABILITY-<feature>.md`.

ISTQB usability testing involves real users for full validity; flag where human sessions are needed versus what can be evaluated heuristically here. Read-only on code.
