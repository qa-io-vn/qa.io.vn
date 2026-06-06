---
description: Set up or document the test environment and configuration management of testware. Use to provision a test environment, manage test environment requirements, or version-control testware.
argument-hint: "[environment name]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test environment & configuration management${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test implementation (environment) + Configuration management (CTFL v4.0 §1.4, §5.4).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Target environment from `$ARGUMENTS` (else use `environments` from config).

1. **Define test environment requirements**: services, dependencies, test doubles (stubs/drivers/simulators/service virtualization), data state, network, and the configuration each test level needs (component/integration/system/acceptance).
2. **Provision / document** the environment: produce the setup (docker-compose, env files, seed scripts, mock servers) consistent with `ci.agents_docker_image` and the base URLs in config. Make it reproducible and isolated so parallel runs don't collide.
3. **Configuration management of testware** (ISTQB §5.4): ensure all testware (tests, data, environment definitions, tool configs) is version-controlled, identifiable, and traceable to the test basis; baselines align with product versions.
4. **Verify** the environment is healthy (smoke check) where possible.

Output the environment definition under `paths.tests_dir` and document it in `<paths.docs_dir>/TEST-ENVIRONMENT.md`. Never put secrets in the repo — reference `test_data.secrets_store`.
