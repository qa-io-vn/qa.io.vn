---
description: Wire or run the automated security baseline — SAST, SCA, DAST, and secret scanning — gated by qa.config.yml tooling toggles, OWASP Top 10 / ASVS aligned. Use for security testing of the app/API (CT-SEC).
argument-hint: "[sast|sca|dast|secrets|all]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Security baseline: $ARGUMENTS

**ISTQB process:** Test execution — non-functional **security** testing. Operative framework: **CT-SEC** (Security Testing), **OWASP Top 10** / **OWASP ASVS**, mapping to the **ISO/IEC 25010 Security** characteristic (confidentiality, integrity, non-repudiation, accountability, authenticity). CTFL v4.0 §2.2.2 is only the generic non-functional container, not the operative standard here.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

**Step 0 — Config guard.** If the config above is `none` or lacks `tooling.security`, stop and ask the user to run `/qa:qa-init` first (or supply the security toggles). Do not assume tools — every scanner is gated by an explicit `tooling.security.*` value.

**Step 1 — Resolve scope from `$ARGUMENTS`.**
- If `$ARGUMENTS` is `sast`, `sca`, `dast`, or `secrets` → run only that scanner.
- If `$ARGUMENTS` is `all` → run every scanner whose `tooling.security.*` toggle is not `none`.
- If `$ARGUMENTS` is **empty** → default to `all` (every enabled scanner). State this default to the user before proceeding.

This is the **automated baseline** (OWASP Top 10 / ASVS Level 1), not a full pen-test. Deep penetration testing and threat modeling remain a specialist engagement — record this as residual risk (Step 8).

**Step 2 — SAST** (only if `tooling.security.sast` is not `none`): wire `<tooling.security.sast>` into CI; report insecure patterns/injection sinks in `<stack.frontend>`/`<stack.backend>` source. Coordinate findings with `/qa:static-analysis` (shared static-analysis surface).

**Step 3 — SCA** (only if `tooling.security.sca` is not `none`): run `<tooling.security.sca>` for dependency vulnerability scanning; fail the run on any severity listed in `gates.security_block_on`.

**Step 4 — DAST** (only if `tooling.security.dast` is not `none`): run `<tooling.security.dast>` as a baseline crawl plus an API scan driven by `<stack.api_spec_path>` against a non-prod environment from `environments` (never production).

**Step 5 — Secrets** (only if `tooling.security.secrets` is not `none`): run `<tooling.security.secrets>` over git history and the working tree for keys/tokens.

**Step 6 — Functional security tests** in the `<tooling.e2e>` / `<tooling.api>` suite under `<paths.tests_dir>`, concentrated on `risk_areas.critical` (e.g. authentication, authorization, payments, PII):
- **Authorization matrix** — every protected endpoint rejects wrong-role / no-token (IDOR / BOLA).
- **Input validation** — SQLi / XSS payloads handled safely.
- **Security headers** — CSP / HSTS / X-Frame-Options / etc. present.
- **Rate limiting** and **account-enumeration protection**.

**Step 7 — Classify and gate.** Assign each finding a severity (critical / high / medium / low) per the scanner's rating or CVSS. **Decision rule:** if any finding's severity is in `gates.security_block_on` (e.g. `["high","critical"]`) → the run/gate **fails**. Ticket every finding below the gate with a remediation owner and an SLA by severity.

**Step 8 — Execution mode.** Run scans where an environment/tooling is available; otherwise scaffold the scanner config and CI wiring and say so explicitly. Never run intrusive scans against production.

## Output — work product

Produce a **security findings report (Test Execution Log / Test Results, ISO/IEC/IEEE 29119-3)**, with each confirmed finding above the gate also raised as an **Incident (Defect) Report** routed to `/qa:triage`. Write the report to `<paths.reports_dir>/SECURITY-SCAN-<scope>.md` (and scanner config/CI under `<paths.tests_dir>`/CI as wired). Structure: scope and tools run; findings table `| Finding | OWASP/ASVS ref | Location | Severity | Gate (block/ticket) | Remediation |`; gate decision (pass/fail vs `gates.security_block_on`) with counts by severity; residual risk.

This realizes the ISO 25010 **Security** characteristic. It complements `/qa:static-analysis` (SAST source surface), `/qa:risk-assessment` (which security risk areas to prioritize), and routes confirmed defects to `/qa:triage`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`tooling.security.sast/sca/dast/secrets`, `gates.security_block_on`, `risk_areas`, `paths.*`, `stack.api_spec_path`, `environments`) is honored; no scanner or path is hardcoded.
- [ ] **Scope honored** — only the `$ARGUMENTS`-selected scanners (or all enabled on empty) ran; disabled (`none`) tools were skipped and noted.
- [ ] **Traceability intact** — each finding traces to a `risk_areas` / OWASP-ASVS condition and forward to a gate decision and (if confirmed above gate) an incident report; no orphan findings.
- [ ] **Measurable** — output states finding counts by severity and the explicit pass/fail gate decision against `gates.security_block_on`, not prose claims of "secure".
- [ ] **Residual risk stated** — name what is NOT covered (deep pen-testing, threat modeling, business-logic abuse, un-scanned areas) and why this is a baseline, not proof of absence (ISTQB Principle 1).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Execution Log / Test Results (security findings report) and written to the correct `<paths.reports_dir>` location, with confirmed defects routed to `/qa:triage`.
