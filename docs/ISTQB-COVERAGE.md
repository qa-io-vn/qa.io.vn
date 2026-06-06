# ISTQB Coverage — Body-of-Knowledge Gap Analysis

A systematic check that **every aspect of testing in the ISTQB syllabi has a command** (or is intentionally excluded with a reason). This is the completeness proof behind the toolkit: it walks the CTFL v4.0 chapters and the Advanced/Specialist syllabi topic by topic.

Legend: ✅ command exists · 📘 covered as reference/knowledge (via `qa-context` skill + `istqb-coach`) · ⛔ intentionally excluded.

## CTFL v4.0 — Foundation Level

### Ch.1 Fundamentals of testing
| Topic | Coverage |
|---|---|
| What/why testing, objectives | 📘 `qa-context`, `istqb-coach` |
| Seven testing principles | 📘 enforced as standing rules in `qa-context` |
| Test process & activities | ✅ mapped across all commands (see ISTQB-COMPLIANCE §3) |
| Testware & work products | ✅ each command names its work products |
| Traceability | ✅ `review-coverage`, `test-cases`, `test-design` |
| Tester's mindset, whole-team, independence | 📘 `istqb-coach` (soft topic, no action command) |

### Ch.2 Testing throughout the SDLC
| Topic | Coverage |
|---|---|
| SDLC models, shift-left | 📘 `create-strategy` (agile mapping) |
| Component (unit) testing | ✅ `unit-test` |
| Component integration testing | ✅ `integration-test`, `api-automate`, `contract-sync` |
| System testing | ✅ `web-automate`, end-to-end commands |
| System integration testing | ✅ `integration-test` |
| Acceptance testing (UAT, OAT, contractual, alpha/beta) | ✅ `acceptance` |
| Functional / non-functional / white-box / change-related types | ✅ see Ch.4 + non-functional commands |
| Confirmation & regression testing | ✅ `triage`+`implement` (confirmation), `regression` |
| Maintenance testing (modification, migration, retirement) | ✅ `maintenance-test` |
| Testing & DevOps / CI/CD / shift-right | ✅ `scaffold`, `fix-ci`, `fix-jenkins`, `shift-right` |

### Ch.3 Static testing
| Topic | Coverage |
|---|---|
| Reviews of the test basis (review types, roles) | ✅ `static-review` |
| Static analysis of code (flow, complexity) | ✅ `static-analysis` |

### Ch.4 Test analysis & design
| Topic | Coverage |
|---|---|
| Black-box: EP, BVA (2-/3-value), decision table, state transition | ✅ `test-cases`, `test-design` |
| White-box: statement & branch | ✅ `unit-test`, `coverage-measure` |
| Experience-based: error guessing, exploratory, checklist | ✅ `exploratory`, `test-cases` |
| Collaboration-based: user-story writing, acceptance criteria, ATDD | ✅ `acceptance` |

### Ch.5 Managing the test activities
| Topic | Coverage |
|---|---|
| Test planning, estimation | ✅ `create-plan`, `estimate` |
| Risk-based testing | ✅ `risk-assessment` |
| Test monitoring, control, metrics | ✅ `status-report`, `coverage-measure` |
| Configuration management of testware | ✅ `test-env` |
| Defect management | ✅ `triage` |

### Ch.6 Test tools
| Topic | Coverage |
|---|---|
| Tool support, categories | ✅ `tool-select` |
| Tool selection, benefits/risks, pilot | ✅ `tool-select` |

## Advanced Level

### Test Analyst (CTAL-TA)
| Topic | Coverage |
|---|---|
| Domain analysis | ✅ `test-design` (technique) |
| Defect-based techniques | ✅ `test-design` (technique) |
| Combinatorial: pairwise, classification tree, orthogonal arrays | ✅ `combinatorial` |
| Use-case testing | ✅ `test-cases`/`test-design` (labeled Advanced) |
| Quality characteristics (functional, usability) | ✅ `usability-test`, `nonfunctional` |

### Technical Test Analyst (CTAL-TTA)
| Topic | Coverage |
|---|---|
| White-box (incl. higher coverage) | ✅ `coverage-measure`, `unit-test` |
| Static analysis (control/data flow, complexity) | ✅ `static-analysis` |
| Dynamic analysis (memory/resource leaks) | ✅ `dynamic-analysis` |
| Non-functional (performance, reliability, security, …) | ✅ `perf-test`, `nonfunctional`, `security-scan` |
| Reviews (technical) | ✅ `static-review` |

### Test Manager (CTAL-TM) / Expert
| Topic | Coverage |
|---|---|
| Test policy, strategy, planning | ✅ `test-policy`, `create-strategy`, `create-plan` |
| Risk management | ✅ `risk-assessment` |
| Estimation, monitoring, reporting | ✅ `estimate`, `status-report`, `release-report` |
| Test process improvement (TMMi/TPI) | ✅ `process-improvement` |
| People/team skills | 📘 `istqb-coach` (soft topic) |

## Specialist Level
| Syllabus | Coverage |
|---|---|
| Test Automation Engineering (CT-TAE) + Strategy | ✅ `automation-strategy`, `automate`, `api-automate`, `web-automate`, `mobile-automate`, `scaffold` |
| Performance Testing (CT-PT) | ✅ `perf-plan`, `perf-test` |
| Security Testing (CT-SEC) | ✅ `security-scan` |
| Acceptance Testing (CT-AcT) | ✅ `acceptance` |
| Usability Testing (CT-UT) | ✅ `usability-test` |
| Mobile Application Testing (CT-MAT) | ✅ `mobile-automate`, `mobile-test` |
| AI Testing (CT-AI) | ✅ `ai-test` |
| Testing with Generative AI (CT-GenAI) | ✅ `genai-assist` |
| Model-Based Testing (CT-MBT) | ✅ `mbt` |
| Quality in DevOps | ✅ `scaffold`, `fix-ci`, `shift-right` |

## Intentional exclusions (with reason)
| Area | Why excluded |
|---|---|
| Automotive (CT-AuT), Finance, Gambling, Game testing | ⛔ Domain-gated — not applicable to a general Web + API product. Extensible: add a command + config domain if needed. |
| Soft skills / tester psychology / team leadership | 📘 Knowledge, not an automatable action — handled by `istqb-coach` on demand. |
| Expert-level management process specifics | 📘 Covered at the practical level by `test-policy` + `process-improvement`; full Expert assessment is an org engagement. |

**Conclusion:** every actionable testing aspect in the ISTQB Foundation, Advanced (TA/TTA/TM), and applicable Specialist syllabi maps to a `/qa:*` command; non-actionable knowledge topics are served by `istqb-coach`; only domain-gated syllabi are excluded (and extensible). See `docs/ISTQB-COMPLIANCE.md` for the syllabus→command matrix and `docs/ISTQB-AUDIT.md` for the conformance audit.
