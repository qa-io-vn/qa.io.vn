---
description: Derive test conditions and test cases from the test basis using ISTQB test design techniques (EP, BVA, decision table, state transition, ATDD). Use to design test cases for a feature, story, or endpoint.
argument-hint: "<feature / story / endpoint>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ISTQB test analysis & design for: $ARGUMENTS

**ISTQB process activities:** Test analysis + Test design (CTFL v4.0 §1.4, §4).

> For focused **test case generation** from a single requirement/story/endpoint (with the full Test Case Specification + CSV export), use `/qa:test-cases`. Use this command for broader design context across a feature.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Your task

Target from `$ARGUMENTS`. If empty, ask for the feature/story/endpoint.

1. **Test analysis** — read the **test basis** for this item: the user story + acceptance criteria, and the OpenAPI spec at `stack.api_spec_path` for the relevant endpoints. Identify and list **test conditions** (what to test). Flag any ambiguity/gaps in the basis as static-testing findings (suggest `/qa:static-review`).
2. **Test design** — derive **test cases** from the conditions using the appropriate ISTQB **techniques**, and record which technique and which **coverage items** each case exercises:
   Use the **CTFL v4.0 Chapter 4** categorization strictly:
   - **Black-box (§4.2):** Equivalence Partitioning (valid + invalid partitions); Boundary Value Analysis (2-value or 3-value form); Decision Table (one case per rule); State Transition (valid + invalid transitions, state the coverage).
   - **White-box (§4.3):** Statement and Branch testing/coverage — when source is in scope.
   - **Experience-based (§4.4):** Error Guessing, Exploratory, Checklist-Based — for risk areas and gaps.
   - **Collaboration-based (§4.5):** ATDD — acceptance-criteria cases as Given/When/Then.
   - *Advanced (CTAL-TA, not Foundation — label as such if used):* **domain analysis** (combine partitions/boundaries across related inputs), **defect-based** techniques (taxonomy-driven), pairwise/classification tree (→ `/qa:combinatorial`), use-case testing.
3. Set each case's **test level** (component/integration/system/acceptance) and **type** (functional/non-functional). Prioritize by the feature's **risk level** (`risk_areas`).
4. Maintain **traceability**: basis → condition → case → coverage item.
5. Output a Test Design Specification (conditions) + Test Case Specification table: TC ID | title | level | type | technique | coverage items | preconditions | Given/When/Then | expected result | priority. Write to `<paths.docs_dir>/TEST-DESIGN-<item>.md`, or append to the relevant Test Plan.

Offer to implement the highest-priority cases via `/qa:implement`. Do not write automation here — this is analysis & design.
