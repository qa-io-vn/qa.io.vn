---
description: Interview the user and generate the per-project qa.config.yml — the single file every other /qa command reads. Run this first in a new project.
argument-hint: "(no args — interactive)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Generate qa.config.yml for this project

You are setting up the **single per-project config** that powers the whole QA toolkit.

## Existing config (if any)
```!
cat qa.config.yml 2>/dev/null || echo "none yet"
```

## Detected project signals
```!
echo "--- package.json ---"; cat package.json 2>/dev/null | head -40
echo "--- specs/openapi ---"; ls -1 openapi.* swagger.* api/openapi* 2>/dev/null
echo "--- CI files ---"; ls -1 Jenkinsfile .github/workflows/*.yml .gitlab-ci.yml azure-pipelines.yml 2>/dev/null
echo "--- existing tests ---"; ls -1d tests test e2e 2>/dev/null
```

## Your task

1. Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/qa.config.example.yml` to learn every field.
2. Use the detected signals above to pre-fill what you can (stack, CI platform, API spec path, test dir).
3. For anything you cannot infer, **ask the user** — group questions, don't interrogate one-by-one. Prioritise: project name/type, API style + spec path, CI platform, which test tools are in use, quality-gate thresholds (pass rate, perf SLAs, severity gates), and the critical risk areas.
4. Write the completed config to `./qa.config.yml` in the project root.
5. Confirm what was written and suggest next steps: `/qa:create-strategy`, then `/qa:scaffold`.

Keep the YAML structure identical to the template so other commands can parse it. Do not invent values for the team or thresholds — ask or leave a clear `TBD`.
