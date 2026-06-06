---
description: Scaffold the test automation framework — Playwright+TypeScript structure, fixtures, config, plus K6 / Pact / a11y / CI pipeline per qa.config.yml. Use when setting up testing in a project for the first time.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Scaffold the test framework

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "MISSING — tell the user to run /qa:qa-init first and stop."
```

## Current repo state
```!
echo "--- root ---"; ls -1 2>/dev/null | head -40
echo "--- package.json ---"; cat package.json 2>/dev/null | head -30
echo "--- existing tests dir ---"; ls -1R tests 2>/dev/null | head -30
```

## Your task

If `qa.config.yml` is missing, stop and tell the user to run `/qa:qa-init`. Do not overwrite existing files without noting it — prefer creating missing pieces and ask before changing existing config.

Scaffold only what the config's `tooling` enables. Build under `paths.tests_dir` (default `tests/`):

1. **Playwright + TypeScript core**
   - `playwright.config.ts` with projects for each browser in `ci.browsers`, an `api` project (no browser), a `setup` project for auth storage-state, `baseURL` from config, reporters `html` + `junit` + `blob`, `trace: on-first-retry`, `retries: 2` in CI, `fullyParallel: true`.
   - Folder structure: `e2e/`, `api/`, `component/` (if enabled), `a11y/` (if enabled), `visual/` (if enabled), `fixtures/`, `pages/`, `api-clients/`, `data/factories/`, `utils/`, `config/`.
   - A `test-base.ts` that composes fixtures (auth storage-state, seeded data, typed API client), a sample Page Object, and one sample E2E + one sample API spec wired to the config URLs.
   - `tsconfig.json`, and `package.json` scripts (`test`, `test:e2e`, `test:api`, `test:smoke`, `test:report`).
2. **K6** (if `performance: k6`): `tests/performance/` with a parameterized load script and `thresholds` built from `gates.performance`.
3. **Pact** (if `contract: pact`): consumer test skeleton + publish/verify scripts pointing at `contract_broker_url`, with a `can-i-deploy` script.
4. **Accessibility** (if `accessibility: axe`): an axe + Playwright helper and a sample scan of a key page.
5. **Visual** (if enabled): a sample `toHaveScreenshot` spec with masking guidance.
6. **Security** (if enabled): config stubs / scripts for the chosen SAST/SCA/DAST/secret tools.
7. **CI pipeline** for `ci.platform`: a `Jenkinsfile` (or workflow file) implementing a fast PR gate (lint, type-check, unit, component, API mocked, contract-consumer, smoke E2E, a11y key pages, visual, SCA/secret, can-i-deploy) and nightly/pre-release stages (full E2E sharded across `ci.shard_count`, K6, ZAP, full scans). Use `ci.agents_docker_image`.

Use stable selectors and fixtures, no hard waits. After scaffolding, list what you created, note any install commands the user should run, and suggest `/qa:implement <feature>`.
