---
description: From requirements or manual test cases, run the full ISTQB automation pipeline — score priority & complexity, select automation candidates by ROI, design automated test cases, plan, and implement the top ones. Use to decide what to automate and turn manual tests into automated tests.
argument-hint: "<path to manual test cases | requirement | feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Automate: $ARGUMENTS

**ISTQB process:** Test Automation Engineering (CT-TAE — Specialist) + risk-based prioritization (CTFL v4.0 §5.2) + test implementation/execution (CTFL v4.0 §1.4). Verify any specific syllabus section against the current syllabus before quoting it. One command: assess -> select -> design -> plan -> implement.

**Work product (ISO/IEC/IEEE 29119-3):** a **Test Procedure Specification** (the implemented Phase-1 automated scripts under `<paths.tests_dir>`) plus a **Test Plan**-style automation plan (the scope/approach/schedule for what to automate) written to `<paths.docs_dir>`. Automation is an **ROI / investment decision** (CT-TAE): never "automate everything."

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first."
```

## Resolve input (manual test cases / requirements)
```!
ARG="$ARGUMENTS"
if [ -z "$ARG" ]; then echo "NO INPUT"; \
elif [ -f "$ARG" ]; then echo "--- file: $ARG ---"; cat "$ARG"; \
else echo "--- inline / feature name ---"; echo "$ARG"; \
  echo "--- matching test-case docs ---"; ls -1 docs/qa/TEST-CASES-*.md 2>/dev/null; fi
echo "--- existing automation ---"; ls -1 playwright.config.* 2>/dev/null; ls -1R tests 2>/dev/null | head -30
```

## Your task

### Step 0 — Guard inputs (config + test basis)
1. If the **Project config** block above printed `MISSING` (no `qa.config.yml`), STOP and route to `/qa:qa-init`. Do not proceed with hardcoded defaults — every path/tool below is read from config (`<paths.*>`, `<tooling.*>`, `<stack.*>`, `risk_areas`, `process.sprint_length_weeks`).
2. Resolve `$ARGUMENTS` (a path to manual test cases in Markdown/CSV, a requirement, or a feature name → look up its `<paths.docs_dir>/TEST-CASES-*.md`):
   - **If `$ARGUMENTS` is empty** (the resolve block printed `NO INPUT`): do not guess. Ask the user which feature/test cases to automate; if they cannot specify, **default to the highest-tier area in `risk_areas.critical`** and state that you did so.
   - **If no manual test cases exist** for the resolved input: generate them first with `/qa:test-cases`, then continue.
3. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/automation-plan-template.md` and produce its sections in order.

### Step 1 — Suitability filter
Drop items inherently unsuitable for automation and keep them **manual**, recording a one-line reason for each. Exclude an item when ANY of these holds:
- Subjective / look-and-feel / UX judgment → keep manual, route to `/qa:usability-test`.
- One-off or rarely-run / throwaway check.
- Exploratory or experience-based testing → route to `/qa:exploratory`.
- UI/feature not yet stable (automate after it settles).
- Requires human judgment or physical interaction (CAPTCHA, true visual subjectivity).

### Step 2 — Score PRIORITY (value of automating), 1–5 → P1…P5
Weighted, **risk-led**. Score each factor, then set the overall P-score by the dominant factors (risk level and business criticality dominate ties):
1. Risk level = likelihood × impact, from `risk_areas` (critical-tier area → push toward 5).
2. Business criticality — core revenue/user journeys → higher.
3. Execution frequency — runs every build / every regression → higher.
4. Regression value / repetitiveness — stable, repeated checks → higher.
5. Manual cost saved — slow/tedious by hand → higher.
6. Data-driven potential — same logic over many data sets → higher.

Give each item a P-score (**P1 = automate first … P5 = deprioritize**) **and** a one-line rationale.

### Step 3 — Score COMPLEXITY (cost of automating), 1–5 → C1…C5
Score each factor, then set the overall C-score (oracle determinability and external/UI volatility dominate):
1. Steps & system integrations — many steps, cross-system → higher.
2. Test-data setup/teardown — hard state to create/reset → higher.
3. **Test-oracle determinability** — hard to assert the expected result → higher.
4. External/unstable dependencies — third-party/flaky services → higher.
5. UI volatility — frequently-changing selectors/layout → higher.
6. Environment needs — special infra/devices → higher.

