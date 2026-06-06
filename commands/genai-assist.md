---
description: Use generative AI responsibly to accelerate testing tasks (test idea generation, test data, case drafting) with ISTQB CT-GenAI safeguards. Use to speed up test work while keeping human oversight.
argument-hint: "<task, e.g. 'generate test ideas for checkout'>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# GenAI-assisted testing: $ARGUMENTS

**ISTQB process:** Using Generative AI in testing (CT-GenAI / "Testing with Generative AI" syllabus).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Task from `$ARGUMENTS`. Apply GenAI to accelerate the testing activity while following ISTQB CT-GenAI guidance:

1. **Useful applications** — generate test ideas/conditions, draft test cases, synthesize realistic-but-synthetic test data, summarize requirements, suggest edge cases, draft documentation, and explain failures. Do the requested task now using the project's test basis.
2. **Mandatory human oversight** — treat all GenAI output as a draft to be reviewed by a tester, never as authoritative. Flag anything that needs verification.
3. **Risks to manage** — hallucination/incorrectness, missing context, over-reliance, bias, and **data privacy** (never send real PII/secrets to a model; use synthetic data only, per `test_data.sensitive_data_rule`).
4. **Quality control** — validate generated tests actually run and assert meaningfully; validate generated data against the OpenAPI contract; cross-check generated conditions against risk areas for gaps.

Produce the requested artifact, clearly marked as AI-assisted draft for tester review, and list what a human must verify before it's trusted. This command is about applying GenAI *to* testing; to test an AI feature in the product use `/qa:ai-test`.
