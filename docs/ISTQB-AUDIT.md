# ISTQB Conformance Audit — Test Case Design

A deep check of the toolkit's test-case design (`/qa:test-cases`, `/qa:test-design`, the test-case template, and supporting docs) against the **ISTQB Certified Tester Foundation Level Syllabus v4.0/v4.0.1**, Chapter 4 (Test Analysis and Design). This records what was verified, what was found non-conformant, and how it was resolved.

**Audited:** `commands/test-cases.md`, `commands/test-design.md`, `templates/test-case-template.md`, `docs/GLOSSARY.md`, `docs/ISTQB-COMPLIANCE.md`, `templates/strategy-template.md`, `skills/qa-context/SKILL.md`.
**Reference:** CTFL v4.0.1 syllabus (Chapter 4), ISTQB Glossary, verified against official ISTQB/ASTQB sources (see [References](#references)).

## Findings & resolutions

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | **Use-case testing** was listed as a CTFL black-box technique. It was **removed from Foundation in v4.0** (now a CTAL Test Analyst topic). | High (mis-attribution) | **Fixed** — removed from the v4.0 black-box set everywhere; retained only as an explicitly-labeled *Advanced (CTAL-TA)* option. |
| 2 | **Pairwise / classification tree** was presented alongside Foundation techniques. It is **not in CTFL v4.0** (Advanced/CTAL-TA). | High (mis-attribution) | **Fixed** — relabeled as Advanced (CTAL-TA), used only when justified. |
| 3 | **Boundary Value Analysis** was described generically (min−1/min/max/max+1) without the v4.0 distinction. | Medium (imprecise) | **Fixed** — now specifies **2-value** and **3-value** BVA forms explicitly, and requires stating which is used. |
| 4 | **White-box** wording risked the old v3.1 "decision testing" term. | Low | **Verified/clarified** — v4.0 uses **Statement** and **Branch** testing/coverage; docs now say so explicitly. |
| 5 | **State Transition** lacked explicit coverage criteria. | Low | **Fixed** — now references all-states / all-transitions (0-switch) / invalid transitions. |

## Verified conformant (no change needed)

- **Process flow** — analysis (derive **test conditions** from the **test basis**) precedes design (derive **test cases** + **coverage items**). Matches CTFL §1.4.3–1.4.4.
- **Technique categories** — the four v4.0 groups are correct: black-box (§4.2), white-box (§4.3), experience-based (§4.4: error guessing, exploratory, checklist-based), collaboration-based (§4.5: collaborative user-story writing, writing acceptance criteria, ATDD).
- **Black-box set (§4.2)** — exactly Equivalence Partitioning, Boundary Value Analysis, Decision Table, State Transition.
- **Test case fields** — preconditions, inputs/test data, expected results, postconditions — consistent with the ISTQB definition of a test case.
- **High-level (logical) vs low-level (concrete) test cases** — correct ISTQB Glossary terms; risk-based mixing is a legitimate tailoring.
- **Equivalence Partitioning** — requires valid **and** invalid partitions, one representative each: conformant.
- **Decision Table** — coverage by rule/column: conformant.
- **Traceability** — bidirectional test basis → condition → case → coverage item (CTFL §1.4.4, §5.4): conformant.
- **Terminology** — ISTQB Glossary terms used throughout (test object, test basis, test condition, test case, coverage item, test procedure).

## Residual considerations

- ISTQB syllabi are **copyrighted**; this toolkit implements concepts and terminology, it does not reproduce syllabus text. Verify wording against your exam version if certifying.
- The current Foundation syllabus is **v4.0.1**. If ISTQB issues a later revision, re-run this audit (`/qa:istqb-coach` can check specific concepts against official sources).
- Foundation techniques are the floor. For deeper test design (pairwise, classification trees, use-case testing, defect-based, domain analysis), the **Advanced Test Analyst (CTAL-TA)** techniques are available in the design commands, labeled as Advanced.

## References

- [ISTQB CTFL v4.0.1 syllabus](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)
- [ASTQB — 4.2 Black-Box Test Techniques](https://astqb.org/4-2-black-box-test-techniques/)
- [ISTQB CTFL v4.0 overview](https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/)

*Audit performed for toolkit v3.1.1. Re-audit on any syllabus revision or technique-related change.*
