---
name: implementation-loop
description: Use when an approved design is ready to build, or the user asks to start implementing a phase — Stage 4 of the app-bootstrap methodology, phased implementation where each phase is an author followed by a chain of fresh adversarial passes that fix in place, under the six gate-honesty rules
argument-hint: "[path to the approved design doc, or the phase to run]"
---

# Stage 4 — The implementation loop

Implement an approved design, **one phase at a time**, each phase its own author → adversarial-pass chain (playbook §12) that runs until a pass changes nothing beyond line level.

Shared doctrine: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** Touchpoint 1 is cleared — the design has SHIPped *and* the maintainer has reviewed the delegated design decisions and approved implementation (playbook §1). Not one or the other. Once entered, the loop runs autonomously under delegated authority through every phase; the next standing maintainer review is Touchpoint 2, after the whole implementation loop closes.
**Exit gate per phase:** a pass whose verdict line is "CODE CHANGED beyond line-level: no" with its receipts, plus the coordinator's own closure checks.

---

## Phase structure

The approved design carries a phased build plan with a **named verification gate per phase**. Run them in order. For each phase:

1. **Author agent** (background, continued within the phase, retired at the playbook §5 bound) implements the phase against the design doc with its named gate and every injection watched to fail, commits with named paths, and writes notes with the injection record and a RESUME STATE.
2. **A fresh adversarial pass** — briefed per the playbook §3 and §12 — replays every injection from a `cp` backup, hunts for gates that pass against the defect they name, opens every cited `file:line`, fixes what it finds in place (minimal diff, fix-only, a gate per fix), and commits the code with its trail entry. It ends with the verdict line of the playbook §2.
3. **Another fresh pass** only if the previous one changed code beyond line level; the previous pass's own additions are its first target. Two passes by default; the coordinator extends the chain when a pass finds a MAJOR inside the previous pass's own change. Leftovers carry to the next phase's brief.
4. **The coordinator closes the phase** (below), then moves to the next.

Every pass is a fresh agent; the committed trail is the memory. Fixer ≠ judge, one step removed: a pass fixes, the next pass judges its fixes first.

---

## The six gate-honesty rules

These are first-class instructions, not advice. Each exists because a defect shipped past a gate that claimed to catch it. Carry them into every author brief and every reviewer brief in this stage.

### 1. Every fault-injecting gate must assert the fault actually landed

A test that injects a crash, a kill, a timeout, a network failure, a partial write, or a corrupted input must **assert that the injection took effect** before it asserts anything about the recovery. Otherwise it certifies the happy path under a scary name.

The canonical failure: a crash-recovery gate spawned the work through a wrapper command, so the signal killed the wrapper while the real work continued uninterrupted in a grandchild process. Every "crash trial" was actually a clean run, and the gate printed PASS. The same failure class recurred in five consecutive phases of the project this methodology comes from, each time in a different disguise.

Concretely: capture evidence that **the work itself was interrupted** — its output stops mid-record, its effect is absent, the write really was truncated, the request really did fail — and assert on *that*, not merely that some process received the signal. "A process died" is not evidence: in the anecdote above a process really did die, and it was the wrong one. Anchor on the work, then fail the gate when the injection did not land — separately, and with a distinct message from the recovery assertion, so the two failures are never confused.

### 2. Detectors report precision AND recall — never how often they fire

For anything that classifies, selects, flags, or matches, the reportable measurements are:

- **Precision** — of the things it flagged, what fraction were right?
- **Recall** — of the things it should have flagged, what fraction did it catch?

**Firing frequency is not a measurement of correctness.** "The rule matched 340 times" tells you nothing about whether those 340 were right or how many were missed. In the source project, two wrong rules reached the design doc as "corrections" because someone measured how often they fired rather than whether the hits were correct.

Recall requires a labeled set the detector did not choose. Build it, sample it honestly, and report both numbers together — a precision number alone is as misleading as a frequency count.

### 3. A gate is believed only after its defect has been introduced and seen to fail it

Mutation testing, applied to gates. **Do not trust a gate you have not watched fail.** For each meaningful gate: introduce the exact defect the gate claims to catch, run the gate, confirm it fails, revert, confirm it passes.

