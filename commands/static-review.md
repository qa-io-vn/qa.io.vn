---
description: Perform ISTQB static testing — review the test basis (requirements, user stories, API spec) for testability and defects, and route source-code static analysis to /qa:static-analysis. Use to review a story/spec before writing tests (shift-left). Produces a Review Report (review findings).
argument-hint: "<story / spec / file to review> [informal|walkthrough|technical|inspection]"
allowed-tools: Read, Glob, Grep, Bash
---

# ISTQB static testing: $ARGUMENTS

**ISTQB process:** Static testing (CTFL v4.0 §3). Reviewing the test basis realizes Principle 3 (early testing / shift-left). This command reviews the **test basis** (documents). For static analysis of **source code** (complexity, control/data flow, coding standards), hand off to `/qa:static-analysis`.

> **Scope boundary.** Two distinct static-testing activities — keep them separate:
> - **Test-basis review** (this command): human/AI review of requirements, user stories, acceptance criteria, the API spec — for testability, completeness, consistency, clarity. CTFL v4.0 §3.
> - **Source-code static analysis** (`/qa:static-analysis`): tool-driven analysis of code structure (SAST, linters, complexity). CTFL v4.0 §3.1 / CTAL-TTA. Route there; do not run it here.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Test-basis discovery
```!
echo "--- candidate test-basis files (requirements / stories / specs) ---"
ls -1 *.md docs/**/*.md requirements/* stories/* 2>/dev/null | head -40
echo "--- API spec (test basis for contract/API tests) ---"
ls -1 openapi.* swagger.* api/openapi.* 2>/dev/null | head
```

## Your task

**Step 0 — Read config.** Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed with documented defaults — do not invent paths/tools; use the `<paths.*>` / `<stack.*>` / `<tooling.*>` values the user confirms. Treat `risk_areas` as the prioritization driver.

**Step 1 — Establish subject and review type.**
1. Subject = `$ARGUMENTS` (a story, the API spec, requirements, or a file path). **If `$ARGUMENTS` is empty:** ask the user which test-basis item to review; if no answer, default to the highest-tier basis — the requirements/stories covering `risk_areas.critical` from config (then `risk_areas.high`). State which subject you selected and why.
2. A review-type hint may follow the subject. Select the review type using this decision rule (formality types per the current CTFL v4.0 §3 syllabus — verify the exact subsection against the syllabus):

   | If the subject is… | Default review type | Formality |
   |---|---|---|
   | a quick peer check / low-risk wording | **informal review** | none; brief notes only |
   | author-led, knowledge-sharing across the team | **walkthrough** | author drives; scenarios/dry-runs |
   | a `risk_areas.high` item needing peer/expert consensus | **technical review** (default when no hint and risk is high) | documented; reviewers' consensus on findings |
   | a `risk_areas.critical` item, contract, or regulated/safety-relevant basis | **inspection** | most formal; defined roles, entry/exit criteria, metrics, logged defects |

   If a hint is supplied it wins; otherwise pick from the table by the subject's risk tier. State the chosen type and the formality you will apply.

**Step 2 — Review the test basis** for the qualities ISTQB targets in reviews. For each, list concrete findings (not "looks fine"):
- **Testability** — is each requirement / acceptance criterion verifiable, measurable, and unambiguous? Could a test case be derived directly?
- **Completeness** — missing cases, error/exception paths, non-functional needs (ISO/IEC 25010 characteristics), edge conditions, boundary definitions?
- **Consistency** — contradictions within the basis, or against the API spec / other requirements?
- **Correctness & clarity** — ambiguity, undefined terms, implicit assumptions, conflicting wording.

**Step 3 — Review the API spec** (if in the basis) for gaps that would weaken contract/API tests: undefined error responses, missing schemas, unconstrained fields, undocumented status codes, auth gaps.

**Step 4 — Source-code static analysis is out of scope here.** If the subject implicates related source code, **route it to `/qa:static-analysis`** (it runs `<tooling.security.sast>` / configured linters and structural analysis). Do not execute SAST/linters in this command.

**Step 5 — Produce the Review Report.** Output review findings as a table:

| ID | Location (file/section/line) | Issue | Type (testability / completeness / consistency / ambiguity) | Severity (critical/high/medium/low) | Suggested fix |

Order by severity, critical first. Then summarize: counts per type and per severity (state numbers, not prose), the review type applied, and a one-line note that fixing these now is far cheaper than finding the resulting defects in execution (Principle 3).

**Work product:** the output is a **Review Report (review findings)** — the static-testing equivalent under ISO/IEC/IEEE 29119-3 (verify the exact work-product name against the standard for your project). This command does **not** write files or modify the test object; it returns the report inline for the author to act on.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `risk_areas` drove subject selection/prioritization; `<paths.*>` / `<tooling.*>` come from `qa.config.yml`, nothing hardcoded.
- [ ] **Scope kept clean** — test-basis review only; any source-code static analysis was routed to `/qa:static-analysis`, not run here.
- [ ] **Review type explicit** — the chosen review type and its formality are stated, justified by the hint or the subject's risk tier.
- [ ] **Measurable** — the report states finding counts per type and per severity, not prose claims.
- [ ] **Residual risk stated** — name what was NOT reviewed (out-of-scope sections, basis items deferred) and why; static testing shows the presence of defects, not their absence (Principle 1). No code was executed and no files were modified.
- [ ] **Work product named** — output is identified as a Review Report (review findings) and handed forward.

Hand the clarified, testable criteria to `/qa:test-design` (or `/qa:acceptance` for ATDD criteria). Route source-code findings to `/qa:static-analysis`.
