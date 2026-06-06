---
description: Design and run non-functional tests beyond performance/security/a11y — reliability, compatibility, portability, maintainability — per ISO/IEC 25010. Use to cover non-functional quality characteristics.
argument-hint: "<characteristic, e.g. reliability, compatibility>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Non-functional testing: $ARGUMENTS

**ISTQB process:** Non-functional test types (CTFL v4.0 §2.3; CTAL-TTA; ISO/IEC 25010 quality characteristics).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Characteristic from `$ARGUMENTS`. Performance → use `/qa:perf-test`; security → `/qa:security-scan`; usability/accessibility → `/qa:a11y-audit` / `/qa:usability-test`. This command covers the rest:

- **Reliability** — error recovery, fault tolerance, availability; soak/recovery scenarios; behavior under dependency failure (use mocks to inject timeouts/500s). Maturity, recoverability.
- **Compatibility** — cross-browser/device (the `ci.browsers` matrix), co-existence, interoperability with external services and API versions.
- **Portability** — install/deploy across environments, configuration, containerization.
- **Maintainability** — modularity, analyzability of the codebase/testware (link to `/qa:static-review`).

1. Identify the relevant **quality sub-characteristics** (ISO 25010) and define measurable acceptance criteria / SLAs (extend `gates` if needed).
2. Design the test approach and concrete cases; implement what's automatable (e.g. cross-browser Playwright projects, dependency-failure simulations).
3. Run where feasible and report results against the criteria, with residual risk.

Output to `<paths.docs_dir>/NONFUNCTIONAL-<characteristic>.md` and any tests under `paths.tests_dir`.
