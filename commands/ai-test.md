---
description: Test AI/ML-based components using ISTQB CT-AI methods — data quality, model performance metrics, bias/fairness, robustness, explainability, drift. Use when the system under test includes AI/ML features.
argument-hint: "<AI/ML feature or model>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AI/ML system testing: $ARGUMENTS

**ISTQB process:** Testing AI-based systems (CT-AI Specialist syllabus).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target AI/ML feature from `$ARGUMENTS` (e.g. recommendations, search ranking, fraud detection, a chatbot). If the product has no AI component, say so and stop.

Address the ISTQB CT-AI testing concerns:
1. **The test oracle problem** — AI outputs are often non-deterministic/probabilistic; define acceptance via metrics and tolerances, not exact-match assertions.
2. **ML functional performance metrics** — choose and measure the right ones: accuracy, precision, recall, F1, confusion matrix, ROC/AUC (classification); MAE/RMSE (regression). Set thresholds as acceptance criteria.
3. **Data testing** — training/test data quality, representativeness, labeling correctness, data bias, and data/train-serve skew. Validate the data pipeline.
4. **Bias & fairness** — test for discriminatory behavior across relevant groups; define fairness criteria.
5. **Robustness & adversarial** — behavior on noisy, edge, or adversarial inputs; negative testing.
6. **Explainability/transparency** — can decisions be explained where required?
7. **Concept/data drift** — monitoring approach so model quality degradation is detected over time.
8. **Non-determinism handling** — flakiness-tolerant test design (statistical assertions, fixed seeds where possible, metamorphic testing).

Output an AI test approach + cases to `<paths.docs_dir>/AI-TEST-<feature>.md`, and implement automatable checks (metric thresholds, data validation) under `paths.tests_dir`. Note where human/ethical review is required.
