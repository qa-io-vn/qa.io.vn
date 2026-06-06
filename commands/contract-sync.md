---
description: Generate or verify Pact consumer/provider contracts and run can-i-deploy. Use for contract testing between the web app and the REST API.
argument-hint: "[consumer|provider|can-i-deploy]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Contract testing: $ARGUMENTS

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

If `tooling.contract` is not `pact`, say it's disabled and offer to enable it. Mode from `$ARGUMENTS` (default: do consumer + provider as relevant).

1. **Consumer (web):** add/extend Pact consumer tests that record the web app's expectations for the endpoints it calls (drive shapes from `stack.api_spec_path`). Publish pacts to `tooling.contract_broker_url`, tagged with branch/version.
2. **Provider (API):** add/extend provider verification that replays recorded pacts against the API, with provider states for setup.
3. **can-i-deploy:** wire/run the `can-i-deploy` check so a deploy is blocked unless the contract matrix is green for the target environment.
4. Ensure the CI definition triggers consumer publish on web changes and provider verification on API changes (webhook or pipeline stage).
5. Explain how this backstops any API mocking (mocks that drift are caught here).

Report what was generated/verified and the current compatibility status.
