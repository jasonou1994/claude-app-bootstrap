---
name: e2e-review
description: Use when every implementation phase has shipped and the running app needs end-to-end journey testing in a real browser — Stage 5 of the app-bootstrap methodology, currently an unvalidated STUB
argument-hint: "[journey name, or 'all']"
---

# Stage 5 — End-to-end review

> **⚠️ THIS SKILL IS A STUB.**
>
> It records the intended shape of the stage and nothing more. It has not been run end to end, so none of the procedure below has been proven against a real app. **Do not treat it as validated methodology.** It is to be fleshed out — and corrected — after the first full e2e cycle runs on a real project, at which point this banner comes off and the lessons go in.
>
> Until then: use it as a checklist to think with, expect to improvise, and write down what actually happened so the next version of this file is real.

Shared doctrine: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** every implementation phase has SHIPped and the app runs locally.
**Exit gate (intended):** every journey defined from the wireframes passes against the running app, and the adversarial reviewer's verdict on the journey results is a plain SHIP.

---

## Intended shape

### 1. Derive journeys from the wireframes

The Stage 2 artifact is the journey source (its URL, or its committed path where Stage 2 fell back to a self-contained page). A journey is a path a real user takes across surfaces, not a single-screen check. Derive them systematically rather than by intuition:

- one journey per primary user goal, start to finish;
- one journey per empty state — the day-one experience is the one nobody tests and everybody sees first;
- one journey per error/recovery path drawn in the wireframes;
- one journey per global control that changes what other surfaces show, asserting the effect on each affected surface *and* the non-effect on each exempt one.

Each journey names its **binding callouts** by number. The callout text is the assertion; the journey is how you reach it.

### 2. Drive the running app in a real browser

Use Claude in Chrome (or the equivalent browser automation available in the environment) against the locally running app — a real browser, real rendering, real network. Automated component tests already passed; this stage exists to catch what they structurally cannot.

Per journey, capture: the steps taken, a screenshot at each assertion point, the console output, and the network activity. Evidence is the deliverable; a journey that "passed" without artifacts did not run.

### 3. Review the results adversarially

The journey run is authored work and gets reviewed like any other: a fresh adversarial reviewer, briefed that the journeys contain defects — including defects *in the journeys themselves*. The highest-value sweep here is the same as everywhere else in this methodology: **find a journey that would pass even if the behavior it claims to check were broken.** A screenshot taken before the state settled, an assertion on text that appears on every page, a journey that never reached the surface it names.

Gate-honesty rules 1, 3 and 5 from [`../implementation-loop/SKILL.md`](../implementation-loop/SKILL.md) apply unchanged — read them there rather than working from this summary: an injected-failure journey must prove the failure landed; a journey is believed only once the defect it claims to catch has been introduced and observed to fail it; the reviewer hunts rather than validates.

---

## Open questions to resolve on the first real cycle

- How journeys are stored and re-run — a checked-in spec, or regenerated from the wireframe artifact each time?
- What is asserted automatically versus judged visually, and who judges.
- How flakiness is distinguished from a real defect without eroding the "believe no gate you have not watched fail" rule.
- Whether this stage runs once at the end, or once per implementation phase against the surfaces that phase touched.
- What the maintainer sign-off at this stage actually certifies.

Record the answers here after the first cycle.
