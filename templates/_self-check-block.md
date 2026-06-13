# Canonical Self-Check Block (reference snippet)

This file holds the single source of truth for the self-check block shared across the toolkit's commands (~28 of them).

**How to use:** Paste-and-adapt the block below into each command as its **penultimate step** — i.e., the last action before the command emits/finalizes its output. Keep the wording verbatim; only adjust surrounding phrasing if a command needs to reference its specific work product. When this canonical block changes, re-roll it into the consuming commands so they stay in sync.

---

## Self-check (run before finalizing output)

Do not finalize until every item passes:
- [ ] **Config reflected** — every relevant `qa.config.yml` field in scope (`paths.*`, `tooling.*` toggles, `gates`, `risk_areas`) is honored; nothing hardcoded.
- [ ] **Traceability intact** — the chain test basis -> condition -> case -> coverage item -> procedure -> result (-> defect) is preserved and bidirectional; no orphans.
- [ ] **Measurable** — output states counts/coverage (e.g. N conditions, M cases by priority, % coverage) rather than prose claims.
- [ ] **Residual risk stated** — name what is NOT covered and why (ISTQB Principle 1: testing shows the presence, not the absence, of defects).
- [ ] **Work product named** — output is identified as its ISO/IEC/IEEE 29119-3 work product and written to the correct `<paths.*>` location.
