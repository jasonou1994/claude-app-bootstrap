# user-journeys skill: adversarial review

Rounds newest-first. Reviewer: adversarial, briefed on the premise that the work contains defects.
Target: `skills/user-journeys/` (SKILL.md, `assets/brief-template.md`, `assets/journey-map-template.html`,
`assets/build-map.py`) plus playbook §11, README and both manifests at 0.3.0. Nothing committed.

---

# Round 1 (2026-09-05)

## Verdict: ONE MORE ROUND

Five structural defects. Four of them are in the generator, and they matter more than their
count suggests, because the generator is the whole honesty claim of this skill: SKILL.md's
"Every number on the map is counted from the register. None is typed" is load-bearing, and
`build-map.py`'s own docstring promises it "fails loudly on anything it cannot parse, because a
silently skipped row is a wrong number on the page." Three input shapes make it fail quietly
instead, each producing a wrong number on the page with exit 0. The fifth is that Stage 1b is
announced as a pipeline stage that no downstream skill has heard of.

What is genuinely good, stated so the findings are read in proportion: the firewall's primary
mechanism works, and I verified it by running it rather than by reading about it. The three
required injections all fail loudly. The map renders correctly in both themes with zero external
resources. The register is clean. The worked example's numbers are real and I reproduced all of
them.

---

## Part A: Structural findings (back to the author)

### S1. The generator silently drops a journey that pass 2 forgot to tag. BLOCKER. CONFIRMED.

`build-map.py:190-195` checks the walk against the journey headings in one direction only: it
dies on walk rows whose journey has no heading (`unknown_j`), and on walk rows naming an unknown
persona (`unknown_p`). It never checks the converse, so a journey with a heading in `journeys.md`
and zero rows in the register passes.

Receipt. Working from copies of the chess `journeys.md` and `gap-register.md`, I deleted every
J31 walk row (15 rows) and reran:

```
J31 walk rows before: 15
J31 walk rows after: 0
personas 11 journeys 31 steps 410 totals {"served": 61, "part": 7, "awkward": 88, "missing": 234, "na": 20} gaps 43 ({"blocks": 14, "degrades": 25, "nice": 4}) summary 12 -> o.html
EXIT=0
```

"journeys 31" is still printed. The map draws J31 as a row of empty cells, which is
indistinguishable from a journey that legitimately has no persona variants, and eleven such rows
(J17 to J27) appear on the real chess map, so the tell is invisible by construction. Every count
on the page is now wrong and the page still says "Nothing here is estimated."

This is the exact omission pass 3 defect class 9 and author checklist item 8 exist to catch, and
the coordinator's prescribed second count does not catch it either: SKILL.md:208 has the
coordinator check the generator's counts with `grep -c` on the walk rows, and both counts agree
at 410 because both are counting the same surviving rows. An untagged journey is the single most
likely pass-2 error, since the author tags 425 rows by hand across 31 tables.

Disposition: add the converse check. A journey heading with no walk rows is a hard error unless
the register declares it (for example a `## Part A` line naming journeys deliberately not walked).

### S2. A semicolon defeats the closed tag vocabulary. BLOCKER. CONFIRMED.

`TAG_RE` at `build-map.py:41` accepts a qualifier group `([;:(\[].*)?` after the tag and discards
it. The qualifier exists for the sanctioned `missing; planned` and `missing today; in build`
(SKILL.md:152), but it accepts *any* text, including a second tag or the invented tag the
vocabulary was closed to stop.

Receipt. I injected the chess run's own off-vocabulary tag, respelled with a semicolon:

```
INJECTED: | J9.P7.1 | served; for a developer | No way to lock it off; every endpoint
personas 11 journeys 31 steps 425 totals {"served": 63, "part": 8, "awkward": 94, "missing": 235, "na": 25} gaps 43 ... EXIT=0
```

served went 62 to 63, missing 236 to 235, exit 0. A step nothing serves is now counted as served.
And two tags at once passes the same way:

```
INJECTED: | J9.P7.1 | served; awkward | No way to lock it off; every endpoint is open on l
personas 11 journeys 31 steps 425 totals {"served": 63, ... "missing": 235, ...} EXIT=0
```

