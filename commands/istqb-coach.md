---
description: Explain or apply any ISTQB concept, technique, term, or process on demand — a built-in ISTQB reference and coach. Use to learn a technique, check a definition, or get guidance on how to test something the ISTQB way.
argument-hint: "<ISTQB concept, technique, term, or question>"
allowed-tools: Read, Glob, Grep, Bash, WebSearch
---

# ISTQB coach: $ARGUMENTS

**Purpose:** on-demand ISTQB reference so a tester can do anything the standard covers, in context of this project.

## Project context
```!
cat qa.config.yml 2>/dev/null | head -40 || echo "none"
```

## Your task

Question/topic from `$ARGUMENTS`. If empty, ask what they want to learn or do.

1. **Explain** the ISTQB concept/technique/term accurately and concisely, using ISTQB Glossary terminology (cross-reference `docs/GLOSSARY.md`). Cite the syllabus area (e.g. CTFL §4.2 Boundary Value Analysis; CTAL-TM risk-based testing).
2. **Apply it to this project** — show a concrete worked example using the actual stack, OpenAPI endpoints, or features (not a generic textbook example).
3. **Point to the command** that operationalizes it (e.g. "to do this across the suite, run `/qa:test-design`"). Map the concept into the workflow.
4. If the topic is newer than the toolkit or you're unsure, **search the official sources** (istqb.org, the Glossary) to confirm — never invent syllabus content. Respect copyright: explain concepts, don't reproduce syllabus text verbatim.

Keep it practical and short. This command teaches and routes; the other `/qa:*` commands do the work. See `docs/ISTQB-COMPLIANCE.md` for the full concept→command map.
