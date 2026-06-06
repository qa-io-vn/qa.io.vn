# Organizational Test Strategy — {{project.name}}

> Structure for `/qa:create-strategy`. Aligns to **ISTQB CTFL v4.0** and **ISO/IEC/IEEE 29119-3 (Organizational Test Strategy)**.
> Long-lived & project-general. Use strict ISTQB Glossary terminology. Omit sections whose tool is `none` in `tooling`. Prose with tables, not bullet walls.

**Process:** {{process.methodology}} (Agile) · **Core automation:** Playwright + {{tooling.language}} · **Performance:** {{tooling.performance}} · **CI/CD:** {{ci.platform}}
**Standards basis:** ISTQB CTFL v4.0, relevant Advanced/Agile/Specialist syllabi, ISO/IEC/IEEE 29119, ISO/IEC 25010.

## 1. Scope & objectives
Test object(s): {{project.name}} ({{project.type}}). Purpose, in/out of scope, intended audience.

## 2. Quality policy & ISTQB principles
State adherence to the seven ISTQB testing principles and how each is realized here.

## 3. Test approach
Risk-based, shift-left, whole-team. State the test process tailoring for {{process.methodology}}: planning → monitoring & control → analysis → design → implementation → execution → completion, run continuously per iteration.

## 4. Test levels (CTFL §2.2)
Component, component integration, system, system integration, acceptance — and the tooling realizing each (unit {{tooling.unit}}, API/contract, E2E, UAT/ATDD).

## 5. Test types (CTFL §2.3 / ISO 25010)
Functional; non-functional (performance {{tooling.performance}}, security, accessibility {{tooling.accessibility}}, reliability, compatibility); white-box; change-related (confirmation + regression). Only enabled types.

## 6. Test design techniques (CTFL §4)
Which CTFL v4.0 techniques apply and where: black-box (EP, BVA 2-value/3-value, decision table, state transition), white-box (statement, branch), experience-based (error guessing, exploratory, checklist), collaboration-based (ATDD). Note any Advanced (CTAL-TA) techniques used (pairwise, use-case) as such.

## 7. Static testing (CTFL §3)
Review of the test basis (requirements, user stories, {{stack.api_spec_path}}) and static analysis (SAST/lint). Review types and when applied.

## 8. Test automation architecture (CT-TAE)
Playwright + {{tooling.language}}: generic test automation architecture, folder structure, Page Object Model, fixtures, storage-state auth, typed API clients from the OpenAPI spec, stable selectors, maintainability and flakiness policy. Browsers: {{ci.browsers}}.

## 9. Risk-based testing (CTFL §5.2)
Product-risk and project-risk approach; risk level = likelihood × impact; how risk drives depth, technique rigor, and level. Tiers from `risk_areas`.

## 10. Specialist test types
Sub-sections, only if enabled: API & integration testing; contract testing ({{tooling.contract}}, broker {{tooling.contract_broker_url}}); performance ({{tooling.performance}}, thresholds from `gates.performance`); accessibility ({{gates.accessibility_standard}}, axe); security (SAST/SCA/DAST/secrets per `tooling.security`, OWASP-aligned, CT-SEC); visual regression; service virtualization/mocking ({{tooling.mocking}}, contract-backed).

## 11. Test data & environment management
`test_data` strategy {{test_data.strategy}}, seeding {{test_data.seed_via}}, {{test_data.sensitive_data_rule}}, secrets {{test_data.secrets_store}}. Environments from `environments`.

## 12. Test monitoring, control & metrics (CTFL §5.3)
Metrics (test-case progress, defect, coverage of requirements/risk, pipeline health); status reporting cadence; control actions.

## 13. CI/CD & quality gates ({{ci.platform}})
Fast PR gate vs nightly vs pre-release; sharding {{ci.shard_count}}; image {{ci.agents_docker_image}}. Entry/exit criteria as gates using `gates`.

## 14. Entry & exit criteria / Definition of Done
Generic entry/exit criteria; story DoD as the team's exit criteria; release exit using `gates` (pass rate {{gates.min_pass_rate_pct}}%, block on {{gates.block_on_severity}}).

## 15. Defect management (CTFL §5.5)
Defect lifecycle; severity vs priority; root-cause and regression-proofing.

## 16. Configuration management & traceability (CTFL §5.4, §1.4.4)
Versioning of testware; bidirectional traceability test basis → condition → case → procedure → result → defect.

## 17. Roles & responsibilities
From `team`; whole-team quality; tester independence considerations.

## 18. Test tools (CTFL §6)
Classification and the specific tools from `tooling`; benefits/risks of automation.

## 19. Risks to the strategy, assumptions, mitigations
Flakiness, maintenance, slow pipeline, mock drift, environment instability, skills.

## 20. Implementation roadmap
Phased: foundation → breadth → contracts/non-functional → optimization.

---
*References ISTQB CTFL v4.0 and ISO/IEC/IEEE 29119-3. See `docs/ISTQB-COMPLIANCE.md` for the full mapping.*
