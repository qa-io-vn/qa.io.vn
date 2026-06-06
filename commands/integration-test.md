---
description: Design integration testing — component integration and system integration, with an integration strategy (incremental vs big-bang) and test doubles. Use to test interactions between components or systems.
argument-hint: "<components / systems / interface>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Integration testing: $ARGUMENTS

**ISTQB process:** Component integration & system integration testing — test levels (CTFL v4.0 §2.2.2, §2.2.4).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS` (which components/systems/interface). Distinguish the two ISTQB integration levels:

1. **Component integration testing** — interactions and interfaces **between integrated components** of the system (e.g. service ↔ repository, module ↔ module). Focus on the interfaces and data passed, not the components' internal logic.
2. **System integration testing** — interactions between the system and **other systems / external services** (payment, email, third-party APIs). Use service virtualization / mocking (`tooling.mocking`) for unstable or costly externals, backed by contract testing (`/qa:contract-sync`).

Design the integration tests:
- **Choose an integration strategy** — prefer **incremental** (top-down / bottom-up / functional) over **big-bang** so faults are easier to localize. State which and why.
- Identify the **interfaces** to exercise and the **stubs/drivers/mocks** needed.
- Cover the interface contract: correct data, error propagation, timeouts/failures of the other side, sequencing, and transaction/rollback behavior.
- Apply EP/BVA/decision-table to interface inputs; cover negative and failure paths (the integration points are where defects cluster).

Implement at the API/integration level (Playwright `request`, `/qa:api-automate`) where possible. Run, report interface coverage, and note which externals are virtualized vs hit for real. Keep tests independent and parallel-safe.