This directly falsifies SKILL.md:155: "The map generator refuses a row whose tag is outside this
vocabulary, so a tag invented in the walk ('served for a developer', 'served in design') stops the
map instead of leaking into a count." The bare spelling is refused (I confirmed that below, S6);
the semicolon spelling leaks into the count, and a semicolon is the punctuation the skill itself
taught the author to reach for.

Disposition: allow only the qualifiers the vocabulary sanctions. Whitelist the qualifier for
`missing` and `missing today`, and reject a qualifier on `served`, `served in part`, `awkward` and
`does not apply` outright, or at minimum reject any qualifier that itself begins with a
vocabulary word.

### S3. A walk row written without spaces around the pipes is silently skipped. MAJOR. CONFIRMED.

The row regex at `build-map.py:97` requires exactly `^| ` and ` | ` separators. Markdown does not,
and neither does any renderer. A row written `|J9.1|missing|note|` is not a parse failure, it is
simply not matched, so it vanishes from the count.

Receipt. I removed the spaces from three real rows:

```
INJECTED: |J9.1|missing|Re-derived: "I do not want it messing with my exercises
INJECTED: |J9.2|missing today; planned|The `/mcp` endpoint is shipped (G-MCP-1,
INJECTED: |J9.3|missing today; planned|Audit page and "answered via agent" marke
personas 11 journeys 31 steps 422 totals {"served": 62, "part": 8, "awkward": 94, "missing": 233, "na": 25} gaps 43 ... EXIT=0
```

425 steps became 422, exit 0, no warning. Unlike S1 this one *is* caught by the coordinator's
independent `grep -c`, which is the system working. But the module docstring's contract is that
the generator itself fails loudly, and here it does not; and an author who reformats one table
loses rows with no signal at the point of the error.

Disposition: match rows on a tolerant pipe split and then validate, so an unparseable row is an
error rather than a non-match. A cheap equivalent: count all lines matching `^\s*\|\s*J\d` and die
if that count differs from the number of rows parsed.

### S4. Stage 1b feeds nothing downstream by name. MAJOR. CONFIRMED.

SKILL.md:223 states the greenfield hand-off as fact: "greenfield proceeds to Stage 2 (wireframes),
which now has personas to draw for." The wireframes skill has never heard of it. Receipt:

```
$ grep -niE 'journey|persona|stage 1b|user-journeys' skills/wireframes/SKILL.md
(no output)
```

and its entry gate is unchanged at `skills/wireframes/SKILL.md:13`: "**Entry gate:** the Stage 1
requirements doc is signed off." A maintainer who runs `/app-bootstrap:wireframes` after Stage 1b
is told to draw from the requirements doc and is never told the personas and the journey map
exist. In greenfield mode, where the register's only product is "the people the R-list has not yet
considered" (SKILL.md:165), the wireframe stage is the first place that finding can bite, and the
wiring is absent.

This is a real tension with the constraint that no other skill be modified, so it needs a ruling
rather than a silent fix. Disposition, author's choice with the maintainer: either add the journey
map to the wireframes entry gate as an optional input (a one-line change to
`skills/wireframes/SKILL.md:13` plus a sentence saying to draw the personas' first-run and
error paths), or downgrade SKILL.md:223 to state honestly that the hand-off is the maintainer's to
carry, because no downstream skill reads these documents. I recommend the first. The second leaves
the plugin claiming a stage whose output has no consumer.

### S5. The greenfield mode does not survive its own defect classes. MAJOR. CONFIRMED.

