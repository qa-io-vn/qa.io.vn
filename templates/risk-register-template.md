# Product Risk Register — {{project.name}} {{release}}

> ISTQB / ISO/IEC/IEEE 29119-3 **Risk Register** work product. Aligns to **ISTQB CTFL v4.0 §5.2 (Risk-Based Testing)** and **CTAL-TM (Risk Management)**.
> Risk-based testing driver: risk level sets coverage **depth**, **test level**, **technique**, and **priority**. Release-scoped & living — review at refinement and before scope freeze.
> Write to `<paths.docs_dir>/risk-register-{{release}}.md`. Seed areas from `risk_areas` (critical/high/medium) and `gates`; never hardcode project-specific values.

## Document control
Test object, release, register ID, author, approvers (from `team`), version/status, last review date, related documents (Test Strategy, Test Plan, `stack.api_spec_path`). + change log.

## 1. Scope & method
- **Identification source:** test basis (stories, acceptance criteria, `stack.api_spec_path`), `risk_areas` config, prior defects, change-related areas.
- **Assessment scale:** Likelihood 1–5, Impact 1–5. **Risk Level = Likelihood × Impact** (1–25).
- **Tiers:** **Low** 1–4 · **Medium** 5–12 · **High** 13–15 · **Critical** 16–25.
- **Rule:** an **Owner is required when Risk Level ≥ 13** (High/Critical) before scope freeze. Critical/High → low-level (concrete) cases; Medium/Low → high-level (logical) cases.

## 2. Risk register (assessment)

| Risk ID | Area (`risk_areas`) | Description | Type (product/project) | Likelihood (1–5) | Impact (1–5) | Risk Level (L × I) | Tier | Mitigation / test approach | Test level & technique | Owner (req. if ≥ 13) | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | `<risk_areas.critical[0]>` | … | product | 4 | 5 | 20 | Critical | … (response: mitigate via test depth) | system · decision table / BVA | `<team.qa_lead>` | open |
| R-002 | `<risk_areas.high[0]>` | … | product | 3 | 4 | 12 | Medium | … | integration · EP | — | open |
| R-003 | … | … | project | 2 | 3 | 6 | Medium | … (e.g. environment / schedule mitigation) | n/a (project risk) | — | open |
| R-… | … | … | … | … | … | … | … | … | … | … | … |

*Type: **product risk** = quality risk in the test object (defect impact). **project risk** = risk to delivery (resources, environment, schedule, suppliers).*
*Status: open · mitigated · accepted · transferred · retired.*

## 3. Tier summary (measurable)

| Tier | Risk Level range | Count | Detail policy | Mandatory owner? |
|---|---|---|---|---|
| Critical | 16–25 | N | low-level (concrete) cases, deepest coverage | yes |
| High | 13–15 | N | low-level (concrete) cases | yes |
| Medium | 5–12 | N | high-level (logical) cases | no |
| Low | 1–4 | N | minimal / exploratory only | no |
| **Total** | — | **N** | — | — |

- **Product vs project split:** P product risks, Q project risks.
- **Owner coverage:** every risk ≥ 13 has a named owner (state any exceptions).

## 4. Risk-based depth allocation
How risk level drives test effort — what gets the most depth and why:

| Tier | Test levels in scope | Techniques (CTFL v4.0) | Non-functional checks (`tooling`/`gates`) | Relative effort |
|---|---|---|---|---|
| Critical | component → integration → system → acceptance | decision table · state transition · BVA (2/3-value) · EP | perf (`gates.performance`), security (`tooling.security`), a11y (`gates.accessibility_standard`) as area requires | highest |
| High | integration → system | decision table · BVA · EP · error-guessing | targeted non-functional per area | high |
| Medium | system (logical cases) | EP · checklist | smoke / spot checks | moderate |
| Low | exploratory / regression only | experience-based | none beyond regression | lowest |

- Only include **enabled** `tooling` types; honor `gates` thresholds for the non-functional checks above.
- Tie depth back to `paths.tests_dir` (where the cases live) and the Test Plan's coverage commitment.

## 5. Traceability
Bidirectional chain — no orphans: **risk → test condition → test case → coverage item → procedure → result (→ defect)**. Every Critical/High risk maps to ≥ 1 test condition; every condition traces back to a risk and forward to a case.

## 6. Review & monitoring
Re-assess at each refinement and before scope freeze; adjust Likelihood/Impact as defects emerge or are retired. Record new risks, re-tiered risks, and accepted residual risks in the change log.

## 7. Residual risk
State what is **not** covered and why (deferred areas, accepted Low-tier risks, areas gated out of scope). ISTQB Principle 1: testing shows the presence, not the absence, of defects — residual risk always remains and must be made explicit for the go/no-go decision.

## 8. Approvals
QA Lead, QA Manager, Product Owner, Eng Lead (from `team`) — decision + date. High/Critical risks without an owner block sign-off.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain risk -> test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts (tier counts, product/project split, owner coverage, % areas covered) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Risk Register** and written to the correct `<paths.docs_dir>` location.

---
*References ISTQB CTFL v4.0 §5.2 and CTAL-TM (Risk Management); ISO/IEC/IEEE 29119-3. See `docs/ISTQB-COMPLIANCE.md`.*
