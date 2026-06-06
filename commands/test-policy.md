---
description: Create or refresh the Organizational Test Policy — the highest-level statement of testing objectives, value, and principles for the organization. Use to define why and how the org tests, above any single project.
argument-hint: "(no args)"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Organizational Test Policy

**ISTQB process:** Test management — Test Policy (CTAL-TM; ISO/IEC/IEEE 29119-3 sits below it via the Org Test Strategy).

## Project / org config
```!
cat qa.config.yml 2>/dev/null || echo "none — suggest /qa:qa-init"
```

## Your task

The Test Policy is the top of the documentation hierarchy: **Policy → Organizational Test Strategy → Test Plan**. Keep it short, durable, and org-wide (not project-specific).

Produce a Test Policy covering:
1. **Purpose & objectives of testing** in the organization (what testing is for here).
2. **The value of testing** — how testing contributes to business goals; expected ROI/quality outcomes.
3. **Guiding principles** — adherence to the seven ISTQB principles; whole-team quality; shift-left/right; risk-based.
4. **Test process definition** — the standard ISTQB test process the org uses and how it's tailored.
5. **Evaluation of testing** — how test effectiveness/efficiency is measured (link to metrics).
6. **Test process improvement** — commitment to continuous improvement (link to `/qa:process-improvement`).
7. **Ethics & independence** — tester independence levels and professional conduct.

Write to `<paths.docs_dir>/TEST-POLICY.md`. Keep it to ~1–2 pages. It should rarely change. Point to `/qa:create-strategy` for the layer below.
