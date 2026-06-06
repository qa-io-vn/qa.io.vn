---
description: Generate typed test-data factories, builders, fixtures, and seeding/cleanup helpers per qa.config.yml. Use when tests need data setup.
argument-hint: "<entity or domain, e.g. user, order>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test data for: $ARGUMENTS

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target entity from `$ARGUMENTS`. If empty, ask which entity/domain.

1. Follow `test_data.strategy` (default `factories`): create typed factories/builders under `tests/data/factories/` that produce valid, parallel-safe data with unique identifiers (UUID/timestamp) per call.
2. Add seeding helpers using `test_data.seed_via` (api preferred — exercises real paths; db for bulk setup) and matching teardown/cleanup so runs don't pollute each other.
3. Derive shapes from `stack.api_spec_path` (OpenAPI) where possible so data stays valid against the contract.
4. Enforce `test_data.sensitive_data_rule`: synthetic/anonymized only, never real PII. Pull secrets from `test_data.secrets_store`, never hardcode.
5. Wire the factories into the existing Playwright fixtures so specs get data declaratively.

Show the factory API and an example of using it in a test.
