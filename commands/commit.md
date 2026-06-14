---
description: Create a QA-gated commit — verify the staged change first (lint / affected tests / static review as confirmation testing), then write a Conventional Commits message that traces to the requirement, story, or defect. Refuses to commit an unverified or failing change, and never pushes. Use to commit test/feature work safely with traceability.
argument-hint: "[message hint or scope] (optional)"
allowed-tools: Read, Glob, Grep, Bash
---

# QA-gated commit — verify, then commit with traceability

**ISTQB process:** **Confirmation testing** before integrating a change + **traceability** (CTFL v4.0 §1.4 implementation/execution; confirmation testing per the ISTQB Glossary; §1.4.4 traceability — verify section numbers against the current syllabus). A change is committed **only after** the relevant checks confirm it, and the message links the change back to its test basis (requirement / story / defect) so the chain stays intact. A real defect surfaced by the check is escalated via `/qa:triage`, never hidden by weakening a test (Principle 1: testing shows the presence of defects, not their absence).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Working tree (discovery)
```!
echo "--- branch ---"; git symbolic-ref --short HEAD 2>/dev/null || echo "detached"
echo "--- status ---"; git status -s 2>/dev/null | head -40
echo "--- staged diff stat ---"; git diff --staged --stat 2>/dev/null | tail -40
echo "--- recent messages (for convention) ---"; git log --oneline -8 2>/dev/null
```

## Your task

> **Config-read guard.** Read `qa.config.yml` first. If it is `none`/missing, ask the user for `<tooling.*>` (the runner) and `<stack.*>`, or proceed with explicit, stated assumptions. Resolve the verification tool/command from `<tooling.*>` for the changed `<stack.*>` — **never hardcode** a test command or path.

Goal: commit the staged change **only if it is verified**, with a message that traces to its origin.

1. **Determine scope.** Read the staged changes (`git diff --staged`). If nothing is staged, show `git status` and ask the user what to stage (or stage exactly what they name) — never blanket-stage unrelated files. Classify the change into a Conventional Commits **type** (`feat` · `fix` · `test` · `refactor` · `docs` · `chore` · `perf` · `ci` · `build`) and a **scope** (the affected component/area).

2. **Confirmation gate (the QA part).** Run the relevant fast checks resolved from `<tooling.*>` for the changed `<stack.*>` — the **affected** unit/component/E2E tests, the linter/formatter, and/or a quick `/qa:static-review` of the change — with reruns disabled, targeting only what the change touches (not the whole suite). The commit proceeds **only if these pass**. If a check fails:
   - Test/lint/format issue you can fix in-scope → fix it, re-run, then continue.
   - A **real product defect** → stop, route it to `/qa:triage`, and do **not** commit (and never weaken/skip a test or assertion to force a green check). A masked defect is worse than an uncommitted change.

3. **Craft the message — Conventional Commits.** `type(scope): imperative subject` (≤ ~72 chars), then a body explaining *what* and *why*, then trailers that preserve traceability: `Refs:` the requirement/story (`REQ-…` / `US-…`), `Fixes:` the defect (`DEF-…`) where applicable, and a short note of **what was verified** (e.g. `Verified: 12 affected unit tests + lint, green`). Match any commit convention detected in `git log`.

4. **Commit.** `git commit` the staged change with that message. **Never `git push`, never amend or rewrite already-published history, never force.** Report the resulting commit hash, the message, and the checks that gated it.

## Output

State, concisely:
- **Verified:** the checks run and their result (counts — e.g. "9/9 affected tests + lint passed"), or why the commit was blocked.
- **Committed:** the commit hash + the Conventional Commits subject (or "not committed — <reason>").
- **Routing:** any `/qa:triage` raised for a real defect; reminder that nothing was pushed.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Verified before commit** — the change was confirmed by checks resolved from `<tooling.*>` (named, with pass counts) before committing; an unverified or failing change was **not** committed.
- [ ] **No defect masked** — no test, assertion, or check was weakened/skipped to go green; any real product defect was routed to `/qa:triage` (Principle 1).
- [ ] **Message traces** — the message is Conventional Commits and links the change to its test basis/defect (`Refs:` / `Fixes:`); it follows any detected repo convention.
- [ ] **Safe by default** — only the intended files were staged; nothing was pushed, force-pushed, or amended onto published history.
- [ ] **Measurable** — the report states the verification result as counts, not prose claims. For raising the PR afterwards, see `/qa:open-pr`; for the pre-merge gate, `/qa:merge-gate`.
