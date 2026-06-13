---
description: Evaluate and select a test tool using the ISTQB tool-selection process (categories, criteria matrix, benefits/risks, pilot/PoC, recommendation). Use when choosing a new testing tool or justifying the current toolchain. Writes a Tool Evaluation decision record that feeds the Test Automation Strategy.
argument-hint: "<tool category or need, e.g. 'visual testing', 'API mocking'>"
allowed-tools: Read, Write, Glob, Grep, Bash, WebSearch
---

# Test tool selection: $ARGUMENTS

**ISTQB process:** Test tool selection and evaluation — tool categories, selection criteria, benefits/risks, and pilot, per **Test Automation Engineering (CT-TAE)** and the **Test Automation Strategy (Specialist)** syllabi; the generic tool-support-for-testing concepts are CTFL v4.0 §6. Verify section numbers against the current syllabus. This is a tooling **investment/ROI decision** (CT-TAE) that feeds the program-level Test Automation Strategy (`/qa:automation-strategy`) — never "adopt every tool."

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — suggest /qa:qa-init"
```

## Your task

Produce a **Tool Evaluation** decision record for the capability named in `$ARGUMENTS`, grounded in this project's actual constraints (not generic).

### Step 0 — Guards & inputs (run first)
1. **Config guard.** If the config block above printed `MISSING` (no `qa.config.yml`), STOP and route the user to `/qa:qa-init` to establish project context — do not invent `paths.*`, `tooling.*`, `stack.*`, `gates`, or `risk_areas`. If config is present, read it and resolve every `<paths.*>`, `<tooling.*>`, `<stack.*>`, `gates`, and `risk_areas` value used below from it; never hardcode a path or tool.
2. **Need argument.** `$ARGUMENTS` names the capability/category to evaluate (e.g. `visual testing`, `API mocking`). **If `$ARGUMENTS` is empty:** ask the user which capability is needed; if no answer is given, default the evaluation scope to the highest-impact tooling gap protecting `risk_areas.critical` (a capability needed by a critical area but mapped to `none`/absent in `<tooling.*>`) and state that this default was applied.

### Step 1 — Classify the need (tool category)
Assign the need to exactly one ISTQB tool category, then record it: test management; static analysis; test design / test data preparation; test execution & automation; performance/load; defect (incident) management; CI/CD & build; specialized non-functional (security, accessibility, etc.). State which test level(s)/type(s) and which `risk_areas` the capability supports.

### Step 2 — Define selection criteria (weighted)
Build a fixed criteria set and assign each a weight (1–5, where 5 = decisive for this project). Use exactly these criteria, sourced from config where noted:
1. **Stack fit** — aligns with `<stack.*>`, `<tooling.*>`, and `<tooling.ci.platform>`.
2. **Language alignment** — matches the team's primary language in `<stack.*>` (avoid a new runtime/language unless justified).
3. **CI & reporting integration** — runs on `<tooling.ci.platform>` and emits results to `<paths.reports_dir>`.
4. **Learning curve** — ramp-up cost for the current team.
5. **Licensing / cost** — license model and total cost (note any `gates`/budget constraint).
6. **Maintenance burden** — expected testware churn / upkeep.
7. **Community & support** — release cadence, docs, ecosystem.
8. **Vendor lock-in risk** — exit cost and data portability.
Record the weight rationale for any criterion weighted 4–5.

### Step 3 — Survey candidates
Identify 2–4 realistic candidates for the category (use **WebSearch** for current options when the field moves fast; prefer a tool already present in `<tooling.*>`/`<stack.*>` if it can cover the need). List each candidate with its category and licensing model.

### Step 4 — Score the criteria matrix (deterministic)
Build a matrix: rows = candidates, columns = the 8 weighted criteria. Score each cell **1–5** (1 = poor fit, 5 = excellent fit) and show the score, not prose. Compute each candidate's **weighted total = Σ(score × weight)**. **Decision rule:** rank by weighted total; the top candidate is the leading option **only if** its total exceeds the runner-up by ≥ 10%. If the gap is < 10%, declare the result close and break the tie by the highest-weighted criterion. Disqualify outright any candidate scoring 1 on a criterion weighted 5 (a decisive constraint it fails).

### Step 5 — Benefits & risks (ISTQB)
List, for the leading candidate: **benefits** (repeatability, broader/consistent coverage, efficiency, objective measurement) and **risks** (unrealistic expectations, maintenance cost, over-reliance/false confidence, integration cost, immature tool, vendor dependency). Give each risk a mitigation. **Decision rule:** if any unmitigable risk is high-impact on a `risk_areas.critical` area, do not recommend adoption — recommend a different candidate or staying with the current tool.

### Step 6 — Recommendation & pilot/PoC plan
1. **Recommend** one option (or "retain current tool" / "no tool — out of scope") with the one-line decision rationale tied to the matrix and the benefits/risk verdict.
2. **Pilot/PoC plan** — evaluate on a small, representative scope before rollout. Define: the pilot scope (one feature/surface, prefer one in `risk_areas.critical`), the duration/time-box, who runs it, and the integration target (`<tooling.ci.platform>`, `<paths.reports_dir>`).
3. **Pilot success criteria** — state measurable, numeric go/no-go thresholds (e.g. integrates with CI on `<tooling.ci.platform>`; pass rate ≥ `gates.min_pass_rate_pct`; setup ≤ N hours; flaky rate ≤ target). **Decision rule:** rollout proceeds only if every success criterion is met; otherwise re-evaluate the runner-up or stop.

## Output & work product
Write the result to `<paths.docs_dir>/TOOL-EVALUATION-<category>.md` (`<category>` = the classified need from Step 1). This is a **Tool Evaluation decision record** — there is no dedicated ISO/IEC/IEEE 29119-3 work product for tool selection; it is an input to and is referenced by the program-level **Test Automation Strategy** (`/qa:automation-strategy`, the ISO/IEC/IEEE 29119-3-aligned work product). On adoption, route to `/qa:automation-strategy` to fold the chosen tool into the strategy and tooling fit, and to `/qa:scaffold` to wire it into the framework/CI. For maintainability concerns of an already-adopted tool, route to `/qa:automation-audit`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `<stack.*>`, `<tooling.*>` toggles incl. `ci.platform`, `gates`, `risk_areas`) is honored; no path or tool is hardcoded, and a `none`/absent capability is flagged as a gap rather than assumed present.
- [ ] **Criteria-driven** — every candidate is scored 1–5 against all 8 weighted criteria and a weighted total is shown; the recommendation follows the Step 4/5 decision rules, not preference.
- [ ] **Measurable** — the matrix shows numeric scores/weighted totals and the pilot states numeric go/no-go thresholds (vs `gates.min_pass_rate_pct` where applicable), not prose claims.
- [ ] **Residual risk stated** — name the benefits and the residual risks of the recommended tool, what it does NOT cover, and why adoption could still fail (ISTQB Principle 1: testing shows the presence, not the absence, of defects; a tool does not replace test design or judgment).
- [ ] **Work product named** — output is identified as the **Tool Evaluation decision record**, written to `<paths.docs_dir>/TOOL-EVALUATION-<category>.md`, and explicitly linked to the Test Automation Strategy (`/qa:automation-strategy`).
