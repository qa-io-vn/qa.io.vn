---
description: Plan QA team capacity and skills — staffing vs upcoming backlog, a skills matrix, gaps, and a training/onboarding plan. Use for resourcing decisions and team development. Writes a team plan to the docs dir.
argument-hint: "[release / quarter]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# QA team capacity & skills plan

**ISTQB process:** Test team management — test-team organization, staffing, and skills development. This is **CTAL-TM (Advanced Test Manager) / Test Management (Expert)** territory; capacity planning and skills-matrix techniques are a **complementary test-management practice**, not a CTFL Foundation concept. **Tester independence** is the one piece anchored in Foundation (CTFL v4.0 — organization of testing / levels of independence; verify the exact section against the current syllabus). Cross-check any syllabus claim against `docs/ISTQB-COMPLIANCE.md`, `docs/GLOSSARY.md`, and `docs/ISTQB-AUDIT.md` before asserting it.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

This command produces a **QA resourcing & staffing plan** (a test-management work product that complements the resourcing/staffing section of the ISO/IEC/IEEE 29119-3 **Test Plan** — there is no dedicated 29119-3 document for a skills matrix). It is advisory and human-owned: a manager approves staffing/hiring/training decisions. Do not modify source code or tests — the only file you write is this plan.

**Config-read guard.** If the config block above printed `none`, stop and ask the user to run `/qa:qa-init` (or supply `paths.docs_dir`, `risk_areas`, `team`, `process`, and `tooling.*`). Do not assume defaults for `paths.*`.

### Step 1 — Resolve horizon and roster

1. **Horizon.** Take it from `$ARGUMENTS` (a release or quarter, used in the output filename and capacity window).
   - If `$ARGUMENTS` is empty, **ask** the user for the planning horizon. If they decline to specify, default to **the next release cadence window** from `process.release_cadence` / `process.sprint_length_weeks`, and state the assumed window explicitly.
2. **Roster.** The `team` config section holds named roles (`qa_manager`, `qa_lead`, `product_owner`, `eng_lead`), not a full tester roster. **Ask** the user for the QA roster: per person, their role, FTE/availability for the horizon, and self/lead-rated skill levels. Do not invent team members or ratings.
3. **Privacy.** Record only role and planning-relevant skills. Do not record sensitive personal data (compensation, performance reviews, protected characteristics).

### Step 2 — Skills matrix

Map each team member against the competencies this project actually needs. **Derive the required competency set from config**, not a fixed list: include only competencies whose tooling is enabled (`tooling.e2e`/`tooling.language` automation, `tooling.api`, `tooling.performance`, `tooling.security.*`, `tooling.accessibility`, `tooling.contract`, `tooling.mobile`, `ci.platform`), plus domain knowledge of `project.description`, test design techniques, exploratory testing, and relevant ISTQB certifications.

Rate each person per competency on a fixed scale and emit a table:

| Competency | Required level (0–3) | <Person A> | <Person B> | ... | Team coverage |
|---|---|---|---|---|---|

Use this rating scale (state it in the output):
- **0 — None**, **1 — Aware**, **2 — Proficient**, **3 — Expert/can mentor**.

Decision rules:
- A competency is a **gap** when no team member rates ≥ its Required level.
- A competency is a **key-person risk** when exactly one person rates ≥ Required level (single point of knowledge).
- Set Required level by risk: competencies tied to `risk_areas.critical` require **≥ 2** (Proficient); all others require **≥ 1**.

### Step 3 — Capacity vs backlog calculation

Make the arithmetic explicit and show it:

1. **Available capacity** = Σ over team members of `FTE × availability_factor × working_days_in_horizon`, in person-days. State `availability_factor` (default **0.8** to allow for meetings/leave/overhead) and the working-days count derived from the horizon and `process.sprint_length_weeks`.
2. **Demand** = planned backlog/releases sized in person-days. Pull effort from `/qa:estimate` if available; otherwise size by `risk_areas` depth (more depth for `critical` > `high` > `medium`) and state the basis.
3. **Balance** = Available capacity − Demand. Apply:
   - Balance < 0 → **over-committed**: flag, and recommend de-scope, defer, hire, or external support.
   - 0 ≤ Balance < 10% of capacity → **at capacity / fragile**: no slack for flakiness or sick leave; flag.
   - Balance ≥ 10% → **headroom**: note it can absorb training/cross-training.
4. **Bottlenecks** — flag any competency that is a key-person risk (Step 2) AND on the critical path for `risk_areas.critical` work.

### Step 4 — Gaps, key-person risk, and recommendations

For each gap and key-person risk from Steps 2–3, recommend exactly one primary action: **cross-train**, **hire**, or **external/contract support**. Prioritize specialist coverage gaps in enabled areas (`tooling.security.*`, `tooling.performance`, `tooling.accessibility`) since these are hardest to backfill.

### Step 5 — Training & onboarding plan

1. **Development per person** — targeted actions (courses, ISTQB certifications relevant to the gap, pairing/mentoring), each with an owner and a target date.
2. **Onboarding checklist for new testers** — project QA setup, reading `qa.config.yml`, `<paths.tests_dir>` conventions, `<paths.docs_dir>` plans/strategy, first tasks, and shadowing.

### Step 6 — Test independence

State the appropriate **level of tester independence** for this work (CTFL v4.0 — organization of testing; verify the section against the current syllabus) and any organizational considerations (e.g. embedded vs independent QA, reporting lines).

### Step 7 — Write the plan

Write the assembled plan to **`<paths.docs_dir>/TEAM-PLAN-<horizon>.md`**, containing: the skills matrix, the capacity-vs-backlog calculation (with the arithmetic shown), gaps & key-person risks, and the training/onboarding actions with owners and dates.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, enabled `tooling.*` toggles, `risk_areas`, `team`, `process.*`) is honored; no hardcoded paths, tools, or roster.
- [ ] **Roster sourced, not invented** — every person, FTE, and skill rating came from the user; nothing was assumed. Missing roster data was asked for, not fabricated.
- [ ] **Measurable** — the skills matrix uses the 0–3 scale, and capacity-vs-backlog states person-day numbers and the explicit Balance/threshold result rather than prose claims.
- [ ] **Gaps & key-person risk identified** — every competency below Required level, and every single-point-of-knowledge, is flagged with one recommended action (cross-train / hire / external).
- [ ] **Residual risk & human oversight stated** — name what the plan does NOT cover (e.g. attrition, unplanned scope, estimate uncertainty) and record that staffing/hiring/training decisions require manager approval (advisory output; CTFL v4.0 Principle 1).
- [ ] **Work product named** — output is identified as a **QA resourcing & staffing plan** (complementing the ISO/IEC/IEEE 29119-3 Test Plan resourcing section, no dedicated 29119-3 document) and written to the correct `<paths.docs_dir>` location.

End by pointing to the written file. For effort sizing of the backlog use `/qa:estimate`; to act on systemic capability gaps use `/qa:process-improvement`.
