---
description: Stage 4 — implement an approved design in phases, one author-plus-adversarial-reviewer loop per phase, under the six gate-honesty rules
argument-hint: "[path to the approved design doc, or the phase to run]"
---

# Stage 4 — The implementation loop

Implement an approved design, **one phase at a time**, each phase its own author → adversarial reviewer loop that runs until a plain SHIP.

Shared doctrine: [`../../docs/playbook.md`](../../docs/playbook.md).

**Entry gate:** the design has SHIPped *and* the maintainer has approved it. Not one or the other.
**Exit gate per phase:** a plain SHIP from that phase's adversarial reviewer, plus the coordinator's own independent spot-check.

---

## Phase structure

The approved design carries a phased build plan with a **named verification gate per phase**. Run them in order. For each phase:

1. **Author agent** (background, kept open across the phase's rounds) implements the phase against the design doc, writing files directly.
2. **A fresh adversarial reviewer** for this phase — briefed per the playbook §3 — hunts for defects and applies line-level fixes in place, citing the defect each fix repairs.
3. **Revision rounds** until the verdict is a plain SHIP. Each round verifies dispositions against the revised code, not the author's claims, and attacks the new surfaces the revision introduced.
4. **The coordinator spot-checks independently**, then integrates and moves to the next phase.

A fresh reviewer per phase; a persistent author within a phase. Fixer ≠ judge.

---

## The six gate-honesty rules

These are first-class instructions, not advice. Each exists because a defect shipped past a gate that claimed to catch it. Carry them into every author brief and every reviewer brief in this stage.

### 1. Every fault-injecting gate must assert the fault actually landed

A test that injects a crash, a kill, a timeout, a network failure, a partial write, or a corrupted input must **assert that the injection took effect** before it asserts anything about the recovery. Otherwise it certifies the happy path under a scary name.

The canonical failure: a crash-recovery gate spawned the work through a wrapper command, so the signal killed the wrapper while the real work continued uninterrupted in a grandchild process. Every "crash trial" was actually a clean run, and the gate printed PASS. The same failure class recurred in five consecutive phases of the project this methodology comes from, each time in a different disguise.

Concretely: capture evidence that the fault happened (the process really died and at what point; the write really was truncated; the request really did fail), assert on that evidence, and fail the gate when the injection did not land — separately and with a distinct message from the recovery assertion.

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

### 5. Reviewers are adversarial, never validators

Briefed with the premise that the work contains defects, given an enumerated list of defect classes to sweep, and required to return **per-defect-class receipts** — what was checked, what was found, including "swept, none found" with the evidence examined. "No issues" with no receipts is auto-rejected. See the playbook §3 for the full template.

Note what this catches that mechanical gates cannot: stated behavior contradicted by the code's own handling, invented facts, and **inversions** — a signal that fires on exactly the wrong cases, a count that counts the wrong noun, a direction word computed off an empty baseline. Every inversion of that kind in the source project rendered through a path some gate had already certified, and every one was found by reading code against its own prose and then *executing* it.

### 6. Measured numbers beat estimated numbers

Any budget, projection, cost, latency, throughput, or size estimate that appears in the design or in a brief gets **re-measured in the pipeline** once real work runs through it. Discrepancies between the estimate and the measurement are reported as **headline items**, not footnotes — an order-of-magnitude miss on a budget invalidates the design decision it justified, and burying it means that decision never gets revisited.

Where a number is currently an estimate, label it as one, in the artifact, at the point of use.

---

## Per-phase brief requirements

Author brief:

- the approved design doc, with the phase's section named;
- the wireframe artifact URL for anything user-facing (callouts are binding);
- the ground-truth rule: the code wins over the brief's characterizations; report discrepancies;
- the phase's named verification gate, plus rules 1, 3 and 6 above as binding constraints on how that gate is written;
- project conventions, by pointer to the project's `CLAUDE.md` — never restated;
- the enumerated verification checklist (rule 4).

Reviewer brief: the playbook §3 template, plus the phase's design section, plus rules 1–3 and 6 as explicit defect classes to sweep — *"find a gate that would pass against the defect it claims to catch"* is one of the highest-yield instructions in the list.

---

## Closing a phase

1. SHIP verdict from the reviewer.
2. Coordinator's independent spot-check of the actual code and the actual gate output.
3. Design doc updated in the same change if the phase altered any subsystem's behavior. Stale docs mislead every future agent.
4. Report to the maintainer: what shipped, what the gates now prove, every measured-vs-estimated discrepancy, and any deferred item with the phase that will absorb it.

Then, and only then, start the next phase.
