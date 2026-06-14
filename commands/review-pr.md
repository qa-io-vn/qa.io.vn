---
description: Review a pull request from a QA/testing perspective — change impact & risk, test coverage of the diff, regression scope, test-code quality, and real defects — then give a gate-based merge recommendation and write a Review Report. Reads the PR via the gh CLI or a local diff vs the base branch. Use to QA-review a PR before merge (not a general code review).
argument-hint: "[PR number | PR URL | branch] (optional — defaults to the current branch's PR / diff)"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# QA review of a pull request — coverage, risk, regression, merge call

**ISTQB process:** Static testing — **review** of a change set (CTFL v4.0 §3) + change-related **impact analysis** (§2.3) + **risk-based** test selection (§5.2 — verify section numbers against the current syllabus). **Work product:** ISO/IEC/IEEE 29119-3 **Review Report** (review findings). This is a **test-focused** review — coverage of the change, regression risk, testware quality, and real defects — *not* a general code-style review. Real product defects are filed via `/qa:triage`, never silently fixed (Principle 1: testing shows the presence of defects, not their absence).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Pull request / change set (discovery)
```!
ARG="$ARGUMENTS"
echo "--- current branch: $(git symbolic-ref --short HEAD 2>/dev/null || echo unknown) ---"
BASEREF=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')
BASEREF="${BASEREF:-main}"
if command -v gh >/dev/null 2>&1; then
  if echo "$ARG" | grep -qE '^[0-9]+$|^https?://'; then
    echo "--- PR $ARG (gh) ---"; gh pr view "$ARG" --json number,title,headRefName,baseRefName,state,additions,deletions,changedFiles,url 2>/dev/null || echo "gh pr view failed"
    echo "--- changed files ---"; gh pr diff "$ARG" --name-only 2>/dev/null | head -60
  else
    echo "--- PR for current branch (gh) ---"; gh pr view --json number,title,headRefName,baseRefName,state,additions,deletions,changedFiles,url 2>/dev/null || echo "no open PR for this branch — will use local diff"
  fi
else
  echo "gh CLI not found — using a local git diff vs the base branch ($BASEREF)"
fi
echo "--- diff stat vs base ($BASEREF) ---"
MB=$(git merge-base HEAD "origin/$BASEREF" 2>/dev/null || git merge-base HEAD "$BASEREF" 2>/dev/null || echo "HEAD~1")
git diff --stat "$MB"...HEAD 2>/dev/null | tail -50
```

## Your task

> **Config-read guard.** Read `qa.config.yml` first. If it is `none`/missing, tell the user to run `/qa:qa-init`, or proceed with explicit, stated assumptions for `<tooling.*>` (runner/coverage), `<paths.*>`, `gates`, and `risk_areas.*`. Resolve every `<tooling.*>` / `<paths.*>` / `<stack.*>` / `gates` / `risk_areas.*` reference from this config — **never hardcode** a tool, path, branch, or threshold. The PR/diff above is a **discovery** step.

Goal: assess whether this change is safe and well-tested, and recommend a merge decision — **read-only on product code** (you diagnose and report; you do not edit the change).

1. **Resolve the change set.** By this precedence (stop at the first that yields a diff): a PR number/URL in `$ARGUMENTS` (via `gh`); the current branch's open PR (via `gh`); a local diff vs the base branch; else ask the user for the PR or branch. State the change set: changed files, +/− lines, and the product vs test split.

2. **Map the change to risk.** Which `risk_areas` tiers do the changed areas touch? A diff in `risk_areas.critical` (auth, payments, etc.) gets the deepest review; low-risk diffs get a lighter pass (risk-based testing, Principle 4 — defects cluster).

3. **Coverage of the change.** For the changed *product* files, are they exercised by tests? Resolve the runner/coverage from `<tooling.*>`. Identify changed code with **no covering test** and quantify it (e.g. "4 of 7 changed source files have no covering test"). Route gaps to `/qa:add-test` or `/qa:test-cases` — don't write the tests here.

4. **Regression impact.** What existing behavior could this change break? Name the impacted areas and hand the selection to `/qa:regression "<change>"`; if the suite hasn't been run against the change, say so.

5. **Testware quality.** If the PR adds/edits tests under `<paths.tests_dir>`, review them against the project's conventions: stable selectors, deterministic waits (no blind sleeps), test isolation/own-data, assertions **strengthened or left correct — never weakened to pass**, and no anti-patterns. Hand deep architectural issues to `/qa:automation-audit`.

6. **Defects.** For real product defects in the change (logic, contract, security, data), **change no code** — file each via `/qa:triage`, which writes an ISO/IEC/IEEE 29119-3 **Incident (Defect) Report** using the field schema in `${CLAUDE_PLUGIN_ROOT}/templates/defect-report-template.md` (severity and priority set independently). A defect found in review is the cheapest defect to fix (Principle 3 — early testing).

7. **Merge recommendation.** Evaluate the configured `gates` against the signals you have — `min_pass_rate_pct`, `block_on_severity`, coverage, and `security_block_on` / `a11y_block_on` / performance SLAs where signals exist — and give exactly one verdict, naming the gate that drives it:
   - **Approve** — gates pass, change well-tested.
   - **Approve with conditions** — mergeable but with stated follow-ups/residual risk.
   - **Request changes** — fixable test/coverage/testware issues block it.
   - **Block** — a `gates` blocker trips (e.g. an S1/S2 defect, coverage below threshold).

## Output — Review Report (ISO/IEC/IEEE 29119-3)

Write the review as a **Review Report** (review findings) to `<paths.reports_dir>/PR-REVIEW-<id>-<date>.md` (where `<id>` is the PR number or branch). Include:
- **PR / change identity** — number/branch, base, author if known, files & +/− counts.
- **Risk mapping** — changed areas → `risk_areas` tiers; the review depth chosen.
- **Coverage assessment** — covered vs uncovered changed files (counts), coverage delta if available.
- **Regression scope** — impacted areas and the handoff to `/qa:regression`.
- **Testware findings** — issues in added/edited tests (or "no test changes").
- **Defects filed** — the `DEF-…` IDs raised via `/qa:triage` (or "none").
- **Gate evaluation** — each `gates` item PASS/FAIL/N-A with evidence.
- **Merge recommendation** — the verdict + conditions.
- **Residual risk** — what this review did not/could not cover.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `<tooling.*>`, `<paths.*>`, `gates`, and `risk_areas.*` are read from `qa.config.yml`; no tool, path, branch, or threshold is hardcoded.
- [ ] **Review-only** — no product code in the PR was modified; real defects are filed via `/qa:triage` as Incident (Defect) Reports with severity and priority set independently, never silently fixed (Principle 1).
- [ ] **Measurable** — coverage and findings are stated as counts (covered/uncovered changed files, defects by severity), not prose claims.
- [ ] **Traceability intact** — each finding/defect traces to the changed file/behavior and (for a missing test) the uncovered condition; regression handed to `/qa:regression`, coverage gaps to `/qa:add-test`/`/qa:test-cases`.
- [ ] **Decision traceable** — the merge verdict names the `gates` item(s) that drive it; residual risk is stated (Principle 1).
- [ ] **Work product named** — output is identified as a **Review Report** (ISO/IEC/IEEE 29119-3) written to `<paths.reports_dir>/PR-REVIEW-<id>-<date>.md`. For the merge gate as a standalone decision record, see `/qa:merge-gate`; for release-scope sign-off, `/qa:go-no-go`.
