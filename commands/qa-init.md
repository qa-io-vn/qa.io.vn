---
description: Interview the user and generate the per-project qa.config.yml — the single file every other /qa command reads. Run this first in a new project.
argument-hint: "(no args — interactive)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Generate qa.config.yml for this project

You are setting up the **single per-project config** that powers the whole QA toolkit.

This command realizes the **Test planning** activity of the ISTQB test process (CTFL v4.0 §1.4) — it establishes the project context that every later planning artifact (Organizational Test Strategy, Test Plan, product-risk register, quality gates) is built on. `qa.config.yml` is the ISO/IEC/IEEE 29119-3 context input that those work products consume.

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
4. Run the **pre-write validation** below. Do not write the file until it passes.
5. Write the completed config to `./qa.config.yml` in the project root.
6. Emit the **structured summary** below, then suggest next steps: `/qa:create-strategy`, then `/qa:scaffold`.

Keep the YAML structure identical to the template so other commands can parse it. Do not invent values for the team or thresholds — ask or leave a clear `TBD`.

## Pre-write validation (measurable — must pass before writing)

Block the write to `./qa.config.yml` unless **all** of these hold; if any fails, ask the user the missing question instead of writing:

- [ ] **Schema match** — every top-level key in the template (`stack`, `process`, `tooling`, `ci`, `gates`, `risk_areas`, `environments`, `test_data`, `team`) exists in the output; no extra/renamed keys.
- [ ] **Parseable** — the file is valid YAML (verify with `python3 -c "import yaml,sys; yaml.safe_load(open('qa.config.yml'))"` or equivalent after writing a temp copy).
- [ ] **No invented values** — every threshold/owner not confirmed by the user or a detected signal is a literal `TBD`, not a guessed number or name.
- [ ] **Mandatory minimum** — `stack` and at least one entry in `risk_areas` are populated (a Test Plan cannot be scoped without them); `gates` either has confirmed thresholds or explicit `TBD`.
- [ ] **Readiness checklist emitted** — the table below is produced and shown to the user.

### Readiness checklist (populate before writing)

Mark each config section and report the count of populated vs `TBD` fields. The write proceeds only when no **required** section is `Missing`.

| Config section | Required? | Status (Populated / TBD / Missing) | Source (detected signal / user / TBD) | Notes |
|---|---|---|---|---|
| `stack` | yes | | | language/framework/runtime |
| `process` | no | | | agile/iterative cadence |
| `tooling` | yes | | | unit/api/e2e/perf/sec toggles |
| `ci` | yes | | | platform + pipeline file |
| `gates` | yes | | | pass rate, perf SLAs, severity gates |
| `risk_areas` | yes | | | critical areas (drives risk-based depth) |
| `environments` | no | | | dev/staging/prod targets |
| `test_data` | no | | | factories/fixtures strategy |
| `team` | no | | | roles/owners |

## Structured summary (emit after writing)

```
qa.config.yml written → ./qa.config.yml
Sections populated: <N>/9  (Populated: <list>) (TBD: <list>)
Required sections complete: <yes/no>
Risk areas captured: <count>  |  Gates defined: <count or TBD>
Tooling enabled: <list of true toggles>
Next: /qa:create-strategy → /qa:scaffold
```

State counts, not prose. If any required section is still `TBD`, name it and say which `/qa` command will need it resolved first.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded. (Here the config *is* the output: values come from detected signals or the user, never invented.)
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans. (qa-init seeds this chain by recording `risk_areas` and the test basis location that downstream commands trace from.)
- [ ] **Measurable** — output states counts/coverage (e.g. sections populated N/9, risk areas captured, gates defined) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects). Here: list every `TBD` section and the `/qa` command blocked until it is filled.
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product (the project test-context configuration that feeds the Organizational Test Strategy and Test Plan) and written to the correct location (`./qa.config.yml`).
