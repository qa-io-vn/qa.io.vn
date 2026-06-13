---
description: Use generative AI responsibly to accelerate testing tasks (test idea generation, test data, case drafting) with ISTQB CT-GenAI safeguards — human-in-the-loop review and privacy protection. Use to speed up test work while keeping human oversight.
argument-hint: "<task, e.g. 'generate test ideas for checkout'>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# GenAI-assisted testing: $ARGUMENTS

**ISTQB process:** Using Generative AI *to support* testing activities. Operative framework: **CT-GenAI** ("Testing with Generative AI", Specialist syllabus) — a Specialist topic, never CTFL Foundation. Two non-negotiable CT-GenAI safeguards govern this command: **mandatory human oversight** (every GenAI output is an unverified draft a tester must review) and **privacy protection** (never send real PII, production data, or secrets to an external model). Cite CT-GenAI concepts by name; do not assert specific syllabus section numbers — verify any § against the current CT-GenAI syllabus before quoting it.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

**Step 0 — Config guard.** If the config above is `none`, stop and ask the user to run `/qa:qa-init` first (or supply `paths.*`, `risk_areas`, `gates`, `stack.api_spec_path`, and `test_data.sensitive_data_rule`). Do not hardcode paths, tools, or thresholds — read every one from `qa.config.yml`.

**Step 1 — Resolve the task and category from `$ARGUMENTS`.** Classify the request into one `<category>` (used in the output filename) and confirm it before proceeding:
- `test-ideas` — generate test conditions / coverage ideas.
- `test-data` — synthesize realistic-but-synthetic test data.
- `test-cases` — draft high/low-level test cases.
- `summarize` — summarize requirements or the test basis.
- `explain-failure` — explain a failing test / log.
- `doc-draft` — draft test documentation.
- **Decision rule (empty `$ARGUMENTS`):** if `$ARGUMENTS` is empty, default the task to `test-ideas` scoped to `risk_areas.critical` (highest-risk areas first per ISTQB Principle 4, defect clustering). State the chosen default and category before proceeding; if the request is ambiguous between categories, ask rather than guessing.

**Step 2 — Apply the privacy safeguard before generating anything (CT-GenAI).** This gate runs before any content is produced.
- **Decision rule (PII/secrets):** honor `test_data.sensitive_data_rule` (e.g. "synthetic-only — never real PII"). Do **not** read, paste, copy, log, or write real PII, production data, customer records, or secrets into the prompt context, the generated artifact, or the report. Generate synthetic/anonymized data only, per `test_data.strategy`.
- If the task appears to require real data to be useful, **stop and escalate** for data-handling approval rather than proceeding. Record in the output that this safeguard was applied and what (if anything) was redacted.

**Step 3 — Ground the generation in the project test basis.** Read the relevant test basis before generating, so output is project-specific rather than generic:
- API contract from `stack.api_spec_path` (when `stack.api_spec == openapi`); requirements/user stories under `<paths.docs_dir>`; existing tests under `<paths.tests_dir>`.
- Concentrate generation on `risk_areas.critical` then `high` (allocate depth by risk, not uniformly).
- If the test basis is missing for the requested scope, say so and generate from the available context, flagging the gap as a coverage limitation.

**Step 4 — Generate the requested artifact, marked as an AI-assisted draft.** Produce the deliverable for the resolved category. Every item must carry an explicit `AI-DRAFT — requires tester verification` marker. Apply the category-specific rule:
- `test-ideas` / `test-cases` → tie each item to a test basis reference and (where applicable) an ISTQB technique label; keep Foundation vs Advanced (CTAL-TA) techniques correctly attributed.
- `test-data` → synthetic only (Step 2); validate the shape against `stack.api_spec_path` where applicable.
- `summarize` / `explain-failure` / `doc-draft` → keep claims traceable to the source; do not invent requirements, defects, or results.

**Step 5 — Quality control (manage GenAI risks).** Cross-check the draft for the known CT-GenAI failure modes and record the result:
- **Hallucination/incorrectness** — verify every factual claim, requirement reference, and API field against the test basis; remove or flag anything unsupported.
- **Missing context / over-reliance** — list assumptions the model made and what context was unavailable.
- **Bias / gaps** — cross-check generated test conditions against `risk_areas` for uncovered critical/high areas.
- **Runnability (when generating tests or data)** — confirm drafted tests would assert meaningfully and generated data validates against the contract; mark any that are illustrative only.

**Step 6 — Human-in-the-loop handoff.** Compile a **"Human must verify before trusting"** checklist enumerating every item a tester must confirm (count them). State explicitly that nothing here is authoritative until a tester reviews it (CT-GenAI human-oversight expectation; ISTQB Principle 1). Route any confirmed defect surfaced while generating to `/qa:triage`; route generated test cases onward to `/qa:test-design` or `/qa:implement` for formalization and execution.

## Output — work product

Produce a **GenAI-assisted testing draft** for the resolved category, written to `<paths.docs_dir>/GENAI-ASSIST-<category>.md`. This is a **supporting input to** an ISO/IEC/IEEE 29119-3 work product — depending on category it feeds the Test Design / Test Case Specification (`test-ideas`/`test-cases`), Test Data Requirements (`test-data`), or other testware — never a finalized work product on its own, because it is an unverified AI draft pending human review.

Structure the doc: resolved task + `<category>`; privacy-safeguard statement (what was applied / redacted); test basis consulted; the AI-DRAFT deliverable (each item marked and traced to its basis reference); quality-control findings (hallucination/context/bias/runnability) with counts; the **Human-must-verify checklist** with a count of open items; residual risk and the explicit human-oversight note.

This command applies GenAI *to* testing. To **test an AI/ML feature in the product**, use `/qa:ai-test` (the inverse). It also complements `/qa:test-design` and `/qa:test-cases` (formalize the drafted cases), `/qa:test-data` (synthetic datasets), and `/qa:exploratory` (idea generation); confirmed defects route to `/qa:triage`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`/`paths.tests_dir`, `risk_areas`, `stack.api_spec_path`, `gates`, `test_data.strategy`/`sensitive_data_rule`) is honored; no path, tool, or threshold is hardcoded.
- [ ] **Privacy safeguard enforced (CT-GenAI)** — no real PII, production data, or secrets were placed in the prompt context, the artifact, or the report; `test_data.sensitive_data_rule` was honored (synthetic/anonymized only); the safeguard outcome is recorded.
- [ ] **Traceability intact** — each generated item traces to a test basis reference (requirement / user story / OpenAPI field), and drafted cases preserve the chain test basis → condition → case → coverage item; no orphans.
- [ ] **Measurable** — output states counts (items generated, AI-DRAFT items, open human-verify items, uncovered risk areas) rather than prose claims of "done".
- [ ] **Residual risk & human oversight stated** — every output is marked an unverified AI draft; the Human-must-verify checklist is present with a count; what is NOT covered is named (ISTQB Principle 1; CT-GenAI mandatory human oversight).
- [ ] **Work product named** — output is identified as a GenAI-assisted draft supporting the relevant ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.docs_dir>/GENAI-ASSIST-<category>.md` location, with confirmed defects routed to `/qa:triage`.
