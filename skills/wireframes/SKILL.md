---
name: wireframes
description: Use when requirements are signed off and the UI has not been drawn yet, or the user asks what the app will look like — Stage 2 of the app-bootstrap methodology, wireframing every surface as one artifact whose numbered callouts carry binding semantics
argument-hint: "[path to the signed-off requirements doc]"
---

# Stage 2 — Wireframes

Turn the signed-off requirements into a picture of every surface the product has. This stage exists because a design doc written before the UI is known will encode a data model the UI cannot render, and nobody finds out until implementation.

Shared doctrine: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** the Stage 1 requirements doc is signed off.
**Exit gate:** the maintainer signs off the wireframes, and the artifact's stable identity — its published URL, or the committed path of the fallback below — is recorded in the project's `CLAUDE.md` as the UI source of truth.

## Before drawing

**Invoke the `frontend-design` skill if it is available in this environment**, and follow its guidance on aesthetic direction, typography, and avoiding templated defaults. These wireframes are a design decision, not a box diagram; a wireframe that reads as a generic admin panel will produce a generic admin panel.

Then re-read the requirements doc. Every hard requirement R1..Rn must be visible somewhere in the wireframes or explicitly marked as non-visual.

## Cover every surface

Not the main screen. Every surface:

- every primary screen or view;
- every empty state (day one, nothing ingested, nothing to do);
- every error and failure state a user can reach;
- every modal, drawer, filter, and settings surface;
- the loading/partial state of anything slow;
- any global control that changes what every other surface shows — draw it once and mark what it does and does not affect.

A surface you skip is a surface the design loop will not account for.

## Numbered callouts carry binding semantics

This is the mechanism that makes wireframes useful downstream. Every non-obvious behavior on a surface gets a **numbered callout** with a one- or two-sentence statement of the rule:

> **(4)** The count shown here is the number of items due today *after* the scope filter, not the total. When the filter excludes everything, this reads `0` and the action below is disabled rather than hidden.

Callout text is **binding**. Design docs and implementations are held against it exactly like a hard requirement, and reviewers cite it by number (`callout 4`). Two consequences:

- Write callouts as rules with defined behavior at the edges, not as descriptions of the drawing.
- If a callout turns out to be wrong, it changes by maintainer ruling and the artifact is re-published — not by an implementer quietly doing something else.

Mark any surface exempt from a global control explicitly (`scope-exempt`), because exemptions are exactly what implementations get wrong.

## Publish as an artifact

Produce the wireframes as **one published artifact** — a single page containing every surface with its callouts, in a stable order, with a heading per surface. One page, one URL, one thing to keep current.

**If artifact publishing is unavailable in this environment**, produce a single self-contained HTML file at a stable committed path in the repository, and use that path everywhere this methodology says "the artifact URL". The requirement is *one page with one stable identity that every downstream brief can open* — not the hosting. Do not silently substitute a scattering of images, a doc per surface, or a description of what the UI would look like.

Stamp the page with a decision date: `Locked 2026-03-21`. When a surface changes later, update the artifact in place (same URL or path), bump the date, and note what changed. That identity is the point; do not mint a new one for a revision.

## Lock it

On maintainer sign-off:

1. Record the artifact's URL or committed path in the project's `CLAUDE.md` under a **UI source of truth** line, with the note that the numbered callouts carry binding semantics.
2. Reference the same identity from the requirements doc.
3. Give every downstream author and reviewer brief that identity as required reading, and confirm they can open it.

From this point, "the UI does X" is settled by the artifact, not by argument.
