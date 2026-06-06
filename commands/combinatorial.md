---
description: Design combinatorial test cases for features with many parameters — pairwise, classification tree, or orthogonal arrays — to get strong coverage with few cases. Use when several inputs/options combine and exhaustive testing is infeasible.
argument-hint: "<feature with multiple parameters>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Combinatorial test design: $ARGUMENTS

**ISTQB process:** Combinatorial test techniques — pairwise, classification tree, orthogonal arrays (CTAL Test Analyst; Advanced, beyond CTFL v4.0). Realizes Principle 2 (exhaustive testing is impossible).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS` — a feature whose behavior depends on **multiple parameters** (e.g. checkout = {payment method × shipping × currency × user tier × coupon}). Exhaustive combinations explode; combinatorial techniques cover the important interactions with far fewer cases.

1. **Model the parameters** — list each parameter and its values/partitions (use EP to reduce each parameter to representative values first). Note invalid values and constraints (combinations that can't co-occur).
2. **Choose a technique:**
   - **Pairwise (all-pairs)** — cover every pair of parameter values at least once; strong defect detection for far fewer cases. Default choice.
   - **Classification tree** — visualize parameters as a tree and select combinations deliberately; good for documenting coverage.
   - **Orthogonal arrays** — balanced statistical coverage when applicable.
   - Raise to higher strength (3-wise) only for the highest-risk interactions.
3. **Generate the combination set** honoring constraints (exclude invalid pairings). Show the resulting cases as a table.
4. **Add boundary/negative cases** that combinatorics alone won't catch, for high-risk parameters.
5. **Traceability & coverage** — state the technique, strength (e.g. pairwise), and the interaction coverage achieved vs the full Cartesian size (show the reduction).

Output the combinatorial test cases to `<paths.docs_dir>/COMBINATORIAL-<feature>.md` (compatible with the test-case spec), and offer to automate them **data-driven** via `/qa:implement` or `/qa:api-automate`. Label these as an **Advanced (CTAL-TA)** technique, not CTFL Foundation.
