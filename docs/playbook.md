# The Bootstrap Playbook

Shared doctrine for all five stage-skills in the `app-bootstrap` plugin. Each skill points here rather than restating these rules — forked rules drift silently.

Read this once at the start of a stage. Everything below is binding unless the maintainer rules otherwise.

---

## 1 · Two loops: design first, then implementation

Every major feature runs **two sequenced loops, never one**:

1. **Design loop** — produces a design doc. Author agent + adversarial reviewer in revision rounds, including the interface-consumer exercise.
2. **Maintainer approval gate** — the shipped design goes to the maintainer. Implementation does not begin until they approve it. SHIP ends the *design loop*, not the design.
3. **Implementation loop** — author subagents implement against the approved design doc, one phase at a time; the adversarial reviewer reviews the code in rounds under the same findings discipline.

**Termination rule for both loops: the loop proceeds — revision round after revision round — until the adversarial reviewer's verdict is a plain SHIP.** Nobody but the reviewer ends a loop, and the coordinator still independently spot-checks after SHIP, before anything reaches the maintainer.

**Fixer ≠ judge.** The agent that wrote something never certifies it alone.

---

## 2 · Verdict vocabulary

There are exactly two verdicts:

- **SHIP**
- **ONE MORE ROUND**

Nothing else exists. "Mostly fine", "ship with reservations", "SHIP modulo two nits", "LGTM" — all of these are **ONE MORE ROUND**. Reviewers are told this in their brief, and a hedged verdict is treated as ONE MORE ROUND regardless of how the reviewer meant it.

Findings inside a round use a separate two-axis vocabulary:

- **Severity**: BLOCKER / MAJOR / MINOR / NIT
- **Confidence**: CONFIRMED (with `file:line`) or PLAUSIBLE (with what would confirm it)

---

## 3 · Adversarial briefing template

**The review step is adversarial by construction: the reviewer's brief states as a premise that the work under review contains defects, and the reviewer's job is to find them.** A review that returns "looks good, no issues" without having hunted is a failed review, not a passed one.

Every reviewer brief carries all six of these:

1. **Skeptic framing, never validator framing.** Write "this work contains at least one real defect — find it" (or, when that would be a lie, "assume it does until you have exhausted the defect classes below"). Never write "check whether this looks right." Validators rubber-stamp; hunters read.
2. **A target list of defect classes.** Enumerate what to sweep — wrong behavior on edge inputs, contract violations between modules, convention breaches, stated-behavior-vs-actual-code contradictions, invented facts, missing error handling, gates that certify something they never tested. An unscoped "find problems" degrades into style nitpicks.
3. **Per-defect-class receipts.** A clean report must prove the hunt happened: for each class, what was checked and what was found, including "swept, none found" with the evidence examined. "No issues" with no receipts is auto-rejected.
4. **Demonstrated, not asserted.** Each finding needs a concrete failing input, a traced code path, or a cited contradiction — plus a **concrete failure scenario** and a minimal fix. Verify-then-drop: suspicions that check out clean are not reported.
5. **Scope of authority.** Reviewers apply line-level fixes in place (never hand back a diff), and every applied fix cites the defect it repairs. Reviewers do **not** unilaterally make architecture changes — those become design-level concerns for the maintainer. Reviewers do not "fix" correct code they merely dislike.
6. **Ledger obligations.** A requirement scorecard (R1..Rn: satisfied / partial / violated, with evidence), a verdict per Departure (uphold / reverse / amend), a "what this got right" list so later rounds don't regress the strengths, and the closing verdict from §2.

**Reviewers verify by reading, not just by running gates.** Green build, lint and tests are necessary and nowhere near sufficient: the dominant defect classes — stated behavior contradicted by the code's own handling, invented facts, a gate that never exercised its subject — survive every mechanical check.

**Reviewers argue back with evidence.** A reviewer that defers without checking the claim will break correct work. Disagreement backed by a cited source is a feature.

---

## 4 · Subagent discipline

- **Verification checklist (required).** Every subagent brief ends with an enumerated checklist of concrete, checkable criteria. The agent must not finish until it has re-read its own output and confirmed every item, and must return the completed checklist (each item PASS + a one-line justification) in its report. Vague goals produce shallow, unverified work.
- **Self-certified "all PASS" is necessary but not sufficient.** Checklist items have blind spots. The coordinator always reads the actual output before declaring anything done.
- **Briefs are self-contained.** Each agent starts fresh; the brief carries context, scope, inputs, and output expectations completely — or points at exactly the doc sections that do. "Based on your findings, do X" pushes synthesis onto the agent and produces shallow work.
- **Never restate in a brief a rule that lives in a doc.** Point at the doc. (Exception: worked examples that must not be compressed travel verbatim.)
- **Ground truth wins over the brief.** Give every author agent a reading list of the actual code/artifacts, with the standing rule: the source wins over the brief's characterizations, and discrepancies get reported rather than silently reconciled.
- **Slice work cleanly.** Non-overlapping scopes, one report per agent, run in parallel when there are no ordering dependencies; one at a time when there are. Batch very large fan-outs in waves so completed work survives context exhaustion.

