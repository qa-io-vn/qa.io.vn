---
description: Design testing in production (shift-right) — synthetic monitoring, observability/SLO checks, canary/A-B validation, feature-flag and post-deploy smoke testing. Produces a Production Verification Report. Use to verify quality in the live environment safely.
argument-hint: "[feature / journey]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Shift-right / testing in production: $ARGUMENTS

**ISTQB process:** Testing in production — shift-right / continuous testing & monitoring (**Quality in DevOps**, Specialist stream). Complements, and never replaces, pre-release (shift-left) testing (ISTQB Principle 3 — early testing). Verify any specific syllabus section against the current syllabus before quoting a number; this command does not assert a CTFL Foundation section it cannot trace.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```
**Config guard:** if the read above prints `none`, state that no `qa.config.yml` was found, use documented defaults for every `<paths.*>` / `<tooling.*>` / `<stack.*>` / `gates` / `risk_areas` placeholder, and flag the missing config in the report's residual risk. Never substitute a hardcoded path or tool name.

## Your task

Produce a **Production Verification Report** — the ISO/IEC/IEEE 29119-3 work product for shift-right (testing in production). Follow `${CLAUDE_PLUGIN_ROOT}/templates/shift-right-template.md` for structure; write the result to `<paths.reports_dir>/production-verification-<scope>.md` and any synthetic-check scripts under `<paths.tests_dir>`.

Shift-right validates quality in the real environment, where pre-release testing cannot fully reach — done **safely**: read-only, synthetic accounts, no PII (`test_data.sensitive_data_rule`), never load or destructive against production data.

### 1. Scope (resolve `$ARGUMENTS` first)
- If `$ARGUMENTS` names a feature/journey, scope to it.
- If `$ARGUMENTS` is **empty**: default to the `risk_areas.critical` journeys from `qa.config.yml`. If `risk_areas` is absent or empty, ask the user which critical journey/feature to verify before proceeding — do not guess.
- List the scoped journeys, each traced to its `risk_areas` entry (critical → high → medium). State N of M `risk_areas` journeys covered.

### 2. Synthetic checks / post-deploy smoke
- Define scripted probes of each scoped journey running continuously against production-safe endpoints (`<stack.base_url_web>` / `<stack.base_url_api>`), built on the configured framework (`<tooling.e2e>` for browser journeys, `<tooling.api>` for API probes — fall back to the detected stack only if those toggles are unset).
- For each check specify: journey ref, type (browser/API/uptime), tool, target env (`environments`), frequency, locations, assertion/oracle, owner.
- Rule: every scoped journey has ≥1 synthetic check (no orphans). State total checks by type and by journey.

### 3. Observability — SLIs & SLOs
- Define the Service Level Indicators to measure (latency, error rate, saturation/availability, journey success rate) and the SLO target each is evaluated against.
- Derive SLO thresholds from `gates` where applicable (e.g. `gates.performance` for latency/error-rate, `gates.min_pass_rate_pct` for journey success); mark any target that is "agreed" rather than config-derived.
- Verify logging/metrics/tracing actually expose each SLI's source signal; flag any SLI with no telemetry source as a residual-risk gap. State error-budget remaining/consumed per SLO.

### 4. Progressive-delivery validation (canary / A-B / feature flags)
- **Canary:** define cohort/% traffic, promotion criteria (named SLIs within SLO for N minutes), and the rollback trigger (SLO breach / error-budget burn rate).
- **A/B experiment:** define variant cohorts and the guardrail SLIs that must not regress.
- **Feature flags:** verify behavior with each flag on/off and that the flag kill-switch provides a safe, automated rollback.
- Record one explicit decision — **promote / hold / roll back** — with the SLI/SLO evidence that justified it.

### 5. Production health gates & verdict
- Define post-deploy checks that confirm the release is healthy and the rollback/flag-off plan actually works.
- Evaluate overall health: **healthy / degraded / roll back**, evidence = SLO status (§3) + any incidents observed.
- Give a recommendation (continue / hold promotion / roll back / open follow-up testing); approvers from `team`.

### 6. Traceability (preserve and report)
Maintain the bidirectional chain end-to-end — no orphans:

```
risk area (risk_areas) → test condition (what could fail in prod)
   → synthetic check (§2) → SLI / SLO (§3) → result (met / breached)
      → incident / defect (if a breach is observed)
```

State the count of `risk_areas` covered end-to-end versus total, and list any gap.

### 7. Residual risk in production
Name what this verification does **not** cover and why (ISTQB Principle 1 — testing shows the presence, not the absence, of defects; shift-right observes only what live traffic exercises): journeys with no synthetic check or no SLO, low-traffic paths not exercised in the window, sampling/cardinality blind spots, alerts without runbooks. "No incidents observed" is a result, not a clearance — state the observation window and coverage so absence is not over-read.

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`, `environments`, `team`) is honored; nothing hardcoded (no literal tool/path names).
- [ ] **Traceability intact** — the chain risk area → condition → synthetic check → SLI/SLO → result (→ defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (synthetic checks by type, N of M `risk_areas` journeys, SLO met/at-risk/breached, error-budget %) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered in production and why (ISTQB Principle 1).
- [ ] **Safety honored** — read-only, synthetic data only, no load/destructive tests against production; rollback/flag-off path verified.
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Production Verification Report** and written to `<paths.reports_dir>/production-verification-<scope>.md`.

---

**Routing:** pair with `/qa:dynamic-analysis` (runtime defects such as leaks/exhaustion observed under load) and `/qa:release-report` (the Test Completion Report that consumes post-deploy verification evidence). If a synthetic check or SLO breach surfaces a confirmed defect, route it to `/qa:triage`.
