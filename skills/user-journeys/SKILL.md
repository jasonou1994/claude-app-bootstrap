---
name: user-journeys
description: Use when requirements are signed off and nobody has written down who the users are and what they walk through, or when substantial code exists and the question is who it fails to serve. Stage 1b of the app-bootstrap methodology, personas and journeys written blind behind a firewall, mapped against the R-list (greenfield) or the feature surface (brownfield), reviewed adversarially to a plain SHIP, and drawn as one self-contained map the maintainer rules the roadmap from
argument-hint: "[greenfield | brownfield, then the path to the requirements doc or the feature map]"
---

# Stage 1b: User journeys

Write down who uses the product and what each of them walks through, before the product's own shape can tell you. Then hold the product against those walks and count where it serves, where it strains, and where it has nothing.

Shared doctrine: [`../../docs/playbook.md`](../../docs/playbook.md). Read it first; this skill adds to it and never restates it.

**Entry gate:** either a signed-off requirements doc with no code yet (greenfield), or a running product with a feature map, meaning a one-page inventory of what is shipped, in build and planned (brownfield). Section "Two modes" says which you are in.
**Exit gate:** a plain SHIP from the adversarial reviewer on the journeys and the register, then the maintainer reads the map and rules on the roadmap. **This skill never changes the roadmap, the R-list, or a phase plan itself.** It hands the maintainer a counted picture and stops.

---

## Why this stage exists

A product is built by someone, and that someone has a shape: a rating, a volume of data, a device, a way of working. Every requirement they write and every screen they draw fits that shape, because it is the only one they can feel from the inside. Requirements say what must hold. They do not say who is standing in front of the product on a Tuesday evening, what they came for, what they need to see first, and where they give up.

The chess trainer this methodology comes from had thirteen shipped or planned features, a signed-off R-list, six wireframed surfaces, and 105 recorded decisions. When eleven people were written down and walked through it, the feature map served one of them completely: the maintainer. Two of the eleven had no games in the corpus at all, because the ingest rule admitted only the time control the maintainer plays. Five of the eleven could not get through the first run without a terminal. None of this was visible from the requirements, the wireframes, or the code, because all three had been written from the one shape that fit.

The exercise finds this only if the people are written down **before** the product is read. An author who has read the product writes journeys the product serves, and then the mapping pass certifies the product against a description of itself. That circularity is the failure this skill is built to prevent, and the firewall below is the mechanism.

---

## Two modes

The skill runs in one of two modes. Detect it from the repository, or take it from the argument; when told, obey what you are told.

**Greenfield.** Immediately after `product-discovery`, when the requirements doc is signed off and no product exists beyond a skeleton (no running UI, no served API, or only scaffolding). The deliverable is the personas, the journeys, the cross-cutting needs and the core loop, and a gap pass held against the requirements doc's R-list and negotiable baseline instead of a feature surface. Its purpose is to find the people the R-list forgot before a wireframe encodes the omission. Its output feeds the maintainer's ruling on the requirements doc: add an R, add a baseline item, or record a non-goal that names the personas it excludes.

**Brownfield.** When substantial code exists: surfaces a person can reach, a route table, a feature map (or enough code to build one). The deliverable is the three-pass setup below in full: the blind write, the mapping walk against the feature surface with code facts checked read-only, the adversarial review, and the visual map. Its purpose is to find who the shipped product fails and to give the maintainer a counted basis for reordering the roadmap.

Detection rule: if the repository has a running UI or a served API beyond scaffolding, and the maintainer has not said greenfield, it is brownfield. If in doubt, ask; the two modes read different inputs in pass 2 and the author's brief must name the right ones.

Both modes share pass 1 unchanged. The firewall, the persona breadth rule, the required-journeys list and the seven parts do not vary by mode. What varies is what pass 2 opens and what "served" means there.

---

## The three passes and who runs them

1. **Pass 1, the blind write.** One author agent, behind the firewall, writes `journeys.md`: personas, journeys, cross-cutting needs, matrix, core loop.
2. **Pass 2, the mapping walk.** The same author, firewall lifted, writes `gap-register.md`: every step tagged, gaps by theme with severity, journeys nobody completes, a one-page summary, a per-persona scorecard.
3. **Pass 3, the adversarial review.** A fresh reviewer, never behind the firewall, hunts both files by defect class and closes with SHIP or ONE MORE ROUND. Rounds until SHIP, then the map is built.

