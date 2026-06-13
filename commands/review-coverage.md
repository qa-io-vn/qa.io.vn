---
description: Audit test-coverage gaps against the strategy and risk areas, verify the bidirectional traceability chain, and recommend the highest-value missing tests. Use when the user asks what's under-tested or wants a coverage review.
argument-hint: "[area or path to focus on]"
allowed-tools: Read, Glob, Grep, Bash, Write
---

# Coverage review

**ISTQB process:** Test monitoring (coverage) + test analysis — coverage and traceability audit (CTFL v4.0 §5.3 monitoring/coverage; §1.4.4 traceability). Verify any section number against the current syllabus. Use strict ISTQB terminology and preserve bidirectional traceability (test basis → condition → case → coverage item → procedure → result → defect).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Inventory (discovery)
```!
echo "--- test files ---"; find . -path ./node_modules -prune -o \( -name "*.spec.*" -o -name "*.test.*" -o -name "*Test.*" -o -name "*_test.*" -o -name "test_*.*" -o -name "*Steps.*" \) -print 2>/dev/null | head -80
echo "--- api spec endpoints ---"; find . -path ./node_modules -prune -o \( -name "openapi.*" -o -name "swagger.*" \) -print 2>/dev/null | head -5; cat $(find . -path ./node_modules -prune -o \( -name "openapi.*" -o -name "swagger.*" \) -print 2>/dev/null | head -1) 2>/dev/null | grep -E "^\s*(/|get:|post:|put:|delete:|patch:)" | head -60
echo "--- coverage report? ---"; find . -path ./node_modules -prune -o -name "coverage-summary.json" -print 2>/dev/null | head -5; ls -1 coverage 2>/dev/null | head
```

## Your task

If `qa.config.yml` is missing above, stop and tell the user to run `/qa:qa-init`. Otherwise honor it: read `paths.*` (e.g. `paths.tests_dir`, `paths.api_spec`, `paths.reports_dir`, `paths.docs_dir`), `risk_areas` (critical/high/medium), `tooling.*` toggles (only audit a test type when its tooling is enabled), and `gates`. Never hardcode project-specific paths, tools, or areas — use the discovery output above and `<paths.*>` / `<tooling.*>` / `<stack.*>` values from config.

**Scope resolution (`$ARGUMENTS`):**
1. If `$ARGUMENTS` names an area or path, scope the audit to it; state the scope.
2. If `$ARGUMENTS` is empty, default the scope to the areas in `risk_areas.critical`; state that you defaulted and which areas were used.

Then perform the audit in order:

1. **Map what exists.** For each feature/endpoint/journey in scope, record which test levels have coverage — component, integration (incl. contract where `<tooling.contract>` is enabled), system/E2E, acceptance — and which non-functional types (`<tooling.performance>`, `<tooling.security.*>`, `<tooling.accessibility>`) apply. Derive this from the discovery output and `<paths.api_spec>`, not from assumption.

2. **Audit the bidirectional traceability chain** (CTFL v4.0 §1.4.4) for each item in scope: test basis → test condition → test case → coverage item → test procedure → result → defect. Flag every orphan in either direction:
   - **Forward gaps** — a test basis element (requirement / user story / endpoint) with no condition or case downstream.
   - **Backward orphans** — a test/script with no link up to a condition or basis element (a test that traces to nothing).

3. **Compare against `risk_areas`.** Apply this rule: every **critical** and **high** area MUST have layered coverage — API + E2E + contract (where `<tooling.contract>` enabled) + the non-functional checks the enabled tooling and `gates` require. Mark any critical/high area missing a required layer as a **gap**.

4. **Detect coverage inversions and defects** (apply each rule explicitly):
   - Logic tested only via slow E2E that could move down the pyramid → **inversion**.
   - Missing negative / authorization / boundary cases on a covered endpoint → **gap**.
   - Endpoint with no schema/contract validation while `<tooling.contract>` is enabled → **gap**.
   - Critical user journey with no system/E2E coverage → **gap**.
   - Missing a11y/perf/security on a high-risk area where that tooling is enabled → **gap**.
   - Stale tests on changed code (pesticide paradox, Principle 5) → flag for refresh/retire.

5. **Assign a risk tier to each gap** using the area's tier in `risk_areas` (critical/high/medium/low). Gaps in untiered areas inherit the tier of the nearest enclosing `risk_areas` entry, or **medium** if none.

6. **Output the gap list** as a prioritized table, sorted by risk tier descending (critical first), with columns: `gap/orphan | risk tier | type (forward gap | backward orphan | inversion | missing layer) | recommended test level/type | why it matters (link to basis/risk) | suggested command`. Name the specific endpoint/feature/file — never a generic placeholder. Include a **counts summary**: total items in scope, items fully covered, forward gaps, backward orphans, inversions, gaps by tier.

This is **read-only** analysis — do not modify product or test files.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded; only enabled test types were audited.
- [ ] **Traceability intact** — the chain test basis → condition → case → coverage item → procedure → result (→ defect) was audited in **both** directions; forward gaps and backward orphans are both reported; no orphan is silently dropped.
- [ ] **Measurable** — output states counts/coverage (items in scope, covered, gaps by tier, orphans, inversions) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why, and note that an absent gap does not prove an area is defect-free (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — the gap list is identified as a coverage/traceability analysis contributing to the ISO/IEC/IEEE 29119-3 **Test Status (Progress) Report** (coverage dimension); if written, it goes to the correct `<paths.reports_dir>` (or `<paths.docs_dir>`) location.

Hand off the prioritized gaps: `/qa:test-design` to derive the missing conditions/cases, `/qa:implement` to author the top items, and `/qa:coverage-measure` to quantify structural/requirements/risk coverage once gaps are closed. Feed findings back into `/qa:risk-assessment` (coverage gaps surface new product risks) and `/qa:status-report` (which reports against this coverage dimension).
