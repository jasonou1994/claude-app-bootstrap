# User journeys: briefs for the three passes

Copy the parts you need into the agents' briefs. Angle brackets mark what the coordinator
fills in. Before writing Brief A, seed it: list eight to twelve concrete candidate persona
shapes for THIS product (the chess run's read "a 600-rated beginner with 40 games; a 1000
casual blitz-only player; ... a player who wants to study a friend or rival"), and say in the
brief that they are candidates and not a ceiling. The breadth the chess run got came from that
seeded list, not from the abstract categories alone. Keep the rules by pointer to `SKILL.md`; restate only what an agent cannot read
(the closed reading list, the product statement, the paths). The two briefs below are the
pass-1-and-2 author's and the pass-3 reviewer's. A round-2 brief for the author follows.

---

## Brief A: the author (pass 1 blind, then pass 2 mapping)

Written <date> by the coordinator. Mode: <greenfield | brownfield>. You write two files in
order. Pass 1 is written behind a firewall; pass 2 opens the product. Nothing from pass 2 may
be started before pass 1 is saved.

### The firewall (pass 1)

In pass 1 you may read ONLY the items on this list. Do not open any other file, directory,
URL, or tool output, and do not search the repository. If a fact you want is not on the list,
write the journey without it and note the want.

1. This brief.
2. The product statement below.
3. <the one real user's usage summary, if one exists, as context for ONE persona, not as the
   design; path>
4. <greenfield: the non-goals section of the requirements doc, path and section; brownfield:
   the non-goals sections only of each requirements doc, paths and sections>

Do NOT open: <the project's CLAUDE.md, HANDOFF, design docs, wireframes, the feature map, the
requirements docs beyond their non-goals, any code>. You are writing what people need, not
what the product has. If you find yourself using the product's own vocabulary (<list the
product's surface names and internal terms here, e.g. Today, Lines, Patterns, funnel, scope,
card>) stop and write the person's word instead.

If your session's system context carries anything about this product beyond this brief (a
project instructions file, a user-scope instructions file, memory notes), say so in your report
under "Firewall receipt", and do not consult it while writing pass 1. The coordinator's probe
answer (`SKILL.md`, "Probe before pass 1 begins") is pasted here: <probe answer>.

**Product statement.** <three to five sentences, in plain words, no surface names: what it
pulls in, what it finds, how it groups, what it drills, what it explains, who runs it and
where. Say who the single user is if there is one and whether other people or agents can
connect.>

### Pass 1 deliverable: `<path>/journeys.md`

Follow `SKILL.md` "Pass 1: the blind write" for the content rules: persona breadth, the seven
parts of a journey, the required-journeys list, cross-cutting needs, the matrix and the core
loop. Follow "File formats the generator reads" for the headings and id scheme exactly; the
map is built from them mechanically.

Register: plain prose, the person's words, no em dashes, no product jargon.

### Pass 2 deliverable: `<path>/gap-register.md`

Only after pass 1 is written and saved (record the save time), read: <greenfield: the
requirements doc in full (R-list, baseline, decisions log); brownfield: the wireframe artifact
<URL or path>, the feature map <path>, the project's product concepts <path and section>, the
requirements docs in full <paths>, and read-only greps of the code for facts>. Then walk every
numbered step of every journey and tag it with the vocabulary in `SKILL.md` "Pass 2: the
mapping walk". Produce the register's four parts (the tagged walk; the gap register by theme
with personas, journeys and severity per gap; the journeys no persona can complete; the
one-page summary) plus the per-persona scorecard. Do not propose phases or designs.

Brownfield only: every code fact you rely on carries a `file:line` and the time you checked
it; a fact can invert between your grep and your save when other loops are writing.

### Verification checklist (re-read your output; return it filled in, PASS plus one line each)

1. Pass 1 was written and saved before any pass-2 material was opened; the report states both
   timestamps and lists every file opened in pass 1.
