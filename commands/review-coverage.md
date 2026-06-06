---
description: Audit test coverage gaps against the strategy and risk areas, and recommend the highest-value missing tests. Use when the user asks what's under-tested or wants a coverage review.
argument-hint: "[area or path to focus on]"
allowed-tools: Read, Glob, Grep, Bash
---

# Coverage review${ARGUMENTS:+ — focus: $ARGUMENTS}

**ISTQB process:** Test monitoring (coverage) + analysis (CTFL v4.0 §5.3, §1.4.4). Audit coverage of the test basis and risk, and the integrity of the traceability chain (basis → condition → case → procedure → result).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Inventory
```!
echo "--- test files ---"; find tests -name "*.spec.*" -o -name "*.test.*" 2>/dev/null | head -80
echo "--- api spec endpoints ---"; cat openapi.yaml openapi.json swagger.* 2>/dev/null | grep -E "^\s*(/|get:|post:|put:|delete:|patch:)" | head -60
echo "--- coverage report? ---"; ls -1 coverage 2>/dev/null
```

## Your task

Optionally focus on `$ARGUMENTS` (an area or path).

1. Map what exists: which features/endpoints have tests and at which levels.
2. Compare against `risk_areas` — every **critical/high** area must have layered coverage (API + E2E + contract where relevant + the non-functional checks the strategy requires).
3. Identify **gaps** and **inversions** (logic tested only via slow E2E, missing negative/authz cases, endpoints with no schema validation, critical journeys with no E2E, missing a11y/perf/security on high-risk areas).
4. Output a prioritized table: gap, risk tier, recommended test level, why it matters. Put critical-risk gaps first.
5. Offer to generate the top items via `/qa:implement`.

This is read-only analysis — do not modify files. Be specific (name the endpoint/feature/file), not generic.
