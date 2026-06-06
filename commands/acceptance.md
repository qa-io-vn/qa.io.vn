---
description: Author acceptance criteria and acceptance tests collaboratively using ATDD/BDD (Given/When/Then). Use to turn a user story into agreed, testable acceptance tests before development.
argument-hint: "<user story or feature>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Acceptance test design (ATDD/BDD): $ARGUMENTS

**ISTQB process:** Collaboration-based test approach — ATDD (CTFL v4.0 §4.5; CT-AcT Acceptance Testing; Agile Tester).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Story/feature from `$ARGUMENTS`. If empty, ask for the user story.

1. **Three Amigos perspective** — consider business, development, and testing views to surface assumptions and edge cases before coding (shift-left).
2. **Write clear acceptance criteria** that are specific, measurable, and verifiable (each becomes a test condition).
3. **Express acceptance tests in Gherkin** (Given/When/Then) covering: the happy path, key alternative/negative paths, boundary conditions, and authorization where relevant. Keep them business-readable.
4. Cover the **acceptance testing forms** relevant to the story: user acceptance (UAT), operational acceptance, and contractual/regulatory if applicable.
5. Make them automatable: map each scenario to the test level it will run at (API/E2E) so `/qa:implement` can turn them into procedures/scripts. If the project uses a BDD runner, format accordingly; otherwise keep Gherkin as the spec that drives Playwright tests.

Output the acceptance criteria + scenarios to `<paths.docs_dir>/ACCEPTANCE-<story>.md` (or the Test Plan's cases section). These are the definition of "done" for the story.
