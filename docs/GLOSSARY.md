# Glossary (ISTQB-aligned)

The toolkit uses **ISTQB Glossary** terminology consistently. These are the core terms every command, template, and document uses. Definitions are summarized in the toolkit's own words and aligned to ISTQB usage; for the authoritative wording see the [official ISTQB Glossary](https://astqb.org/resources/glossary-of-software-testing-terms/).

## Core process terms

- **Test object** — the work product being tested (the Web app / the REST API).
- **Test basis** — the source from which test cases are derived: requirements, user stories, acceptance criteria, the OpenAPI specification, designs.
- **Test condition** — a testable aspect of the test object identified during **test analysis** (a feature, function, quality attribute, or scenario). Answers *what* to test.
- **Test case** — a set of preconditions, inputs, actions, expected results, and postconditions developed during **test design** to cover one or more test conditions. Answers *how* to test.
- **Coverage item** — an attribute derived from the test basis that a test technique aims to exercise (e.g. an equivalence partition, a boundary value, a decision-table rule, a statement, a branch).
- **Test procedure** — a sequence of test cases in execution order, plus any setup/preconditions (the executable spec/script).
- **Test suite** — a set of test cases or procedures to be executed together.
- **Test script** — an automated test procedure (e.g. a Playwright spec, a K6 script).
- **Testware** — all work products produced by the test process: plans, conditions, cases, procedures, scripts, data, environment artifacts, logs, reports.

## Process activities (CTFL v4.0 §1.4)

- **Test planning** — defining objectives, scope, approach, and resources.
- **Test monitoring and control** — comparing actual progress against the plan (monitoring) and acting on deviations (control).
- **Test analysis** — analyzing the test basis to identify test conditions ("what to test").
- **Test design** — elaborating test conditions into test cases and coverage items ("how to test").
- **Test implementation** — creating/organizing testware needed for execution (procedures, scripts, data, environment).
- **Test execution** — running tests and comparing actual to expected results.
- **Test completion** — collating testware, reporting, and capturing lessons learned.

## Levels & types

- **Test level** — a group of test activities organized together: component, component integration, system, system integration, acceptance.
- **Test type** — a group of activities targeting specific characteristics: functional, non-functional, white-box (structural), change-related.
- **Functional testing** — what the system does.
- **Non-functional testing** — how well the system behaves (performance, security, usability/accessibility, reliability, compatibility — see ISO/IEC 25010).
- **White-box (structural) testing** — derived from the internal structure (statement, branch coverage).
- **Confirmation testing (re-testing)** — re-running tests that failed, after a fix, to confirm the defect is resolved.
- **Regression testing** — testing to detect that changes haven't broken previously working behavior.

## Techniques

- **Black-box techniques (CTFL v4.0 §4.2)** — Equivalence Partitioning (EP), Boundary Value Analysis (BVA; 2-value and 3-value forms), Decision Table testing, State Transition testing. *(Use-case testing is CTAL Test Analyst, not CTFL v4.0.)*
- **White-box techniques (CTFL v4.0 §4.3)** — Statement testing/coverage, Branch testing/coverage.
- **Coverage criteria (state transition)** — all states, all transitions (0-switch), invalid transitions.
- **Experience-based techniques** — Error guessing, Exploratory testing, Checklist-based testing.
- **Collaboration-based** — ATDD (Acceptance Test-Driven Development), deriving tests from user stories and acceptance criteria.

## Management & quality

- **Entry criteria** — conditions that must be met to start a test activity.
- **Exit criteria** — conditions that must be met to consider an activity complete (ISTQB; "Definition of Done" in Agile is the team's exit criteria).
- **Test strategy** — the organization-wide, generic description of the test approach (long-lived).
- **Test plan** — documentation describing the test objectives, scope, and approach for a specific project/release (disposable).
- **Product risk (quality risk)** — a risk that the product may fail to satisfy a quality need.
- **Project risk** — a risk around managing/executing the project.
- **Risk level** — likelihood × impact; drives test prioritization in risk-based testing.
- **Severity** — the degree of impact a defect has on the test object.
- **Priority** — the urgency with which a defect should be fixed (a business decision; independent of severity).
- **Defect (bug)** — a flaw in the test object that can cause it to fail.
- **Failure** — an event in which the test object does not perform a required function within limits.
- **Error (mistake)** — a human action producing an incorrect result.
- **Test completion report (test summary report)** — a report summarizing testing performed, produced at a milestone.
- **Test status (progress) report** — a periodic report on the status of test activities against the plan.

## Agile-specific

- **Testing quadrants** — a model classifying tests as technology- or business-facing and as supporting the team or critiquing the product.
- **Definition of Done (DoD)** — the agreed exit criteria for a story/increment.
- **Three Amigos** — collaboration between business, development, and testing to refine acceptance criteria.

Every command in this toolkit uses these terms exactly. If a config field or report uses a casual word (e.g. "test"), it maps to the precise term above.
