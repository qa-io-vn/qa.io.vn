# Test Plan — {{project.name}} {{release}}

> Structure for `/qa:create-plan`. Aligns to **ISTQB CTFL v4.0 §5.1** and **ISO/IEC/IEEE 29119-3 (Test Plan)**.
> Release-scoped & disposable. Use strict ISTQB Glossary terminology. Link to the Organizational Test Strategy instead of repeating it. Only include enabled `tooling` types.

## Document control
Test object, release, plan ID, author, approvers (from `team`), version/status, related documents (Test Strategy, {{stack.api_spec_path}}). + change log.

## 1. Context & objectives
What {{release}} delivers; test objectives; relationship to the Organizational Test Strategy.

## 2. Scope of testing
- **Features / test items in scope:** table — ID | feature | test object surface | risk level (from `risk_areas`).
- **Test types in scope:** only enabled `tooling`.
- **Out of scope:** items + one-line justification.
- **Regression scope:** which existing areas, and why (change-related testing).

## 3. Test approach (this release)
Per type: what is tested in {{release}} | technique(s) (EP/BVA/decision table/state transition/ATDD…) | test level | tool | where it runs. Note mocking ({{tooling.mocking}}) is contract-backed.

## 4. Test basis & traceability
The test basis for {{release}} (stories, acceptance criteria, {{stack.api_spec_path}}). Commit to bidirectional traceability: basis → condition → case → procedure → result.

## 5. Entry criteria
Conditions to start test execution (basis baselined, spec frozen, environment ready, test data available).

## 6. Exit criteria / Definition of Done
Built from `gates`: pass rate ≥ {{gates.min_pass_rate_pct}}%; no open defects at {{gates.block_on_severity}}; performance SLAs ({{gates.performance}}); security block on {{gates.security_block_on}}; accessibility block on {{gates.a11y_block_on}}; can-i-deploy green. Plus suspension & resumption criteria.

## 7. Test deliverables (testware)
Plan, test conditions, test cases, test procedures/scripts, test data, execution logs/reports, status report, completion report, defect reports.

## 8. Test environment & data
Environments from `environments`; test data per `test_data` ({{test_data.strategy}}, seed {{test_data.seed_via}}, synthetic-only, secrets {{test_data.secrets_store}}).

## 9. Schedule, estimation & resourcing
Map test activities to {{process.sprint_length_weeks}}-week iterations: planning/analysis at refinement → design + implementation in-sprint → execution → completion. Estimate effort; resourcing.

## 10. Test cases (specification)
Per feature, a table: TC ID | title | test level | type | technique | coverage items | preconditions | Given/When/Then steps | expected result | priority. Cover valid (EP) and invalid/boundary (BVA), authorization (decision table/role matrix), state transitions where relevant, and the non-functional checks the feature's risk level requires. (Full set is maintained in the test repository.)

## 11. Product & project risks (this release)
Table: risk | type (product/project) | likelihood (1–5) | impact (1–5) | risk level | mitigation (test response) | owner. Risk level drives coverage depth. Anything high needs an owner before scope freeze.

## 12. Responsibilities (RACI)
Activity × roles (from `team`): R/A/C/I.

## 13. Defect management
Reference the strategy; severity vs priority; this release's blocker rule ({{gates.block_on_severity}}).

## 14. Test status report (template — filled during execution)
Planned/executed/passed/failed/blocked, defect metrics, coverage of requirements & risk, entry/exit status. *(Produced by `/qa:status-report`.)*

## 15. Test completion report (template — filled at end)
Summary, exit-criteria evaluation, residual risk, lessons learned, ship/hold recommendation. *(Produced by `/qa:release-report`.)*

## 16. Approvals
QA Lead, QA Manager, Product Owner, Eng Lead — decision + date.

---
*References ISTQB CTFL v4.0 §5 and ISO/IEC/IEEE 29119-3. See `docs/ISTQB-COMPLIANCE.md`.*
