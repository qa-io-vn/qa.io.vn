---
description: Plan maintenance testing for changes to a deployed system — modifications, migration, or retirement — with impact analysis. Use when testing patches, upgrades, data migrations, or decommissioning.
argument-hint: "<change / migration / retirement scope>"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Maintenance testing: $ARGUMENTS

**ISTQB process:** Maintenance testing (CTFL v4.0 §2.4) + impact analysis.

## Project config
```!
cat qa.config.yml 2>/dev/null || echo "none"
```

## Recent changes
```!
git diff --name-only HEAD~10 2>/dev/null | head -30 || echo "no git history"
```

## Your task

Identify the **maintenance trigger** from `$ARGUMENTS` and test accordingly (ISTQB §2.4):

1. **Modification** — planned enhancements, patches, hotfixes, emergency fixes, or environment/OS/platform upgrades.
2. **Migration** — moving to another platform, or **data migration/conversion**: test the migration process itself **and** verify migrated data integrity and the system on the new platform.
3. **Retirement** — decommissioning: test data archiving/migration, restore/retrieval procedures, and any remaining processes.

Approach:
- **Impact analysis** — determine what the change affects directly and indirectly (use `/qa:regression` for selection). Identify side effects and the regression scope; flag areas where impact analysis is hard (poor traceability) as a risk.
- **Test the change** itself (confirmation testing of fixes/new behavior) **and** run **regression testing** on the impacted + high-risk areas so nothing previously working broke.
- For migrations, add data-validation tests (counts, integrity, transformation correctness) and rollback verification.
- Define entry/exit criteria for the maintenance release and residual risk.

Output a maintenance test plan to `<paths.docs_dir>/MAINTENANCE-<scope>.md`, and implement/run the confirmation + regression tests. Tie results into `/qa:release-report`.
