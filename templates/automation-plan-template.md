# Test Automation Plan — {{item}}

> ISTQB **Test Automation Engineer (CT-TAE)** workflow. Produced by `/qa:automate`.
> Source: {{source}} (requirements / manual test cases) · Generated: {{date}}

Automation is an **investment decision**, not "automate everything" (ISTQB CT-TAE / CTFL §6: automation has benefits *and* costs/risks). Each candidate is scored on **priority** (value of automating) and **complexity** (cost of automating), then selected by ROI.

## 1. Suitability filter (apply first)

Exclude tests that are inherently unsuitable for automation; keep them manual:
- Subjective checks — usability look-and-feel, UX judgment (→ `/qa:usability-test`).
- One-off / rarely-run tests, throwaway checks.
- Exploratory / experience-based testing (→ `/qa:exploratory`).
- Highly volatile UI/feature not yet stable (automate after it settles).
- Tests needing human judgment or physical interaction (CAPTCHA, true visual subjectivity).

| Test item | Suitable to automate? | Reason if no |
|---|---|---|

## 2. Priority score (value of automating) — 1–5

Driven by (weighted, risk-led):

| Factor | What raises the score |
|---|---|
| **Risk level** (likelihood × impact, from `risk_areas`) | Critical/high-risk areas |
| **Business criticality** | Core revenue/user journeys |
| **Execution frequency** | Run every build / every regression |
| **Regression value / repetitiveness** | Stable, repeated checks |
| **Manual cost saved** | Slow/tedious to run by hand |
| **Data-driven potential** | Same logic over many data sets |

→ **P1 (automate first) … P5 (deprioritize).**

## 3. Complexity / effort score (cost of automating) — 1–5

| Factor | What raises the score |
|---|---|
| Steps & system integrations | Many steps, cross-system |
| Test data setup/teardown | Hard state to create/reset |
| Test oracle determinability | Hard to assert expected result |
| External dependencies | Third-party/unstable services |
| UI volatility | Frequently-changing selectors/layout |
| Environment needs | Special infra, devices |

→ **C1 (cheap/stable) … C5 (costly/fragile).**

## 4. Automation candidacy matrix (ROI)

Combine priority × complexity:

| | **Low complexity (C1–C2)** | **High complexity (C4–C5)** |
|---|---|---|
| **High priority (P1–P2)** | **Automate first** — quick wins | **Automate (plan carefully)** — high value justifies cost |
| **Low priority (P4–P5)** | **Automate if cheap** — fill-in | **Do NOT automate** — keep manual |

| Test item | Priority (score + why) | Complexity (score + why) | Decision | Recommended level | Notes |
|---|---|---|---|---|---|
| TC-… | P1 — payment, every build | C2 — API-level, deterministic | Automate first | API | data-driven |

**Recommended test level (pyramid / CT-TAE maintainability):** prefer the **lowest** level that can verify the check — API/integration over UI E2E — to cut complexity and maintenance. Reserve UI automation for genuine end-to-end journeys.

## 5. Prioritized automation backlog

Ordered by ROI (quick wins first, then high-value/high-effort):

| Rank | Test item | Level | Effort (est.) | Sprint | Owner |
|---|---|---|---|---|---|

## 6. Automation approach & architecture

- Framework: Playwright + {{language}} (gTAA: test cases / adaptation / execution layers — `/qa:scaffold`).
- Reusable components: page objects, API clients, fixtures, data factories to build/extend.
- Data-driven / parameterized design where partitions or boundaries repeat the same logic.
- Stable selectors, web-first assertions, no hard waits (maintainability).

## 7. Plan: phases, schedule, entry/exit

- **Phase 1** — quick wins (P1–P2 / C1–C2), wire into the PR gate.
- **Phase 2** — high-value/high-effort (P1–P2 / C4–C5).
- **Phase 3** — fill-ins (P3 / low complexity).
- Entry: framework scaffolded, test data available, SUT testable.
- Exit: candidates automated, green in CI, added to regression set.

## 8. Automation metrics (CT-TAE)

Automation progress (% of selected candidates automated), automated pass rate, execution time saved, maintenance effort/flaky rate, defects found by automation. Track over time.

## 9. Risks to automation

Flaky tests, maintenance burden, unstable SUT/test data, over-reliance, tool limitations — with mitigations.
