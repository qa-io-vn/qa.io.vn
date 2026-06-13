---
description: Audit an existing test-automation project end-to-end — architecture (gTAA layering/POM), SOLID & clean-code adherence, test-case/test-design quality, anti-patterns, and pyramid/level distribution — and produce a scored health report with prioritized fixes. Use to assess or onboard an inherited automation suite. Modifies nothing in the audited suite (writes only the report); distinct from /qa:static-analysis (source metrics) and /qa:review-coverage (coverage gaps).
argument-hint: "[path / module to focus on]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Automation project audit

**ISTQB process:** Static testing of **testware** + Test Automation Engineering assessment (CTFL v4.0 §3.1; CT-TAE — gTAA architecture, maintainability, reporting; ISO/IEC 25010 maintainability: modularity, reusability, analysability, modifiability, testability). The automation codebase *is* the test object here. Analyze and report only — never modify the audited code; the only file you write is the assessment report.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — stack/risk will be inferred from the repo"
```

## Stack & framework signals
```!
echo "--- language/build ---"; find . -maxdepth 2 \( -name 'package.json' -o -name 'pom.xml' -o -name 'build.gradle*' -o -name 'requirements.txt' -o -name 'pyproject.toml' -o -name '*.csproj' -o -name 'go.mod' \) -not -path '*/node_modules/*' 2>/dev/null
echo "--- automation framework ---"; find . -maxdepth 2 \( -name 'package.json' -o -name 'pom.xml' -o -name 'build.gradle*' -o -name 'requirements.txt' -o -name 'pyproject.toml' -o -name '*.csproj' \) -not -path '*/node_modules/*' -print0 2>/dev/null | xargs -0 grep -ilE "playwright|selenium|cypress|webdriverio|puppeteer|appium|rest-?assured|pytest|junit|testng|nunit|xunit|cucumber|karate" 2>/dev/null | head
echo "--- runner config ---"; find . -maxdepth 3 \( -name 'playwright.config.*' -o -name 'cypress.config.*' -o -name 'wdio.conf.*' -o -name 'testng.xml' -o -name 'pytest.ini' -o -name 'conftest.py' \) -not -path '*/node_modules/*' 2>/dev/null
echo "--- CI ---"; ls Jenkinsfile .gitlab-ci.yml azure-pipelines.yml 2>/dev/null; find .github/workflows -name '*.y*ml' 2>/dev/null
```

## Structure & size signals
```!
echo "--- top-level test tree ---"; find . -type d \( -iname "tests" -o -iname "test" -o -iname "e2e" -o -iname "src" -o -iname "pages" -o -iname "fixtures" -o -iname "support" -o -iname "specs" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -40
echo "--- test file count ---"; find . \( -name "*.spec.*" -o -name "*.test.*" -o -name "*Test.*" -o -name "*_test.*" -o -name "test_*.*" -o -name "*Steps.*" \) -not -path "*/node_modules/*" 2>/dev/null | wc -l
echo "--- page objects ---"; find . \( -iname "*page*.*" -o -iname "*.po.*" \) -not -path "*/node_modules/*" 2>/dev/null | grep -ivE "spec|test" | head -30
echo "--- smell: hard waits ---"; grep -rinE "waitForTimeout|Thread\.sleep|time\.sleep|sleep\(" . --include='*.ts' --include='*.js' --include='*.java' --include='*.py' --include='*.cs' 2>/dev/null | grep -v node_modules | wc -l
echo "--- smell: fragile selectors (xpath/nth) ---"; grep -rinE "xpath=|By\.xpath|//\*\[|nth-child" . --include='*.ts' --include='*.js' --include='*.java' --include='*.py' --include='*.cs' 2>/dev/null | grep -v node_modules | wc -l
echo "--- smell: hardcoded secrets/urls ---"; grep -rinE "password\s*[=:]\s*[\"']|https?://[a-z0-9.-]+/" . --include='*.ts' --include='*.js' --include='*.java' --include='*.py' --include='*.cs' 2>/dev/null | grep -v node_modules | wc -l
echo "--- skipped/disabled tests ---"; grep -rinE "\.skip|\.only|@Disabled|@Ignore|xit\(|xdescribe\(|pytest\.mark\.skip" . --include='*.ts' --include='*.js' --include='*.java' --include='*.py' --include='*.cs' 2>/dev/null | grep -v node_modules | wc -l
```

## Your task

Scope from `$ARGUMENTS` (a path/module) else the whole automation project; if `risk_areas` exist in config, weight depth toward critical/high areas (Principle 4 — defects cluster). Read representative files across each layer — don't audit by grep counts alone; open the page objects, base classes, fixtures, a sample of specs, the runner config, and CI. Produce a **structured assessment** across these dimensions:

### 1. Architecture & gTAA layering
Map the project to the **generic test automation architecture** (CT-TAE): **test definition** (how cases are specified — specs, BDD features, data tables), **test adaptation** (page objects, API clients, drivers, fixtures, service virtualization), and **test execution** (runner, CI, reporting). Assess:
- **Separation of concerns** — is the SUT decoupled from tests via an adaptation layer? Or do specs talk to raw selectors/HTTP directly?
- **Project structure** — coherent folders (pages/components, fixtures, data, utils, specs by level), naming consistency, base classes vs duplication.
- **Configuration & environment management** — env/URL/credential handling centralized (not hardcoded), parameterized per environment.
- **Test data layer** — factories/builders/fixtures vs inline literals; ownership and isolation.
- **Reporting & execution** — runner config, parallelization/sharding, retries policy, reporters, artifacts.

### 2. SOLID & design principles (applied to test code)
Evaluate each, with concrete file/line evidence and a fix:
- **SRP** — each Page Object models one page/component; each test verifies one behavior; **assertions live in tests, not in page objects**; no "god" objects or fat `utils` dumping grounds.
- **OCP** — framework extended via base classes/composition/fixtures, not by editing core for every new test; reusable component objects.
- **LSP** — base-page / base-test subclasses honor the base contract; overrides don't break expectations.
- **ISP** — focused, cohesive interfaces/helpers; tests don't depend on methods they don't use.
- **DIP** — tests depend on **abstractions** (interfaces, injected fixtures/DI), not concrete drivers/clients instantiated inline; config and driver are injected.
- **DRY / KISS** — duplication (copy-pasted flows/selectors), over-engineering, dead code, magic numbers/strings (cross-check the `page-object-clean-code` discipline where applicable).

### 3. Test-case & test-design quality (ISTQB + FIRST)
For a representative sample of tests, assess:
- **Independence & atomicity (FIRST)** — Fast, Independent (no order/shared-state coupling), Repeatable (deterministic, parallel-safe, each test owns its data), Self-validating (clear pass/fail, real assertions — not "element clickable"), Timely. Flag inter-test dependencies and shared mutable state.
- **Single responsibility per test** — one condition per case; no hidden multi-case loops/conditionals/branching in test bodies.
- **Naming & readability** — names state the test condition/expected outcome; arrange-act-assert clarity.
- **Assertion quality** — web-first/explicit assertions, meaningful oracles tied to requirements, no missing or trivial assertions, no over-asserting unrelated state.
- **Technique coverage (ISTQB §4)** — are EP, BVA (2-/3-value), decision-table, state-transition evident where the feature warrants? Is there **negative & boundary** coverage, not just happy path?
- **Traceability** — do the tests and conditions link back to requirements/risk (basis → condition → case)? Route deep coverage-gap analysis to `/qa:review-coverage`.

### 4. Anti-patterns & flakiness risk
Confirm each grep signal by reading the code (counts include false positives):
- **Hard waits** (`waitForTimeout`/`sleep`/fixed timeouts) instead of state-based waiting.
- **Fragile selectors** — XPath, CSS coupled to layout/styling, brittle indexes; missing `data-testid`/role-based locators.
- **Hardcoded** URLs, credentials, secrets, environment data, or test data in code (secrets must come from `test_data.secrets_store`).
- **Skipped/`.only`/disabled** tests left in the suite; commented-out tests; no-assertion tests.
- **Pesticide paradox** — stale tests that no longer find defects; recommend refresh/retire (route to `/qa:flaky-hunt`, `/qa:self-heal`).

### 5. Test pyramid / level distribution
Count tests by level (unit/component · integration/API/contract · UI-E2E) and flag **inversion** (ice-cream cone — logic verified only through slow E2E). Recommend pushing coverage to the lowest effective level (route target architecture to `/qa:automation-strategy`).

### 6. CI/CD & execution health
PR-gate vs nightly placement, parallelization/sharding, flaky-retry policy, reporting/artifacts, quality-gate wiring against `gates`. Note pipeline fragility (route fixes to `/qa:fix-ci`).

## Output

Write an **Automation Project Assessment Report** to `<paths.docs_dir>/AUTOMATION-AUDIT.md`. This is not a dedicated ISO/IEC/IEEE 29119-3 work product; it is a static-testing review record of the testware (the closest 29119-3 analogue is review/static-analysis findings), scoring maintainability per ISO/IEC 25010 (modularity, reusability, analysability, modifiability, testability). It must contain:
- **Executive summary** — what the suite is, stack/framework detected, headline strengths & top risks.
- **Maturity scorecard** — rate each dimension above (Architecture, SOLID/clean-code, Test-design quality, Anti-patterns/flakiness, Pyramid, CI) on a 1–5 scale with a one-line justification each, plus an overall rating.
- **Findings table** — `finding | location (file:line) | dimension | severity (critical/high/medium/low) | recommendation`. Be specific (name the file/class/test), never generic. Order critical first; weight toward `risk_areas`.
- **Prioritized remediation roadmap** — quick wins vs structural refactors, each routed to the command that does the work: `/qa:static-analysis` (code metrics/complexity), `/qa:review-coverage` (coverage gaps), `/qa:automation-strategy` (target gTAA/pyramid), `/qa:self-heal` & `/qa:flaky-hunt` (selectors/flakiness), `/qa:test-cases` / `/qa:scan-ui` (fill gaps), `/qa:fix-ci` (pipeline).

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*` for the report location, `tooling.*` toggles, `gates`, `risk_areas`) is honored; no path or tool is hardcoded, and depth is weighted toward `risk_areas.critical`/`high` (Principle 4).
- [ ] **Evidence-based, not grep-counted** — every finding cites a concrete `file:line` confirmed by reading the code; grep signals were verified (false positives discarded), not reported as-is.
- [ ] **Measurable** — the scorecard states 1–5 ratings per dimension and counts (test files by level, smell counts, skipped tests) rather than prose claims.
- [ ] **Read-only honored** — nothing in the audited suite was modified; the report at `<paths.docs_dir>/AUTOMATION-AUDIT.md` is the only file written.
- [ ] **Routing complete** — each remediation item is routed to the sibling command that does the work (`/qa:static-analysis`, `/qa:review-coverage`, `/qa:automation-strategy`, `/qa:self-heal`, `/qa:flaky-hunt`, `/qa:test-cases`, `/qa:scan-ui`, `/qa:fix-ci`); no orphaned recommendation.
- [ ] **Residual risk stated** — name what the audit did NOT cover (sampled, not exhaustive — Principle 1/2) and why, and identify the ISO/IEC 25010 maintainability sub-characteristics most at risk.

State residual risk, not "the suite is good/defect-free" (Principle 1). The audit is a sampled static review, not exhaustive (Principle 2): name the layers/files not opened and the maintainability sub-characteristics left at risk. This assessment modifies nothing in the audited suite — propose changes; apply none (the report is the only file written).
