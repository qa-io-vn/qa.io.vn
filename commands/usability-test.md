---
description: Evaluate usability and user experience (distinct from accessibility) using ISTQB usability-evaluation methods, heuristics, and ISO/IEC 25010 usability sub-characteristics, and write a findings document. Use to assess how usable a feature or flow is.
argument-hint: "<feature / flow>"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Usability evaluation: $ARGUMENTS

**ISTQB process:** Test execution — non-functional usability evaluation (Usability Testing, CT-UT — Specialist; quality-characteristic analysis per Advanced Test Analyst, CTAL-TA), assessed against ISO/IEC 25010 **usability**. Verify any specific syllabus section against the current syllabus before quoting it. Complements `/qa:a11y-audit` (accessibility), which this command defers detailed WCAG checks to.

**Work product (ISO/IEC/IEEE 29119-3):** this command produces a **non-functional usability evaluation report** (a usability-focused **Test Execution / analysis result**, organized by ISO/IEC 25010 usability sub-characteristic). There is no dedicated 29119-3 template for it; structure it like the other findings reports in `<paths.docs_dir>` (heuristic findings, task scenarios, recommendations). It is **advisory** — heuristic evaluation predicts usability problems but does not replace usability testing with real users.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Your task

**Step 0 — guards (do these first, in order).**
1. If `qa.config.yml` is missing (the block above printed `MISSING`), **stop** and tell the user to run `/qa:qa-init`. Do not evaluate against assumptions.
2. Read these fields and use them instead of any hardcoded value: `paths.docs_dir` (where the report is written), `risk_areas.*` (criticality of the target), `project.primary_locale` and `project.type` (context for the evaluation).
3. **Determine the target.** Take it from `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask the user which feature/flow to evaluate; if they decline to specify, default to the flows in `risk_areas.critical` (e.g. authentication, checkout) and state that you applied this default.

**Step 1 — evaluate against ISO/IEC 25010 usability sub-characteristics.** Assess the target against each, recording at least one observation (or an explicit "no issue found") per sub-characteristic. Use these sub-characteristics, verifying the exact set/wording against the current ISO/IEC 25010:
1. **Appropriateness recognizability** — can users recognize whether the feature fits their needs?
2. **Learnability** — how easily can a first-time user accomplish the task?
3. **Operability** — is the UI easy to operate and control?
4. **User-error protection** — does it protect users against making errors (and recover from them)?
5. **User-interface aesthetics** — is the interaction pleasing and satisfying?
6. **Accessibility** — note at a high level only; **defer detailed WCAG checks to `/qa:a11y-audit`** and link to it rather than duplicating.

**Step 2 — heuristic evaluation.** Walk the target against a published heuristic set (e.g. Nielsen's 10 usability heuristics): visibility of system status, match between system and the real world, user control and freedom, consistency and standards, error prevention, recognition rather than recall, flexibility and efficiency of use, aesthetic and minimalist design, help users recognize/diagnose/recover from errors, help and documentation. For **each violation** record: (a) the heuristic, (b) the location/element, (c) a **severity rating 0–4** (0 = not a problem, 1 = cosmetic, 2 = minor, 3 = major, 4 = catastrophe), and (d) a concrete remediation. Map each violation to the ISO/IEC 25010 sub-characteristic it most affects so findings tie back to Step 1.

**Step 3 — define usability test scenarios / tasks** a real user would perform, for moderated or unmoderated sessions. For each task specify: the **user goal**, **preconditions**, **steps**, and explicit **success criteria** — task completion (yes/no), error count, and time/efficiency target. Provide at least one task per ISO/IEC 25010 sub-characteristic assessed in Step 1.

**Step 4 — review forms/flows for user-error protection.** Check that the target prevents avoidable errors and that every error message is specific, actionable, and states how to recover. List each weak/missing message with a suggested replacement.

**Step 5 — assemble and write the report.** Write the findings to `<paths.docs_dir>/USABILITY-<feature>.md` with these sections: (1) target + scope, (2) ISO/IEC 25010 sub-characteristic assessment (Step 1), (3) heuristic violations table, severity-rated and ISO-mapped (Step 2), (4) usability task scenarios with success criteria (Step 3), (5) user-error-protection findings (Step 4), (6) prioritized recommendations, (7) **what requires human sessions** — explicitly separate findings derivable by heuristic evaluation here from what only real-user usability testing can validate (CTFL v4.0 Principle 7 — absence-of-errors fallacy: validation against real user needs). Do **not** modify code — the only file you write is this findings document.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — relevant `qa.config.yml` fields in scope (`paths.docs_dir`, `risk_areas.*`, `project.*`) are honored; no hardcoded paths, locales, or targets.
- [ ] **ISO/IEC 25010 coverage** — every usability sub-characteristic in scope has at least one recorded observation, and each heuristic violation is mapped to the sub-characteristic it affects; no orphan findings.
- [ ] **Measurable** — the report states counts (N heuristic violations by severity 0–4, M task scenarios) and per-task success criteria, not prose claims.
- [ ] **Residual risk / human oversight stated** — the report names what heuristic evaluation here cannot validate and that real-user usability testing is still required (ISTQB Principle 1: testing shows the presence, not the absence, of defects; Principle 7: validation against real user needs).
- [ ] **Work product named** — output is identified as a non-functional **usability evaluation report** (29119-3 usability Test Execution/analysis result) and written to `<paths.docs_dir>/USABILITY-<feature>.md`.

## After evaluating

State the report path and the counts (sub-characteristics assessed, violations by severity, task scenarios). Then hand off:
- `/qa:a11y-audit <page>` for the detailed WCAG accessibility checks deferred above.
- `/qa:triage` to log any confirmed usability defects as incident reports.
- `/qa:exploratory <feature>` to drive a session-based exploration of the same area using these scenarios as charters.
