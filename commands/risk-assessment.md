---
description: Perform ISTQB risk-based testing analysis — identify and score product and project risks (likelihood x impact) and derive the test response. Use for risk analysis or to prioritize testing.
argument-hint: "[release or area]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# ISTQB risk assessment${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Risk-based testing (CTFL v4.0 §5.2; CTAL-TM).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Your task

Scope from `$ARGUMENTS` (a release or area); default to the whole product.

1. **Identify risks**, separating:
   - **Product (quality) risks** — ways the test object could fail to meet a quality characteristic (functional, performance, security, accessibility, reliability — ISO 25010). Seed from `risk_areas` and the features in scope.
   - **Project risks** — schedule, resources, environment, dependencies, test data.
2. **Assess** each: **likelihood** (1–5) × **impact** (1–5) = **risk level**. Justify the scores briefly.
3. **Derive the test response** per risk: which test level(s), test type(s), and design technique rigor; how much depth; whether it gates the release. Higher risk → earlier, deeper, more independent testing.
4. **Identify risk mitigation triggers** and owners. Anything high-risk needs an owner before scope freeze.
5. Output a **Product Risk Register**: risk | type | likelihood | impact | risk level | affected quality characteristic | test response | owner. Sort by risk level. Write to `<paths.docs_dir>/RISK-REGISTER-<scope>.md` and reconcile with `risk_areas` in `qa.config.yml` (suggest updates if they diverge).

Feed the result into `/qa:create-plan` (scope & depth) and exit-criteria thinking. Read-only on product code.
