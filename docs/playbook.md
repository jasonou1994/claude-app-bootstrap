# The Bootstrap Playbook

Shared doctrine for all six stage-skills in the `app-bootstrap` plugin. Each skill points here rather than restating these rules, because forked rules drift silently.

Read this once at the start of a stage. Everything below is binding unless the maintainer rules otherwise.

---

## 1 · Two loops under delegated authority, bracketed by two maintainer touchpoints

Every major feature runs **two sequenced loops, never one**:

1. **Design loop** — produces a design doc. Author agent + adversarial reviewer in revision rounds, including the interface-consumer exercise.
2. **Implementation loop** — author subagents implement against the approved design doc, one phase at a time; the adversarial reviewer reviews the code in rounds under the same findings discipline.

**Delegated authority is the default posture.** Within a loop the coordinator holds delegated authority to rule the design and implementation decisions itself and drive the loop to a SHIP, without surfacing each decision for maintainer approval mid-loop. The coordinator tags and records every decision it rules and presents the major ones at the next touchpoint (§6); it does not pause the loop to pre-clear them. The delegation covers decisions taken inside a loop. It does not let the coordinator end a loop (only the adversarial reviewer's plain SHIP does that), skip its own post-SHIP spot-check, or override the adversarial reviewer's authority.

**Two standing maintainer touchpoints bracket the implementation, and they are the only two:**

- **Touchpoint 1, after the design loop SHIPs.** The maintainer reviews the batch of delegated design decisions (the major ones presented as four-part walkthroughs, §6) *and* approves before the implementation loop begins. This single touchpoint is both the decision review and the go-ahead to implement; it replaces the former standalone approval gate. SHIP ends the *design loop*, not the design.
- **Touchpoint 2, after the implementation loop SHIPs.** The maintainer reviews what was built.

Between the two loops and within each of them, the coordinator runs autonomously under the delegation. These two touchpoints are the only standing ones; the gated actions below are separate per-action holds, not additional touchpoints.

**Gated actions always wait for an explicit maintainer go, regardless of loop state.** Even under delegated authority a fixed set is never taken autonomously: merging to a shared trunk, any outward-facing "this is ready" signal (publishing, announcing, marking a PR ready), and anything hard to reverse. These wait for an explicit go whatever the loop's state, so the delegation is never read as "autonomous merges."

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

**Which severities block a SHIP:** a SHIP asserts that no BLOCKER or MAJOR finding is open, and that every remaining MINOR and NIT is explicitly listed in the verdict as accepted residue for the maintainer. Listing accepted residue is not a hedge — it is the verdict doing its job; what §2 bans is the *unenumerated* qualifier ("mostly fine", "modulo a few nits") that leaves the reader to guess what is still open. Without this rule the loop has no termination condition, since a reviewer instructed that "no issues found" is a failed review can always produce one more NIT.

---

## 3 · Adversarial briefing template

**The review step is adversarial by construction: the reviewer's brief states as a premise that the work under review contains defects, and the reviewer's job is to find them.** A review that returns "looks good, no issues" without having hunted is a failed review, not a passed one.

Every reviewer brief carries all six of these:

1. **Skeptic framing, never validator framing.** Write "this work contains at least one real defect — find it" (or, when that would be a lie, "assume it does until you have exhausted the defect classes below"). Never write "check whether this looks right." Validators rubber-stamp; hunters read.
2. **A target list of defect classes.** Enumerate what to sweep — wrong behavior on edge inputs, contract violations between modules, convention breaches, stated-behavior-vs-actual-code contradictions, invented facts, missing error handling, gates that certify something they never tested. An unscoped "find problems" degrades into style nitpicks.
3. **Per-defect-class receipts.** A clean report must prove the hunt happened: for each class, what was checked and what was found, including "swept, none found" with the evidence examined. "No issues" with no receipts is auto-rejected.
4. **Demonstrated, not asserted.** Each finding needs a concrete failing input, a traced code path, or a cited contradiction — plus a **concrete failure scenario** and a minimal fix. Verify-then-drop: suspicions that check out clean are not reported.
5. **Scope of authority — and it differs by loop.** In the **implementation loop**, reviewers apply line-level fixes in place (never hand back a diff), and every applied fix cites the defect it repairs. In the **design loop**, the author owns every edit to the design doc and the reviewer only reports — a reviewer that edits the doc will be clobbered by the persistent author's next revision, and would then be "verifying dispositions" against text it wrote itself, breaking Fixer ≠ judge (§1). A **journey-results reviewer** (Stage 5) follows the implementation-loop rule — it reviews produced artifacts, so it fixes in place and cites the defect per fix — though Stage 5 is a stub and this assignment is provisional until a real cycle tests it. In every loop, reviewers do **not** unilaterally make architecture changes — those become design-level concerns for the maintainer — and never "fix" correct work they merely dislike.
6. **Ledger obligations.** A requirement scorecard (R1..Rn: satisfied / partial / violated, with evidence); where the artifact under review has a Departures section, a verdict per Departure (uphold / reverse / amend); a "what this got right" list so later rounds don't regress the strengths; and the closing verdict from §2.

**Reviewers verify by reading, not just by running gates.** Green build, lint and tests are necessary and nowhere near sufficient: the dominant defect classes — stated behavior contradicted by the code's own handling, invented facts, a gate that never exercised its subject — survive every mechanical check.

**Reviewers argue back with evidence.** A reviewer that defers without checking the claim will break correct work. Disagreement backed by a cited source is a feature.

---

## 4 · Subagent discipline

- **Verification checklist (required).** Every subagent brief ends with an enumerated checklist of concrete, checkable criteria. The agent must not finish until it has re-read its own output and confirmed every item, and must return the completed checklist (each item PASS + a one-line justification) in its report. Vague goals produce shallow, unverified work.
- **Self-certified "all PASS" is necessary but not sufficient.** Checklist items have blind spots. The canonical example: a checklist item reading *"every question ends in ?"* passed, while the interrogative sentences it existed to catch ended in a period — the item was satisfiable without the property it stood for being true. Phrase items to close that gap, and have the coordinator read the actual output before declaring anything done.
- **Briefs are self-contained.** Each agent starts fresh; the brief carries context, scope, inputs, and output expectations completely — or points at exactly the doc sections that do. "Based on your findings, do X" pushes synthesis onto the agent and produces shallow work.
- **Never restate in a brief a rule that lives in a doc.** Point at the doc. (Exception: worked examples that must not be compressed travel verbatim.)
- **Ground truth wins over the brief.** Give every author agent a reading list of the actual code/artifacts, with the standing rule: the source wins over the brief's characterizations, and discrepancies get reported rather than silently reconciled.
- **Slice work cleanly.** Non-overlapping scopes, one report per agent, run in parallel when there are no ordering dependencies; one at a time when there are. Batch large fan-outs — more than about 20 agents — in waves of roughly 20 at a time, so completed batches survive context exhaustion.
- **Do not commit or push unless explicitly requested.** This binds every agent in every stage, and it matters most in the implementation loop, where author agents write files across a whole repository unattended. An agent that commits on its own initiative destroys the maintainer's ability to review a phase as a unit; one that pushes publishes unreviewed work.
- **Prefer editing existing files over creating new ones.** New files are where duplicated doctrine and orphaned artifacts come from. This is the same instinct as §9's ban on `-v2` copies.
- **Do not delegate test or verification runs to subagents for concurrency.** Run them from the coordinator. Delegating a gate run puts a summarizing layer between you and the output — and the output of a gate is exactly the thing this methodology refuses to accept second-hand (see the gate-honesty rules in the implementation-loop skill). Delegate the *work*; read the gate yourself.

---

## 5 · Persistent author, persistent reviewer

- **The author agent is continued, never respawned mid-loop.** Keep its agent id and continue it (via SendMessage, or the environment's equivalent) for every revision round — the accumulated context is the value. Retire it and start a fresh author when its cumulative usage reaches roughly 500k tokens: it finishes the round it is on, and every later round goes to a successor whose brief hands over the design doc, the round-stacked review file, and the current dispositions as ground truth. (Threshold set by maintainer ruling 2026-08-09, first applied to a live loop the same day; "the author is starting to lose earlier rounds" remains the early-warning signal at any count.)
- **The reviewer is persistent across rounds within a loop.** One reviewer sees every round, so it can verify dispositions against the revised text rather than re-deriving the design each time. Rounds stack **newest-first** in a single review file next to the artifact under review.
- **A fresh reviewer starts each new loop or phase.** The design loop's reviewer does not review the implementation; each implementation phase gets its own reviewer. Fresh eyes per unit of work; continuity within it.
- **Keep reviewer contexts open after they finish**, so the coordinator can ask follow-up questions instead of re-litigating from scratch.

---

## 6 · Weight-sorted decisions and the four-part walkthrough

Under delegated authority (§1) the coordinator rules the decisions a loop produces and drives on without pausing for per-decision approval. What replaces the pause is a recording-and-presentation discipline:

- **Tag every delegated decision major or mechanical.** Major means it settles a contract, an architecture choice, or a risk trade-off. Mechanical is everything else.
- **Record all of them in the design artifact's decision table** — major and mechanical alike — each with its ruling and accepted costs. The artifact is the single home for the decision record (§9).
- **Present the major ones to the maintainer at Touchpoint 1** (§1), each as a four-part walkthrough. Mechanical decisions are recorded, not walked.

The four-part walkthrough survives as the presentation FORMAT at the touchpoint, not as a per-decision gate that blocks the loop. Each major decision is presented in exactly four parts:

1. **Background** — written for a low-context reader. Assume the maintainer has not read the diff or the finding thread.
2. **Concrete failure scenario** — the specific sequence of events in which this goes wrong, with real values.
3. **Options, each with what it GIVES UP** — not a list of upsides. Every option's cost is stated explicitly; an option with no stated cost has not been analyzed.
4. **Recommendation with reasoning** — a real recommendation, not a shrug.

Batch related decisions into one presentation rather than drip-feeding them. **Spot-check load-bearing findings yourself before relaying them** — reviewers can be wrong, and a BLOCKER relayed without verification wastes a maintainer decision.

A decision the maintainer overrides at a touchpoint travels into the next revision brief **verbatim and binding**, alongside every other finding with its required disposition, and explicit discretion boundaries (which fix shapes are the author's call — those require a one-paragraph justification).

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

## 10 · Writing register for design and doc artifacts

Design docs and the doc artifacts a loop produces are written **from absolute first principles**. The rationale is mechanism-before-memorization: a reader handed the motivation and the moving parts can re-derive the design under pressure, where a reader handed only conclusions can recite but not extend them. State the rationale so the register is followed, not cargo-culted. The register:

- **Assume the reader knows nothing about the subsystem.** Build from the ground up; introduce each concept only as the solution to a problem the previous concept created.
- **Motivation before mechanism.** State the problem a mechanism solves before the mechanism itself.
- **Define every term before first use.** Never reference a concept the document has not yet introduced, including one introduced later in the same document.
- **A worked example with real values for every abstract mechanism.** Show the state before, the action, and the state after, with concrete values, plus one allowed and one denied case traced against that state. A slogan is not an explanation; if the reader cannot picture the stored data changing, the mechanism has not been explained.
- **Flag every simplification explicitly** at the point you make it, so it is a stated contract rather than a later surprise.
- **End with a single compressed takeaway sentence.**
- **No em dashes.** State the fact upfront and let each claim stand as its own sentence, rather than burying a lead behind a preface or bolting an afterthought onto the tail.

The template `skills/design-loop/assets/design-doc-template.html` carries this register's section skeleton and the decision-table styling; the shipped design docs it is modeled on are the worked exemplars, opening with a from-nothing orientation section, grounding every claim in `file:line`, and carrying a wire-level worked example for each mechanism.

---

## 11 · Loop operations

Rules for running several loops at once in one repository and for closing what they produce. Each one was adopted after a specific failure in the completion drive of 2026-09-02 to 2026-09-05 (retrospective in the source project, `docs/drive/retrospective-2026-09-05.md`); the failure is stated before the rule so the rule can be re-derived.

- **A worktree per loop when loops share directories; merge at SHIP after a fresh build.** Four loops on one checkout meant three phase closures in a row swept a neighbour's half-typed hunks into the wrong commit, three closures left HEAD uncompilable, and reviewers saw `Tests: 0 total` from files another author was mid-edit on. So: any loop whose directories overlap another live loop's runs in its own git worktree, and its author and reviewer share that worktree. At SHIP the coordinator merges to the trunk only after building the merged tree from scratch (including any shared package whose build output a type-check reads) and running the touched suites there. Loops on disjoint directories may share a checkout; the moment they touch the same file, they split.
- **The fresh-checkout build is the last step of every phase closure.** Closure commits were staged from the author's list of touched files, and four times that list was incomplete (a route, a fixture, a seam, a wiring file), so HEAD did not compile for anyone who checked it out. So: before a closure is declared, check out HEAD into a fresh directory and build it. Read the author's touched-file list against the working tree's status; a hunk a neighbour left in a shared file is named in the closure message, never swept in silently.
- **Reviewers replay injections from `cp` backups and rebuild after restoring.** A gate is believed only after it has been watched to fail (implementation-loop rule 3), and the reviewer, not the author, does the watching. So: the reviewer copies the file aside, pastes the defect in, runs the gate and records the red, restores from the copy, runs it again and records the green. The injection window is not confined to source: a neighbour's build can capture an injected expression in compiled output (`dist/`) between the paste and the restore, and a later run then tests the defect under a green name. Rebuild after restoring, and treat a gate that passes against the defect it names as a finding.
- **Only the coordinator numbers decisions.** Authors running in parallel each assigned their own ids to rulings they needed, and the ids collided three times, so two different rulings share a number in the record. So: decision ids are assigned by the coordinator alone; an author that needs one asks and waits. A ruling is written into the decision record before the brief that cites it is sent.
- **A dated, immutable scoring protocol before a measurement's first call.** A measurement whose rules are written after its results are seen measures the rule-writer. So: before the first call of any measurement (an agent campaign, a precision-and-recall sample, a benchmark), write the labels, the scoring rules and the counting method into a dated file, and never edit that file afterwards. A rule discovered post hoc goes into a new dated file beside the original, which states what it changes and why, so a reader can see which results were scored under which rules.

---

## Provenance

This playbook is a generalization of the working methodology used to build the Postmortem chess-trainer project (a chess.com/Stockfish/FSRS training app), which itself ported the loop from an earlier flashcards project. The specific rules here — the two-loop sequencing, the interface-consumer exercise, the verdict vocabulary, and the six gate-honesty rules in the implementation-loop skill — each exist because a defect got through without them.