Fixer is not judge (playbook §1): the author of passes 1 and 2 never reviews them. The pass-3 reviewer is persistent across rounds (playbook §5) and stacks rounds newest-first in `review.md` beside the two files.

Files live in a scratch directory under the project's docs tree during the loop (the chess run used `docs/drive/user-journeys/`), and are promoted on SHIP with the maintainer's say-so (playbook §9).

---

## The firewall

**The rule.** The pass-1 author's reading list is closed. It contains: the brief; a product statement of three to five sentences in plain words; optionally one real user's usage summary, as context for one persona and not as the design; and the non-goals sections only of the requirements docs. Nothing else. Not the project's `CLAUDE.md`, not the design docs, not the wireframes, not the feature map, not the requirements beyond their non-goals, not the code. Pass 2 opens only after pass 1 is saved, and the author records both timestamps.

**Why the non-goals are allowed and the rest is not.** A non-goal tells the author what the product refuses to be, which is a boundary a person can stand outside of and still want something. A requirement or a feature tells the author what the product is, and a person written after reading it wants exactly that. The product statement is allowed for the same reason: it says what the product does at the level a stranger would be told, not how.

**How to hold it in Claude Code.** There are two mechanisms; use the first whenever you can.

- **A clean session outside the project tree.** Claude Code loads instructions from three places: the project's `CLAUDE.md` and the user's project-keyed memory, both found from the working directory and its ancestors; the user-scope `~/.claude/CLAUDE.md`, which loads from any directory; and any enterprise managed-policy file, which also loads everywhere. A subagent launched from inside the project therefore carries the project `CLAUDE.md` in its system prompt whatever the brief says, and that is exactly how the chess run's firewall leaked (finding S1: the vocabulary grep was clean and the shape leaked anyway). Leaving the project tree escapes the first source only. So: create a directory outside the project (the session scratchpad is right), copy the allowed inputs into it, write the brief there with the inputs named by absolute path, and start the pass-1 author from that directory (`cd <clean dir> && claude -p "$(cat brief.md)"`, or an interactive session there). The author saves `journeys.md` into the clean directory; the coordinator moves it into the project afterwards. Pass 2 can then be a continuation of that session with the project paths added, or a fresh in-project agent handed `journeys.md` as ground truth.

  **Probe before pass 1 begins.** The user-scope and managed files are silent: the coordinator follows the recipe, the author reports a clean receipt, and the product is in the system prompt anyway. So, from the clean directory and before the brief is sent, run a probe: `cd <clean dir> && claude -p "List every product, project, codebase or instruction file described anywhere in your context before this message. If there is none, say NONE."` The answer is pasted into the firewall receipt verbatim. If it names the product, or names any instruction file at all, move or empty that file for the duration of pass 1 (`~/.claude/CLAUDE.md` first; a managed-policy file needs the administrator) and re-run the probe until it says NONE. The reviewer replays the probe as part of the breach test.
- **An in-project subagent with a closed list.** When a clean session is not available, launch a fresh general-purpose agent whose brief carries the closed reading list, the instruction not to open any other file, directory, URL or search result, and the instruction to disclose in its report whatever its system context carried about the product. Treat this as a known-leaky firewall: the reviewer's breach test below is mandatory and the coordinator should expect a round 2.

Either way the author's report carries a **firewall receipt**: every file opened in pass 1, the save time of `journeys.md`, the first open time of any pass-2 material, and the disclosure about system context.

**When the firewall leaks (the round-2 remedy).** Words are the weak signal; shape is the strong one. A step can use none of the product's terms and still restate one of its rules. The chess run's clean-grep pass 1 carried "if their move was equally good, it must say so and give full credit" (the maintainer's grading ruling), "the tree of what happens next, one move at a time" (the tree design's one-ply rule), and "paused, not deleted, and come back if the rule widens" (the scope-suspension semantics). No 600-rated beginner asks for any of these unprompted. The remedy, applied in round 2 of that run to twelve steps:

1. The reviewer lists every step beside the excluded sentence it mirrors.
2. The author re-derives each from one question: **would this person say this before seeing the product?** If yes, rewrite it in the person's words (a person says "see what usually happens next", not "one move at a time"). If no, cut it.
3. Every rewritten step is marked `[round 2]` and re-tagged in the register on its new wording, on merit, not on the surface it used to mirror.
4. The reviewer re-runs the question on every rewritten step and reports each as held, moved down, or moved up. Moving up is suspicious; in the chess run nine held, three moved down, none moved up.

