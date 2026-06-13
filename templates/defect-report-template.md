# Incident (Defect) Report — {{project.name}} {{release}}

> ISTQB / ISO/IEC/IEEE 29119-3 **Incident (Defect) Report** work product. Aligns to **ISTQB CTFL v4.0 §5.5 (Defect Management)**.
> One report per defect. Written when a test **result** deviates from the expected result, or an anomaly is observed outside a planned test.
> Write to `<paths.reports_dir>/defects/<defect-id>.md` (or the project tracker; this template is the field schema). Seed area, severity and blocker rules from `risk_areas` and `gates`; never hardcode project-specific values.
>
> **Severity ≠ Priority.** *Severity* = the impact of the defect on the system/test object. *Priority* = the urgency to fix it. A high-severity defect in a never-used feature can be low priority; a low-severity defect on the critical path (e.g. a typo on the checkout button) can be high priority. Record both, independently.

## Document control
Reporter, date raised, test object & version, related documents (Test Plan, Risk Register, `stack.api_spec_path`), tracker link. + change log / status history.

## 1. Defect ID *(unique)*
`DEF-<item>-<nnn>` — unique, stable, never reused.

| Field | Value |
|---|---|
| Defect ID | `DEF-{{item}}-001` |
| Reported by | `<team.qa_lead>` / reporter |
| Date raised | {{date}} |
| Tracker link | … |

## 2. Summary
One-line title (what is broken, where) + a short description of the failure / anomaly. State it factually and reproducibly.

## 3. Test object & version
| Field | Value |
|---|---|
| Test object | feature / component / endpoint under test |
| Build / version | release tag, commit SHA, or `stack.api_spec_path` version |
| Test level | component · integration · system · acceptance |
| Found by | test case ID / exploratory session / monitoring / user report |

## 4. Environment
Where it was observed — from `environments`; never hardcode URLs.

| Field | Value |
|---|---|
| Environment | `<environments[].name>` (e.g. ci / qa / staging) |
| URL / target | `<environments[].url>` |
| Browser / device / OS | from `tooling.mobile_device_matrix` or `ci.browsers` where relevant |
| Test data | per `test_data` (synthetic-only — never real PII) |
| Config / flags | feature flags, account/role, locale (`project.primary_locale`) |

## 5. Steps to reproduce
Numbered, deterministic, minimal. Anyone should reproduce from these alone.

1. Precondition / state / data (per `test_data`).
2. …
3. …

**Reproducibility:** always · intermittent (N of M) · once-only.

## 6. Expected vs Actual result
| Expected result | Actual result |
|---|---|
| Observable outcome per the test basis / acceptance criterion (the postcondition that *should* occur). | What actually happened — error, wrong value, status code, crash, screenshot ref. |

**Deviation:** one line stating how Actual differs from Expected (the failure).

## 7. Severity *(impact on the system)*
Impact of the defect on the test object — independent of urgency. Blocker rule comes from `gates.block_on_severity`.

| Severity | Meaning (impact) |
|---|---|
| **S1 — Critical** | System down / data loss / security breach / no workaround. Blocks per `<gates.block_on_severity>`. |
| **S2 — Major** | Key function broken; workaround painful or none. |
| **S3 — Minor** | Function impaired; acceptable workaround exists. |
| **S4 — Trivial** | Cosmetic / low impact (typo, alignment). |

**Assigned severity:** `S_` — justification (impact on the system).

## 8. Priority *(urgency to fix)*
Urgency to schedule the fix — set with reference to the affected `risk_areas` tier and release timing, **independently of severity**.

| Priority | Meaning (urgency) |
|---|---|
| **P1 — Urgent** | Fix now; blocks release / critical path (`risk_areas.critical`). |
| **P2 — High** | Fix this release. |
| **P3 — Medium** | Fix when capacity allows / next release. |
| **P4 — Low** | Backlog; fix opportunistically. |

**Assigned priority:** `P_` — justification (urgency, business/risk impact). *Reminder: severity ≠ priority — set this from urgency, not from §7.*

## 9. Status *(lifecycle)*
Current state in the defect lifecycle. Record transitions in the change log.

`New → Assigned → Open/In progress → Fixed → Retest → Closed` · (or `Rejected` / `Duplicate` / `Deferred` / `Reopened`).

| Field | Value |
|---|---|
| Current status | `New` |
| Assigned to | … |
| Resolution | (set on close: fixed · won't-fix · duplicate · not-a-defect · deferred) |
| Target release | {{release}} |

## 10. Risk area
Affected area mapped to `risk_areas` — drives priority and regression scope.

| Field | Value |
|---|---|
| Risk area | `<risk_areas.critical[0]>` / `<risk_areas.high[0]>` / … |
| Risk tier | Critical · High · Medium · Low |
| Linked risk | Risk Register ID (`R-nnn`) if applicable |

## 11. References (traceability)
Bidirectional chain — no orphans. Every defect traces back to what it was found against.

| Reference | Value |
|---|---|
| Requirement / story / acceptance criterion | REQ-… / story ref / `stack.api_spec_path` |
| Test condition | TCond-… |
| Test case | `TC-{{item}}-nnn` (the case whose result deviated) |
| Test run / execution log | run ID / CI build (`ci.platform` / `ci.jenkins_job`) |
| Related defects | duplicates / blockers / blocked-by |

## 12. Attachments / evidence
Screenshots, screen recording, logs/stack trace, HAR/network capture, request/response, `tooling.e2e` trace/video, failing assertion. Reference paths under `<paths.reports_dir>` — never paste secrets or real PII.

| Type | Location / link |
|---|---|
| Screenshot / video | `<paths.reports_dir>/…` |
| Log / stack trace | … |
| Trace / HAR | … |

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISTQB CTFL v4.0 §5.5 (Defect Management); ISO/IEC/IEEE 29119-3 (Incident/Defect Report). See `docs/ISTQB-COMPLIANCE.md`.*
