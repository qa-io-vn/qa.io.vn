---
description: Open a pull request with a QA summary — what changed, what was tested, coverage delta, the regression set run, residual risk, and linked defects/tickets — a change-level test summary reviewers can trust. Generates the PR body and opens it via the gh CLI on confirmation. Use to raise a PR with the QA evidence attached.
argument-hint: "[base branch | PR title] (optional)"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Open a PR with a QA summary — the evidence reviewers need

**ISTQB process:** Test reporting at change scope — a change-level **completion-style summary** (CTFL v4.0 §1.4 test completion; §5.3 test reporting — verify section numbers against the current syllabus). **Work product:** a PR description structured as a mini ISO/IEC/IEEE 29119-3 **Test Completion**-style summary; use `${CLAUDE_PLUGIN_ROOT}/templates/completion-report-template.md` as the field guide, scoped to this change. It states residual risk rather than implying none (Principle 1: testing shows the presence, not the absence, of defects).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Branch / change set (discovery)
```!
ARG="$ARGUMENTS"
HEAD=$(git symbolic-ref --short HEAD 2>/dev/null || echo unknown)
BASEREF=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##'); BASEREF="${BASEREF:-main}"
echo "--- head: $HEAD · base (default): $BASEREF ---"
MB=$(git merge-base HEAD "origin/$BASEREF" 2>/dev/null || git merge-base HEAD "$BASEREF" 2>/dev/null || echo "HEAD~1")
echo "--- commits on this branch ---"; git log --oneline "$MB"..HEAD 2>/dev/null | head -30
echo "--- diff stat vs base ---"; git diff --stat "$MB"...HEAD 2>/dev/null | tail -50
command -v gh >/dev/null 2>&1 && (echo "--- existing PR? ---"; gh pr view --json number,url,state 2>/dev/null || echo "no PR yet for $HEAD") || echo "gh CLI not found — will output the body for manual PR creation"
```

## Your task

> **Config-read guard.** Read `qa.config.yml` first. If it is `none`/missing, tell the user to run `/qa:qa-init`, or proceed with explicit, stated assumptions for `<tooling.*>`, `<paths.*>`, `risk_areas.*`, and `gates`. Resolve every `<tooling.*>` / `<paths.*>` / `risk_areas.*` reference from this config — **never hardcode** a tool, path, or base branch.

Goal: raise a PR whose description is real QA evidence — what changed, what was tested, and what risk remains.

1. **Resolve base + head.** Use the base from `$ARGUMENTS` if given, else the repo default branch; head is the current branch. Confirm the branch is pushed (push it **only on the user's confirmation** — never force-push).

2. **Summarize the change.** From the branch commits/diff: *what* changed and *why*, and the areas touched mapped to `risk_areas` tiers.

3. **State what was tested.** Which test levels/suites were run (resolved from `<tooling.*>`), the coverage delta if available, the **regression set** run (handing selection to `/qa:regression` if not yet scoped), and any performance/security/accessibility checks relevant to the change. Be honest where something was not tested.

4. **Residual risk + links.** State residual risk (areas thin on coverage, deferred follow-ups), and link defects/tickets (`DEF-…` from `/qa:triage`, issue refs).

5. **Assemble the PR body.** Build it from `${CLAUDE_PLUGIN_ROOT}/templates/completion-report-template.md`, scoped to the change (Summary · What changed · What was tested + counts · Regression scope · Residual risk · Linked defects/tickets). Write it to `<paths.reports_dir>/PR-<head>-<date>.md` so there is a saved artifact, and use the same content as the PR description.

6. **Open the PR.** With `gh`: `gh pr create --base <base> --head <head> --title "<title>" --body-file <the saved file>` — **only after confirming** the base/title with the user. If `gh` is unavailable, output the title + body for the user to create the PR manually. Never open against the wrong base; never force-push.

## Output — change-level QA summary (ISO/IEC/IEEE 29119-3 Test Completion-style)

The PR body (also saved to `<paths.reports_dir>/PR-<head>-<date>.md`) contains: Summary, What changed (areas → `risk_areas`), What was tested (levels/suites + coverage counts), Regression scope, Residual risk, Linked defects/tickets. Report the PR URL (or the body for manual creation) and the saved artifact path.

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — `<tooling.*>`, `<paths.*>`, `risk_areas.*`, and `gates` are read from `qa.config.yml`; no tool, path, or base branch is hardcoded.
- [ ] **Evidence is measurable** — "what was tested" is stated as counts/coverage (levels run, % delta), not prose claims; untested areas are named honestly.
- [ ] **Residual risk stated** — the summary names what is not covered (Principle 1), not "fully tested".
- [ ] **Traceability intact** — the change maps to `risk_areas`; defects link to `/qa:triage` IDs; regression selection traces to `/qa:regression`.
- [ ] **Safe by default** — the branch was pushed and the PR opened **only on confirmation**; nothing was force-pushed; the base branch is correct.
- [ ] **Work product named** — output is a change-level **Test Completion-style summary** (ISO/IEC/IEEE 29119-3) written to `<paths.reports_dir>/PR-<head>-<date>.md` and used as the PR body. For the pre-merge gate decision, see `/qa:merge-gate`.
