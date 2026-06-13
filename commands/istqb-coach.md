---
description: Explain or apply any ISTQB concept, technique, term, or process on demand — a built-in ISTQB reference and coach. Use to learn a technique, check a definition, or get guidance on how to test something the ISTQB way. Optionally writes a concept note.
argument-hint: "<ISTQB concept, technique, term, or question>"
allowed-tools: Read, Glob, Grep, Bash, Write, WebSearch
---

# ISTQB coach: $ARGUMENTS

**Purpose:** on-demand ISTQB reference so a tester can do anything the standard covers, in the context of this project. This command is advisory (it teaches and routes); the other `/qa:*` commands do the work.

## Project context
```!
cat qa.config.yml 2>/dev/null | head -40 || echo "none"
```

## Your task

Topic/question is `$ARGUMENTS`.

### Step 1 — Resolve the input (decision rule)

1. **If `$ARGUMENTS` is empty**, do not guess. Print this topic menu and ask the tester to pick one (or type their own question), then stop until they answer:

   - **Principles & process** — the 7 principles, the 7 test-process activities, tailoring.
   - **Test design techniques** — Equivalence Partitioning, Boundary Value Analysis (2-value / 3-value), Decision Table, State Transition; experience-based; collaboration-based.
   - **Test levels & types** — component / integration / system / acceptance; functional vs non-functional; change-related (confirmation, regression).
   - **Risk-based testing** — likelihood × impact, risk levels, risk-driven depth.
   - **Static testing** — reviews (informal/walkthrough/technical/inspection), static analysis.
   - **Test management & metrics** — strategy, plan, monitoring & control, completion, estimation.
   - **Defect management** — incident lifecycle, severity vs priority.
   - **Traceability & coverage** — test basis → condition → case → coverage item → procedure → result → defect.
   - **A term/definition** — look it up in the Glossary.

   Default only if the tester explicitly declines to choose: explain the seven ISTQB principles (CTFL §1.3), as they underpin every other topic.

2. **If `$ARGUMENTS` is non-empty**, proceed with that exact topic.

### Step 2 — Explain (always)

Explain the ISTQB concept/technique/term accurately and concisely, using ISTQB Glossary terminology (cross-reference `${CLAUDE_PLUGIN_ROOT}/docs/GLOSSARY.md`). Cite the syllabus area, but only assert a section number you can confirm:

- Cite a **specific section** only when it is traceable in `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md`, `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-AUDIT.md`, or `${CLAUDE_PLUGIN_ROOT}/docs/GLOSSARY.md` (e.g. CTFL v4.0 §4.2 Boundary Value Analysis; CTFL §5.2 / CTAL-TM risk-based testing; CTFL §1.4 test process).
- If you cannot confirm the exact number, name the **stream and topic** instead (e.g. "a CTAL-TM risk-management topic") and say "verify against the current syllabus" rather than inventing a section number.
- **Never tag a Specialist or Advanced topic as CTFL Foundation.** Use-case testing and pairwise/combinatorial are **CTAL-TA**, not CTFL v4.0 §4.2 — label them Advanced (per `docs/ISTQB-AUDIT.md` findings #1–#2).

### Step 3 — Apply it to this project (always)

Show a concrete worked example using *this* project's config — the `stack`, the OpenAPI endpoints under `<paths.api_spec>`, the `risk_areas`, and enabled `tooling.*` — not a generic textbook example. If `qa.config.yml` was "none" above, state the assumption you are making and show a representative example. Examples to prefer:

- For a black-box technique: apply it to a real endpoint/parameter or form field from the test basis.
- For risk-based testing: rank against the project's actual `risk_areas.critical` / `risk_areas.high`.
- For a metric or report: reference the matching ISO/IEC/IEEE 29119-3 work product produced by the sibling command (Step 4).

### Step 4 — Route to the command that operationalizes it (always)

Map the concept into the workflow and name the sibling command that does it at scale, using `/qa:` form. Use the concept→command matrix in `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` §13. Common handoffs:

- Test design techniques → `/qa:test-design`, `/qa:test-cases`, `/qa:combinatorial`
- Risk-based testing → `/qa:risk-assessment`
- Static testing / reviews → `/qa:static-review`
- Monitoring & metrics → `/qa:status-report`; completion → `/qa:release-report`
- Defect lifecycle → `/qa:triage`
- Exploratory / experience-based → `/qa:exploratory`

### Step 5 — Confirm against official sources when unsure (conditional)

If the topic is newer than the toolkit, ambiguous, or not traceable in the docs above, **WebSearch** the official sources (istqb.org, the ISTQB Glossary at astqb.org) to confirm before asserting — never invent syllabus content. Respect copyright: explain concepts and use the terminology, but do not reproduce syllabus or glossary text verbatim.

### Step 6 — Optional concept note (only if asked)

If `$ARGUMENTS` requests a written reference (e.g. "...and save it", "write a note", "document this"), write the explanation + worked example to `<paths.docs_dir>/ISTQB-COACH-<concept>.md` (slugify `<concept>` from the topic). Otherwise reply inline only — do not write a file unprompted.

## Version & staleness note

The toolkit aligns to **CTFL v4.0 / v4.0.1**. Today's syllabus may be newer. Treat section numbers as guidance, not gospel: if ISTQB has issued a later revision, the section labels here may have shifted — confirm via Step 5. Flag to the tester when an answer depends on a version-specific detail (e.g. the v3.1→v4.0 change from "decision testing" to "branch testing", or the removal of use-case/pairwise from Foundation).

## Residual-risk & human-oversight note (run before finalizing)

This command gives guidance; it does not, by itself, prove anything was tested. Before finalizing:

- [ ] **Citation verified** — every section number asserted is traceable in the toolkit docs or confirmed via Step 5; otherwise it was softened to "verify against the current syllabus."
- [ ] **Stream tagged correctly** — Foundation vs Advanced/Specialist topics are not mixed up (no Specialist topic mislabeled CTFL Foundation).
- [ ] **Config reflected** — the worked example uses this project's `stack`, `<paths.*>`, `risk_areas`, and `tooling.*`, not a generic textbook case.
- [ ] **Routed** — the tester is pointed at the sibling `/qa:*` command that operationalizes the concept.
- [ ] **Residual risk stated** — note that this is reference guidance only; the actual testing happens in the routed command, and coverage/defects are evidenced there (ISTQB Principle 1: testing shows presence, not absence, of defects).

Keep it practical and short. See `${CLAUDE_PLUGIN_ROOT}/docs/ISTQB-COMPLIANCE.md` for the full concept→command map.
