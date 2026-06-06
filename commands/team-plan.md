---
description: Plan QA team capacity and skills — staffing vs upcoming backlog, a skills matrix, gaps, and a training/onboarding plan. Use for resourcing decisions and team development.
argument-hint: "[release / quarter]"
allowed-tools: Read, Glob, Grep, Bash
---

# QA team capacity & skills plan${ARGUMENTS:+ — $ARGUMENTS}

**ISTQB process:** Test team management — skills, staffing, development (CTAL-TM People Skills / Team Composition).

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Your task

Horizon from `$ARGUMENTS` (release/quarter). Help the QA manager plan the team. Use the `team` section of config and ask for any missing roster/skills detail rather than assuming.

1. **Skills matrix** — map team members against the competencies this project needs: domain knowledge, test design techniques, automation (Playwright/TS), API testing, performance (K6), security, accessibility, CI/CD, exploratory, and relevant ISTQB certifications. Rate current level and mark gaps.
2. **Capacity vs demand** — estimate available QA capacity for the horizon (people × availability) against the planned backlog/releases and their `risk_areas` depth (pull effort from `/qa:estimate`). Flag over/under-capacity and bottlenecks (e.g. single point of knowledge).
3. **Gaps & risks** — critical skill gaps, key-person risk, coverage of specialist areas (security/perf/a11y). Recommend cross-training, hiring, or external support.
4. **Training & onboarding plan** — targeted development per person (courses, ISTQB certs, pairing), and an onboarding checklist for new testers (project QA setup, config, conventions, first tasks).
5. **Test independence** — note the appropriate level of tester independence for the work and any organizational considerations.

Output a team plan to `<paths.docs_dir>/TEAM-PLAN-<horizon>.md`: skills matrix, capacity summary, gaps, and the training/onboarding actions with owners and dates. Read-only on the repo. Do not record sensitive personal data beyond role/skills relevant to planning.
