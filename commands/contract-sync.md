---
description: Generate or verify consumer/provider contracts (consumer-driven contract testing) and run a can-i-deploy gate, then write the Test Execution Log. Use for contract testing across the integration boundary between the web app and the REST API.
argument-hint: "[consumer|provider|can-i-deploy]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Contract testing: $ARGUMENTS

**ISTQB process:** Test implementation & execution applied at the **component/system integration** test level (consumer-driven contract testing) (CTFL v4.0 §2.2 — test levels, component/system integration; CT-TAE). Verify section numbers against the current syllabus before quoting.
**Work product:** ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the contract suite (consumer pact results, provider verification results, and the `can-i-deploy` matrix), plus an **Incident (Defect) Report** for any contract mismatch.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Step 0 — Read config & gate on contract tooling (do this first)

1. Read `qa.config.yml` from the block above. If it printed `none`, tell the user config is missing, suggest `/qa:qa-init`, and proceed only with documented defaults the user confirms — do **not** invent paths, tools, or a broker URL. Resolve the config-derived inputs in scope: `<tooling.contract>` (the contract tool), `<tooling.contract_broker_url>` (the broker/matrix endpoint), `<stack.api_spec_path>` (source of truth for expected shapes), `<paths.tests_dir>` (where contract tests live), `<paths.docs_dir>` (where the execution log is written), `<paths.reports_dir>` (where raw tool output lands), `environments` (deploy targets for the matrix), `gates` (deploy gate), and `risk_areas` (which endpoints to prioritize). Nothing about paths, tools, or the broker is hardcoded.
2. **Contract-tooling guard:** if `<tooling.contract>` is unset or `none`, state that contract testing is **disabled** for this project, offer to enable it (set `tooling.contract` and `tooling.contract_broker_url` in `qa.config.yml`), and stop — do not generate contract tests against a disabled toggle.
3. Resolve the **mode** from `$ARGUMENTS`:
   - **`consumer`** → Step 1 only (record/publish consumer expectations).
   - **`provider`** → Step 2 only (verify recorded pacts against the API).
   - **`can-i-deploy`** → Step 3 only (run the deploy gate against the matrix).
   - **If `$ARGUMENTS` is empty:** do **not** guess. Ask the user which mode they want. If the user declines or cannot specify, **default to the full flow** — consumer (Step 1) then provider (Step 2) then the can-i-deploy gate (Step 3) — and state explicitly that you defaulted there and why. Prioritize the endpoints touching `risk_areas.critical` first.

## Step 1 — Consumer (web)

1. Add/extend consumer contract tests that record the web app's expectations for each endpoint it calls, deriving request/response shapes from `<stack.api_spec_path>` (the test basis). Place tests under `<paths.tests_dir>` per project convention.
2. One interaction per consumer expectation: method, path, request body/headers, and the **minimal** response shape the consumer actually depends on (avoid over-specifying fields the consumer ignores).
3. Run the consumer suite and **publish** the resulting pacts to `<tooling.contract_broker_url>`, tagged with the branch and version (e.g. the commit SHA). Capture raw results under `<paths.reports_dir>`.

## Step 2 — Provider (API)

1. Add/extend provider verification that replays the recorded pacts from `<tooling.contract_broker_url>` against the API, using **provider states** to set up the data each interaction assumes.
2. Run verification against the appropriate entry in `environments`. Publish the verification result back to the broker, tagged with the provider branch/version.
3. Any failed interaction is a **contract mismatch** — log it as an Incident (Defect) Report (interaction, expected vs actual shape, consumer/provider versions) rather than silently passing.

## Step 3 — can-i-deploy gate

1. Run the `can-i-deploy` check for the target environment from `environments`, querying the broker's compatibility matrix.
2. **Decision rule:** the deploy is **allowed** only when every consumer↔provider pair required for that environment is **verified green** in the matrix; if any required pair is missing, pending, or failing, the gate is **blocked**. Wire this as a hard gate consistent with `gates` so a red matrix stops the deploy.
3. Report the matrix outcome as a clear **deploy / hold** decision with the specific failing/missing pairs named.

## Step 4 — CI wiring & mock backstop

1. Ensure the `<ci.platform>` pipeline triggers **consumer publish** on web changes and **provider verification** on API changes (webhook or pipeline stage), and runs `can-i-deploy` before any deploy stage.
2. Explain how contract testing **backstops API mocking**: any interface virtualized via `<tooling.mocking>` (in `/qa:integration-test` / `/qa:api-automate`) is held honest here, so mocks that drift from the real provider are caught.

## Output

Write the **Test Execution Log** to `<paths.docs_dir>/CONTRACT-RESULTS-<scope>.md` (`<scope>` = the mode or the integration boundary, slugified from `$ARGUMENTS`). It is the ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the contract suite. Include:

1. **Scope & mode** — consumer / provider / can-i-deploy / full, and the endpoints in scope (with `risk_areas` tier).
2. **Consumer results** — interactions recorded, pacts published, broker tag/version (counts).
3. **Provider results** — interactions verified pass/fail against which `environments` entry (counts).
4. **can-i-deploy matrix** — the compatibility outcome per consumer↔provider pair for the target environment, and the **deploy / hold** decision.
5. **Contract mismatches** — any failed interaction as an Incident (Defect) Report reference.
6. **Coverage summary (counts)** — endpoints under contract vs endpoints in `<stack.api_spec_path>` not yet covered, as numbers not prose.

Then run the Self-check below.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`tooling.contract`, `tooling.contract_broker_url`, `stack.api_spec_path`, `paths.tests_dir`, `paths.docs_dir`, `paths.reports_dir`, `environments`, `gates`, `risk_areas`) is honored; no path, tool, or broker URL is hardcoded; the contract-tooling guard ran.
- [ ] **Traceability intact** — the chain test basis (`<stack.api_spec_path>`) -> consumer expectation -> interaction -> provider verification result (-> defect for mismatches) is preserved and bidirectional; no orphan interactions.
- [ ] **Measurable** — output states counts (interactions recorded/verified, pass/fail, endpoints covered vs uncovered, matrix pairs green/red) rather than prose claims.
- [ ] **Gate explicit** — the can-i-deploy decision is a clear deploy/hold with the failing/missing pairs named; a red or incomplete matrix blocks deploy.
- [ ] **Residual risk stated** — name what is NOT covered (endpoints without contracts, untested provider states, environments not in the matrix) and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects; exhaustive testing is impossible).
- [ ] **Work product named** — output is identified as the ISO/IEC/IEEE 29119-3 **Test Execution Log / Test Results** for the contract suite and written to `<paths.docs_dir>/CONTRACT-RESULTS-<scope>.md`.

## Handoff

- `/qa:integration-test` — design the component/system integration interfaces this command backstops; reciprocate any mocked interface here.
- `/qa:api-automate` — implement/extend the underlying API-level tests and the endpoints under contract.
- `/qa:triage` — file and lifecycle any contract mismatch as a defect report.
- `/qa:release-report` — feeds the can-i-deploy status into the Test Completion Report's exit-criteria evaluation.
- `/qa:fix-ci` (or `/qa:fix-jenkins`) — for pipeline-level failures wiring the consumer-publish / provider-verify / can-i-deploy stages.
