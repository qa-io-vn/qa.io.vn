# Test Completion Report — {{project.name}} {{release}}

> ISTQB / ISO/IEC/IEEE 29119-3 **Test Completion Report** work product. Aligns to **ISTQB CTFL v4.0 §5.3 (Test Monitoring & Control / Completion)** and **CTAL-TM (Test Closure)**.
> Produced at the end of test execution — summarizes what was tested in {{release}}, evaluates the agreed exit criteria, states residual risk, and makes a ship/hold recommendation.
> Write to `<paths.reports_dir>/completion-report-{{release}}.md`. Drive every threshold from `gates`; seed scope from `risk_areas`; honor enabled `tooling` only — never hardcode project-specific values.

## Document control & approvals
Test object, release, report ID, author, version/status, report date, related documents (Test Strategy, Test Plan, Risk Register at `<paths.docs_dir>`, `stack.api_spec_path`). + change log.

| Field | Value |
|---|---|
| Test object / release | {{project.name}} / {{release}} |
| Report ID | CR-{{release}} |
| Author | `<team.qa_lead>` |
| Version / status | v0.1 / draft |
| Report date | {{date}} |
| Related documents | Test Plan, Risk Register (`<paths.docs_dir>`), `stack.api_spec_path` |

**Approvals** (from `team` — decision + date):

| Role | Name | Decision (approve/reject) | Date |
|---|---|---|---|
| QA Lead | `<team.qa_lead>` | | |
| QA Manager | `<team.qa_manager>` | | |
| Product Owner | `<team.product_owner>` | | |
| Eng Lead | `<team.eng_lead>` | | |

## 1. Executive summary
One paragraph: what {{release}} delivered, overall quality verdict, headline pass rate, open blockers, and the ship/hold recommendation in a single sentence. State counts, not adjectives.

## 2. Exit-criteria evaluation
Evaluate each criterion from the Test Plan's Definition of Done against `gates`. Every row resolves to PASS or FAIL.

| Criterion | Target (from `gates`) | Actual | PASS/FAIL |
|---|---|---|---|
| Pass rate | ≥ `gates.min_pass_rate_pct`% | …% | |
| Open defects at blocking severity | 0 at `gates.block_on_severity` | N | |
| Performance SLAs | `gates.performance` (p95/p99/error-rate/RPS) | … | |
| Security findings | none at `gates.security_block_on` | N | |
| Accessibility | none at `gates.a11y_block_on` (`gates.accessibility_standard`) | N | |
| Requirement / risk coverage | 100% Critical/High `risk_areas` | …% | |
| can-i-deploy | green | … | |

*Any FAIL row must be reflected in the §9 recommendation (ship/hold) and in §6 residual risk.*

## 3. Test execution results
Counts across all enabled `tooling` test levels/types (component, integration, system, acceptance). Source: execution logs in `<paths.reports_dir>`.

| Test level / type | Planned | Executed | Passed | Failed | Blocked | Pass rate % |
|---|---|---|---|---|---|---|
| Unit (`tooling.unit`) | | | | | | |
| Component (`tooling.component`) | | | | | | |
| Integration / API (`tooling.api`) | | | | | | |
| System / E2E (`tooling.e2e`) | | | | | | |
| Contract (`tooling.contract`) | | | | | | |
| **Total** | | | | | | |

- **Not-executed reason:** for any planned-but-not-executed, state why (blocked, descoped, environment).
- **Coverage:** test conditions exercised vs total; % requirements covered; % Critical/High `risk_areas` covered.

## 4. Defect summary (by severity)
Open + total defects raised in {{release}}, severity aligned to `gates.block_on_severity`.

| Severity | Raised | Closed/Fixed | Open | Deferred | Blocking? (`gates.block_on_severity`) |
|---|---|---|---|---|---|
| S1 (critical) | | | | | yes |
| S2 (major) | | | | | yes |
| S3 (minor) | | | | | no |
| S4 (trivial) | | | | | no |
| **Total** | | | | | — |

- **Blocking open defects:** list IDs at any `gates.block_on_severity` level (these force a Hold).
- **Deferred defects:** ID + justification + owner; carried into residual risk (§6).

## 5. Non-functional results (vs SLAs)
Only rows for enabled `tooling`; compare each measure to its `gates` threshold.

| Area | Tool | Metric | Target (`gates`) | Actual | PASS/FAIL |
|---|---|---|---|---|---|
| Performance | `tooling.performance` | checkout p95 / p99 / error-rate / RPS | `gates.performance` | | |
| Security | `tooling.security.sast`/`sca`/`dast`/`secrets` | findings by severity | none at `gates.security_block_on` | | |
| Accessibility | `tooling.accessibility` | violations by impact | none at `gates.a11y_block_on` (`gates.accessibility_standard`) | | |

## 6. Residual risk
State what is **NOT** covered and why — deferred defects (§4), descoped areas, accepted Low-tier risks from the Risk Register, environments/devices (`tooling.mobile_device_matrix`) not exercised, and any non-functional gaps. ISTQB Principle 1: testing shows the presence, not the absence, of defects — residual risk always remains and must be explicit for the go/no-go decision.

| Residual risk | Area (`risk_areas`) | Why not covered | Impact if it triggers | Accepted by |
|---|---|---|---|---|
| | | | | |

## 7. Lessons learned
Brief, actionable. What worked, what to improve, process/tooling/coverage changes to feed into the next plan and the Organizational Test Strategy.

- **Went well:** …
- **To improve:** …
- **Actions (owner + due):** …

## 8. Traceability
Confirm the chain holds with no orphans: **test basis → condition → case → coverage item → procedure → result (→ defect)**. Every executed result traces back to a requirement/condition; every blocking defect traces to a failed result and a risk in the Risk Register (`<paths.docs_dir>`).

## 9. Ship / Hold recommendation
Tie directly to `gates` — this is the decision, not a summary.

- **Recommendation:** **SHIP** / **HOLD** (choose one).
- **Pass rate:** …% vs `gates.min_pass_rate_pct`% → meets / fails.
- **Blocking defects:** N open at `gates.block_on_severity` → 0 required to ship.
- **can-i-deploy:** green / red.
- **Conditions / caveats:** if SHIP-with-conditions, list the conditions and the accepted residual risk (§6); if HOLD, list the exact gate(s) that must turn green and the owner for each.

**Decision rule:** Ship only when pass rate ≥ `gates.min_pass_rate_pct`%, **zero** open defects at `gates.block_on_severity`, all §5 non-functional rows PASS against `gates`, and can-i-deploy is green. Any FAIL → Hold.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISTQB CTFL v4.0 §5.3 and CTAL-TM (Test Closure); ISO/IEC/IEEE 29119-3 (Test Completion Report). See `docs/ISTQB-COMPLIANCE.md`.*
