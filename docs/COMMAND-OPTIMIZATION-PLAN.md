# Command Optimization Plan — phase by phase, with evidence

A roadmap to optimize all **59 `/qa:*` command prompts** so each one produces higher-quality, more deterministic, standards-conformant output — and so we can *prove* the improvement with before/after samples and a verifiable standards trace.

> **How this plan was produced (so it's evidence-grounded, not opinion):** every command was audited by an independent agent against a 7-dimension rubric, then a second agent adversarially verified each finding and checked that its ISTQB/ISO citation is real and correctly attributed (a 121-agent pass). The scores, themes, and exemplars below come from that audit. Re-run it after any syllabus revision.

> ## ✅ Execution status — COMPLETE (2026-06-13)
> All 7 phases have been executed. **Enablers:** `scripts/lint-commands.sh` + `templates/_self-check-block.md` + 8 new ISO 29119-3 templates (policy, automation-strategy, risk-register, test-data, test-environment, shift-right, completion-report, defect-report). **Commands:** all 59 optimized — `create-plan`/`qa-init` (golden) plus 57 via per-command agents, then the compliance map updated centrally.
> **Gate result:** `bash scripts/lint-commands.sh` → **59/59 passing, 0 violations** (exit 0), up from 21/59 at baseline. **59/59** commands now carry a self-check / residual-risk heading; all frontmatter intact; no command mechanics broken. ~3,100 insertions across 63 files. The 33 remaining lint *warnings* are non-blocking (commands that emit an inline/freeform report with no dedicated template).

---

## 1. The optimization standard (the rubric we score against)

Each command is scored **0–5 on seven dimensions**. This rubric *is* the "standard" — every fix must move a dimension and cite the authority that justifies it (ISTQB CTFL v4.0 / CTAL / Specialist syllabi, ISTQB Glossary, ISO/IEC/IEEE 29119-3, ISO/IEC 25010, WCAG, OWASP).

| Dim | Name | What "good" looks like | Authority |
|---|---|---|---|
| **D1** | Standards conformance & attribution | Correct syllabus citation; correct Glossary terms; right 29119-3 work-product / 25010 characteristic; **no Foundation-vs-Specialist mis-tags** | CTFL v4.0, CTAL/CT-*, ISO 29119, ISO 25010 |
| **D2** | Determinism & clarity | Numbered steps, explicit thresholds/decision rules, defined input **and** empty-input path, exact output location | CTFL §1.4 (entry/exit), §5.2 (risk = L×I) |
| **D3** | Config-driven | Reads `qa.config.yml`; uses `<paths.*>` / `<tooling.*>`; **zero hardcoded** tools/URLs/paths/thresholds | CT-TAE gTAA adaptation layer |
| **D4** | Output & template alignment | Names the exact 29119-3 work product; references a `templates/` file; specifies fields/tables/coverage | ISO 29119-3; ISTQB-COMPLIANCE §11 |
| **D5** | Traceability, self-check & evidence | Preserves basis→condition→case→coverage→procedure→result→defect; built-in self-check; states **residual risk**; measurable counts | CTFL Principle 1, §1.4.4, §5.3 |
| **D6** | Composition & routing | Correct, reciprocated `/qa:` handoffs; no overlap/contradiction | toolkit design |
| **D7** | Structure & token efficiency | Correct frontmatter (`description`/`argument-hint`/`allowed-tools`); concise | plugin spec |

---

## 2. Portfolio state today

**Mean 67/100, median 68.** Strong tail (`automation-audit` 82, `test-design`/`istqb-coach` 78, `status-report` 76, `create-plan` 74); weak tail needing near-rebuilds (`genai-assist` 38, `team-plan` 42, `mobile-test` 52, `add-test`/`security-scan` 58). **Verified gaps: 33 high · 46 medium · 9 low.**

The strengths are D1 standards-awareness and D7 efficiency. The weaknesses are concentrated and *systemic* — which is why the plan is built as reusable workstreams, not 59 one-off edits.

### Five systemic themes (the majority of all findings)

| # | Theme | Dim | Commands | Fix pattern | Authority |
|---|---|---|---|---|---|
| T1 | No built-in self-check + residual-risk before finalizing | D5 | ~28 | Roll out one paste-in self-check block (config-completeness · traceability · counts · residual risk) as the penultimate step | CTFL Principle 1; §1.4.4; ISO 29119-3 |
| T2 | Hardcoded paths/tools instead of config placeholders | D3 | ~20 | Replace `tests/`, `docs/qa/`, `playwright-report`, `npx playwright`, `vitest/jest`, `openapi.yaml` with `<paths.*>`/`<tooling.*>`; add a config-read guard | CT-TAE gTAA |
| T3 | Output not named per 29119-3 / no template | D4 | ~18 | Name the work product + reference a template; **create the 6+ missing templates** | ISO 29119-3 |
| T4 | Foundation-vs-Specialist mis-attribution / wrong § number | D1 | ~12 | One citation-accuracy pass traced to `ISTQB-COMPLIANCE.md` | CTFL/CTAL/Specialist map |
| T5 | Vague, non-deterministic decision rules | D2 | ~22 | Numbered steps + explicit thresholds + empty-input branch | CTFL §1.4, §5.2, §5.3 |

---

## 3. The validation method — how we prove each command is "pretty good" (the *evidence* gate)

This is the heart of your request: every optimized command must pass the **same five-point evidence gate**, with the artifacts attached.

1. **Lint pass** — the Phase-1 lint script reports **zero** hardcoded paths, a present self-check block, a `templates/` reference for any produced work product, and complete frontmatter (incl. `Write` in `allowed-tools` when it writes files).
2. **Before/after sample** — run the command against the toolkit's own `qa.config.example.yml` (or a fixture repo), capture the generated artifact, and **diff it against the pre-optimization output** to show the specific fix is live (new Coverage Summary, Residual-Risk section, config-driven path, RED/YELLOW/GREEN table, etc.).
3. **Citation check** — every standard reference in the command is **traced to a line** in `ISTQB-COMPLIANCE.md` or `GLOSSARY.md`. Anything not found there is downgraded to "verify upstream" wording rather than asserted verbatim (this closes the hallucinated-section risk).
4. **Self-check + traceability present** — grep confirms the self-check block exists and the sample output shows an intact basis→condition→case→result chain with a stated residual risk.
5. **Sibling-routing check** — grep the command's `/qa:` handoffs; each referenced sibling must exist and reciprocate (no one-way or contradictory routing).

A command is **done** only when all five pass and the lint log + before/after diff + citation trace are attached as evidence.

---

## 4. Cross-cutting workstreams (build once, reuse every phase)

- **W1 · Lint script** *(Phase 1)* — fails a command on hardcoded paths, a missing self-check where it writes a file, a produced work product without a `${CLAUDE_PLUGIN_ROOT}/templates` reference, or incomplete frontmatter. It is the Definition-of-Done gate for every phase.
- **W2 · Standard self-check block** *(Phase 1 → ~28 commands)* — one paste-in snippet (config-completeness · bidirectional traceability · measurable counts · residual risk). The single biggest D5 lever.
- **W3 · Golden command exemplar** *(Phase 1)* — promote `create-plan` (top D3/D4/D7) to the reference every command is diffed against for structure, config-read block, and self-check placement.
- **W4 · Citation-accuracy pass** *(spans Phases 2/6/7)* — index every section ref to a line in `ISTQB-COMPLIANCE.md`/`GLOSSARY.md`; fix Foundation-vs-Specialist mis-tags and wrong § numbers; flag any ref not in the toolkit docs as "verify upstream."
- **W5 · Template-creation workstream** *(spans Phases 2–7)* — author the missing ISO 29119-3 templates the audit repeatedly flags: **policy, automation-strategy, risk-register, test-data, test-environment, shift-right (Production Verification Report), completion-report, defect-report**. After they exist, each D4 fix is a one-line reference.
- **W6 · Work-product naming map** *(Phase 1 artifact)* — a table binding each command to its 29119-3 work product, auditable against `ISTQB-COMPLIANCE.md §11`.

---

## 5. The phased roadmap

Sequenced by **leverage and dependency**: enablers → governance spine → risk/design core → implementation → automation surface → specialist non-functional → reporting/gates (the consumers come last, once upstream outputs are standardized). Every command appears in exactly one phase.

### Phase 1 — Cross-cutting enablers + golden exemplar  ·  *~2–3 days*
Build W1–W6 before touching 59 commands.
- **Commands:** `create-plan` (promote to golden), `qa-init`.
- **Key fixes:** add `create-plan` step-5 self-check (every feature ≥1 case, acceptance criteria mapped, Residual-Risk section); `qa-init` pre-write config validation + readiness-checklist table; fix `qa-init` loose `§1.4.1`→`§1.4`.
- **DoD evidence:** lint runs clean on both · before/after shows the added self-check · self-check snippet file exists · citation index shows the `qa-init` correction traced · `qa-init` writes the readiness table.

### Phase 2 — Governance & planning spine (Policy → Strategy → Plan)  ·  *~4–5 days*
Top of the documentation hierarchy; the most damaging mis-attribution lives here.
- **Commands:** `test-policy`, `create-strategy`, `automation-strategy`, `estimate`, `team-plan`, `process-improvement`, `cost-of-quality`.
- **Key fixes:** `test-policy` → **ISO/IEC/IEEE 29119-2** Organizational Test Policy (not 29119-3/CTAL-TM); move process-definition items to `create-strategy`; create `policy-template.md` + `automation-strategy-template.md`; re-anchor `cost-of-quality`→CTAL-TM and `process-improvement` to measurable TMMi/IDEAL bands; resolve `team-plan`'s D1=1 (find the CTAL-TM section or reframe/merge); bidirectional policy↔strategy↔plan routing.
- **DoD evidence:** the two new templates exist & are referenced · `test-policy` ISO-29119-2 citation before/after · lint pass on all 7 · reciprocal routing grep · residual-risk block on every strategy/plan output · `team-plan` D1 resolved with a traced citation or explicit non-ISTQB note.

### Phase 3 — Risk-based analysis & test-design core  ·  *~4–5 days*
Risk drives priority across the whole toolkit; traceability is born here.
- **Commands:** `risk-assessment`, `test-design`, `test-cases`, `combinatorial`, `mbt`, `add-test`, `istqb-coach`.
- **Key fixes:** `risk-assessment` explicit **L×I tier bands** (1–4 Low, 5–12 Med, 13–15 High, 16–25 Critical), owner-rule ≥13, empty-scope path, create `risk-register-template.md` (Product Risk Register); `test-design` Step-0 input validation + Step-4 quality gate + Coverage Summary with counts; explicit `risk_areas`→priority mapping (critical→P1 …); `add-test` technique-selection decision tree (EP/BVA/decision-table/state-transition/error-guessing) **before** implementation; `combinatorial` residual-risk for uncovered n-way interactions + reduction metric.
- **DoD evidence:** risk-register template exists & referenced · L×I tier table before/after · Coverage Summary with technique counts + non-orphan traceability in a sample · BVA 2-value/3-value distinction confirmed (per `ISTQB-AUDIT.md` Finding #3) · `add-test` decision tree traced to CTFL §4 · lint pass.

### Phase 4 — Implementation, scaffolding, data & environment  ·  *~5–6 days*
Where config-driven discipline matters most; heaviest D3/D4 concentration.
- **Commands:** `scaffold`, `implement`, `unit-test`, `integration-test`, `test-data`, `test-env`, `maintenance-test`.
- **Key fixes:** eliminate all hardcoded paths/tools (`<paths.*>`/`<tooling.*>` + qa-init guards); name 29119-3 work products (Test Procedure Spec, Test Execution Log, Test Data / Environment Requirements) and create `test-data-template.md` + `test-environment-template.md`; `unit-test` replace literal `{{vitest/jest}}` with a `tooling.unit` config read; `maintenance-test` config-read block + trigger-type tree (modification/migration/retirement) + label confirmation-vs-regression; `scaffold` add tsc/playwright validation + hard-wait anti-pattern check + residual-risk; `test-data` secrets/PII/parallel-safe self-check + Handoffs boundary vs `test-env`.
- **DoD evidence:** two new templates exist & referenced · lint pass **zero** hardcoded-path hits across all 7 · `test-data` secrets/PII self-check before/after · `unit-test` dynamic `tooling.unit` before/after · `maintenance-test` confirmation-vs-regression citation traced · `scaffold` validation step in a sample.

### Phase 5 — Automation surface & reliability  ·  *~5–6 days*
All CT-TAE commands share one hardcoded-path pattern → one remediation pass covers the family. Depends on Phase 4.
- **Commands:** `web-automate`, `api-automate`, `mobile-automate`, `scan-ui`, `self-heal`, `flaky-hunt`, `fix-ci`, `fix-jenkins`.
- **Key fixes:** replace `tests/pages`, `tests/e2e`, `playwright-report`, `test-results` with `<paths.*>` + config-driven tool detection (`tooling.e2e`/`api`); name Test Procedure Spec + Test Execution Log; `flaky-hunt` config-aware runner (no hardcoded `--repeat-each`) + SLA thresholds (quarantine >10% or critical >2 sprints); `mobile-automate` numbered routing (`tooling.mobile` null→`/qa:tool-select`; appium vs web_app) + device-matrix traceability table; CI fixers emit a Confirmation Test Execution Log + route incidents to `/qa:triage`.
- **DoD evidence:** lint pass **zero** hardcoded-path hits across all 8 · work-product names grep-confirmed · `flaky-hunt`/`fix-*` dynamic `tooling.e2e` before/after · `self-heal` routing to `triage`/`flaky-hunt` confirmed · `mobile-automate` device-matrix table in a sample.

### Phase 6 — Specialist non-functional & acceptance  ·  *~5–6 days*
Specialist syllabi share Foundation-vs-Specialist mis-attribution + missing ISO-25010 thresholds. Lower in the dependency chain.
- **Commands:** `perf-plan`, `perf-test`, `security-scan`, `a11y-audit`, `usability-test`, `nonfunctional`, `mobile-test`, `ai-test`, `acceptance`, `shift-right`, `dynamic-analysis`.
- **Key fixes:** fix attribution — `security-scan`→**CT-SEC**/OWASP (CTFL §2.2.2 is only the generic container), `shift-right`→**Quality in DevOps Specialist**, `acceptance` separate CTFL §4.5 ATDD from CT-AcT UAT/operational/alpha-beta; anchor outputs to **ISO 25010** characteristics with measurable SLA + entry/exit criteria; create `shift-right-template.md` (Production Verification Report); `dynamic-analysis` numbered leak thresholds (≥8h/500 iters, 25/50/75/100% snapshots, >5% growth = leak) + 9-point gate; empty-input defaults to `risk_areas.critical` + residual-risk self-checks.
- **DoD evidence:** corrected Specialist citations traced to the stream map · `shift-right` template exists & referenced · `dynamic-analysis` leak thresholds + gate before/after · `perf-plan` entry/exit + residual-risk in a sample · a11y/usability/mobile enumerate ISO-25010/WCAG coverage with explicit empty-input default · lint pass on all 11.

### Phase 7 — Reporting, decision gates & remaining commands  ·  *~5–6 days*
The consumers at the end of the chain — sequenced last so upstream outputs are already standardized.
- **Commands:** `status-report`, `release-report`, `quality-report`, `go-no-go`, `triage`, `audit-prep`, `static-analysis`, `static-review`, `review-coverage`, `coverage-measure`, `exploratory`, `genai-assist`.
- **Key fixes:** deterministic **RED/YELLOW/GREEN** and **Ship/Hold** logic tied to all gates (`min_pass_rate_pct`, `block_on_severity`, perf/security/a11y, `can-i-deploy`); create `completion-report-template.md` + `defect-report-template.md`; make reporting config-driven (gather only enabled tooling, mark missing as "not run", never fabricate); `triage` add **`Write` to allowed-tools** + S1–S4 severity thresholds + unique defect-ID rule; fix remaining citations (`coverage-measure` §4→§5.3+§4.3; `static-review` review types per §3.2; `audit-prep` reference `ISTQB-COMPLIANCE.md §3`; `exploratory`→CTAL-TA §5); `quality-report` correct the fabricated "Test Measurement Report" to Status/Completion Report; **full numbered rebuild of `genai-assist`** (lowest score, 38).
- **DoD evidence:** two new templates exist & referenced · `triage` frontmatter includes `Write` · gate-threshold tables (Ship/Hold + RED/YELLOW/GREEN) before/after · corrected citations traced · `genai-assist` rebuilt with output location + self-check + lint pass · `status-report` identical-before/after bash false-positive resolved.

---

## 6. Quick wins (do these first — cheap, high-value, low-risk)

- `triage`: add `Write` to `allowed-tools` (confirmed missing) — one line; unblocks it writing its own defect report.
- `self-heal`: replace `tests/pages` / `playwright-report` / `test-results` with `<paths.*>` — highest-severity D3, pure find/replace.
- Section-number typos: `regression` §2.2.3→§2.2.2, `coverage-measure` §4→§5.3, `contract-sync` §2.2.1→§2.2.
- Re-tag descriptions: `tool-select`→CT-TAE, `cost-of-quality`→CTAL-TM, `security-scan`→CT-SEC, `shift-right`→Quality in DevOps Specialist (description-only).
- `audit-prep`: swap `ISTQB-COVERAGE.md` ref for `ISTQB-COMPLIANCE.md §3`.
- `unit-test`: replace literal `{{vitest/jest}}` with a `tooling.unit` config read.
- Add the standard empty-input line to commands missing it (`test-design`, `dynamic-analysis`, `test-data`, `a11y-audit`).

---

## 7. Worked evidence — two before/after exemplars (proof the approach lands)

These are the two highest-impact commands from the audit, optimized end-to-end. They are the template for the before/after evidence every phase produces.

### 7a. `/qa:dynamic-analysis` — D2 2→5, D4 2→5, D5 2→5

| # | Change | Standard | Before | After |
|---|---|---|---|---|
| 1 | Empty-input default | CTFL §1.4; Glossary "test item" | "Target from `$ARGUMENTS`." | "…If empty, ask which flow; **default to the highest-risk area from `risk_areas`**." |
| 2 | Measurable leak thresholds | CTFL §5.2 (testable criteria) | "run repeatedly / under sustained load and watch for growth that never releases" | "baseline at **t=0**; run **≥8h or ≥500 iterations**; sample at **25/50/75/100%**; flag any resource **growing >5% without release**." |
| 3 | Prose → numbered procedure | ISO 29119-3 test procedure | bulleted "Approach:" | "Procedure: 5. Define scenario … 6. Instrument (stack-specific profilers) … 7. Execute & capture snapshots … 8. Analyze & report." |
| 5 | Named work product + structure | ISO 29119-3 Test Execution Log | "Output a dynamic-analysis report to …" | "Output a **Test Execution Log (29119-3)** with a metrics table `\| Metric \| Baseline \| Final \| Growth% \| Threshold \| Status \|` + severity bands." |
| 6 | Quality-gate self-check | CTFL Principle 1; §5.3 | "Report findings with evidence." | "9. **Quality gate** — verify baseline, ≥3 snapshots, trend-not-noise, root-cause correlated, severity justified; **state residual risk**; do not publish until all gates pass." |
| 7 | Traceability chain → triage | CTFL §1.4.4 | (none) | "Record basis → monitored resources → result → defect ID → status; route confirmed leaks to `/qa:triage`." |

### 7b. `/qa:test-data` — D2 2→5, D3 2→5, D4 2→5, D5 1→5, D6 3→5

| # | Change | Standard | Before | After |
|---|---|---|---|---|
| 1 | Empty-input decision tree | Glossary "test data"; CTFL §1.4 | "If empty, ask which entity/domain." | "If empty: 1) ask; 2) **validate it maps to a test condition or OpenAPI schema**; 3) else route to `/qa:test-design`. Do not proceed without a clear entity." |
| 2 | Config-driven factory path | D3 gTAA | "create … under `<paths.tests_dir>/data/factories/`" | "…under `<paths.tests_dir>/<test_data.factories_path or 'data/factories'>` (override for `src/testFixtures` etc.)." |
| 4 | Named work product **(citation corrected)** | ISO 29119-3 "Test Data / Environment Requirements" (`ISTQB-COMPLIANCE.md` L154) | unnamed artifact | named to the **repo's actual mapping label** — *not* the audit's invented "Test Data Specification §5.3.2" (which doesn't exist). |
| 5 | Output section + coverage/traceability | ISO 29119-3; CTFL §1.4.4 | "Show the factory API and an example." | "## Output → `<paths.docs_dir>/TEST-DATA-<entity>.md` with a **traceability table** (factory → conditions → cases) and a **coverage summary** (N factories, M conditions covered, gaps)." |
| 6 | Built-in quality self-check | ISTQB Principle 5 | (none) | "6. Quality check: **secrets grep**, uniqueness, teardown-pairing, PII scan before finalizing." |
| 7 | Handoffs (routing) | D6 | (none) | "## Handoffs — `/qa:test-env` owns env provisioning; this owns data factories; hand off to `/qa:implement`." |

> Note one of the value-adds of the verify pass: in 7b the audit *itself* proposed a hallucinated citation ("Test Data Specification §5.3.2"); the verification step caught it and used the repo-accurate label instead. That is exactly the citation-hygiene the W4 workstream enforces across all 59.

---

## 8. Appendix — full scorecard (low → high)

Weakest dimensions shown per command. `H/M/L` = verified high/medium/low gap counts.

| Command | Score | H/M/L | Weakest dims |
|---|---:|---|---|
| genai-assist | 38 | 0/0/0 | D4=0, D2=1, D5=1 |
| team-plan | 42 | 0/0/0 | D1=1, D3=1, D4=1 |
| mobile-test | 52 | 0/0/0 | D4=1, D5=1, D2=2 |
| add-test | 58 | 0/0/0 | D3=1, D2=2, D4=2 |
| security-scan | 58 | 0/0/0 | D3=1, D2=2, D4=2 |
| release-report | 61 | 1/1/1 | D4=2, D5=2, D2=3 |
| tool-select | 62 | 0/0/0 | D1=2, D4=2, D5=2 |
| process-improvement | 62 | 0/0/0 | D3=1, D2=2, D4=2 |
| cost-of-quality | 62 | 0/1/0 | D2=2, D4=2, D5=2 |
| static-review | 62 | 0/0/0 | D2=2, D3=2, D4=2 |
| integration-test | 62 | 0/0/0 | D3=1, D2=2, D4=2 |
| maintenance-test | 62 | 2/3/0 | D3=1, D2=2, D4=2 |
| regression | 62 | 0/0/0 | D3=1, D1=2, D4=2 |
| mobile-automate | 62 | 0/0/0 | D3=1, D2=2, D4=2 |
| flaky-hunt | 62 | 0/0/0 | D3=1, D4=1, D2=2 |
| perf-test | 62 | 0/0/0 | D4=2, D5=2, D2=3 |
| a11y-audit | 62 | 0/0/0 | D2=2, D3=2, D4=2 |
| usability-test | 62 | 1/0/0 | D3=2, D4=2, D5=2 |
| contract-sync | 62 | 1/0/0 | D4=1, D5=1, D1=2 |
| ai-test | 62 | 0/0/0 | D2=2, D3=2, D4=2 |
| coverage-measure | 62 | 0/0/0 | D1=2, D3=2, D4=2 |
| shift-right | 64 | 2/0/0 | D4=1, D1=2, D2=2 |
| implement | 67 | 0/0/0 | D3=2, D4=2, D5=2 |
| quality-report | 68 | 0/0/0 | D2=2, D4=2, D5=2 |
| audit-prep | 68 | 0/0/0 | D3=2, D2=3, D4=3 |
| static-analysis | 68 | 0/0/0 | D2=2, D3=2, D4=2 |
| test-cases | 68 | 0/0/0 | D3=2, D2=3, D5=3 |
| acceptance | 68 | 0/1/0 | D3=2, D4=2, D2=3 |
| review-coverage | 68 | 0/0/0 | D3=2, D2=3, D4=3 |
| unit-test | 68 | 0/0/0 | D3=2, D4=2, D2=3 |
| dynamic-analysis | 68 | 4/4/1 | D2=2, D4=2, D5=2 |
| scaffold | 68 | 1/0/0 | D4=2, D5=2, D1=3 |
| test-data | 68 | 3/6/0 | D4=2, D5=2, D2=3 |
| test-env | 68 | 0/0/0 | D4=2, D5=2, D1=3 |
| fix-jenkins | 68 | 1/1/0 | D3=2, D4=2, D2=3 |
| nonfunctional | 68 | 0/0/0 | D2=2, D3=2, D4=2 |
| triage | 68 | 2/3/0 | D3=2, D2=3, D4=3 |
| api-automate | 71 | 0/0/0 | D3=2, D2=3, D4=3 |
| qa-init | 72 | 0/0/0 | D5=2, D2=3, D3=3 |
| test-policy | 72 | 2/5/0 | D4=2, D5=2, D1=3 |
| create-strategy | 72 | 1/1/0 | D5=2, D2=3, D3=3 |
| risk-assessment | 72 | 0/2/3 | D3=2, D2=3, D4=3 |
| estimate | 72 | 0/0/0 | D3=2, D4=2, D2=3 |
| go-no-go | 72 | 0/0/0 | D3=2, D2=3, D4=3 |
| combinatorial | 72 | 1/0/0 | D3=2, D4=2, D5=2 |
| mbt | 72 | 0/0/0 | D4=2, D2=3, D3=3 |
| exploratory | 72 | 0/0/0 | D3=2, D1=3, D2=3 |
| automate | 72 | 1/3/0 | D2=3, D5=3, D1=4 |
| automation-strategy | 72 | 1/4/0 | D4=2, D5=2, D1=3 |
| web-automate | 72 | 2/3/2 | D3=2, D4=2, D2=3 |
| scan-ui | 72 | 0/0/0 | D3=2, D2=3, D4=3 |
| self-heal | 72 | 1/0/0 | D3=1, D4=2, D5=2 |
| perf-plan | 72 | 1/4/2 | D3=2, D5=2, D2=3 |
| fix-ci | 72 | 0/0/0 | D3=2, D4=2, D5=2 |
| create-plan | 74 | 1/0/0 | D5=2, D2=3, D1=4 |
| status-report | 76 | 0/0/0 | D3=2, D2=3, D5=3 |
| test-design | 78 | 2/2/0 | D5=2, D2=3, D3=3 |
| istqb-coach | 78 | 2/2/0 | D3=2, D4=2, D2=3 |
| automation-audit | 82 | 0/0/0 | D3=3, D5=3, D2=4 |

*Generated 2026-06-13 from a 121-agent audit + adversarial-verification pass. Re-run on any ISTQB syllabus revision.*
