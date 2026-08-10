---
description: Stage 1 — interrogate a product idea in conversation until requirements stabilize, then deliver a requirements doc splitting hard requirements from the negotiable baseline
argument-hint: "[the product idea, or a path to existing notes]"
---

# Stage 1 — Product discovery

Turn an idea into a requirements artifact the rest of the methodology can be held against. Nothing downstream — no wireframe, no design doc, no line of code — is valid without this.

Shared doctrine: `${CLAUDE_PLUGIN_ROOT}/docs/playbook.md` (the playbook ships inside this plugin; that variable resolves to the plugin's install directory at runtime).

**Exit gate: the maintainer signs off the requirements doc.** Not "seems reasonable" — an explicit sign-off. Until then this stage is still running.

## The mode: interrogation, not intake

This is a conversation, not a form. Do not collect answers to a checklist and write them up. Push on the idea until the requirements stop moving.

- **Ask about the failure cases first.** "What does the product do when there's no data yet / the user does the wrong thing / the input is enormous?" Answers here fix more requirements than answers about the happy path.
- **Chase the numbers.** Any requirement stated as an adjective ("fast", "a lot of", "recent") is unfinished. Convert it to a number or a rule with the maintainer, in the conversation.
- **Name the thing you are not building.** Explicit non-goals are requirements. Write them down.
- **Stop when they stop moving.** The signal to exit is a full pass through the surfaces where the maintainer changes nothing.

## Explain technical concepts from first principles

Whenever a technical concept becomes load-bearing for a product decision — a scheduling algorithm, a consistency model, a scoring function, an identity scheme — **explain it from first principles until the maintainer can challenge it.** Not until they nod. Until they can push back on a specific mechanism.

This is not a courtesy. A maintainer who understands the mechanism produces objections a specialist would not, because they are reasoning from the product rather than from the convention.

## Convert challenges into measurable questions

When the maintainer challenges a technical choice, **do not debate it on taste.** Restate the challenge as a question with a measurable answer, then go measure it.

- Challenge: "I don't think that heuristic is picking the right cases."
- Wrong response: an argument about why the heuristic is principled.
- Right response: "Then the question is what fraction of the cases it selects are actually right, and what fraction of the right cases it misses. Let me sample and count both."

Report the measurement, not a defense. A measured answer settles the question in one round and frequently reverses the original position — this pattern is where the largest design corrections come from. Note also that "how often does it fire" is not a measurement of correctness; see the precision-and-recall rule in the implementation-loop skill.

## The deliverable: a requirements doc with two tiers

One document. It must separate two things, and the separation must be visible on the page:

**Hard requirements — R1..Rn.** What the maintainer actually mandated. **Few** (if you have twenty, most of them are baseline), and **stated abstractly** — a requirement names the property that must hold, not the mechanism that would hold it. "Every rendered number traces to a computed source" is a requirement; "use a placeholder grammar" is a design.

Downstream, R1..Rn are scored by every reviewer as satisfied / partial / violated. Write them so that scoring is possible.

**Negotiable baseline.** Every other conclusion reached in discussion. The design author may depart from any of it **with rationale**; departures are never silent, and each one is recorded (baseline position / new position / rationale). Framing session conclusions as hard constraints is a real failure mode: it forbids the design author from fixing them.

If the tier of a given conclusion is ambiguous, ask the maintainer rather than guessing. Guessing high freezes a mistake; guessing low loses a mandate.

**Product decisions log.** Capture each explicit product decision as it is made, with its date and a one-line rationale: `2026-03-14 — grade on outcome only, not on path taken (matches what the user can observe)`. Months later this log is the only thing that can distinguish a considered decision from an accident, and it is what a future agent reads before proposing to "fix" something deliberate.

## Structure

1. What this product is, in three sentences.
2. Who it is for and what they do today instead.
3. Hard requirements R1..Rn.
4. Non-goals.
5. Negotiable baseline, by area.
6. Product decisions log (dated).
7. Open questions — each with the measurement that would close it.

## Closing this stage

Present the doc to the maintainer, walk the R-list explicitly, and ask directly whether each R is really an R. On sign-off, place the doc in the project's docs tree and reference it from the project's `CLAUDE.md`. Then proceed to Stage 2 (wireframes) — not to design, and never to code.