2. The firewall receipt states what the session's system context carried about the product.
3. At least eight personas, each with every field in `SKILL.md`; the maintainer's shape, an
   explicit volume or usage edge case, an accessibility persona with a goal of their own beyond
   operating the product, and (where the product allows)
   a "studies someone else" persona are present and named.
4. Every persona survives the swap test as `SKILL.md` defines it, or is declared a feature
   wearing a name with the reason.
5. Every required journey is present, numbered, with the seven parts, with a persona variant
   or an explicit "does not apply" line for every persona; every added journey names the
   persona that demanded it.
6. The vocabulary grep on `journeys.md` for <the product's terms> returns zero hits, or each
   hit is justified as ordinary English in the report; and every step was re-read before
   saving against "would this person say this before seeing the product?", with the steps
   that survive only because of something you already knew marked in the report.
7. The matrix covers every journey and every persona; the core-loop section names two or
   three journeys per persona with a reason argued from the persona.
8. Pass 2 tags every numbered step with one of the five tags; no row carries a tag outside
   the vocabulary; every "missing" and "awkward" row says, in the person's terms, what would
   serve it.
9. Every gap cites step ids, names the personas it hits, the journeys it breaks, and one
   severity; the scorecard's per-persona counts are consistent with the walk.
10. Brownfield: every code fact carries `file:line` and a check time. Greenfield: every
    "served" tag names the R or baseline item that serves it.
11. Zero em dashes in both files; no product file modified; no commit.

---

## Brief B: the adversarial reviewer (pass 3)

Written <date> by the coordinator. Playbook §3 applies in full; this brief adds the defect
classes and the authority rule for this stage. Both documents contain defects; find them.

Inputs: Brief A above; `<path>/journeys.md`; `<path>/gap-register.md`; everything the author
was allowed in pass 2, plus the project's instructions file and design docs (you are NOT
behind the firewall; you are checking whether the author was); read-only access to the code.

Sweep every defect class in `SKILL.md` "Pass 3: the adversarial review" and return a receipt
per class. Authority: wording-level defects and mis-citations you fix in place, each marked
`[pass 3]`; structural defects (a breached firewall, a missing persona or journey, a wrong
severity, a false code fact that moves a tag) go back to the author as findings with the
required disposition. Recompute the scorecard yourself and present it; do not adopt the
author's.

Round 2 and later: verify every disposition against the revised text; re-run the firewall test
on every rewritten step and report held, moved down, or moved up; attack every new journey for
invention; close with a plain SHIP or ONE MORE ROUND.

### Verification checklist (return it filled in)

1. A receipt per defect class: ten in brownfield, eight in greenfield (classes 5 and 6 recorded
   as not applicable, every served tag re-judged against its cited R or baseline id): what was
   checked, what was found, or "swept, none found" with the evidence examined.
2. The firewall breach test was run as `SKILL.md` describes (vocabulary grep AND the mirror
   test against the excluded documents AND the clean-directory probe replayed), with the
   mirrored steps listed side by side.
3. Every finding cites a persona, journey, step, or gap id, and every corrected tag or
   severity cites a code fact with `file:line` or a requirements item by id.
4. The scorecard is recomputed, not copied.
5. Edits in place are all marked `[pass 3]` and listed; no product code touched; no commit.
6. The verdict is exactly SHIP or ONE MORE ROUND, with accepted residue enumerated.
7. Zero em dashes in the review file.

---

## Brief C: the author's round 2 (after ONE MORE ROUND)

The reviewer's findings are at `<path>/review.md`, newest round first. Structural findings
<S-ids> are binding. For every step the reviewer names as product-shaped, apply the leak remedy
in `SKILL.md` "When the firewall leaks": re-derive from the question "would this person say
this before seeing the product?", rewrite in the person's words or cut it, mark it
`[round 2]`, and re-tag it in the register on the new wording, on merit. Add the journeys and
variants the reviewer's persona-demanded list names. Adopt the reviewer's recomputed
severities and scorecard, or argue a severity with the persona's own words beside it.
Discretion: <which fix shapes are the author's call>. Return Brief A's checklist filled in
again, plus the list of every `[round 2]` id.