Give each item a C-score (**C1 = cheap/stable … C5 = costly/fragile**) + a one-line rationale.

### Step 4 — Select candidates (5×5 priority × complexity ROI matrix)
Plot every item on the full 5×5 matrix and apply this decision rule for **all 25 cells** (priority rows P1→P5, complexity columns C1→C5):

| Priority \ Complexity | **C1** | **C2** | **C3** | **C4** | **C5** |
|---|---|---|---|---|---|
| **P1** | Automate first | Automate first | Automate | Automate (plan) | Automate (plan) |
| **P2** | Automate first | Automate first | Automate | Automate (plan) | Defer/manual* |
| **P3** | Automate if cheap | Automate if cheap | Automate | Defer | Manual |
| **P4** | Automate if cheap | Automate if cheap | Defer | Manual | Manual |
| **P5** | Automate if cheap | Defer | Manual | Manual | Manual |

\* P2 + C5: automate only if the risk it covers cannot be mitigated more cheaply at a lower level; otherwise keep manual and record the residual risk.

Decision-band summary: **Automate first** = quick wins (do now); **Automate / Automate (plan)** = high value, schedule the effort; **Automate if cheap** = fill-in when capacity allows; **Defer** = backlog, re-score next cycle; **Manual** = do NOT automate, keep in the manual/exploratory set.

For every **automate** decision, assign the **recommended test level**: prefer the **lowest effective level** — component/unit (`<tooling.unit>`/`<tooling.component>`) and API/integration (`<tooling.api>`/`<tooling.contract>`) over UI E2E (`<tooling.e2e>`) — to minimize complexity and maintenance (pyramid + CT-TAE maintainability). Output the populated candidacy matrix + a prioritized **automation backlog** (count by P-band) with effort estimates.

### Step 5 — Design the automated test cases
For each selected candidate, convert the manual test case into an **automated test design**: target level, the test data (parameterize/data-drive where equivalence partitions or boundaries repeat the same logic), preconditions via fixtures/factories, the assertion (oracle), and the stable locators/endpoints. Preserve **bidirectional traceability**: requirement (test basis) → test condition → manual test case + coverage item → automated test procedure. Keep the ISTQB technique/coverage labels from the source cases unchanged.

### Step 6 — Plan
Produce the phased automation plan (Phase 1 quick wins → Phase 2 high-value/high-effort → Phase 3 fill-ins), mapped to `process.sprint_length_weeks` sprints, with: framework prerequisites (if the framework is missing, run `/qa:scaffold` first), reusable components to build, entry/exit criteria, automation metrics (CT-TAE — % candidates automated, automated pass rate, execution time saved, maintenance/flaky rate, defects found), and automation risks. Write the full plan to `<paths.docs_dir>/AUTOMATION-PLAN-<item>.md`.

### Step 7 — Implement the top candidates
Implement the **Phase 1 (P1)** candidates now using the project's framework (`<tooling.e2e>`/`<tooling.api>`/`<tooling.unit>`/`<tooling.component>`/`<tooling.contract>`, language `<tooling.language>`) and conventions (reuse fixtures, page objects, typed API clients; stable selectors; web-first assertions; no hard waits; synthetic test data only). Place scripts under `<paths.tests_dir>`. Run them with the configured runner's test command against the spec under `<paths.tests_dir>` (output lands in `<paths.reports_dir>`) and fix failures. If a failure reflects a real product defect, do not mask it — record an Incident Report and route to `/qa:triage`. For the unimplemented candidates, leave clear backlog tickets. (This step is the same engine as `/qa:implement`; do it inline for the selected set.)

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles incl. `none`, `risk_areas`, `process.sprint_length_weeks`) is honored; no hardcoded paths/tools/runner commands.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphaned automated tests.
- [ ] **Measurable** — output states counts (N assessed, M candidates by P-band, K kept manual, Phase-1 implemented + run result) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT automated (kept-manual set, deferred cells) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; CT-TAE — automation does not replace human judgment).
- [ ] **Work product named** — the plan is identified as the automation **Test Plan** written to `<paths.docs_dir>/AUTOMATION-PLAN-<item>.md`, and the Phase-1 scripts as the **Test Procedure Specification** under `<paths.tests_dir>`.

### Output summary
End with: N items assessed → M automation candidates (by P-band), K not suitable (kept manual), Phase-1 tests implemented and their run result, and where the plan was written.
