---
description: Test AI/ML-based components using ISTQB CT-AI methods — data quality, ML functional-performance metrics, bias/fairness, robustness, explainability, and drift, mapped to ISO/IEC 25010 plus AI-specific quality characteristics. Use when the system under test includes AI/ML features.
argument-hint: "<AI/ML feature or model>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AI/ML system testing: $ARGUMENTS

**ISTQB process:** Test execution + analysis for AI-based systems. Operative framework: **CT-AI** (Testing AI-Based Systems, Specialist syllabus) — a Specialist topic, never CTFL Foundation. Quality model: **ISO/IEC 25010** functional suitability, reliability, performance efficiency, and security, extended with **AI-specific quality characteristics** (functional correctness under non-determinism, adaptability, flexibility, autonomy, evolution/drift resistance, transparency/explainability, freedom from unwanted bias). Cite CT-AI concepts by name; do not assert specific syllabus section numbers — verify any § against the current CT-AI syllabus before quoting it.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

**Step 0 — Config guard.** If the config above is `none`, stop and ask the user to run `/qa:qa-init` first (or supply `paths.*`, `risk_areas`, `gates`, and `test_data.sensitive_data_rule`). Do not hardcode paths, tools, or thresholds — read every one from `qa.config.yml`.

**Step 1 — Resolve the target from `$ARGUMENTS`.**
- If `$ARGUMENTS` names an AI/ML feature (e.g. recommendations, search ranking, fraud detection, a chatbot/LLM feature) → scope to that feature.
- If `$ARGUMENTS` is **empty** → default to the AI/ML-bearing entries in `risk_areas.critical`; if none are obviously AI/ML, ask the user which feature to test rather than guessing. State the chosen default before proceeding.
- If the product has **no AI/ML component**, say so and stop (this command is not applicable).

**Step 2 — Classify the AI component and pick the oracle strategy.** Record: model type (classification / regression / ranking / generative-LLM / clustering), determinism (deterministic vs probabilistic), and whether an exact-match oracle exists.
- **Decision rule:** if outputs are non-deterministic/probabilistic, do **not** use exact-match assertions. Use one or more of: metric-threshold assertions, statistical assertions over a sample, metamorphic relations, and fixed seeds where the runtime supports them. Name the oracle strategy for each test.

**Step 3 — ML functional-performance metrics (set measurable thresholds).** Choose metrics by task and bind each to an acceptance threshold from `gates` (or propose one and flag it for sign-off):
- Classification → accuracy, precision, recall, F1, confusion matrix, ROC/AUC.
- Regression → MAE, RMSE, R².
- Ranking/recommendation → precision@k, recall@k, NDCG, MRR.
- Generative/LLM → task-appropriate quality + safety measures (e.g. groundedness/faithfulness, refusal correctness, toxicity rate); state that these need human review.
Every metric must have a numeric acceptance threshold and a measured value, not a prose claim.

**Step 4 — Data testing.** Validate the data pipeline and datasets: training/test split integrity (no leakage), representativeness vs production distribution, label correctness, missing/outlier handling, and train–serve skew. Concentrate checks on `risk_areas.critical`/`high`.
- **Decision rule (PII/data safeguard):** honor `test_data.sensitive_data_rule` (e.g. "synthetic-only — never real PII"). Do **not** read, copy, log, or write real PII or production secrets into test fixtures or reports; use synthetic or anonymized data per `test_data.strategy`. If real data is unavoidable for a check, stop and escalate for data-handling approval rather than proceeding.

**Step 5 — Bias & fairness.** Define protected groups and a fairness criterion (e.g. demographic parity, equalized odds, predictive parity), measure the chosen metric across groups, and set an acceptance tolerance. Flag any group disparity above tolerance as a finding. Mark fairness/ethical acceptance as requiring **human review** — this command does not adjudicate ethical acceptability.

**Step 6 — Robustness & adversarial.** Test behavior on noisy, edge, out-of-distribution, and adversarial inputs (negative testing, perturbations, prompt-injection for LLMs). Set a robustness threshold (e.g. max accuracy drop under defined perturbation) and measure against it.

**Step 7 — Explainability/transparency.** Where decisions are user-facing, regulated, or in `risk_areas.critical`, verify that explanations are available and faithful to the model behavior. Record where explainability is required but absent as a finding.

**Step 8 — Concept/data drift monitoring.** Define the monitoring approach so quality degradation is detected in production: which metrics are tracked, the alert threshold, and the cadence. Coordinate production observability with `/qa:dynamic-analysis` (shift-right monitoring). State that drift detection is ongoing, not a one-time gate.

**Step 9 — Gate decision.** Compare each measured metric to its threshold. **Decision rule:** if any metric in scope fails its acceptance threshold, or any bias disparity exceeds tolerance → the AI gate **fails**. Report counts of pass/fail by category; route confirmed defects to `/qa:triage`.

**Step 10 — Execution mode.** Run checks where data/tooling is available; otherwise scaffold the metric-threshold and data-validation checks (under `<paths.tests_dir>`) plus the test-approach doc and say so explicitly. Never use production PII to make this runnable (see Step 4).

## Output — work product

Produce an **AI test approach and case specification** — a Test Design / Test Case Specification (ISO/IEC/IEEE 29119-3) specialized for AI-based systems — written to `<paths.docs_dir>/AI-TEST-<feature>.md`. Implement the automatable checks (metric-threshold assertions, data-validation, robustness/bias measurements) under `<paths.tests_dir>`; route any measured results that fail their gate as an **Incident (Defect) Report** to `/qa:triage`.

Structure the doc: target feature and model classification; oracle strategy per test; metrics table `| Quality char (ISO 25010 / AI) | Metric | Threshold | Measured | Pass/Fail | Oracle |`; data-testing findings; bias/fairness results by group with tolerance; robustness results; explainability status; drift-monitoring plan; gate decision with counts; residual risk and where human/ethical review is required.

This maps to the ISO 25010 functional suitability, reliability, performance efficiency, and security characteristics plus AI-specific characteristics. It complements `/qa:risk-assessment` (which AI risk areas to prioritize), `/qa:test-data` (synthetic/representative datasets), `/qa:dynamic-analysis` (production drift/observability), and `/qa:genai-assist` (using GenAI *to* test, the inverse of this command); confirmed defects route to `/qa:triage`.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.docs_dir`/`paths.tests_dir`, `risk_areas`, `gates` thresholds, `test_data.strategy`/`sensitive_data_rule`) is honored; no path, tool, or threshold is hardcoded.
- [ ] **Data/PII safe** — no real PII or production secrets were read, logged, or written into fixtures/reports; `test_data.sensitive_data_rule` was honored (synthetic/anonymized only).
- [ ] **Measurable** — every metric in scope has a numeric threshold and a measured value with an explicit pass/fail, plus the overall gate decision — not prose claims of "works" or "fair".
- [ ] **Oracle stated** — each test names its oracle strategy (metric threshold / statistical / metamorphic / fixed-seed); no exact-match assertion is used on non-deterministic output.
- [ ] **Traceability intact** — each AI quality concern traces test basis → condition (ISO 25010 / AI characteristic) → case → measured result → gate decision (→ defect); no orphans.
- [ ] **Residual risk & human oversight stated** — name what is NOT covered (e.g. full adversarial/ethical review, long-horizon drift, exhaustive fairness) and where human/ethical sign-off is required (ISTQB Principle 1; CT-AI human-oversight expectation).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 Test Design / Test Case Specification (AI test approach) and written to the correct `<paths.docs_dir>` location, with failing results routed to `/qa:triage`.