Walking the skill as if invoked the day after `product-discovery` on a repo with only a
requirements doc, the inputs do exist and the mapping rule is real. Specifically, and to the
skill's credit, the firewall's one substantive greenfield input is guaranteed: `product-discovery`
mandates non-goals both as doctrine ("**Name the thing you are not building.** Explicit non-goals
are requirements. Write them down.", `skills/product-discovery/SKILL.md:21`) and as a numbered
section of the deliverable (`:59`, "4. Non-goals."). Pass 2 tags against the R-list and baseline by
id, which SKILL.md:165 defines properly. That much is not a paragraph, it is a mode.

Three places still assume a product exists.

1. **Pass 3 classes 5 and 6 are brownfield-only, with no exemption.** Class 6 (SKILL.md:184) is
   "Every code fact in the register re-grepped by the reviewer with `file:line`"; class 5 (`:183`)
   is "Over-fit to the existing surface", judged on "tags that lean on planned surfaces". In
   greenfield there is neither code nor surface. Yet the reviewer's checklist item 1 (`:260`)
   demands "A receipt per defect class, ten classes" with no mode split, while the *author's*
   checklist item 10 (`:255`) does split cleanly by mode. A greenfield reviewer must either write
   two empty receipts against a checklist that says ten, or invent them.
2. **The generator's defaults are brownfield-worded and there is no greenfield invocation.**
   `build-map.py:177` defaults `--summary-heading` to "What the surface is missing", and the
   default `--intro` at `:245` hardcodes "against what exists today". The only invocation the skill
   shows (SKILL.md:203-206) passes the brownfield heading "What the feature map is missing". A
   greenfield run maps against a requirements list, not a surface, and the page will say otherwise
   unless the coordinator notices and overrides two flags.
3. **The register's Part D is specified in surface terms**: SKILL.md:169, "a one-page 'what the
   surface is missing' summary that also names what the surface does well." There is no surface.

Disposition: mark classes 5 and 6 brownfield-only and say so in the reviewer checklist; add the
greenfield invocation with both flags set; give Part D its greenfield wording.

---

## Part B: Wording defects fixed in place

All four are marked here and applied to the working tree. None is structural.

**W1. The worked example's counts are not reproducible from the register it cites.** MINOR.
CONFIRMED. SKILL.md's worked example presented "425 tagged steps (62 served, 8 served in part, 94
awkward, 236 missing ..., 25 does not apply), 43 gaps (14 block, 25 degrade, 4 nice), every number
counted by the generator from the register". Run against the shipped chess register, the shipped
generator dies:

```
build-map: row J9.P3.1 carries a tag outside the vocabulary: 'served for a developer'
EXIT=1
```

The chess register carries two rows the closed vocabulary now refuses,
`gap-register.md:330` (`served for a developer`) and `:335` (a bare `planned`), and the shipped
chess map absorbed them with a hand-extended legend, its footer reading "'served for a developer'
count as served in part". Retagging exactly those two rows, everything reproduces:

```
personas 11 journeys 31 steps 425 totals {"served": 62, "part": 8, "awkward": 94, "missing": 236, "na": 25} gaps 43 ({"blocks": 14, "degrades": 25, "nice": 4}) summary 12 -> out.html
EXIT=0
```

So the generator is honest and the numbers are real; the claim that they came out of *this*
generator was not. Fixed in place: the worked example now states the two rows, the retagging
needed to reproduce, and that closing the vocabulary is the change that run argued for.

**W2. The generator accepts a tag the skill does not sanction.** MINOR. CONFIRMED.
`build-map.py:26,41,43` read `n/a` as a spelling of "does not apply", and 25 rows of the chess
register use it, but `n/a` appears nowhere in SKILL.md or the brief template. A reviewer checking
author checklist item 8 ("no row carries a tag outside the vocabulary") against the skill would
flag 25 correct rows. Fixed in place at SKILL.md:153.

**W3. The brief template drops the clause that was the round-1 defect.** MINOR. CONFIRMED.
SKILL.md:248 requires "an accessibility persona with her own goal"; the brief template's item 3,
which is the text the author actually reads, said only "an accessibility persona". The dropped
clause is precisely what the chess run's round 1 got wrong (SKILL.md:90: five of her variants read
"same as the spine, as text"). Fixed in place in `assets/brief-template.md`.

**W4. README onboarding list and path.** NIT. CONFIRMED. `README.md:290` began a line with `1b.`,
which is not an ordered-list marker, so it renders as a broken paragraph splitting the list; and it
named an output path `docs/journeys/` that SKILL.md:50 does not use (SKILL.md leaves the promoted
location to the maintainer). Fixed in place: indented as a sub-item, path generalised.

---

## Part C: Receipts per defect class

### Class 1. Greenfield mode is real, not a paragraph. Receipt.

Examined: SKILL.md "Two modes", the firewall reading list, pass 2's greenfield rules, the exit
section, `assets/brief-template.md` Brief A item 4, `skills/product-discovery/SKILL.md` for whether
the one allowed input exists, `skills/wireframes/SKILL.md` for the downstream consumer,
`build-map.py` defaults.

