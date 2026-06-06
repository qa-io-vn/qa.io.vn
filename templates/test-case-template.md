# Test Case Specification — {{item}}

> ISTQB / ISO/IEC/IEEE 29119-3 **Test Case Specification**. Produced by `/qa:test-cases`.
> Test basis: {{source}} · Generated: {{date}} · Author: {{author}}

## Test case fields (definition)

Each test case uses these ISTQB-aligned fields:

| Field | Meaning |
|---|---|
| **ID** | `TC-<item>-<nnn>` — unique, stable. |
| **Title** | One-line objective ("what this verifies"). |
| **Traces to** | Requirement / user story / acceptance criterion + **test condition** ID (bidirectional traceability). |
| **Level** | component · integration · system · acceptance. |
| **Type** | functional · non-functional (perf/security/usability/…). |
| **Technique** | CTFL v4.0: black-box (EP · BVA 2-value/3-value · decision table · state transition) · white-box (statement · branch) · experience-based (error-guessing · exploratory · checklist) · collaboration-based (ATDD). *Advanced (CTAL-TA, label explicitly): pairwise · use-case.* |
| **Coverage item** | The exact item exercised: the partition, boundary value, decision rule, state/transition, etc. |
| **Priority** | P1 (critical path) · P2 · P3 — set by the feature's **risk level**. |
| **Detail** | `low` (concrete: exact data + steps) or `high` (logical: what to test, data deferred). Risk-based. |
| **Preconditions** | State/data that must exist before execution. |
| **Test data** | Concrete inputs (low-level) or data classes (high-level). |
| **Steps** | Ordered actions (Given/When) — present for low-level cases. |
| **Expected result** | Observable outcome / postcondition (Then). |

## Test conditions (test analysis)

List the **test conditions** derived from the test basis before the cases (what to test):

| TCond ID | Test condition | Traces to | Risk |
|---|---|---|---|
| TCond-01 | … | REQ/story ref | Critical/High/Med/Low |

## Test cases (test design)

### Detail policy (risk-based, mixed)
- **Critical / High risk areas → low-level (concrete)** cases: exact preconditions, data, steps, expected results — directly executable/automatable.
- **Medium / Low risk areas → high-level (logical)** cases: the condition and expected behavior, data deferred to execution.

### Specification table

| ID | Title | Traces to | Level | Type | Technique | Coverage item | Priority | Detail | Preconditions | Test data | Steps (Given/When) | Expected result (Then) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-{{item}}-001 | … | TCond-01 / REQ-x | system | functional | EP (valid) | valid-email partition | P1 | low | user on signup page | email=`a@b.com`, pwd=`Aa1!aaaa` | Given …, When submit | Then account created, 201 |

## Coverage summary

- **Techniques applied:** which ISTQB techniques and where.
- **Coverage achieved:** equivalence partitions (valid + invalid), boundary values (per chosen 2-value/3-value BVA form), decision-table rules, state transitions (valid + invalid), negative/error paths, authorization matrix.
- **Traceability:** every requirement/condition has ≥1 case; no orphan cases.
- **Counts:** total cases, by priority, by level, by type.

---

## Worked example — "Login with email + password" (illustrative)

**Test conditions:** valid login (TCond-01), invalid credentials (TCond-02), input validation (TCond-03), account lockout after N failures (TCond-04, stateful), authorization of returned session (TCond-05).

| ID | Title | Traces to | Level | Type | Technique | Coverage item | Pri | Detail | Preconditions | Test data | Steps | Expected |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-001 | Valid credentials log in | TCond-01 | system | functional | EP (valid) | valid creds partition | P1 | low | active user exists | email=`user@x.com`, pwd=`Correct1!` | enter creds, submit | 200, session created, redirect to dashboard |
| TC-LOGIN-002 | Wrong password rejected | TCond-02 | system | functional | EP (invalid) | invalid-password partition | P1 | low | active user exists | email=`user@x.com`, pwd=`wrong` | enter creds, submit | 401, generic error, no session |
| TC-LOGIN-003 | Email format validation | TCond-03 | system | functional | EP (invalid) | invalid-email-format partition | P2 | low | on login page | email=`a@`, pwd=`Correct1!` | enter, submit | 400/inline error, not submitted |
| TC-LOGIN-004 | Password min-length boundary | TCond-03 | system | functional | BVA | length = min−1 (7) | P2 | low | on login page | pwd=7 chars | enter, submit | rejected (below boundary) |
| TC-LOGIN-005 | Password min-length boundary | TCond-03 | system | functional | BVA | length = min (8) | P2 | low | on login page | pwd=8 chars valid | enter, submit | accepted (at boundary) |
| TC-LOGIN-006 | Lockout after 5 failures | TCond-04 | system | functional | state transition | transition: 4→5 fails → Locked | P1 | low | active user, 4 prior fails | 5th wrong pwd | submit | account Locked, lockout message |
| TC-LOGIN-007 | Locked account rejects valid creds | TCond-04 | system | functional | state transition | invalid transition from Locked | P1 | low | account Locked | correct creds | submit | still denied while locked |
| TC-LOGIN-008 | Session cannot access other user's data | TCond-05 | integration | non-functional (security) | decision table | role×resource rule | P1 | low | logged-in user A | request B's resource | call API | 403/404, no data leak |

*Decision-table example for authorization (TCond-05): conditions = {authenticated?, owns-resource?, role} → action = {200 / 403 / 404}.*
