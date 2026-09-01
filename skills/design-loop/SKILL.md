---
name: design-loop
description: Use when a feature is large enough to need a design doc before any code gets written — Stage 3 of the app-bootstrap methodology, a persistent author and an adversarial reviewer running rounds, including the interface-consumer exercise, until a plain SHIP
argument-hint: "[topic, or path to an existing design doc]"
---

# Stage 3 — The design loop

Run the full adversarial design-review workflow for: **$ARGUMENTS**

If nothing was named above, ask the maintainer which design this loop is for before launching anything.

Use it for any design large enough to deserve a design doc — especially one that ships interface sketches. **The loop does not exit until the adversarial reviewer's verdict is a plain SHIP.** The coordinator runs the loop under the maintainer's standing delegated authority (playbook §1): it rules the design decisions itself and drives to SHIP without per-decision approval. Implementation then begins only after **Touchpoint 1** — the maintainer reviews the batch of delegated decisions and approves the shipped design (playbook §1, §6).

Shared doctrine — read it before launching anything: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** signed-off requirements (Stage 1) and locked wireframes (Stage 2).
**Exit gate:** a plain SHIP verdict, then Touchpoint 1 — the maintainer's batch decision review and approval to implement (playbook §1).

---

## Phase 0 — Distill requirements

Before any agent launches, separate two things and confirm the split with the maintainer if ambiguous:

- **Hard requirements (R1..Rn)** — what the maintainer actually mandated. Few, stated abstractly. Lift them from the Stage 1 doc; add any that the wireframe callouts made binding.
- **Negotiable baseline** — every design conclusion reached in prior discussion. The author may depart from any of it **with rationale**; departures are never silent.

Getting this split wrong in the brief is a real failure mode: framing session conclusions as hard constraints forbids the author from fixing them.

---

## Phase 1 — Author agent (background, keep open)

Launch a general-purpose author agent in the background. Keep its agent id and continue it for every revision round — never spawn a fresh author mid-loop; the context is the value.

The brief must include:

- **Deliverable**: one design doc at a stated scratchpad path (promoted into the docs tree only after SHIP + Touchpoint 1 approval). Start it from the HTML template [`assets/design-doc-template.html`](assets/design-doc-template.html) so the styled format is recreated by default.
- **The R-list as binding**; the baseline as a starting point with a required **Departures** section (baseline position / author position / rationale, per departure).
- **A ground-truth reading list** of the actual code and artifacts, with the rule: **the source wins over the brief's characterizations; discrepancies get reported.**
- **The wireframe artifact URL** — or, where artifact publishing was unavailable at Stage 2, the committed path of the single self-contained wireframe page — with the note that numbered callouts are binding. Confirm the author agent can actually open it; a brief that points at an unreachable artifact silently degrades the binding-callout mechanism to whatever the author remembers.
- **Required structure** (carried by the template [`assets/design-doc-template.html`](assets/design-doc-template.html), which also ships the decision-table styling): problem statement; first principles with wire-level examples; the design; interface sketches; per-consumer instantiation grounded with `file:line` refs; a decision table (# / Question / Options-and-costs / Ruling, with status badges); a migration/build plan with a **named verification gate per phase**; an error-copy table if anything is user-facing; telemetry; **Concerns** (honest open questions, each with a recommendation); **Departures**; a **revision log**. Write it in the first-principles register of playbook §10: assume the reader knows nothing about the subsystem, motivation before mechanism, every term defined before first use, a real-valued worked example per mechanism (state before / action / state after), every simplification flagged, a single compressed takeaway, no em dashes.
- **A filled-in completion checklist** returned with the report (self-certified PASS is necessary, not sufficient).

---

## Phase 2 — Adversarial reviewer (background, keep open)

Launch after the author reports, briefed per the playbook's adversarial briefing template: **assume the design contains defects; the job is to find them.** Same persistence rule — one reviewer, continued across all rounds, rounds stacked newest-first in a single review file next to the design doc.

Findings discipline is non-negotiable; see the playbook §3. In addition, every round produces a requirement scorecard R1..Rn and a verdict per Departure (uphold / reverse / amend).

### The interface-consumer exercise — mandatory, every round that touches interfaces

The reviewer must **write the consumers** — each feature's real usage and topology — as actual code against the doc's interface sketches, report the line counts, and report any path that cannot be expressed.

Rationale, learned the hard way: adversarial *reading* only exercises the paths the author drew. Attention goes where risk is believed to be, so failure paths get audited carefully while the happy path is "obviously fine". *Building* forces traversal of every path the program actually needs. In the loop this methodology comes from, the exercise caught a BLOCKER — a primary branch missing from an outcome type — that three full reading rounds had missed.

---

## Phase 3 — Rule the decisions and record them weight-sorted

Under delegated authority (playbook §1) the coordinator rules contested findings and reviewer-vs-author disagreements itself, inside the loop, rather than pausing to send each to the maintainer. Tag each decision **major** (contract / architecture / risk) or **mechanical**, and record all of them in the design doc's decision table with the ruling and its accepted costs (playbook §6).

The major decisions are the ones the maintainer reviews at Touchpoint 1, each presented as a **four-part walkthrough** (background for a low-context reader / concrete failure scenario / options with what each one GIVES UP / recommendation with reasoning). The walkthrough is the presentation format at the touchpoint, not a per-decision pre-approval gate. Mechanical decisions are recorded, not walked. Batch related decisions.

Spot-check load-bearing findings yourself against the source before relaying them — reviewers can be wrong, and an unverified BLOCKER wastes a maintainer decision.

---

## Phase 4 — Revision rounds

- Revisions are **in-place edits to the one design doc**, with a revision-log section extended per round. No addendum files, no v2 copies.
- The revision brief carries: rulings (binding, verbatim), every finding with its required disposition, and discretion boundaries — which fix shapes are the author's call, each requiring a one-paragraph justification.
- The reviewer's next round verifies dispositions **against the revised text, not the author's claims**, attacks the **new** surfaces the revision introduced (new content is where new defects live), and adjudicates any coordinator-made judgment calls on the merits.
- The final round is narrow by instruction: verify fixes, re-run the consumer exercise, no padding, and close with a plain verdict — **SHIP or ONE MORE ROUND**. No other verdict vocabulary exists; "SHIP with reservations" is ONE MORE ROUND.

Consider one dedicated round — after the technical rounds converge — that reviews the design against the *product*: walk the wireframes surface by surface and ask whether the design can render each one. Technical rounds systematically miss coverage gaps because they audit what is written, not what is absent.

---

## Exit

On SHIP:

1. Independently spot-check the design doc yourself before presenting it.
2. Deliver the doc plus the full review trail to the maintainer.
3. List any deferred one-line edits with the phase that will absorb them.
4. Ask — never assume — about promoting the doc into the project docs tree, indexing it from `CLAUDE.md`, and archiving the review trail.

**SHIP ends the design loop only.** The implementation loop starts only after Touchpoint 1: the maintainer reviews the batch of delegated design decisions and approves the shipped design (playbook §1).