**This applies with full force to pins added to close review findings.** A pin written in response to a finding is exactly the case where nobody checks — the finding is closed and everyone moves on. One such pin was proven vacuous this way: it passed against the reverted (defective) code for an unrelated reason, so it had never been testing the thing it was written to protect.

Beware the fixture that makes the branch under test unreachable. A gate that passes against both the fixed code and the deliberately-broken code has not tested the branch; it has tested a path that never enters it.

### 4. Every subagent brief ends with an enumerated verification checklist

Concrete, checkable criteria. The agent must not finish until it has re-read its own output and confirmed every item, and must return the completed checklist (each item PASS with a one-line justification).

**Self-certified "all PASS" is necessary but not sufficient.** Checklist items have blind spots — an item can pass for a reason unrelated to what it meant to check. Phrase items to close those gaps, and read the actual output yourself before declaring anything done.

### 5. Passes are adversarial, never validators

Briefed with the premise that the work contains defects, given an enumerated list of defect classes to sweep, and required to return **per-defect-class receipts** — what was checked, what was found, including "swept, none found" with the evidence examined. "No issues" with no receipts is auto-rejected. See the playbook §3 for the full template. A pass that finds nothing writes "CODE CHANGED beyond line-level: no" over those receipts, and that closes the phase; a pass that fixes anything beyond a line hands the phase to the next fresh pass.

Note what this catches that mechanical gates cannot: stated behavior contradicted by the code's own handling, invented facts, and **inversions** — a signal that fires on exactly the wrong cases, a count that counts the wrong noun, a direction word computed off an empty baseline. Every inversion of that kind in the source project rendered through a path some gate had already certified, and every one was found by reading code against its own prose and then *executing* it.

### 6. Measured numbers beat estimated numbers

Any budget, projection, cost, latency, throughput, or size estimate that appears in the design or in a brief gets **re-measured in the pipeline** once real work runs through it. Discrepancies between the estimate and the measurement are reported as **headline items**, not footnotes — an order-of-magnitude miss on a budget invalidates the design decision it justified, and burying it means that decision never gets revisited.

Where a number is currently an estimate, label it as one, in the artifact, at the point of use.

---

## Per-phase brief requirements

Author brief:

- the approved design doc, with the phase's section named;
- the wireframe artifact URL for anything user-facing — or its committed path, where Stage 2 fell back to a self-contained page — with callouts binding, and confirmed reachable by the agent you are briefing;
- the ground-truth rule: the code wins over the brief's characterizations; report discrepancies;
- the phase's named verification gate, plus rules 1, 3 and 6 above as binding constraints on how that gate is written;
- project conventions, by pointer to the project's `CLAUDE.md` — never restated;
- the enumerated verification checklist (rule 4).

Pass brief: the playbook §3 template and the §12 order of work, plus the phase's design section, the author's notes and injection record, the trail file, plus rules 1–3 and 6 as explicit defect classes to sweep — *"find a gate that would pass against the defect it claims to catch"* is one of the highest-yield instructions in the list. A second pass's brief names the first pass's additions as its first target. Every brief ends with the enumerated completion checklist (rule 4) and the verdict line.

---

## Closing a phase

1. A pass that changed nothing beyond line level, with its receipts, and every carried item named.
2. The coordinator's own checks: the delivery's diffstat touches the files the findings named; one injection replayed under the coordinator's own test namespace; a staging worktree with its own dependency install, a fresh build and both full suites; the version resolved on the version line alone (playbook §11); a fast-forward of the trunk.
3. Design doc updated in the same change if the phase altered any subsystem's behavior. Stale docs mislead every future agent.
4. Record the phase outcome for the eventual Touchpoint 2 review: what shipped, what the gates now prove, every measured-vs-estimated discrepancy, and any deferred item with the phase that will absorb it. This is a non-blocking record, not a per-phase approval gate — under delegated authority (playbook §1) the coordinator does not wait for the maintainer between phases.

Then, once steps 1-3 hold, write the ledger and registry rows and start the next phase. The maintainer reviews the accumulated phase records at Touchpoint 2, after the implementation loop's final phase closes.
