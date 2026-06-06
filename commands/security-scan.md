---
description: Wire or run the automated security baseline — SAST, SCA, DAST (OWASP ZAP), and secret scanning — per qa.config.yml. Use for security testing of the app/API.
argument-hint: "[sast|sca|dast|secrets|all]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Security baseline: $ARGUMENTS

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Use the tools selected under `tooling.security`. Scope from `$ARGUMENTS` (default: all enabled). This is the **automated baseline** (OWASP Top 10 / ASVS), not a full pen-test.

1. **SAST** (`tooling.security.sast`): wire the scanner in CI; report insecure patterns/injection sinks.
2. **SCA** (`tooling.security.sca`): dependency vulnerability scan; fail on `gates.security_block_on` severities.
3. **DAST** (`tooling.security.dast`): OWASP ZAP baseline + API scan driven by the OpenAPI spec against a non-prod env.
4. **Secrets** (`tooling.security.secrets`): scan history/working tree for keys/tokens.
5. **Functional security tests** in the Playwright/API suite: the authz role matrix (every protected endpoint rejects wrong-role / no-token — IDOR/BOLA), input-validation (SQLi/XSS handled safely), security headers (CSP/HSTS/etc.), rate limiting, and account-enumeration protection.
6. Gate per `gates.security_block_on`; ticket lower findings with SLAs.

Run scans where an environment/tooling is available; otherwise scaffold the config and CI wiring. Report findings by severity with remediation, and note that deep pen-testing remains a specialist engagement.
