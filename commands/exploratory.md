---
description: Plan and run session-based exploratory testing with time-boxed charters and a session sheet. Use for experience-based testing of a feature, especially high-risk or newly changed areas. Outputs an exploratory test charter set and session sheet (ISO/IEC/IEEE 29119-3 testware).
argument-hint: "<feature / area to explore>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Exploratory testing: $ARGUMENTS

**ISTQB process:** Experience-based test techniques — Exploratory / Checklist-Based / Error Guessing (CTFL v4.0 §4.4). Charters and time-boxed debriefs follow **session-based test management** (a CTAL Test Analyst topic — verify the exact section against the current syllabus). This complements, never replaces, the scripted coverage from `/qa:test-cases` / `/qa:test-design`.

**Work product:** ISO/IEC/IEEE 29119-3 testware — an **exploratory test charter set + session sheet** (a focused Test Design / Test Procedure artifact for unscripted execution). There is no dedicated template; write Markdown in the structure under **Output** below. Defects found are logged via `/qa:triage` using `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md`.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING"
```

## Your task

**Step 0 — Read config and resolve placeholders.** Parse `qa.config.yml` from the block above. If it printed `MISSING`, stop and tell the user to run `/qa:qa-init` first (do not invent paths or risk areas). Resolve and use throughout — never hardcode:
- `<paths.docs_dir>`, `<paths.reports_dir>`
- `<risk_areas.critical>`, `<risk_areas.high>`, `<risk_areas.medium>`, `<risk_areas.low>` (these drive charter selection and priority)
- `<stack.*>` / `<tooling.*>` only as context for the resources/tours below (do not hardcode tool names)

**Step 1 — Resolve the target.** Take the area to explore from `$ARGUMENTS`. If `$ARGUMENTS` is empty, do NOT guess — follow this rule, in order:
1. Ask: "Which feature/area should I write exploratory charters for?"
2. If the user cannot name one, default the scope to **`<risk_areas.critical>`** (one charter per critical area) and state explicitly that you defaulted to the critical risk areas.
3. If `qa.config.yml` is missing entirely, stop (per Step 0).

**Step 2 — Derive charters from risk (one per area, time-boxed).** For the target, write focused charters. Select and order areas by risk tier: `<risk_areas.critical>` first, then `<risk_areas.high>`, then `<risk_areas.medium>`/`<risk_areas.low>` only if in scope. Each charter MUST use this exact format:

> **Explore** `<area>` **with** `<resources/tools/data>` **to discover** `<information sought>`.

Time-box each charter using this rule:
| Risk tier of the area | Session length | Charters |
|---|---|---|
| `critical` | 90 min | 1+ per area (split if multi-feature) |
| `high` | 60 min | 1 per area |
| `medium` / `low` | 45 min | 1 per area, only if in scope |

Assign each charter a **priority** matching its risk tier (critical→P1, high→P1–P2, medium/low→P2–P3) so debrief and follow-up are prioritized consistently.

**Step 3 — Guide each session with ISTQB experience-based heuristics.** For every charter, supply concrete guidance under three headings:
1. **Error guessing** — where defects likely hide for this area (past defects, defect clusters per ISTQB Principle 4, fragile integrations).
2. **Checklist-based heuristics** — apply the relevant items: boundaries/data extremes, error handling, interruptions, concurrency, permissions/authorization, security, usability, empty/null and oversized inputs, special characters, duplicates.
3. **Tours** — name the tours to run (e.g. feature tour, money/risk tour, configuration tour, data tour), and what each is looking for.

**Step 4 — State oracles.** For each charter, give the **oracles** (how to recognize a problem): the expected behavior, the test basis or spec it is checked against, and the observable signal of a failure. Without an oracle a session cannot detect a defect.

**Step 5 — Produce the session sheet.** Provide a reusable **session sheet** for the tester to record per session: session ID, charter, date/tester, time-box (planned vs actual), areas/setup touched, **bugs** (with repro), **issues/questions**, **coverage notes** (what was and was NOT exercised), and a **debrief** summary.

## Output

Write the charter set + session sheet to `<paths.docs_dir>/EXPLORATORY-<feature>.md` with this structure:
- §1 **Scope & risk basis** — the target, which `<risk_areas.*>` tiers are in scope, and why (state if defaulted to `<risk_areas.critical>`).
- §2 **Charter set** — a table of charters: ID | charter (Explore…/with…/to discover…) | owning `<risk_areas.*>` area | risk tier | time-box | priority.
- §3 **Per-charter guidance** — for each charter: error-guessing notes, checklist heuristics, tours, and **oracles**.
- §4 **Session sheet template** — the reusable recording sheet from Step 5.
- §5 **Coverage & residual risk** — measurable: N charters across the in-scope risk areas, which areas are covered vs deferred, and what exploratory does NOT cover (it complements scripted coverage — ISTQB Principle 1).

State counts, not prose: "N charters covering M of K critical/high areas; L areas deferred (reason)."

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `risk_areas`, `stack.*`/`tooling.*` context) is honored; nothing hardcoded. Empty `$ARGUMENTS` was handled (asked, or defaulted to `<risk_areas.critical>` with that stated).
- [ ] **Charters risk-driven** — every charter maps to a `<risk_areas.*>` area, carries the correct time-box and priority for its tier, and uses the exact "Explore…/with…/to discover…" format.
- [ ] **Oracles present** — each charter states how a problem is recognized; no charter without an oracle.
- [ ] **Measurable** — output states counts/coverage (N charters, M of K critical/high areas covered, areas deferred) rather than prose claims.
- [ ] **Residual risk stated** — name what exploratory does NOT cover and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible). Exploratory complements, not replaces, scripted coverage.
- [ ] **Work product named** — output is identified as ISO/IEC/IEEE 29119-3 testware (exploratory charter set + session sheet) and written to `<paths.docs_dir>/EXPLORATORY-<feature>.md`.

---

## Handoffs

- **Inbound — what to explore:** if no scripted coverage or risk picture exists yet, run `/qa:risk-assessment` (to populate `risk_areas`) and `/qa:test-design` first; exploratory targets the high-risk and newly-changed areas those surface. `/qa:test-design` reciprocally routes deeper unscripted exploration here.
- **Sibling — usability:** for structured usability/UX evaluation (vs. defect-finding), hand off to `/qa:usability-test`.
- **Outbound — defects:** log every reproducible defect found in a session via `/qa:triage`, producing an ISO/IEC/IEEE 29119-3 Incident (Defect) Report.
- **Outbound — regression protection:** convert reproducible escapes into automated regression tests via `/qa:implement`, so the same defect is caught by scripted coverage next time.
