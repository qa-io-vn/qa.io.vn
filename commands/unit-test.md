---
description: Design or review component (unit) testing at the lowest test level — structural coverage targets, isolation, test doubles. Use for unit/component test guidance and coverage at the component level.
argument-hint: "<module / component / file>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Component (unit) testing: $ARGUMENTS

**ISTQB process:** Component testing — the lowest **test level** (CTFL v4.0 §2.2.1). White-box techniques (§4.3).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target from `$ARGUMENTS` (module/component/file). Component (unit) tests are usually **developer-owned**; this command helps design, review, and strengthen them.

1. **Scope** — test a single component in **isolation**, using test doubles (stubs/mocks/fakes) for its dependencies. Verify functional behavior, and where relevant non-functional aspects (e.g. resource use) and structure.
2. **Derive cases** with the appropriate techniques: black-box (EP/BVA on the component's inputs) plus **white-box** structural coverage (statement, branch) for the logic.
3. **Coverage target** — aim for meaningful statement/branch coverage of the component, especially in `risk_areas.critical`; coverage is a guardrail, not a vanity metric (avoid the absence-of-errors fallacy). Use `tooling.unit` ({{vitest/jest}}).
4. **Quality** — each test fast, isolated, deterministic, one behavior; clear arrange/act/assert; no reliance on real I/O or other tests.
5. If reviewing existing unit tests, identify untested branches, missing negative cases, brittle mocks, and over-coupling; recommend additions.

Place/extend tests next to the component per project convention, run them, and report coverage and gaps. For structural-coverage measurement across the codebase use `/qa:coverage-measure`; for higher levels use `/qa:integration-test`, `/qa:api-automate`, `/qa:web-automate`.
