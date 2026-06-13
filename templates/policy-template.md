# Organizational Test Policy — {{project.name}}

> Structure for `/qa:test-policy`. Aligns to **ISO/IEC/IEEE 29119-2 (Test Policy)** and **ISTQB CTFL v4.0**.
> Highest-level, longest-lived document. States **WHY** testing exists and **WHAT** quality means here (intent + principles). Keep **HOW** out — that belongs in the Organizational Test Strategy. Prose with tables, not bullet walls. Use strict ISTQB Glossary terminology.

**Standards basis:** ISTQB CTFL v4.0, ISO/IEC/IEEE 29119, ISO/IEC 25010.
**Owns:** intent, quality goals, mandated standards. **Delegates HOW to:** Organizational Test Strategy → Test Plan(s).
**Location:** write to `<paths.docs_dir>/test-policy.md`.

## Document control
Policy ID, owner (`<team.qa_manager>`), approvers (`<team>`), version/status, effective date, review cycle, related documents (Organizational Test Strategy, Test Plans). + change log (see §9).

## 1. Purpose & scope
Why this policy exists; the organizational intent for testing. Scope: which products/teams it governs (e.g. {{project.name}} — {{project.type}}), intended audience, and what is explicitly out of scope. State that the policy says **why/what**; the **how** lives in the Strategy.

## 2. Test objectives & quality goals
The organization's test objectives (build confidence, find defects, reduce residual risk, satisfy contractual/regulatory needs) and the quality goals expressed against **ISO/IEC 25010** quality characteristics. Anchor depth to `risk_areas`.

| Quality goal (ISO 25010 characteristic) | Why it matters here | Success indicator |
|---|---|---|
| Functional suitability | … | meets acceptance criteria; gate `<gates.min_pass_rate_pct>`% pass |
| Security | governs `<risk_areas.critical>` | block on `<gates.security_block_on>` |
| Performance efficiency | … | within `<gates.performance>` SLAs |
| Reliability / Compatibility / Usability | … | … |

## 3. Organizational test process overview
A high-level statement of the test process the organization commits to (analysis → design → implementation → execution → completion, run continuously). Name the work products produced (per ISO/IEC/IEEE 29119-3) and where they live (`<paths.docs_dir>`, `<paths.tests_dir>`, `<paths.reports_dir>`). **Intent only** — sequencing, techniques and tooling are defined in the Strategy.

## 4. Roles & responsibilities
Who is accountable for quality across the organization (whole-team quality; appropriate tester independence). Reference `<team>` for named owners.

| Role | Responsibility (intent) |
|---|---|
| QA Manager (`<team.qa_manager>`) | owns this policy; ensures standards are followed |
| QA Lead (`<team.qa_lead>`) | translates policy intent into the Strategy |
| Product Owner (`<team.product_owner>`) | defines acceptance / quality expectations |
| Eng Lead (`<team.eng_lead>`) | whole-team quality; build-in-quality |

## 5. Standards & methods to follow
The mandated frameworks and what each governs. (Method tailoring and tool choices are deferred to the Strategy.)

| Standard | Governs | Mandate |
|---|---|---|
| ISTQB CTFL v4.0 (+ relevant Advanced/Agile syllabi) | terminology, principles, techniques, process | required vocabulary & technique basis |
| ISO/IEC/IEEE 29119 | test processes & work products | documentation & process conformance |
| ISO/IEC 25010 | product quality model | quality goals in §2 map to its characteristics |

## 6. Competency & training
The competencies expected of testers and the whole team, and the organization's commitment to maintaining them (certification expectations, onboarding, continuous learning). State intent only — not the curriculum.

| Competency area | Expectation | Maintained by |
|---|---|---|
| ISTQB foundation (terminology, techniques) | all testers | training / certification |
| Test automation (per `<tooling.*>`) | automation engineers | onboarding + mentoring |
| Domain & risk awareness (`risk_areas`) | whole team | refinement participation |

## 7. Testware / asset management
The organization's intent for managing testware as a controlled asset: version control, ownership, retention, and bidirectional traceability of all work products. Testware lives under `<paths.tests_dir>` / `<paths.docs_dir>` / `<paths.reports_dir>`; configuration management detail is defined in the Strategy.

| Asset class | Intent | Location |
|---|---|---|
| Test basis & conditions | versioned, traceable | `<paths.docs_dir>` |
| Test cases / procedures / scripts | owned, reviewed, version-controlled | `<paths.tests_dir>` |
| Test data | synthetic-only per policy | per Strategy |
| Results / reports / defect records | retained, auditable | `<paths.reports_dir>` |

## 8. How test value is measured
The principle that test value is **measured, not asserted**: the organization reports against `gates` and coverage rather than prose. Defines *what* is measured (intent); the *how/cadence* is in the Strategy and Plans.

| What is measured | Tied to | Reported as |
|---|---|---|
| Exit-criteria conformance | `<gates.min_pass_rate_pct>`, `<gates.block_on_severity>` | pass/fail per release |
| Requirement & risk coverage | `risk_areas`, traceability chain | % coverage, N conditions / M cases |
| Non-functional conformance | `<gates.performance>`, `<gates.security_block_on>`, `<gates.a11y_block_on>` | within / outside SLA |
| Residual risk | what is **not** covered | named explicitly at sign-off |

## 9. Review, approval & revision history
How and when this policy is reviewed (review cycle), who approves it (`<team>`), and the change log.

**Approvals:** QA Manager, QA Lead, Product Owner, Eng Lead — decision + date.

| Version | Date | Author | Approved by | Change |
|---|---|---|---|---|
| 0.1 | YYYY-MM-DD | `<team.qa_manager>` | … | initial draft |

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.

---
*References ISO/IEC/IEEE 29119-2 (Test Policy), ISTQB CTFL v4.0, and ISO/IEC 25010. Says WHY/WHAT; the Organizational Test Strategy says HOW. See `docs/ISTQB-COMPLIANCE.md`.*
