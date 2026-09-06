---
name: design-loop
description: Use when a feature is large enough to need a design doc before any code gets written — Stage 3 of the app-bootstrap methodology, an author and a chain of fresh adversarial passes that fix the design in place, including the interface-consumer exercise, until a pass changes nothing
argument-hint: "[topic, or path to an existing design doc]"
---

# Stage 3 — The design loop

Run the full adversarial design-review workflow for: **$ARGUMENTS**

If nothing was named above, ask the maintainer which design this loop is for before launching anything.

Use it for any design large enough to deserve a design doc — especially one that ships interface sketches. **The loop does not exit until a fresh adversarial pass changes nothing beyond line level and shows its receipts (playbook §12).** The coordinator runs the loop under the maintainer's standing delegated authority (playbook §1): it rules the design decisions itself and drives the chain to its close without per-decision approval. Implementation then begins only after **Touchpoint 1** — the maintainer reviews the batch of delegated decisions and approves the shipped design (playbook §1, §6).

Shared doctrine — read it before launching anything: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** signed-off requirements (Stage 1) and locked wireframes (Stage 2).
**Exit gate:** a closing pass ("CODE CHANGED beyond line-level: no"), then Touchpoint 1 — the maintainer's batch decision review and approval to implement (playbook §1).

---

## Phase 0 — Distill requirements

Before any agent launches, separate two things and confirm the split with the maintainer if ambiguous:

- **Hard requirements (R1..Rn)** — what the maintainer actually mandated. Few, stated abstractly. Lift them from the Stage 1 doc; add any that the wireframe callouts made binding.
- **Negotiable baseline** — every design conclusion reached in prior discussion. The author may depart from any of it **with rationale**; departures are never silent.

Getting this split wrong in the brief is a real failure mode: framing session conclusions as hard constraints forbids the author from fixing them.

---

## Phase 1 — Author agent (background, continued within the phase)

Launch a general-purpose author agent in the background. Keep its agent id for the author's own phase (retire it at the playbook §5 bound with a RESUME STATE); the passes that follow are fresh agents and read the committed doc and trail, never the author's context.

The brief must include:

- **Deliverable**: one design doc at a stated scratchpad path (promoted into the docs tree only after SHIP + Touchpoint 1 approval). Start it from the HTML template [`assets/design-doc-template.html`](assets/design-doc-template.html) so the styled format is recreated by default.
- **The R-list as binding**; the baseline as a starting point with a required **Departures** section (baseline position / author position / rationale, per departure).
- **A ground-truth reading list** of the actual code and artifacts, with the rule: **the source wins over the brief's characterizations; discrepancies get reported.**
- **The wireframe artifact URL** — or, where artifact publishing was unavailable at Stage 2, the committed path of the single self-contained wireframe page — with the note that numbered callouts are binding. Confirm the author agent can actually open it; a brief that points at an unreachable artifact silently degrades the binding-callout mechanism to whatever the author remembers.
- **Required structure** (carried by the template [`assets/design-doc-template.html`](assets/design-doc-template.html), which also ships the decision-table styling): problem statement; first principles with wire-level examples; the design; interface sketches; per-consumer instantiation grounded with `file:line` refs; a decision table (# / Question / Options-and-costs / Ruling, with status badges); a migration/build plan with a **named verification gate per phase**; an error-copy table if anything is user-facing; telemetry; **Concerns** (honest open questions, each with a recommendation); **Departures**; a **revision log**. Write it in the first-principles register of playbook §10: assume the reader knows nothing about the subsystem, motivation before mechanism, every term defined before first use, a real-valued worked example per mechanism (state before / action / state after), every simplification flagged, a single compressed takeaway, no em dashes.
- **A filled-in completion checklist** returned with the report (self-certified PASS is necessary, not sufficient).

---

## Phase 2 — Adversarial pass (background, fresh)

Launch after the author reports, briefed per the playbook's adversarial briefing template and §12: **assume the design contains defects; find them, and fix them in place.** The pass opens every cited `file:line`, re-derives every number, runs the consumer exercise below, edits the design directly (minimal edits, a revision-log row per edit), writes its entry newest-first in the review file next to the design doc, and ends with the verdict line of the playbook §2. A ruling it needs is written "needs a number" and the coordinator numbers it before the next brief.

Findings discipline is non-negotiable; see the playbook §3. In addition, every pass produces a requirement scorecard R1..Rn and a verdict per Departure (uphold / reverse / amend).

### The interface-consumer exercise — mandatory, every pass that touches interfaces

The pass must **write the consumers** — each feature's real usage and topology — as actual code against the doc's interface sketches, keep them compiling (paste the exit code), and report any path that cannot be expressed.

Rationale, learned the hard way: adversarial *reading* only exercises the paths the author drew. Attention goes where risk is believed to be, so failure paths get audited carefully while the happy path is "obviously fine". *Building* forces traversal of every path the program actually needs. In the loop this methodology comes from, the exercise caught a BLOCKER — a primary branch missing from an outcome type — that three full reading rounds had missed.

---

## Phase 3 — Rule the decisions and record them weight-sorted

Under delegated authority (playbook §1) the coordinator rules contested findings and reviewer-vs-author disagreements itself, inside the loop, rather than pausing to send each to the maintainer. Tag each decision **major** (contract / architecture / risk) or **mechanical**, and record all of them in the design doc's decision table with the ruling and its accepted costs (playbook §6).

The major decisions are the ones the maintainer reviews at Touchpoint 1, each presented as a **four-part walkthrough** (background for a low-context reader / concrete failure scenario / options with what each one GIVES UP / recommendation with reasoning). The walkthrough is the presentation format at the touchpoint, not a per-decision pre-approval gate. Mechanical decisions are recorded, not walked. Batch related decisions.

Spot-check load-bearing findings yourself against the source before recording them — passes can be wrong, and an unverified BLOCKER wastes a maintainer decision.

---

## Phase 4 — Further passes

- Every edit is an **in-place edit to the one design doc**, with a revision-log row per edit. No addendum files, no v2 copies.
- A second pass runs only if the first changed the design beyond line level. Its brief names the previous pass's additions as its first target: new content is where new defects live. It re-runs the consumer exercise, opens the citations again, and re-derives the numbers.
- Two passes by default; the coordinator extends the chain when a pass finds a MAJOR inside the previous pass's own change (the tenancy design in the source project needed four; a hard cap would have shipped a broken closure check).
- The closing pass writes "CODE CHANGED beyond line-level: no" over its receipts; nothing else closes the loop.

Consider one dedicated pass — after the technical passes converge — that reviews the design against the *product*: walk the wireframes surface by surface and ask whether the design can render each one. Technical passes systematically miss coverage gaps because they audit what is written, not what is absent.

---

## Exit

On the closing pass:

1. Independently spot-check the design doc yourself before presenting it (open two citations, re-derive one number, compile the consumers).
2. Deliver the doc plus the full review trail to the maintainer.
3. List any deferred one-line edits with the phase that will absorb them.
4. Ask — never assume — about promoting the doc into the project docs tree, indexing it from `CLAUDE.md`, and archiving the review trail.

**The closing pass ends the design loop only.** The implementation loop starts only after Touchpoint 1: the maintainer reviews the batch of delegated design decisions and approves the shipped design (playbook §1).
