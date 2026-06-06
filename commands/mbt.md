---
description: Apply Model-Based Testing — build a behavioral model (e.g. state machine) and derive test cases from it. Use for complex stateful flows where model coverage beats ad-hoc cases.
argument-hint: "<feature / stateful flow>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Model-Based Testing: $ARGUMENTS

**ISTQB process:** Model-Based Testing (CT-MBT Specialist; relates to state-transition testing, CTFL §4).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target stateful flow from `$ARGUMENTS` (e.g. order lifecycle, payment/3DS, session, subscription states). If empty, ask.

1. **Build the model** — capture the behavior as a model from the test basis: a state-transition diagram/table (states, events, transitions, guards, actions) or a decision/flow model. Represent it explicitly (a table or Mermaid `stateDiagram`).
2. **Choose coverage criteria** — e.g. all-states, all-transitions (0-switch), all transition-pairs (1-switch), or all-paths to a bound. State which you target and why (risk-based).
3. **Generate test cases** from the model to meet the chosen coverage, including **invalid transitions** (negative testing). Each case lists the path, events, expected states/outputs, and the coverage it contributes.
4. **Traceability** — link model elements to the test basis and the resulting cases.
5. Output the model + derived cases to `<paths.docs_dir>/MBT-<feature>.md`, and offer to implement them via `/qa:implement`.

Keep the model maintainable — it becomes the single source for regenerating tests when behavior changes (counters the pesticide paradox).