---

## 5 · Persistent author, persistent reviewer

- **The author agent is continued, never respawned mid-loop.** Keep its agent id and continue it (via SendMessage, or the environment's equivalent) for every revision round — the accumulated context is the value. Retire it and start a fresh author only when its context approaches exhaustion (roughly 500k tokens), and then hand the successor the design doc plus the review trail as its ground truth.
- **The reviewer is persistent across rounds within a loop.** One reviewer sees every round, so it can verify dispositions against the revised text rather than re-deriving the design each time. Rounds stack **newest-first** in a single review file next to the artifact under review.
- **A fresh reviewer starts each new loop or phase.** The design loop's reviewer does not review the implementation; each implementation phase gets its own reviewer. Fresh eyes per unit of work; continuity within it.
- **Keep reviewer contexts open after they finish**, so the coordinator can ask follow-up questions instead of re-litigating from scratch.
- **Agent model choice is a maintainer setting, recorded in the project's `CLAUDE.md`** (the source project ran all authors and reviewers on its strongest available subagent model). Reviewers are never given a weaker model than authors.

---

## 6 · Maintainer rulings: the four-part walkthrough

Contested findings, reviewer-vs-author disagreements, and any decision that trades off product behavior go to the maintainer. Each one is presented in exactly four parts:

1. **Background** — written for a low-context reader. Assume the maintainer has not read the diff or the finding thread.
2. **Concrete failure scenario** — the specific sequence of events in which this goes wrong, with real values.
3. **Options, each with what it GIVES UP** — not a list of upsides. Every option's cost is stated explicitly; an option with no stated cost has not been analyzed.
4. **Recommendation with reasoning** — a real recommendation, not a shrug.

**A recommendation is never auto-applied.** The maintainer rules; the coordinator implements the ruling. Batch related decisions into one message rather than drip-feeding them. Spot-check load-bearing findings yourself before relaying them — reviewers can be wrong, and a BLOCKER relayed without verification wastes a maintainer decision.

Rulings travel into the next revision brief **verbatim and binding**, alongside every other finding with its required disposition, and explicit discretion boundaries (which fix shapes are the author's call — those require a one-paragraph justification).

**Propose the ideal plan — no sunk-cost pre-compromise.** Plans, proposals, and briefs optimize for the best end state, judged purely on outcome quality. Implementation effort, edit cheapness, and sunk cost in already-built artifacts are never decision criteria and must not be baked into a brief. Present the ideal plan first; then, separately, discuss how it could be compromised down if required. Real costs are inputs to the maintainer's trade-off, never reasons to self-censor a recommendation.

---

## 7 · Delegation economics

The coordinator's job is to hold the thread, not to do all the work — and not to delegate all of it either.

- **Delegate substantial work to agents that hold context.** Anything that requires reading a lot of source, writing a lot of output, or sustaining a line of reasoning across many files belongs in a subagent — and preferably in one that is *continued* rather than respawned.
- **Make trivial edits yourself.** When writing the brief would cost more than the edit, do the edit. A one-line fix, a renamed symbol, a corrected typo in a doc: delegating these costs more tokens and more wall-clock time than doing them, and it adds a round-trip where a defect can be introduced.
- **The dividing line is briefing cost vs. edit cost**, not importance. An important one-liner is still a one-liner.
- **Never build LLM-via-subprocess pipelines.** Subagents writing files directly outperform any chain of CLI-invoked models.

---

## 8 · Background-agent hygiene

- **Run long agents in the background** so foreground work continues. Design and review agents on large artifacts always qualify.
- **Keep review agents continuable** — do not consider a reviewer disposable until the maintainer says the loop is closed.
- **Never fabricate or predict a pending agent's result.** If the maintainer asks before the notification arrives, say it is still running.
- **Capture expensive output to a file first, then grep it.** Inspecting a failure should never require re-running the thing that failed.
- **Scripts are idempotent and pre-flight-validated**, never one-shot. Destructive runs require an explicit dry-run mode first. One-shot apply scripts get merged into the tree and deleted — they decay into noise.

---

## 9 · Artifact hygiene across loops

- **Revisions are in-place edits to the one artifact**, with a revision-log section extended per round. No addendum files, no `-v2` copies.
- **Reviews stack newest-first in one review file** beside the artifact.
- **Keep design docs current.** When a change alters a subsystem, the subsystem's design doc changes in the same commit. Stale docs mislead every future agent that reads them.
- **On SHIP**, promote the artifact into the project's docs tree and index it from the project's `CLAUDE.md`, then archive the review trail — but ask the maintainer first; never assume.

---

## Provenance

This playbook is a generalization of the working methodology used to build the Postmortem chess-trainer project (a chess.com/Stockfish/FSRS training app), which itself ported the loop from an earlier flashcards project. The specific rules here — the two-loop sequencing, the interface-consumer exercise, the verdict vocabulary, and the six gate-honesty rules in the implementation-loop skill — each exist because a defect got through without them.
