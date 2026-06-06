---
description: Scaffold or run accessibility (axe) checks against the WCAG target in qa.config.yml. Use for accessibility audits or to add a11y tests.
argument-hint: "[page name or URL]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Accessibility audit${ARGUMENTS:+ — $ARGUMENTS}

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

If `tooling.accessibility` is not `axe`, say it's disabled and offer to enable it. Target page comes from `$ARGUMENTS` (default: the critical risk-area pages).

1. Ensure `@axe-core/playwright` is wired via a reusable helper under `tests/a11y/`.
2. Add/extend scans for the target page(s) in key states (logged out, logged in, forms, modals, error states), asserting against `gates.accessibility_standard` (e.g. WCAG 2.1 AA).
3. Fail on the severities in `gates.a11y_block_on` (e.g. critical/serious); report moderate/minor as a burndown.
4. If an environment is available, run the scan and summarize violations by severity with the specific rule, element, and fix.
5. Remind the user of the manual checks axe can't cover: keyboard-only navigation, visible focus order, screen-reader spot checks, contrast, and 200% zoom reflow.

Output a prioritized list of violations with concrete remediations.
