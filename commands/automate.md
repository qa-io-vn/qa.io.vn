---
description: From requirements or manual test cases, run the full ISTQB automation pipeline — score priority & complexity, select automation candidates by ROI, design automated test cases, plan, and implement the top ones. Use to decide what to automate and turn manual tests into automated tests.
argument-hint: "<path to manual test cases | requirement | feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Automate: $ARGUMENTS

**ISTQB process:** Test Automation Engineering (CT-TAE) + risk-based prioritization (CTFL §5.2) + test implementation/execution (CTFL §1.4). One command: assess → select → design → plan → implement.

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

Input (`$ARGUMENTS`) is a path to manual test cases (Markdown/CSV), a requirement, or a feature name (look up its `docs/qa/TEST-CASES-*.md`). If empty or no `qa.config.yml`, ask / route to `/qa:qa-init`. If there are no manual test cases yet, generate them first with `/qa:test-cases`, then continue.

Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/automation-plan-template.md` and produce its sections in order. Automation is an **ROI decision** (CT-TAE) — never "automate everything."

### Step 1 — Suitability filter
Drop items inherently unsuitable for automation (usability/subjective, one-off, exploratory, unstable UI, human judgment) and keep them manual. Record why.

### Step 2 — Score PRIORITY (value of automating), 1–5 → P1…P5
Weighted, **risk-led**: risk level (likelihood × impact from `risk_areas`), business criticality (core journeys), execution frequency (every build/regression), regression value/repetitiveness, manual cost saved, data-driven potential. Give each item a score **and** a one-line rationale.

### Step 3 — Score COMPLEXITY (cost of automating), 1–5 → C1…C5
Steps/integrations, test-data setup/teardown difficulty, **test-oracle determinability**, external/unstable dependencies, UI volatility, environment needs. Score + rationale each.

### Step 4 — Select candidates (ROI matrix)
Place each on the priority × complexity matrix and decide:
- **P1–P2 + C1–C2 → automate first** (quick wins).
- **P1–P2 + C4–C5 → automate, plan carefully** (high value).
- **P4–P5 + C1–C2 → automate if cheap** (fill-in).
- **P4–P5 + C4–C5 → do NOT automate** (keep manual).
Assign each candidate the **recommended test level**: prefer the **lowest effective level** (API/integration over UI E2E) to minimize complexity and maintenance (pyramid + CT-TAE maintainability). Output the candidacy matrix + a prioritized **automation backlog** with effort estimates.

### Step 5 — Design the automated test cases
For each selected candidate, convert the manual test case into an **automated test design**: target level, the test data (parameterize/data-drive where partitions or boundaries repeat the same logic), preconditions via fixtures/factories, the assertion (oracle), and the stable locators/endpoints. Preserve traceability: requirement → manual case → automated test. Keep ISTQB technique/coverage labels from the source cases.

### Step 6 — Plan
Produce the phased automation plan (quick wins → high-value/high-effort → fill-ins), mapped to `process.sprint_length_weeks` sprints, with framework prerequisites (run `/qa:scaffold` if the framework is missing), reusable components to build, entry/exit criteria, automation metrics (CT-TAE), and risks. Write the full plan to `<paths.docs_dir>/AUTOMATION-PLAN-<item>.md`.

### Step 7 — Implement the top candidates
Implement the **Phase 1 (P1)** candidates now using the project's framework and conventions (reuse fixtures, page objects, typed API clients; stable selectors; web-first assertions; no hard waits; synthetic data only). Run them (`npx playwright test <path>`) and fix failures. For the rest, leave clear backlog tickets. (This step is the same engine as `/qa:implement`; do it inline for the selected set.)

### Output summary
End with: N items assessed → M automation candidates (by priority), K not suitable (kept manual), Phase-1 tests implemented and their run result, and where the plan was written.
