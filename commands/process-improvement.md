---
description: Assess test-process maturity and recommend improvements using an ISTQB Expert "Improving the Test Process" / IDEAL lens. Use for retrospectives, test-process audits, or when escaped defects, flakiness, or slow pipelines suggest the process needs work. Advisory — writes one report, changes no code/CI.
argument-hint: "[focus area]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Test process improvement

Focus area (optional): $ARGUMENTS

**ISTQB process:** Test process improvement — ISTQB Expert "Improving the Test Process" and the **IDEAL** improvement cycle, with CTAL-TM monitoring/metrics inputs. A process-maturity model (e.g. TMMi or TPI) is used only as an assessment *lens*; verify any specific level names/criteria against the current model/syllabus before asserting them.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Signals from the repo
```!
echo "--- test counts ---"; find tests -name "*.spec.*" 2>/dev/null | wc -l
echo "--- flaky markers ---"; grep -rl "@flaky\|test.fixme\|skip(" tests 2>/dev/null | wc -l
echo "--- CI file ---"; ls -1 Jenkinsfile .github/workflows/*.yml 2>/dev/null
```
> The block above is generic discovery only. In the task, read the actual locations from config: tests under `<paths.tests_dir>`, reports under `<paths.reports_dir>`, docs under `<paths.docs_dir>`, and enabled test types from `<tooling.*>` toggles. Do not hardcode paths or tools.

## Your task

**Config guard.** If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init`. Otherwise honor `paths.*`, `tooling.*`, `gates`, `risk_areas`, `process.*`, and `team` throughout.

**Scope.** Use `$ARGUMENTS` as the focus area (e.g. `automation`, `defect management`, `metrics`). If `$ARGUMENTS` is empty, ask the user for a focus area; if no answer is given, default the scope to the assets behind `risk_areas.critical` and state that default explicitly in the report.

1. **Collect signals (no fabrication).** Gather quantifiable inputs from real evidence; mark any unavailable metric as `unknown`, never guess:
   - Escaped-defect count/trend (from `<paths.docs_dir>` reports), flaky-test count (markers above vs total), pipeline duration, coverage gaps vs `risk_areas`, missing test types (compare enabled `<tooling.*>` to what is actually exercised), untracked traceability (orphans in the test basis → condition → case → procedure → result chain).

2. **Assess maturity against measurable criteria.** Score each ISTQB test-process area — test policy, strategy, planning, risk-based testing, test design techniques, monitoring/metrics, defect management, configuration management, automation maturity, non-functional coverage — by assigning the **highest level whose criterion is fully met by evidence**. Use this deterministic rubric (TMMi-style lens; verify exact level wording against the current model):

   | Level | Deterministic criterion (must be evidenced to claim the level) |
   |---|---|
   | **1 Initial** | Activity is ad hoc/undocumented; no owner; no metric captured. |
   | **2 Managed** | A documented test policy/strategy and per-release Test Plan exist; entry/exit `gates` are defined; defects are tracked with severity & priority. |
   | **3 Defined** | The seven ISTQB process activities run per iteration with named work products; risk-based testing drives effort (`risk_areas` scored likelihood×impact); test design uses formal techniques. |
   | **4 Measured** | Quantitative gates enforced: requirements/risk coverage measured, defect density & escaped-defect rate trended, flaky rate < the team's threshold, pipeline duration tracked against a target. |
   | **5 Optimizing** | Metrics drive a closed IDEAL loop: each release feeds lessons learned and a measured improvement action with before/after deltas; pesticide-paradox refresh and root-cause/defect-prevention are routine. |

   For every area, record: current level, the **specific quantifiable gap** to the next level (e.g. "escaped-defect rate not trended → blocks Level 4"), and the evidence (or `unknown`).

3. **Diagnose** the top gaps by impact, tying each to its real signal from step 1 (escaped-defect trend, flaky count, pipeline duration, coverage gap, missing test type, traceability orphans).

4. **Recommend** improvements structured by the **IDEAL** cycle (Initiating, Diagnosing, Establishing, Acting, Learning). For each action give: target maturity level it unlocks, the measurable success metric (with current → target values), effort (S/M/L), priority, and owner (from `team`). List quick wins first, then structural changes. Tie each recommendation to a concrete ISTQB practice and, where one exists, the toolkit command that implements it (e.g. `/qa:risk-assessment`, `/qa:status-report`, `/qa:review-coverage`, `/qa:flaky-hunt`, `/qa:create-strategy`, `/qa:test-policy`, `/qa:cost-of-quality`).

5. **Output** a **Test Process Improvement Report** (an improvement-plan work product; not a 29119-3 testware document — it assesses the process that produces testware). Write it to `<paths.docs_dir>/PROCESS-IMPROVEMENT-<date>.md`. Include: scope/focus, the maturity scorecard table (area → current level → gap → evidence), diagnosis, the IDEAL action plan with metrics & owners, and a residual-risk note.

Do not modify code, tests, or CI — the only file you write is the report.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`, `process.*`, `team`) is honored; nothing hardcoded.
- [ ] **Evidence-based, not asserted** — every maturity level claimed is backed by a named signal; anything unmeasured is marked `unknown` rather than scored.
- [ ] **Measurable** — each gap and recommendation states counts/rates/level deltas (current → target), not prose claims.
- [ ] **Standards anchored** — assessment uses the ISTQB Expert "Improving the Test Process" / IDEAL structure; any maturity-model level names are flagged to "verify against the current model" rather than asserted as fixed.
- [ ] **Residual risk stated** — name what the assessment does NOT cover and why (CTFL v4.0 Principle 1: testing shows the presence, not the absence, of defects). This command is advisory: a human owns acting on the recommendations.
- [ ] **Work product named** — output is identified as the **Test Process Improvement Report** (improvement-plan work product) and written to the correct `<paths.docs_dir>` location.

End by pointing to the file and, based on the top gap, suggesting the matching command — e.g. `/qa:risk-assessment` (risk-based gaps), `/qa:status-report` (metrics gaps), `/qa:flaky-hunt` (reliability gaps), or `/qa:test-policy` / `/qa:create-strategy` (policy/strategy gaps).
