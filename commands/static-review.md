---
description: Perform ISTQB static testing — review the test basis (requirements, user stories, OpenAPI spec) for testability and defects, plus static analysis. Use to review a story/spec before writing tests (shift-left).
argument-hint: "<story / spec / file to review> [informal|walkthrough|technical|inspection]"
allowed-tools: Read, Glob, Grep, Bash
---

# ISTQB static testing: $ARGUMENTS

**ISTQB process:** Static testing (CTFL v4.0 §3). Realizes Principle 3 (early testing / shift-left).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Subject from `$ARGUMENTS` (a story, the OpenAPI spec, requirements, or a file). A review-type hint may follow (default: technical review).

1. **Review the test basis** for the qualities ISTQB targets in reviews:
   - **Testability** — is each requirement/acceptance criterion verifiable and unambiguous?
   - **Completeness** — missing cases, error paths, non-functional needs, edge conditions?
   - **Consistency** — contradictions within the basis or against the OpenAPI spec?
   - **Correctness & clarity** — ambiguity, undefined terms, implicit assumptions.
2. Run **static analysis** where applicable (the configured `tooling.security.sast` / linters) on related code, and review the OpenAPI spec for gaps that would weaken contract/API tests.
3. Apply the chosen **review type** formality (informal review, walkthrough, technical review, or inspection) — adjust rigor and output accordingly.
4. Output **review findings**: location | issue | type (testability/completeness/consistency/ambiguity) | severity | suggested fix. Note that fixing these now is far cheaper than finding the resulting defects in execution.

This is static testing — no code is executed against the test object and no files are modified. Hand testable, clarified criteria to `/qa:test-design`.
