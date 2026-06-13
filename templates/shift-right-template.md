# Production Verification Report — {{release}}

> ISO/IEC/IEEE 29119-3 **work product** · *Production Verification Report* (shift-right / testing in production).
> Role: **Quality in DevOps Specialist**. Produced by `/qa:shift-right`.
> Test basis: production telemetry, SLOs, user journeys · Generated: {{date}} · Author: {{author}}
> Written to `<paths.reports_dir>/production-verification-{{release}}.md`. Scope is observation of the **live** system; it complements (does not replace) pre-release testing. ISTQB Principle 7: shift-right does not substitute for early testing.

## Document control

| Field | Value |
|---|---|
| Test object / service | `<project.name>` |
| Release / build under verification | {{release}} |
| Report ID | PVR-{{release}}-{{date}} |
| Author | {{author}} |
| Reviewers / approvers | from `team` (Quality in DevOps Specialist, QA Lead, SRE/Eng Lead) |
| Version / status | draft / reviewed / approved |
| Window observed | from `<timestamp>` to `<timestamp>` (UTC) |
| Related documents | Test Plan, Test Completion Report, Organizational Test Strategy |
| Change log | … |

## 1. Journeys monitored

Critical user/business journeys observed in production, prioritized by `risk_areas` (critical → high → medium). Each must trace to a risk area.

| Journey ID | User/business journey | Risk area (`risk_areas`) | Entry → exit steps | Traffic share (%) | Monitored via (`<tooling.*>`) |
|---|---|---|---|---|---|
| J-01 | … (e.g. checkout) | critical | … | … | synthetic + RUM |

- **Coverage:** N of M `risk_areas` journeys instrumented (% coverage). List any critical journey **not** monitored and why (feeds §9 residual risk).

## 2. Synthetic checks

Active probes that exercise journeys on a schedule against `<stack.base_url_web>` / `<stack.base_url_api>`. Built on `<tooling.e2e>` / `<tooling.api>`; no real PII (`test_data.sensitive_data_rule`).

| Check ID | Journey ref | Type (browser/API/uptime) | Tool (`<tooling.*>`) | Target env (`environments`) | Frequency | Locations | Assertion / oracle | Owner |
|---|---|---|---|---|---|---|---|---|
| SYN-01 | J-01 | API | `<tooling.api>` | production | 1 min | 3 regions | 2xx + body schema | … |

- **Counts:** total synthetic checks, by type, by journey. Every monitored journey has ≥1 synthetic check (no orphans).

## 3. SLIs & SLOs

Service Level Indicators measured in production and the objectives/error budgets they are evaluated against. SLO thresholds derive from `gates` where applicable (e.g. `gates.performance`, `gates.min_pass_rate_pct`).

| SLI ID | SLI (what is measured) | Source | SLO target | Source of target (`gates.*` / agreed) | Error budget | Window | Status (met / at-risk / breached) |
|---|---|---|---|---|---|---|---|
| SLI-01 | checkout latency p95 | RUM | ≤ `<gates.performance.checkout_p95_ms>` ms | `gates.performance` | … | 28d | … |
| SLI-02 | request error rate | logs | ≤ `<gates.performance.error_rate_pct>` % | `gates.performance` | … | 28d | … |
| SLI-03 | journey success rate | synthetics | ≥ `<gates.min_pass_rate_pct>` % | `gates` | … | 28d | … |
| SLI-04 | availability | uptime probe | ≥ … % | agreed | … | 28d | … |

- **Error-budget summary:** budget remaining/consumed per SLO; any breach drives §6 and §9.

## 4. Canary / A-B / feature-flag strategy

Progressive-delivery controls used to limit blast radius of {{release}} in production.

| Mechanism | Used? | Scope / cohort | Promotion criteria (SLIs/SLOs) | Rollback trigger | Automated? | Owner |
|---|---|---|---|---|---|---|
| Canary | … | % traffic / region | SLI-01..04 within SLO for N min | SLO breach / error-budget burn | … | … |
| A/B experiment | … | variant A vs B cohort | guardrail SLIs not regressed | guardrail breach | … | … |
| Feature flag(s) | … | flag key(s), audience | … | flip-to-off on alert | … | … |

- **Decision recorded:** promote / hold / roll back, with the SLI/SLO evidence that justified it.

## 5. Observability & alerting hooks

How the journeys/SLIs are made observable and how breaches page a human. Integrates with `ci` and `<tooling.*>` where relevant.

- **Telemetry:** logs / metrics / traces (distributed tracing across services), RUM, synthetics. Source per SLI in §3.
- **Dashboards:** link(s) — one per critical journey / SLO.
- **Alert hooks:** table below; thresholds align to `gates` and SLO error budgets.

| Alert ID | Fires on (SLI/SLO breach or burn rate) | Severity (`gates.block_on_severity`) | Channel / route | Runbook link | Owner |
|---|---|---|---|---|---|
| ALRT-01 | SLI-02 error rate > SLO for 5 min | S1 | pager + chat | … | … |

- **Hooks:** alert → incident (§6), alert → auto-rollback (§4), alert → CI gate / `can-i-deploy` feedback. Note any alert with **no** runbook (residual risk).

## 6. Incidents observed

Production incidents and SLO breaches detected during the window. Each links back to the SLI/journey that surfaced it; defects raised feed the defect tracker and traceability.

| Incident ID | Detected by (synthetic/alert/SLI) | Journey / risk area | Severity (`gates.block_on_severity`) | Time to detect | Time to mitigate | Root cause (or pending) | Defect ID | Rollback/flag action |
|---|---|---|---|---|---|---|---|---|
| INC-01 | ALRT-01 / SYN-01 | J-01 / checkout | S1 | … | … | … | DEF-… | flag off |

- **Counts:** incidents by severity; SLO breaches; MTTD / MTTR. "No incidents observed" is itself a result — state the window and coverage so absence is not over-read (Principle 1).

## 7. Traceability

Bidirectional chain from risk to production result. No orphans: every `risk_areas` entry in scope reaches a synthetic check and an SLI/SLO; every breached SLO traces back to a risk area and forward to an incident/defect.

| Risk area (`risk_areas`) | Test condition (what could fail in prod) | Synthetic check (§2) | SLI / SLO (§3) | Result (met / breached) | Incident / defect (§6) |
|---|---|---|---|---|---|
| critical / checkout | checkout completes ≤ SLO under live load | SYN-01 | SLI-01 / p95 ≤ `<gates.performance.checkout_p95_ms>` ms | … | INC-… / DEF-… |

- **Traceability check:** count of `risk_areas` covered end-to-end vs total; list any gap.

## 8. Residual risk in production

What this verification does **not** cover, and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; shift-right observes only what traffic exercises).

| Residual risk | Why not covered (no traffic / unmonitored journey / no SLO / sampling) | Risk area | Likelihood × impact | Mitigation / next action | Owner |
|---|---|---|---|---|---|

- Journeys/`risk_areas` with no synthetic check or no SLO.
- Low-traffic paths not exercised in the window; sampling/cardinality blind spots.
- Alerts without runbooks; SLOs without error-budget enforcement.

## 9. Verdict & recommendation

Overall production health for {{release}}: **healthy / degraded / roll back**. Evidence = SLO status (§3) + incidents (§6). Recommendation: continue / hold promotion / roll back / open follow-up testing. Approvers from `team`.

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISO/IEC/IEEE 29119-3 (Production Verification Report) and ISTQB CTFL v4.0. See `docs/ISTQB-COMPLIANCE.md`.*