---

## Pass 1: the blind write

### Personas: cover the base broadly

At least eight. Each is a page: who they are; what they play or do; how much data they have and how fast it accumulates; what "improving" (or the product's equivalent of getting what they came for) means to them; how much time per week; what they already use instead; what they distrust; what would make them stop.

Breadth is a requirement, not a wish. The set must include:

- **the maintainer's own shape**, as one persona among many, and named as such;
- **an explicit edge case in volume or usage**, at both ends where the product has ends (the chess run had a forty-game beginner and a twenty-thousand-game bullet player);
- **an accessibility persona** with a stated goal of their own beyond operating the product (a screen-reader user who wants to hear the fork coming, not "the same steps, as text");
- **a "studies someone else" persona** where the product allows it (a parent, a coach, a rival's scout); and where it does not, a line saying so and why;
- the person who has **almost no data**, the person **returning after a long absence**, the person who **evaluates before committing**, and the person whose real activity happens **somewhere the product cannot see**.

**The swap test.** Take a persona's variant steps and hand them to a different persona. If nothing has to change, the persona is a label, not a person. The chess run's accessibility persona failed this test in round 1 (five of her variants read "same as the spine, as text"); round 2 gave her the goal she had stated in her own page and her variants stopped being swappable. A persona that exists to carry one feature (the rival-scout carrying "a second person") is allowed if the document says so in as many words.

### Journeys: the required list, written from the person's side

A journey is what one person walks through from a trigger to a feeling of done. It is written from their side, in their words, and it is numbered so pass 2 can tag every step. Every journey has **seven parts**:

1. the trigger;
2. what they want to know or do;
3. what they need to see, in order (these are the numbered steps);
4. the decisions they make;
5. where they get stuck or bored;
6. what "done" feels like;
7. what happens tomorrow and next week.

Each journey has a **spine** of steps written for the persona it fits most naturally (`J3.1`, `J3.2`, ...), then **per-persona variants** where a persona's steps differ (`J3.P6.1`, ...), and an explicit **does not apply** line for each persona it does not fit. A persona with no variant and no does-not-apply line is a persona the author forgot.

The required journeys, generalised from the chess run. Write each for every persona it applies to, and say when it does not:

1. **First run** and the wait for the product to have something to show.
2. **The daily loop**: the sitting the product lives on.
3. **Right after the triggering event**: the moment in the person's life that sends them to the product (a lost game, a failed deploy, a bad night's sleep).
4. **The core question the product answers** ("where do I go wrong in my openings", "why is this slow", "what am I spending on").
5. **A periodic look back**: the week, the month.
6. **Asking about one item**: a single position, transaction, incident.
7. **Asking about a pattern**: a recurring habit across many items.
8. **Practising one branch to a chosen depth**: taking one part of the space and working it until it is known.
9. **Connecting an agent** of their own, where the product exposes one.
10. **Returning after absence.**
11. **Plateau and frustration.**
12. **On a phone**, in a place with no desk and little time.
13. **An item they want ignored**: the game that was a misclick, the transaction that was a refund.
14. **Sharing a finding** with a coach, a colleague, a friend.
15. **Changing what counts**: only recent items, only one category, only one account.
16. **The day the product is wrong** about something, and what the person can do about it.

Then add every journey the personas need that this list lacks, and say **which persona demanded it**. A journey nobody demanded is a feature in disguise. The chess run added eleven this way in pass 1 (bringing in games the product cannot see, the parent's view, studying another player, "am I improving over months", the five-minute version, playing it out, privacy and deletion, two accounts one person, trying before committing, and two more) and four in round 2 at the reviewer's finding (the game they won but were losing; the day the numbers changed after an update; the ten minutes before tonight's game; a concept question with no item behind it).

### Cross-cutting needs, the matrix, the core loop

After the journeys, three short sections:

- **Cross-cutting needs** the journeys reveal: how each person checks a claim (trust); their time budget; what motivates and what shames; what they never want to see; what they would pay for.
- **A journeys-by-persona matrix**: rows are journeys, columns personas, cells Y (needs it), V (needs it in a variant form), N (does not apply).
- **The core loop, per persona**: the two or three journeys the product lives or dies on for that person, with the reason argued from the person and not from the product's navigation. The chess run's closing line originally read "across all eleven, the shared spine is first run, then daily, then after a loss", which was the app's nav order restated as a universal and contradicted two of its own persona entries; the reviewer fixed it.

### Register for pass 1

Plain prose, the person's words. No em dashes. No product jargon: the brief lists the product's surface names and internal terms, and the author greps for them before saving. Ordinary English uses of a word that is also a product term ("lines" in "a few lines of explanation") are allowed and are justified in the report.

---

## Pass 2: the mapping walk

Only after `journeys.md` is saved. Now the author opens the product.

**What is opened, by mode.** Greenfield: the requirements doc in full (R-list, baseline, decisions log, non-goals). Brownfield: the wireframe artifact, the feature map, the project's product-concept summary, the requirements docs in full, and read-only greps of the code for facts. If no feature map exists, the coordinator writes one first: a one-page inventory of what is shipped, in build, and planned, with the version and the date, built from the code and the phase plan rather than from memory.

**The tagging vocabulary.** Walk every numbered step and give it exactly one tag:

- **served**: name what serves it (brownfield: the surface; greenfield: the R or baseline item by id).
- **served in part**: one half of the step is served and the other half is not; say which.
- **awkward**: name what serves it and say why the step is harder than it should be for this person.
- **missing**: nothing serves it; say what would, in the person's terms, without designing it. A qualifier may follow (`missing; planned`, `missing today; in build`) when the feature map already carries something that would serve it; it still counts as missing today.
- **does not apply**: the journey's own text says this step is not this persona's. The generator also reads `n/a` as a spelling of this tag and counts it here.

Five tags, no others. The map generator refuses a row whose tag is outside this vocabulary, so a tag invented in the walk ("served for a developer", "served in design") stops the map instead of leaking into a count. The chess run's round 1 used five undeclared tags; the reviewer found them and the legend was extended, which is why the vocabulary is closed here.

**Severity, per gap.** After the walk, group the missing and awkward rows into gaps by theme (`G<theme>.<n>`). Each gap names the personas it hits, the journeys it breaks (by step id), and one severity:

- **blocks**: the persona cannot run their core loop;
- **degrades**: they can, but it costs trust or time;
- **nice**: everything else.

Severity is per persona, and one gap can block one persona and degrade another. Say which. The chess run's round 1 put four personas in the wrong column because it argued severity from the gap rather than from each persona's own page (a returning player whose old games were on a different account was "blocked" by a missing date axis he did not need; a screen-reader user who runs engines from the command line was "blocked" by a CLI-only setup).

**What "served" means in greenfield.** A step is served when an R or a baseline item commits the product to it, by id. A step is awkward when a non-goal or a baseline item serves it in a way that is harder for this person than their need. A step is missing when no requirement mentions it. The register in this mode is a list of the people the R-list has not yet considered, and it ends in the maintainer's ruling on the requirements doc, not in a phase plan.

**Code facts in brownfield.** Every fact the walk relies on ("only rated rapid enters the corpus", "one username", "no export") carries a `file:line` and the time it was checked. Facts invert: in the chess run the register's headline fact, "no game exclusion exists anywhere", was true at 19:43 and false by 19:47, because another loop's author landed the feature in the working tree between the grep and the save. State the time, and let the reviewer re-grep.

**The register's parts.** (A) the tagged walk, one table per journey; (B) the gap register by theme; (C) the journeys no persona can complete today, plus a per-persona scorecard (door: can they get through first run at all, and which gap decides it; past the door: journeys complete, degraded, blocked); (D) a one-page summary, "what the surface is missing" in brownfield and "what the requirements are missing" in greenfield, that also names what the surface (or the R-list) does well, so the reader is not left thinking nothing works. Do not propose phases or designs; that is the maintainer's ruling after the map.

---

## Pass 3: the adversarial review

A fresh reviewer, briefed per playbook §3 with the premise that both documents contain defects. The reviewer is not behind the firewall; it reads everything the author was forbidden, because its first job is to check whether the author really was forbidden.

**Defect classes to sweep, with a receipt per class:**

1. **Invented feature-justifying steps.** A step no person would state, present because it justifies a tool the product has or wants ("show the engine's top three moves before I answer" exists to justify a multi-line search; nobody wants the answer key first). Receipt: each such step with the feature it serves.
2. **Firewall breach.** Two tests, both mandatory. The **vocabulary grep** for the product's terms over `journeys.md`. The **mirror test**: read the excluded documents (the project's instructions file, the requirements beyond non-goals, the design summaries) and list every pass-1 step beside the sentence it restates. A clean grep with mirrored shapes is a breach. Receipt: the side-by-side list, or "swept, none found" with the documents read.
3. **Missing journeys.** Journeys a persona's own page demands and the list lacks; the usual cause is one trigger absorbing its neighbours (in the chess run "after losing" absorbed "after a win that was a loss", and "the daily sitting" absorbed "the ten minutes before tonight's game"). Receipt: candidates with the persona's words, each kept, folded into a variant, or rejected.
4. **Missing or thin personas.** The breadth list above, and the swap test on every persona. Receipt: the swap result per persona.
5. **Over-fit to the existing surface** (brownfield only). Steps tagged served because they were written to be served; tags that lean on planned surfaces; tags inconsistent within one persona (the same person "served" by a screen in one journey and "cannot reach it" in the next). Receipt: each retag with its reason. In greenfield there is no surface; the class is recorded as not applicable and the over-fit question moves to class 2 (a step that mirrors an R is a breach, not an over-fit).
6. **Mis-tagged steps re-judged against code facts** (brownfield only). Every code fact in the register re-grepped by the reviewer with `file:line`; every tag that rests on a false fact retagged. Receipt: a facts table, held or failed, per fact. In greenfield the equivalent is re-judging every served tag against the R or baseline item it cites, by id, which class 9 carries.
7. **Severity errors.** Every blocks and degrades re-argued from the persona's own page. Receipt: a recomputation table.
8. **The core loop argued from the product** rather than the person.
9. **Summary completeness and gap-register arithmetic.** Every gap in the register that a persona is blocked by appears in the one-page summary; the scorecard's counts match the walk; the numbers of personas, journeys, steps and gaps stated anywhere in the documents equal the numbers counted from the files. Receipt: the counts, recomputed.
10. **Voice.** Em dashes, product jargon in pass 1, a rule's internal name used as copy.

**Authority.** Wording-level defects, mis-citations and a tag that contradicts its own note are fixed in place, each marked `[pass 3]`, and listed in the review. Structural defects (a breached step, a missing persona or journey, a wrong severity, a false fact that moves a tag) go back to the author with the required disposition. The reviewer recomputes the scorecard itself and presents it; the author adopts it or argues a row with the persona's words beside it.

**Rounds.** Newest-first in one `review.md` (playbook §5, §9). Round 2 verifies each disposition against the revised text, re-runs the firewall question on every `[round 2]` step, attacks every new journey for invention, and closes with a plain SHIP or ONE MORE ROUND. The chess run took two rounds: round 1 found four structural classes open (a breached firewall, a false headline fact, four wrong severities, five demanded journeys) and round 2 found one tag contradicting its own note, fixed in place, and shipped.

---

## The map

After SHIP, one self-contained HTML page that a maintainer can read in five minutes and rule from. Its structure: a **persona strip** (id, name, one line, core loop); a **journeys-by-persona grid** with one cell per journey and column (spine, then each persona), each step a dot coloured served, served in part, awkward, missing, or does not apply, with the steps readable on click or focus; the **gap register, blocks first**, each gap with its personas, journeys and theme; the one-page summary; and a **footer stating the count method**.

**Every number on the map is counted from the register. None is typed.** The template [`assets/journey-map-template.html`](assets/journey-map-template.html) is filled by [`assets/build-map.py`](assets/build-map.py), which parses `journeys.md` and `gap-register.md`, counts rows, and fails loudly on a duplicate step id, a tag outside the vocabulary (including any text after a tag other than `; planned` or `; in build` on a missing row), a malformed walk row, a gap naming no persona or journey, a journey in the walk with no heading in the journeys file, or a journey heading with no walk rows that the register has not declared `Not walked`. The page has no external scripts, styles, fonts or images, renders in light and dark, and needs no server. Build it with:

```
# brownfield
python3 <skill dir>/assets/build-map.py --mode brownfield \
    --journeys journeys.md --register gap-register.md \
    --template <skill dir>/assets/journey-map-template.html --out journey-map.html \
    --title "<Product> journey map" --summary-heading "What the feature map is missing"

# greenfield: the walk was against the R-list, and the page must say so
python3 <skill dir>/assets/build-map.py --mode greenfield \
    --journeys journeys.md --register gap-register.md \
    --template <skill dir>/assets/journey-map-template.html --out journey-map.html \
    --title "<Product> journey map" \
    --intro "<n> people, <m> journeys, every step held against the signed-off requirements. The person's words throughout." \
    --summary-heading "What the requirements are missing"
```

`--mode` sets the intro and summary-heading defaults ("against what exists today" and "What the surface is missing" for brownfield; "against the signed-off requirements" and "What the requirements are missing" for greenfield); the flags override them. Each dot on the grid carries a shape as well as a colour (filled circle, half circle, diamond, square, hollow circle), so the map reads without colour vision.

The generator prints the counts it used; the coordinator checks them against the register by hand (`grep -c` on the walk rows and the gap lines) before showing the map to anyone. If the documents do not parse, fix the documents to the formats below; never patch numbers into the page.

### File formats the generator reads

`journeys.md`: `## Part A` with persona headings `### P<n>: <Name>, <one-line descriptor>` (the name ends at the first comma followed by a lowercase word or a number, so "Priya Raman, Jr., a 1900 club player" keeps the suffix in the name); `## Part B` with journey headings `### J<n>: <Title>` (an optional `(demanded by ...)` or `[round n]` suffix is stripped); `## Part C` cross-cutting needs; `## Part D` the matrix; `## Part E` the core loop with one line per persona, `- **P<n> <Name>.** <first sentence names the journey ids>.`

`gap-register.md`: `## Part A` the walk, one table per journey with rows `| <step id> | <tag> | <note> |` (spaces around the pipes optional; any line beginning with a pipe and a J id is a row and must have exactly three cells) where the step id is `J<n>.<k>` (spine) or `J<n>.P<m>.<k>` (variant), optionally with a trailing letter for a step added in review; a journey heading with no walk rows stops the generator unless Part A carries a `Not walked: J<n>, J<m> (reason)` line naming it; `## Part B` with `### Theme <n>: <name>` headings and gaps `- **G<n>.<m> <Title>.** <body>` whose body names the personas (`P<m>`), the steps (`J<n>...`) and one bold severity (`**Blocks**`, `**Degrades**`, `**Nice**`); `## Part C` journeys nobody completes and the scorecard; `## Part D` the one-page summary as `**<n>. <title>**` items.

---

## Exit

1. **SHIP from the reviewer**, plain, with accepted residue enumerated.
2. **The coordinator spot-checks** the two documents and the map itself: open the map, pick three cells and three gaps, and read them against the register; re-run the counts; grep both files for em dashes and the product's terms.
3. **The maintainer reads the map and rules on the roadmap.** Present the blocks-first register and the scorecard; propose nothing about phases in this stage's documents. The maintainer's rulings are recorded where the project records decisions (greenfield: in the requirements doc's decisions log, as added Rs, baseline items, or non-goals naming the excluded personas; brownfield: in the project's decision table), by whoever numbers decisions there, never by this loop's agents.
4. **Promote** the three documents and the map into the project's docs tree and index them from the project's `CLAUDE.md`, asking first (playbook §9). Then: greenfield proceeds to Stage 2 (wireframes), whose entry gate names `journeys.md`, `gap-register.md` and the map as inputs when they exist, so the personas' first runs, empty states and error paths get drawn; brownfield returns to the design or implementation loops the maintainer reordered.

---

## Worked example: the chess run, 2026-09-04

Brownfield. Product: a trainer over a player's own online games, engine-found mistakes drilled by spaced repetition and explained by a coach whose numbers come from the engine. One author on Fable for passes 1 and 2, one reviewer on Fable for pass 3, the coordinator building the map.

- **Pass 1** (16 minutes of writing, four saves, firewall receipt with timestamps): **11 personas** (a 600-rated beginner with forty games on a phone; a blitz-only casual; the maintainer's 1487-rapid, one-system, 5,866-game shape; a 1900 club player with a coach; a returner after ten years; a 20,000-game bullet player; a nine-year-old and his mother; a near-titled player giving it fifteen minutes; an over-the-board player whose games are on paper; a player scouting a rival; a low-vision player on a screen reader), the 16 required journeys and 11 demanded ones, cross-cutting needs, matrix, core loop.
- **Pass 2**: the walk, 37 gaps in nine themes (43 after round 2 added six at the reviewer's finding), the journeys nobody completes, an eight-item summary (twelve after round 2), a scorecard.
- **Pass 3, round 1: ONE MORE ROUND.** S1 the firewall had leaked through the project's `CLAUDE.md` in the author's system prompt (clean grep, twelve mirrored steps); S2 the register's headline code fact had inverted between grep and save; S3 four personas in the wrong severity column; S4 five demanded journeys missing; S5 two personas failing the swap test; S6 five invented steps. Eighteen facts re-grepped, thirteen held. Wording fixed in place, marked `[pass 3]`.
- **Round 2: SHIP.** Twelve steps re-derived and marked `[round 2]` (nine tags held, three moved down, none up); **31 journeys** after J28 to J31; the accessibility persona given her own goal; one tag found contradicting its own note, fixed in place.
- **The map**: **425 tagged steps** (62 served, 8 served in part, 94 awkward, 236 missing including planned or in build, 25 does not apply), **43 gaps** (14 block, 25 degrade, 4 nice), every number counted by the generator from the register and stated as such in the footer. That run shipped with two rows still outside the vocabulary (`served for a developer`, a bare `planned`), carried by a hand-extended legend; the generator here refuses both, and reproducing these counts from that register first requires retagging those two rows to `served in part` and `missing; planned`. Closing the vocabulary is the change that run argued for.
- **What the maintainer learned from it**: the feature map served one persona of eleven; two personas had an empty corpus by rule; five could not pass the first run without a terminal; one journey was completable end to end by one persona. The roadmap ruling that followed was the maintainer's, made from the map, and is recorded in the project's decision table, not in the journeys documents.

---

## Verification checklists

Every agent this skill briefs ends with an enumerated checklist and does not finish until it has re-read its own output and confirmed every item (playbook §4). The three lists below are the minimum; [`assets/brief-template.md`](assets/brief-template.md) carries them in brief form.

**Author, passes 1 and 2.**

1. Pass 1 saved before any pass-2 material was opened; both timestamps and every pass-1 file opened are in the report.
2. Firewall receipt discloses what the session's system context carried about the product.
3. At least eight personas with every field; the maintainer's shape, an explicit edge case, an accessibility persona with her own goal, and a "studies someone else" persona (or the line saying why not) are present.
4. Every persona passes the swap test or is declared a feature wearing a name.
5. Every required journey present with the seven parts, a variant or a does-not-apply line per persona; every added journey names its demanding persona.
6. Vocabulary grep on `journeys.md` is zero, or each hit is justified as ordinary English.
6a. Every step was re-read before saving against "would this person say this before seeing the product?", and every step that survives only because of something the author already knew is marked in the report.
7. Matrix complete; core loop argued from the persona, two or three journeys each.
8. Every step tagged with one of the five tags and nothing else; every missing or awkward row says what would serve it in the person's terms.
9. Every gap cites step ids, personas, journeys and one severity per persona; the scorecard matches the walk.
10. Brownfield: every code fact carries `file:line` and a check time. Greenfield: every served tag names an R or baseline id.
11. Zero em dashes; no product file modified; no commit.

**Reviewer, pass 3.**

1. A receipt per defect class: ten in brownfield; eight in greenfield, with classes 5 and 6 recorded as not applicable and every served tag re-judged against its cited R or baseline id under class 9.
2. The firewall breach test run both ways (vocabulary grep and the mirror test against the excluded documents), with the side-by-side list, and the clean-directory probe replayed.
3. Every finding cites an id; every retag or severity change cites a `file:line` or a requirement id.
4. The scorecard recomputed, not adopted.
5. In-place edits all marked `[pass 3]` and listed; no product code touched; no commit.
6. Verdict exactly SHIP or ONE MORE ROUND, accepted residue enumerated.
7. Zero em dashes in the review.

**Coordinator, before the maintainer sees anything.**

1. The pass-1 author ran from a clean directory, or the in-project fallback was declared and the breach test was run.
2. The reviewer's verdict is a plain SHIP.
3. The map was built by the generator, its printed counts match `grep -c` on the register, and no number on the page was typed.
4. Three cells and three gaps on the map read correctly against the register.
5. The documents propose no phases and no designs; the roadmap ruling is left to the maintainer.
6. Promotion and indexing were asked about, not assumed.

---

Write the people down before the product can, hold the product against them, count what you find, and let the maintainer rule from the count.