Found: the mode is real, not decorative. Every pass-1 input exists and is guaranteed by the
upstream skill's deliverable spec (`product-discovery/SKILL.md:21,59`). Pass 2 tags against the
R-list and baseline by id, with a stated definition of served, awkward and missing in requirement
terms (SKILL.md:165), and the author checklist splits by mode at item 10. Three steps still assume
a product exists: S5 above, itemised. The downstream feed named at SKILL.md:223 does not exist:
S4 above.

### Class 2. Brownfield matches what worked. Receipt.

Examined: `/Users/jasonou/code/chess/docs/drive/user-journeys-brief.md` line by line against
SKILL.md and the brief template; `review.md`'s S1 to S6 against the skill's defect classes; the
retrospective's journeys entries (`retrospective-2026-09-05.md:21,69,91`).

Found, kept and correct: the coordinator writes the feature map first (chess `feature-map.html`
predates the brief; SKILL.md:145 keeps the rule and adds the fallback for when none exists); one
real user's usage summary allowed as context for one persona (chess `play-summary.html`; brief
item 3); non-goals only; the seven journey parts; the vocabulary grep. Every tag the skill added
beyond the chess brief's three was needed by the run: `served in part` (7 rows) and `does not
apply` (25 rows) both appear in the real register, so the three-tag brief was under-specified, not
the skill over-specified. The swap test, the mirror test and the severity-per-persona rule each
answer a finding the run actually produced (S5, S1, S3 in `review.md`). Nothing in the skill's
brownfield procedure is added weight the run shows unnecessary.

Dropped, one item. MINOR, CONFIRMED. The chess brief did not ask the author to invent breadth; the
coordinator enumerated ten concrete shapes for this product ("a 600-rated beginner with 40 games; a
1000 casual blitz-only player; ... a player who wants to study a friend or rival rather than
himself", `user-journeys-brief.md`), and the author's eleven personas track that list closely. The
skill generalises those shapes into abstract categories (SKILL.md:82-88) and the brief template
leaves item 3 abstract, so the step that actually produced the breadth, the coordinator writing a
candidate list of concrete shapes for *this* product before briefing, is nowhere instructed.
Disposition: one sentence in the brief template telling the coordinator to seed candidate shapes
and to say they are candidates, not a ceiling. Not blocking.

One deviation noted and not a defect: the chess `review.md` stacks rounds oldest-first (round 1 at
`:13`, round 2 at `:401`), where SKILL.md:48 and :192 require newest-first. The skill follows
playbook §5 and §9; the run deviated from doctrine. The skill is right.

### Class 3. The firewall. Receipt.

Examined: SKILL.md "The firewall" and the leak remedy; `review.md` S1 in full; the actual
CLAUDE.md and memory discovery behaviour, tested rather than assumed.

**The primary mechanism works, verified empirically.** From a clean directory outside the project
tree, `claude -p` loaded nothing about the product:

> (1) NONE. No project instructions, CLAUDE.md, or memory file contents were placed in my context
> before your message. The memory directory exists but no MEMORY.md content was loaded.
> (2) Software products mentioned in this session: Claude Code, ... [no product]

Project memory is keyed by the working directory's slug (`~/.claude/projects/<slug>/memory/`), and
I confirmed no memory directory outside the project's own slug carries product content:
`grep -rl -iE 'chess|postmortem|stockfish|FSRS' ~/.claude/projects/*/memory/` returns nothing
outside `-Users-jasonou-code-chess/`. So the recipe at SKILL.md:62 is sound, and its diagnosis of
the chess leak matches `review.md` S1 exactly, including the twelve mirrored steps and the clean
grep.

**But the skill names only two of the three loaders.** SKILL.md:62 says Claude Code loads "the
project's `CLAUDE.md` (and the user's project-keyed memory) from the working directory and its
ancestors", so a reader concludes that leaving the ancestor chain is sufficient. It is not: the
user-scope `~/.claude/CLAUDE.md` loads from *any* directory. Receipt, by injection. There was no
user-scope file, so I created one naming a fictional product, ran `claude -p` from a clean
directory well outside any project, and removed it:

```
$ printf 'The product in this workspace is ZEPHYRGRID, a warehouse robot scheduler.\n' > ~/.claude/CLAUDE.md
$ cd <clean dir> && claude -p "name any software product described to you in your context before this message"
ZEPHYRGRID, a warehouse robot scheduler, described in the user's global CLAUDE.md instructions.
$ rm ~/.claude/CLAUDE.md      # restored; the file did not exist before
```

MAJOR, CONFIRMED, and it matters because it is silent: the coordinator follows the recipe, the
author reports a clean firewall receipt, and the leak is invisible. This user has no such file,
which is why the chess run was unaffected, but the skill is a generic artifact and its only stated
failure mode is the ancestor chain. Disposition: name the user-scope `~/.claude/CLAUDE.md` and any
enterprise managed-policy file as loaders the clean directory does *not* escape, and add a
coordinator step to check for them and record the result in the firewall receipt.

**The fallback is honestly labelled and the remedy is executable.** SKILL.md:63 calls the
in-project subagent "a known-leaky firewall", makes the reviewer's breach test mandatory and tells
the coordinator to expect a round 2. That is the right register: a stated contract rather than a
later surprise. The four-step leak remedy at SKILL.md:67-72 is executable as written, each step
has an actor and an artifact, and it carries its own falsifier ("Moving up is suspicious").

### Class 4. Generator honesty. Receipt.

Examined: `build-map.py` in full; run against copies of the chess `journeys.md` and
`gap-register.md` in a scratch directory; three required injections; four unexercised input
shapes. The chess repo was not modified (`git status --short docs/drive/user-journeys/` is empty).

Counts reproduce exactly after the two-row retag W1 describes: 11 personas, 31 journeys, 425 steps,
62/8/94/236/25, 43 gaps at 14/25/4, matching the shipped chess map's legend and footer.

Required injection 1, duplicated step id. Fails loudly:

```
BEFORE line 331: | J9.P4.1 | missing | No notion of someone else's agent with revocable
AFTER  line 331: | J9.P3.1 | missing | No notion of someone else's agent with revocable
build-map: duplicate step ids in the walk: J9.P3.1
EXIT=1
```

Required injection 2, off-vocabulary tag. Fails loudly:

```
BEFORE line 332: | J9.P7.1 | missing | No way to lock it off; every endpoint is open on loopback.
AFTER  line 332: | J9.P7.1 | mostly served | No way to lock it off; every endpoint is open on loo
build-map: row J9.P7.1 carries a tag outside the vocabulary: 'mostly served'
EXIT=1
```

Required injection 3, a gap citing no persona. Fails loudly:

```
target gap: G1.1
build-map: gaps naming no persona or no journey: G1.1
EXIT=1
```

Unexercised shapes: three fail silently and are S1, S2 and S3 above. The fourth is cosmetic.
**A persona name containing a comma is truncated at the first comma.** MINOR, CONFIRMED.
`build-map.py:69` does `name, _, desc = head.partition(',')`, so `### P4: Priya Raman, Jr., a 1900
club player with a coach` renders as name `Priya Raman`, descriptor `Jr., a 1900 club player with a
coach`. Exit 0, no count affected, wrong name on a tile and in the panel heading. The format at
SKILL.md:212 does specify `<Name>, <one-line descriptor>`, so this is under-defended rather than
undefined; splitting on the last comma, or on a comma followed by a lowercase word, would hold.

### Class 5. Map template. Receipt.

Examined: `assets/journey-map-template.html` in full; the generated map rendered in headless
Chrome at 1500x1000 in both themes; the token blocks compared programmatically; an external
resource sweep on template and output.

Self-contained: confirmed. `grep -oE '(src|href)="[^"]*"'` and `grep -oE 'https?://'` over both the
template and the 159 KB generated page return nothing. No script, stylesheet, font or image is
fetched, so there is no network surface at all.

Both themes: confirmed by render, not by reading. Light and dark screenshots differ
(`md5` cf6aa748... vs 7bdc699d...) and both are legible. The theming follows the three-state
pattern correctly: the full palette on bare `:root`, redefined under
`@media (prefers-color-scheme:dark){:root:not([data-theme="light"])}` and again under
`:root[data-theme="dark"]`. I verified the two dark blocks are not merely similar but identical
token sets, and that no token is defined only in a dark block:

```
identical: True
media tokens: 16 explicit: 16
light tokens: 16
tokens defined only in dark: set()
```

so no color has its only definition inside a media or attribute block, and the toggle wins in both
directions.

Every grid cell resolves to data: confirmed. Cells with steps are `<button>` carrying a
`data-key` that indexes the embedded JSON; cells without are an inert `<span class="cell empty">`.
The generator dies on a walk row for an unknown journey or persona (`:190-195`), so no dot can
exist without a heading. The reverse hole is S1.

Numbers come from the generator only: confirmed by construction. Every figure on the page is
inside a `BEGIN/END` marker pair filled by `build-map.py` (legend totals `:226-231`, gap and
severity counts `:238-243`, intro `:245`, footer `:247-251`); the typed numbers in the template
are sample content between the markers, which the generator discards, and the template's header
comment says so at lines 14-16.

One finding. **The grid encodes its whole meaning in red against green.** MINOR, CONFIRMED.
`--served:#3D6A50` and `--miss:#A93F2E` (`journey-map-template.html:24-25`) differ only in hue, and
the dots differ only in fill; the sole non-color distinction in the vocabulary is `.d.na`, which is
hollow (`:40`). At a glance, which is the map's entire purpose, a deuteranope reads served and
missing as the same dot. Each dot does carry a `title` and the side panel gives the tag as text, so
the information is recoverable, which is why this is MINOR rather than MAJOR. It is still worth
fixing on a page whose own persona-breadth rule mandates an accessibility persona: give the five
tags five shapes or fills, not five hues.

### Class 6. Brief templates and checklists. Receipt.

Examined: all three checklists in SKILL.md (author 11 items, reviewer 7, coordinator 6) and the two
in `assets/brief-template.md`, item by item, asking of each whether it could pass while the thing it
stands for fails.

Reviewer defect classes are enumerated with receipts required: yes, ten classes at SKILL.md:179-188,
each with an explicit "Receipt:" clause naming the artifact (a side-by-side list, a facts table, a
recomputation table, the swap result per persona), and reviewer checklist item 1 requires a receipt
per class. Class 2 goes further and names its own null form, "or 'swept, none found' with the
documents read", which is the right shape: it forbids a bare no-issues. This part is done properly.

The coordinator's list is the strongest of the three because its items are externally checkable:
item 3 makes the generator's printed counts meet an independent `grep -c`, and item 4 has the
coordinator read three cells and three gaps off the rendered page against the register.

**The item that can pass for a reason unrelated to what it means to check** is author checklist
item 6 (SKILL.md:251), "Vocabulary grep on `journeys.md` is zero, or each hit is justified as
ordinary English." It is the only firewall-integrity item on the author's list, and the chess run
passed it with a completely breached firewall. The evidence is in the run's own review
(`review.md:29-30`): "The vocabulary grep is clean (0 hits for Today, Lines, Patterns, funnel,
scope, card, FSRS; 0 em dashes)", followed by twelve steps mirroring excluded documents. The skill
knows this, and says so at SKILL.md:67: "Words are the weak signal; shape is the strong one." Yet
the author's checklist tests only the weak signal, and item 1 and item 2 next to it are pure
self-report ("both timestamps ... are in the report", "discloses what the session's system context
carried"), which an author cannot fail by accident and can pass while leaking.

MINOR rather than MAJOR because the reviewer's mandatory mirror test does catch it, which is the
system working as designed. Disposition, and it is nearly free: the skill already owns the right
question at SKILL.md:70, so add an author item that applies it self-critically before saving, "every
step was re-read against 'would this person say this before seeing the product?' and the ones that
survive only because of something I already knew are marked", so the author's list tests the strong
signal too.

### Class 7. Plugin integration. Receipt.

`claude plugin validate .claude-plugin/plugin.json --strict` passes, exit 0, both before and after
my in-place edits. `claude --plugin-dir . plugin details app-bootstrap` reports version 0.3.0 and
`Skills (6)  design-loop, e2e-review, implementation-loop, product-discovery, user-journeys,
wireframes`, with user-journeys at ~170 always-on tokens, well clear of the `< 20` collapse the
README names as the tell for a skill that has stopped surfacing. Both manifests read 0.3.0 with
matching descriptions.

No other skill modified: `git diff --stat -- skills/` is empty and `git status --short skills/`
shows only `?? skills/user-journeys/`. Note this is exactly what makes S4 a finding rather than a
fix.

README agreement: the stage list, the exit-gate table and the onboarding prompt all carry 1b, and
the five-to-six counts are updated consistently (the "six SKILL.md files" instruction, the "six
skills" in `plugin details`, `Skills (6)` in the checks table, "all six" for the playbook). One
defect, W4 above, fixed in place. Playbook §11 is new, five rules, each stating its failure before
its rule as §10's register requires; it is doctrine about running loops rather than about this
skill, and nothing in it contradicts the skill.

One observation, not a finding: user-journeys costs ~10.5k tokens on invoke, roughly four times the
next largest skill. That is a real cost the maintainer should know about, and it is defensible for a
stage that runs once, but it is worth a deliberate decision rather than an accident of length.

### Class 8. Register. Receipt.

Examined: SKILL.md against playbook §10's seven rules; an em-dash count on every new file and every
added line; a jargon grep for the chess product's terms.

Motivation before mechanism: holds. "Why this stage exists" precedes every procedure and argues
from a concrete failure (the feature map served one persona of eleven) before naming the firewall
that prevents it. Worked example with real values: present and substantial, the chess run with its
counts, its five findings and its two rounds. Simplifications flagged at the point they are made:
yes, the leaky fallback at SKILL.md:63. Single compressed takeaway sentence at the end: yes,
SKILL.md's closing line.

Em dashes: zero, in all four new files and in every added line of the four edited tracked files.

```
skills/user-journeys/SKILL.md                                0
skills/user-journeys/assets/brief-template.md                0
skills/user-journeys/assets/build-map.py                     0
skills/user-journeys/assets/journey-map-template.html        0
added lines in tracked files                                 0
```

Product jargon: no leak. Every hit for Today, Lines, Patterns, funnel, scope, card, FSRS is either
ordinary English (SKILL.md:169 "the surface", :152 "the feature map already carries") or an
explicitly labelled quotation from the chess run's history (:67, :137, :155). SKILL.md:137 uses
"lines" as its own example of the ordinary-English exemption, which is the rule demonstrating
itself.

Define every term before first use: one MINOR miss. "Feature map" is load-bearing in the entry gate
at SKILL.md:13 and in the "Two modes" section at :34, and is not defined until :145 ("a one-page
inventory of what is shipped, in build, and planned, with the version and the date"). A reader
meets the gate before the definition. Not fixed in place because moving the definition is a
structural edit to the mode section; a five-word gloss at :13 would close it.

---

## Part D: Summary of dispositions

| Id | Severity | Status | Disposition |
| :-- | :-- | :-- | :-- |
| S1 | BLOCKER | CONFIRMED | Author: die on a journey heading with zero walk rows |
| S2 | BLOCKER | CONFIRMED | Author: whitelist qualifiers per tag; reject a qualifier that begins with a vocabulary word |
| S3 | MAJOR | CONFIRMED | Author: parse rows tolerantly then validate, or cross-check the row count |
| S4 | MAJOR | CONFIRMED | Author plus maintainer: wire the wireframes entry gate, or drop the claim at SKILL.md:223 |
| S5 | MAJOR | CONFIRMED | Author: mark classes 5 and 6 brownfield-only; add the greenfield invocation and Part D wording |
| Class 3 leak | MAJOR | CONFIRMED | Author: name `~/.claude/CLAUDE.md` and managed policy as loaders the clean directory does not escape |
| Class 2 breadth | MINOR | CONFIRMED | Author: one sentence, coordinator seeds candidate persona shapes |
| Class 4 comma | MINOR | CONFIRMED | Author: split the persona heading on the last comma |
| Class 5 red/green | MINOR | CONFIRMED | Author: five shapes, not five hues |
| Class 6 item 6 | MINOR | CONFIRMED | Author: add the shape question to the author checklist |
| Class 8 term | MINOR | CONFIRMED | Author: gloss "feature map" at first use |
| W1 to W4 | MINOR, NIT | CONFIRMED | Fixed in place by the reviewer |

Accepted residue, needing no action: the chess run's oldest-first review stacking (the skill is
right, the run deviated); the ~10.5k on-invoke token cost, flagged for a deliberate decision.

## Verdict

ONE MORE ROUND
