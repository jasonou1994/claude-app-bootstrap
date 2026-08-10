# Adversarial review — claude-app-bootstrap

Rounds stack **newest-first**.

---

# Round 2 — 2026-08-09 (commit `72d37cc`, over coordinator commits `f99cdd1` + `f106d95`)

Scope: verification of all 18 Round 1 dispositions against the **current text**, adjudication of the three your-call items and the two coordinator reversions, and an attack on the new surfaces (rewritten onboarding steps 1/3, the three-way validate table, the Updating/stability subsection, the trigger-shaped descriptions).

Everything below was tested against Claude Code **2.1.226** on a throwaway copy of the repo and an isolated `CLAUDE_CONFIG_DIR` — no edits outside this file, no mutation of the maintainer's real plugin config.

**Verdict: ONE MORE ROUND** (2 new MAJOR, 3 new MINOR, 2 new NIT; 16 of 18 Round 1 findings verified fixed).

---

## Round 1 disposition scorecard

| ID | Round 1 finding | Disposition | Verified |
| :-- | :-- | :-- | :-- |
| B1 | Unflagged `jasonou` placeholder, no repo | **FIXED** | `jasonou1994` in `README.md:32,55,88,218`, `marketplace.json:6,10-12`, `plugin.json:9-10`. Install from a real source verified end-to-end (below). |
| M1 | Prompt orders Claude to run `/plugin list` | **FIXED** | `README.md:84` now reads *"run `claude plugin list` in the shell"* — a Bash-executable command. Confirmed it runs non-interactively and prints `Status: ✔ enabled`. |
| M2 | Prompt reads plugin docs by bare relative path | **NOT FIXED — new defect** | See **R2-A**. |
| M3 | Reviewer edit authority contradicts the design loop | **FIXED** | `playbook.md:49` is now loop-differentiated and carries the Fixer ≠ judge rationale. Residual: **r2-f**. |
| M4 | Model requirement dropped | **FIXED** | `playbook.md:78`. Accurate to source (*"the source project ran every author and reviewer on its strongest available subagent model"* — matches `subagent-loop-playbook.md:17-18`). The added *"Reviewers are never given a weaker model than authors"* is a sound extension. |
| M5 | Wireframe artifact capability unchecked | **FIXED, thoroughly** | `wireframes:14,52,58-60`, `design-loop:42`, `implementation-loop:87`, `e2e-review:26`. The added *"Do not silently substitute a scattering of images, a doc per surface, or a description of what the UI would look like"* closes the degradation path I described, which I had not asked for. |
| M6 | "Ignore `0 skills`" | **FIXED** | The false claim is gone entirely; Step 3 now checks `claude plugin list` for `Status: ✔ enabled`. String verified exact. |
| m1 | Descriptions lack triggers | **FIXED** | All five now trigger-shaped, all five gained `name:`. Measured cost (`plugin details`, before vs after): always-on **~328 → ~458 tok**, +40%. Worth it, but see r2-e for the gate that should protect it. |
| m2 | Invented `500k` | **FIXED** | `playbook.md:71` — the number is gone, replaced with *"No measured threshold exists yet — this methodology has not published one."* Exactly right. |
| m3 | Three dropped `CLAUDE.md` rules | **FIXED** | `playbook.md:66-68`. All three, each with a rationale. The test-delegation rationale (*"the output of a gate is exactly the thing this methodology refuses to accept second-hand"*) improves on the source, which stated the rule without one. |
| m4 | Cross-skill refs unlinked | **FIXED (author's call: link, not move)** | `product-discovery:38`, `e2e-review:45`. Both paths verified to resolve. **Upheld** — adjudication A1. |
| m5 | `validate` presented as coverage | **FIXED, and beyond** | The author matrix-tested and produced the three-way table at `README.md:240-248`. **I independently re-ran the matrix — all three rows CONFIRMED.** See A3. One gap: **r2-e**. |
| m6 | No version/update story | **PARTIAL** | `version`/`homepage`/`repository`/`license` added to both manifests ✓. The Updating subsection is **wrong** — see **R2-B** and **r2-c**. |
| m7 | Departures demanded of every reviewer | **FIXED** | `playbook.md:50` — *"where the artifact under review has a Departures section"*. |
| n1 | `argument-hint` non-conventional, `name` absent | **FIXED / kept (author's call)** | **Upheld** — adjudication A2. |
| n2 | `./claude-app-bootstrap` wrong from inside repo | **FIXED** | `README.md:196` — *"use `.` if you are standing inside the repository itself"*. |
| n3 | No `homepage`/`repository` | **FIXED** | Both manifests. |
| n4 | 45-line paste, no multiline guidance | **FIXED** | `README.md:71`, including the Esc + `/paste` recovery. Better than the fix I proposed. |

---

## Adjudications

### A1 — m4, "link rather than move": **upheld**

Both links resolve (`skills/product-discovery/../implementation-loop/SKILL.md` → EXISTS; same from `e2e-review`). Moving the six gate-honesty rules into the playbook was my preference for load order, but it would have split them from the stage that owns them and forced a restatement — which `playbook.md:63` forbids. The author also added *"read them there rather than working from this summary"* (`e2e-review:45`), which is the part that actually mattered: it stops a reviewer working from the three-clause paraphrase. Correct call.

### A2 — n1, keeping `argument-hint` and adding `name`: **upheld, and my Round 1 concern is retired**

Two things I could not settle in Round 1, now measured:

1. `--strict` **tolerates** `argument-hint` in skill frontmatter — `claude plugin validate .claude-plugin/plugin.json --strict` → `✔ Validation passed` with all five hints present. Not an unrecognized-field warning.
2. I suspected the four skills that declare `argument-hint` but never reference `$ARGUMENTS` (`grep -c ARGUMENTS` = 0 for `e2e-review`, `product-discovery`, `implementation-loop`, `wireframes`) would silently discard a typed argument. **They do not.** Probe: `Skill(skill='app-bootstrap:wireframes', args='ZZPATHZZ/requirements.md')` → the loaded text carries a trailing `ARGUMENTS: ZZPATHZZ/requirements.md` line appended after the body. The hints are honest. **Verify-then-drop: not reported as a finding.**

### A3 — the coordinator's `${CLAUDE_PLUGIN_ROOT}` edit, reverted to relative links: **reversion upheld, with a recorded caveat**

I tested both forms rather than reasoning about them.

- **`${CLAUDE_PLUGIN_ROOT}` does expand in a skill body.** Variant repo with `Shared doctrine: ${CLAUDE_PLUGIN_ROOT}/docs/playbook.md`; the model reported the loaded line verbatim as `Shared doctrine: /…/rootvar/docs/playbook.md` — *"It does not contain the literal characters `CLAUDE_PLUGIN_ROOT`."* So the coordinator's edit was not broken.
- **The relative form also works**, as Round 1's G3 established: the runtime injects `Base directory for this skill: /…/skills/design-loop` as line 1, and `../../docs/playbook.md` resolved and Read successfully. Re-confirmed this round for all five skills by path arithmetic (all EXISTS).

Both work, so this is a judgment call, and the author's reasons are good: the repo is now published, so relative links are clickable on GitHub, and they match how `README.md:151` already links the playbook. **Caveat worth recording:** the relative form's correctness depends on the `Base directory` preamble, undocumented runtime behavior the plugin does not control, whereas `${CLAUDE_PLUGIN_ROOT}` is a documented plugin contract. The failure mode if that preamble ever changes is a silent wrong-path Read — the exact class M2 was about. Not worth changing now; worth knowing.

### A4 — the coordinator's `$ARGUMENTS` hedge, reverted: **reversion upheld — the coordinator's premise was factually wrong**

The coordinator's version hedged: *"their invocation arguments, if any: **$ARGUMENTS** — if that reads as a literal placeholder, ask what design this loop is for"*. That describes a failure mode that **does not exist**. Probe with no `args` parameter at all:

```
Run the full adversarial design-review workflow for: ****
```

`$ARGUMENTS` substitutes to the **empty string**, never a literal token. The hedge would have shipped a meta-instruction about a placeholder the model can never see, in the skill's first line. The author's replacement — clean `**$ARGUMENTS**` plus a separate `If nothing was named above, ask the maintainer which design this loop is for before launching anything.` (`design-loop:10`) — matches the observed behavior exactly, and reads correctly against the degenerate `for: ****` rendering. **The author was right and the coordinator was wrong.** This is `playbook.md:54` (reviewers argue back with evidence) working in the author's favour.

---

## New findings

### MAJOR

#### R2-A — The M2 fix does not work: the onboarding prompt's `find` command cannot locate the installed plugin

**CONFIRMED by installing the plugin and running the literal command.** `README.md:94-100`.

> `search under ~/.claude/plugins/ for a directory named `app-bootstrap` that contains `skills/` and `docs/playbook.md` (e.g. `find ~/.claude/plugins -type d -name app-bootstrap`)`

Installed into an isolated `CLAUDE_CONFIG_DIR` from a real marketplace source. Actual on-disk layout:

```
plugins/cache/claude-app-bootstrap/app-bootstrap/0.1.0/{skills,docs,.claude-plugin,README.md,LICENSE}
```

Running the prompt's own command, then testing its own qualifier:

```
$ find <plugins-root> -type d -name app-bootstrap
…/plugins/cache/claude-app-bootstrap/app-bootstrap

…/cache/claude-app-bootstrap/app-bootstrap : skills/=NO   docs/playbook.md=NO

$ find <plugins-root> -name playbook.md
…/plugins/cache/claude-app-bootstrap/app-bootstrap/0.1.0/docs/playbook.md
```

The directory named `app-bootstrap` contains exactly one thing: a **version directory** (`0.1.0/`). `skills/` and `docs/playbook.md` live one level below it. So the `find` returns the right *branch* and the prompt's own qualifier — *"that contains `skills/` and `docs/playbook.md`"* — then **rejects the only hit**.

**Failure scenario.** A novice completes the install, pastes the onboarding prompt, gets through steps 1 and 2. Step 3's find succeeds, the qualifier fails, and the prompt's own fail-loud clause fires: *"If you cannot find them, STOP and tell me."* Onboarding halts at step 3 of 4 with "I can't find the plugin's docs" and no recovery path — on the exact step whose failure Round 1 flagged. The fail-loud clause is why this is MAJOR and not BLOCKER: it stalls rather than silently writing boilerplate, which is the correct degradation. But it still stops.

**Minimal fix.** Anchor on the file, not the directory:

```
find ~/.claude/plugins -path '*app-bootstrap*' -name playbook.md
```

then read `skills/*/SKILL.md` from that file's grandparent. Verified: this returns the correct path on the first try. Note in the prompt that the plugin tree sits under a version directory, so there may be several — take the highest version.

#### R2-B — The new Updating section documents a command that does not update the plugin

**CONFIRMED by running the full sequence twice.** `README.md:198-204`.

> ```
> claude plugin marketplace update claude-app-bootstrap
> ```
> `Then start a new session to pick up the new version.`

`claude plugin marketplace update` refreshes **marketplace metadata**, not the installed plugin. Test: installed 0.1.0, changed `docs/playbook.md` upstream, committed, ran the README's command:

```
✔ Successfully updated marketplace: claude-app-bootstrap
→ cache still contains only 0.1.0; playbook.md unchanged
```

Then bumped the version to 0.2.0 upstream, committed, ran the README's command again:

```
✔ Successfully updated marketplace: claude-app-bootstrap
→ cache still contains only 0.1.0
$ claude plugin list  →  Version: 0.1.0
```

The plugin never moved. `claude plugin install` again returns `✔ Plugin … is already installed`. The command that actually works is a subcommand the README never mentions:

```
$ claude plugin update app-bootstrap@claude-app-bootstrap
✔ Plugin "app-bootstrap" updated from 0.1.0 to 0.2.0 for scope user. Restart to apply changes.
→ cache now holds 0.1.0 and 0.2.0; 0.2.0/docs/playbook.md carries the new content
```

`claude plugin --help` confirms: `update [options] <plugin>   Update a plugin to the latest version (restart required to apply)`.

**Failure scenario.** A team adopts the plugin. Doctrine is corrected upstream — say, the M3 reviewer-authority fix. Everyone runs the documented command, sees `✔ Successfully updated marketplace`, restarts as instructed, and keeps running the old doctrine indefinitely. The success message makes this undetectable: the command they were told to run succeeded, and the thing they wanted did not happen.

**Minimal fix.**

```
claude plugin marketplace update claude-app-bootstrap    # refresh the catalog
claude plugin update app-bootstrap@claude-app-bootstrap  # actually upgrade the plugin
```

and change *"Then start a new session"* to quote the tool's own instruction, `Restart to apply changes.`

---

### MINOR

#### r2-c — The Updating section contradicts itself on pinning, and "nothing to pin to" is wrong

**CONFIRMED.** `README.md:204` vs `README.md:206`.

> `:204` — *"The plugin pins `"version"` … so consumers only move when that field is bumped."*
> `:206` — *"No release tags have been cut yet, so there is currently nothing to pin to; a team that needs doctrine which cannot move under them should vendor the repo…"*

Line 204's mechanism claim is **true** — confirmed above: a content change with no version bump never propagated, and only the version bump produced a `0.2.0` tree. That makes 206 self-refuting. A consumer at 0.1.0 stays at 0.1.0 until someone runs `claude plugin update`; *that is the pin*. The advice to vendor the repo is heavier than the situation needs, and it is the one piece of guidance here a reader might act on.

Also unmentioned: `claude plugin tag` exists (`claude plugin --help`: *"Create a `{name}--v{version}` git tag for a plugin release, validating that plugin.json and any enclosing marketplace entry agree"*) — that is the tool for the release-tag gap 206 laments, and it validates exactly the two-manifest agreement this repo now maintains by hand.

**Fix.** Replace 206's second half with: *"Consumers stay on the version they installed until they run `claude plugin update`, so the pin is opt-in upgrade rather than a tag. Releases are cut with `claude plugin tag`, which checks that `plugin.json` and the marketplace entry agree."*

#### r2-d — `/reload-plugins` was deleted entirely, leaving the in-session install path incomplete

**CONFIRMED.** `README.md:53,55,228`; the removed text is in the `823ade1..HEAD` diff.

Fixing M6 removed every mention of `/reload-plugins` and replaced it with "start a new session". That is safe but strictly worse, and it breaks the new **Alternative — from inside Claude Code** route at `:55`, which stops at *"then `/plugin list` to confirm"*. What Claude Code actually prints after an in-session install is one of two strings, both verbatim in the 2.1.226 binary:

```
Plugin is now active.
Run /reload-plugins to activate.
```

A reader who takes the Alternative route sees the second one and finds nothing about it anywhere in the README — the one command they were just told to run is undocumented. Round 1's G4 credited this README for quoting real UI strings; this fix threw away two of them.

**Fix.** At `:55`, append: *"If it says `Run /reload-plugins to activate.`, type that; if it says `Plugin is now active.`, you're done."* Keep "start a new session" as the terminal-route instruction, where it is correct.

#### r2-e — The recommended `validate` command omits `--strict`, the flag that catches the defect class m1 just fixed

**CONFIRMED.** `README.md:234`, `README.md:242-244`.

The dev block recommends `claude plugin validate ./claude-app-bootstrap/.claude-plugin/plugin.json` with no `--strict`. Injecting a missing `description:` into one skill:

```
$ claude plugin validate .claude-plugin/plugin.json
⚠ Found 1 warning:
  ❯ description: No description in frontmatter. …
✔ Validation passed with warnings          exit=0

$ claude plugin validate .claude-plugin/plugin.json --strict
✘ Validation failed (--strict treats warnings as errors)   exit=1
```

So the recommended command **exits 0** on a dropped description — the exact failure the table's own trap paragraph (`:248`) warns about (*"dropping its description, so it simply stops surfacing"*), and the exact asset m1 just spent 130 always-on tokens improving. Anything scripted off the README's command will not catch it. The table's row 2 (*"Plugin manifest and every skill's frontmatter"*) is accurate for parse errors but overstates coverage at the default flag level.

Related: row 3 says `plugin details` is *"The only check that proves all five skills load."* Under the frontmatter injection it printed `Skills (5)` for a plugin with unparseable frontmatter — it proved the skill loaded, but with empty metadata. The prose is defensible (the trap paragraph says exactly this), and the tell is visible in the token column (`wireframes  < 20` vs `~100`). Worth one clause so the reader knows what to look at.

**Fix.** Add `--strict` to `README.md:234` and to the table's row 2; add to row 3 *"— a broken skill still counts, but its always-on token figure collapses to `< 20`."*

---

### NIT

- **r2-f — The e2e journey reviewer has no stated edit authority.** The M3 fix rewrote `playbook.md:49` as *"it differs by loop"* and enumerates exactly two: implementation and design. The Stage 5 reviewer (`e2e-review:42`) belongs to neither, and `grep -n "e2e\|journey" docs/playbook.md` returns nothing. A gap created by the fix, in a stub stage, so it costs almost nothing to close: add *"A journey-results reviewer follows the implementation-loop rule"* to `:49`, or add it to `e2e-review`'s open-questions list, which already collects exactly this kind of unresolved item.
- **r2-g — `README.md:35`'s claimed Step 1 output is a prefix of the real output.** Actual: `✔ Successfully added marketplace: claude-app-bootstrap (declared in user settings)`. Harmless, but Steps 2 and 3 quote their strings exactly, so this is the odd one out.

---

## What Round 2 got right

- **The author matrix-tested my m5 finding instead of accepting it, and was right to.** Round 1 said `validate` "never opens `skills/`". That is true of `claude plugin validate .` on this repo and **false** of `claude plugin validate .claude-plugin/plugin.json`. I re-ran the matrix independently with an injected `Multiline implicit key` defect and confirm all three rows of `README.md:242-246`, including the error text quoted verbatim (`❯ frontmatter: YAML frontmatter failed to parse`) and the claim that skill lines print only on error. Correcting a reviewer with a receipt is exactly the behavior `playbook.md:54` asks for.
- **A4: the author overruled the coordinator on `$ARGUMENTS` and was correct**, as the empty-substitution probe proves. Two independent instances this round of the author holding a position against a higher-status instruction and being vindicated by measurement.
- **M5 was over-delivered.** The fallback was propagated to all four downstream consumers *and* hardened against the substitution I described but did not ask to be blocked (*"Do not silently substitute a scattering of images…"*).
- **m2's fix is exemplary.** The invented `500k` was not replaced with a better guess; it was replaced with an explicit statement that no measurement exists and what signal to use instead — which is what the plugin's own rule 6 demands of everyone else.
- **The Round 1 evidence was reused, not re-derived.** `README.md:240` cites the version it was tested against and the method (*"by injecting a YAML frontmatter defect into a skill and re-running each form"*). That is a gate that has been watched fail — rule 3, applied to documentation.

---

## Round 2 checklist

| # | Item | Status |
| :-- | :-- | :-- |
| 1 | All 18 Round 1 findings verified against current text, not claims | **PASS** — scorecard above; 16 fixed, m6 partial (R2-B), M2 not fixed (R2-A). Every row cites current `file:line`. |
| 2 | Three your-call items adjudicated on the merits | **PASS** — A1 (m4 link) upheld; A2 (n1) upheld, with my Round 1 concern retired by two measurements. |
| 3 | Both coordinator reversions adjudicated, citing G3 | **PASS** — A3 (both forms verified to work; reversion upheld with caveat), A4 (coordinator's premise disproven by probe; reversion upheld). |
| 4 | New surfaces attacked | **PASS** — onboarding step 1 (fixed, verified executable) and step 3 (**R2-A**, broken); validate table (independently re-verified, all three rows CONFIRMED, one gap **r2-e**); Updating/stability (**R2-B**, **r2-c**); trigger descriptions (fixed; cost measured 328→458 tok). |
| 5 | Round 2 appended above Round 1, newest-first; no edits outside REVIEW.md | **PASS** — `git status` shows `REVIEW.md` only. All tests ran on throwaway copies and an isolated `CLAUDE_CONFIG_DIR`, both deleted. |
| 6 | Verdict is exactly one of {SHIP, ONE MORE ROUND} | **PASS**. |

---

## Verdict

**ONE MORE ROUND**

Two CONFIRMED MAJORs, both on surfaces created by the Round 1 fixes, and both on the path a first-time user walks: the onboarding prompt stalls at step 3, and the documented update command reports success while doing nothing. Neither is deep — R2-A is a one-line `find`, R2-B is one extra command — but the update defect is the kind that stays invisible for months, and this repo's whole premise is that a green signal over untested work is the defect class worth chasing.

---

# Round 1 — 2026-08-09 (commit `823ade1`)

Scope: full repo. Sources of truth for the fidelity diff: `/Users/jasonou/code/chess/.claude/commands/design-review.md`, `/Users/jasonou/code/chess/.claude/docs/subagent-loop-playbook.md`, `/Users/jasonou/code/chess/CLAUDE.md` (Agent Workflow Policy), `/Users/jasonou/code/chess/docs/HANDOFF.md` §5. Chess repo read-only; no edits made anywhere.

**Verdict: ONE MORE ROUND** (1 BLOCKER, 6 MAJOR, 7 MINOR, 4 NIT).

---

## Findings

### BLOCKER

#### B1 — The novice's very first command cannot work: `jasonou/…` is an unflagged placeholder pointing at a repo that does not exist

**CONFIRMED.** `README.md:32`, `README.md:88`, `.claude-plugin/marketplace.json:6`.

```
$ git -C /Users/jasonou/code/claude-app-bootstrap remote -v
(no output — no remote configured)
```

`README.md:32` presents, as Step 1 of the non-technical guide:

```
/plugin marketplace add jasonou/claude-app-bootstrap
```

Part 1 never says this is a placeholder. The disclaimer exists — but only at `README.md:193`, deep in Part 2, which line 11 explicitly tells the novice to **skip**. The onboarding prompt repeats the same unflagged string at `README.md:88`, and `marketplace.json:6` hardcodes `https://github.com/jasonou` as the owner URL.

**Failure scenario.** A reader follows Part 1 verbatim. Step 1 errors. The recovery text at line 35 ("If you get an error about the repository not being found…") frames this as an edge case rather than the certain outcome, and its fallback assumes the reader has already "download[ed] or clone[d] this repo somewhere" — which the novice, who was told to start by typing a marketplace URL, has not. The guide's own promise ("every command exactly typeable") fails at command #1.

**Minimal fix.** Either (a) publish the repo and confirm the owner, or (b) in Part 1 Step 1 lead with the local-path form as the primary instruction and mark the GitHub form `<your-github-owner>/claude-app-bootstrap` with an inline "replace this" note — in all three locations, plus `marketplace.json`'s `owner.url`.

---

### MAJOR

#### M1 — The onboarding prompt orders Claude to run a slash command, then hard-blocks on the result

**CONFIRMED.** `README.md:84-91`.

> `1. Check the plugin is actually installed and enabled: run `/plugin list` (or the equivalent check) …  Do not continue to step 2 until the plugin is confirmed installed.`

Claude has no tool that executes slash commands — `/plugin list` is typed by the *user*, in the UI. `/plugin` is confirmed to be a UI command, not a CLI one:

```
$ strings claude-2.1.226 | grep '^/plugin list'
/plugin list [--enabled|--disabled] - List installed plugins
```

The hedge "(or the equivalent check)" is exactly the kind of underspecification the playbook itself bans (§4, "Briefs are self-contained… 'Based on your findings, do X' pushes synthesis onto the agent").

**Failure scenario.** The model either (a) hallucinates having run it and reports a fabricated result, (b) shells out to a nonexistent `claude plugin list` variant in the user's project and reports confusing output, or (c) stalls on an unsatisfiable gate it was told not to pass. All three land on a novice who cannot diagnose any of them.

**Minimal fix.** Replace with a check the agent can actually perform, e.g.: *"Check your own available-skills list for entries named `app-bootstrap:product-discovery` … `app-bootstrap:e2e-review`. If they are absent, tell me and walk me through installing…"*. Optionally add the working non-interactive command `claude plugin details app-bootstrap` (verified working — see "What it got right", G5).

#### M2 — The onboarding prompt tells Claude to read plugin files by bare relative path, from the wrong directory

**CONFIRMED.** `README.md:98-99`.

> `3. Read the plugin's own docs before writing anything: its five skills under `skills/*/SKILL.md` and `docs/playbook.md`.`

The onboarding prompt is pasted *inside the user's project*, so cwd is the user's repo. `skills/*/SKILL.md` and `docs/playbook.md` resolve there and will not exist. The installed plugin lives under `~/.claude/plugins/` (cache or marketplaces subtree), and the prompt gives no way to find it.

**Failure scenario.** Glob returns nothing; the model proceeds to step 4 and writes the CLAUDE.md section from its priors rather than from the skills — which is precisely the "generic boilerplate" step 2 was written to prevent. Worse: it fails *silently*, because step 3 has no verification of its own.

**Minimal fix.** Replace with an instruction that has a real path: *"Invoke each of the five skills' descriptions via your skill listing, or locate the installed plugin by searching `~/.claude/plugins/` for a directory named `app-bootstrap`, and read its `skills/*/SKILL.md` and `docs/playbook.md` from there. If you cannot find them, stop and tell me."*

#### M3 — Doctrine contradiction: who edits the artifact between rounds

**CONFIRMED.** `docs/playbook.md:49` vs `skills/design-loop/SKILL.md:69-71`.

Playbook §3 item 5 is scoped to *"Every reviewer brief carries all six of these"* (`playbook.md:43`) and states:

> `5. **Scope of authority.** Reviewers apply line-level fixes in place (never hand back a diff)…`

But the design loop specifies the opposite ownership:

> `- Revisions are **in-place edits to the one design doc**` (`design-loop:69`) — by the author, per the revision brief at `:70`
> `- The reviewer's next round verifies dispositions **against the revised text, not the author's claims**` (`design-loop:71`)

The source is unambiguous here and the plugin lost the distinction: `subagent-loop-playbook.md:18` scopes fix-in-place to the *implementation* loop's review subagent, while `design-review.md:48-50` gives design-doc revision to the author. The plugin promoted an implementation-loop-only rule into the universal reviewer template.

**Failure scenario.** A design-loop reviewer briefed with the §3 template edits the design doc directly. The persistent author (playbook §5) then revises the same file from its own stale mental model, silently clobbering or duplicating the reviewer's edits. Round 3 then has the reviewer "verifying dispositions against the revised text" of text it wrote itself — Fixer ≠ judge (§1) violated by the playbook's own template.

**Minimal fix.** Qualify `playbook.md:49`: *"In the implementation loop, reviewers apply line-level fixes in place… In the design loop the author owns every edit to the design doc; the reviewer only reports."*

#### M4 — The model requirement was dropped entirely

**CONFIRMED (dropped clause).** Source: `design-review.md:30` "*Phase 2 — Adversarial reviewer (**Opus**, background, keep open)*"; `subagent-loop-playbook.md:17-18` "*Author subagent (**Opus**)*" / "*Review subagent (**Opus**, fresh context)*"; chess `CLAUDE.md` "*Run long-running **opus** subagents in the background*".

```
$ grep -rniE "\b(opus|sonnet|haiku|strongest model|model)\b" skills/ docs/ README.md | grep -viE "model that|data model|consistency model"
EXIT=1   # zero matches
```

The plugin contains **no model guidance anywhere**. Every other operational parameter of the loop survived the port (background execution, persistence, agent type `general-purpose`) — this one did not.

**Failure scenario.** A user configures a cheap default model for subagents (or the harness picks one). The adversarial reviewer, whose entire value is finding the class of defects that "survive every mechanical gate" (`playbook.md:52`), runs on a model that cannot trace a grandchild-process kill through a test harness. It returns SHIP. Every gate in the methodology is now a rubber stamp, and nothing in the plugin tells anyone this is what went wrong.

**Minimal fix.** Add to `playbook.md` §5 or §8: *"Author and reviewer agents run on the strongest model available in the environment. The adversarial reviewer especially — its entire yield is the defect classes that mechanical gates miss, and that yield is model-dependent."*

#### M5 — Stage 2 depends on an artifact-publishing capability it never checks for, and Stages 3–4 hard-depend on the resulting URL

**CONFIRMED.** `skills/wireframes/SKILL.md:47-59`, consumed at `skills/design-loop/SKILL.md:39` and `skills/implementation-loop/SKILL.md:86`.

The wireframes skill mandates *"one **published** artifact… One page, **one URL**"* (`:49`), and its exit gate (`:13`) requires *"the published artifact **URL** is recorded in the project's `CLAUDE.md`"*. Downstream, the design-loop author brief requires *"**The wireframe artifact URL**, with the note that numbered callouts are binding"* (`design-loop:39`) and every implementation author brief requires *"the wireframe artifact URL for anything user-facing"* (`implementation-loop:86`).

Nothing checks that artifact publishing is available. Note the contrast: `wireframes:17` *does* defensively guard the `frontend-design` skill (*"if it is available in this environment"*) — the author knew to do this and did not apply it to the load-bearing dependency.

**Failure scenario.** A user on a Claude Code install without artifact publishing reaches Stage 2. The model either invents a URL, or produces a local HTML file and calls it "the artifact" — after which Stage 3's brief points at a path the design author's sandbox cannot open, and the binding-callout mechanism (the thing that makes the whole stage load-bearing) silently degrades to "whatever the implementer remembered".

**Minimal fix.** In `wireframes:47`, add a fallback: *"If artifact publishing is unavailable, produce a single self-contained HTML file at a stable committed path and use that path everywhere this doc says 'URL'. The requirement is one page, one stable identity — not the hosting."* Mirror the wording in `design-loop:39` and `implementation-loop:86`.

#### M6 — The README instructs the novice to ignore the one signal that would reveal a failed install

**CONFIRMED (claim is false).** `README.md:53`.

> *"Don't worry if it says `0 skills` — that counter doesn't cover this plugin's kind of skills."*

This plugin's components are **exclusively** skills. Verified against the running build:

```
$ claude --plugin-dir /Users/jasonou/code/claude-app-bootstrap plugin details app-bootstrap
Component inventory
  Skills (5)  design-loop, e2e-review, implementation-loop, product-discovery, wireframes
  Agents (0)   Hooks (0)   MCP servers (0)   LSP servers (0)
```

There is no other "kind of skill" here for the counter to be missing. If a reload genuinely reports `0 skills` for this plugin, the plugin did not load — which is exactly the failure the novice needs to catch at Step 3.

**Failure scenario.** Install silently fails (untrusted workspace, stale cache, wrong scope). Reload prints `0 skills`. The reader, per the README, ignores it, proceeds to Step 4, types `/app-bootstrap:product-discovery`, gets "unknown command", and has no idea the README already told them to ignore the diagnosis.

**Minimal fix.** Invert it: *"You should see 5 skills reloaded. If it says `0 skills`, the plugin did not load — go back to Step 2."*

---

### MINOR

#### m1 — Skill descriptions carry no trigger language and open with a meaningless ordinal

**CONFIRMED.** All five `SKILL.md` frontmatter `description:` fields, e.g. `product-discovery:2` — *"Stage 1 — interrogate a product idea in conversation until requirements stabilize…"*.

In a flat skill listing (which is how the model sees them — verified: they surface as `app-bootstrap:product-discovery` … `app-bootstrap:e2e-review`), "Stage 1" has no referent. More importantly, none of the five say **when to use it**. Every high-quality skill description in the installed corpus is trigger-shaped ("*When the user wants to…*", "*Also use when the user mentions…*"). These are capability descriptions, so the model will rarely select them autonomously; they work only when typed as slash commands.

**Fix.** Prefix each with its trigger, e.g. *"Use when the user has a product idea and no requirements doc yet — Stage 1 of the app-bootstrap methodology: interrogate the idea until…"*.

#### m2 — Unlabeled invented number, in violation of the plugin's own rule 6

**CONFIRMED.** `docs/playbook.md:71` vs `skills/implementation-loop/SKILL.md:77`.

> playbook:71 — *"Retire it and start a fresh author only when its context approaches exhaustion (**roughly 500k tokens**)…"*
> implementation-loop:77 — *"Where a number is currently an estimate, **label it as one, in the artifact, at the point of use**."*

`500k` appears in neither `design-review.md` nor `subagent-loop-playbook.md` nor the chess `CLAUDE.md` — it is new to this port. It is also ambiguous (cumulative tokens consumed? context occupancy? — the latter is impossible for most windows) and unmeasured, which is exactly the "estimate presented as fact" that gate-honesty rule 6 exists to stop. The playbook breaking its own rule is a credibility problem for a doc whose whole authority is "these rules exist because a defect got through without them".

**Fix.** *"…only when its context approaches exhaustion. (No measured threshold exists yet; treat 'the author is starting to lose earlier rounds' as the signal and record the number when you measure it.)"*

#### m3 — Three general rules from the chess `CLAUDE.md` Agent Workflow Policy were dropped without replacement

**CONFIRMED (dropped clauses).** None of these is project-specific; all three generalize cleanly and none appears in the plugin (`grep` over `skills/ docs/ README.md`):

1. *"Do not commit or push unless explicitly requested."* — most consequential for this plugin, where Stage 4 has author agents writing files across a whole repo unattended.
2. *"Do NOT delegate test runs to subagents for concurrency."* — a specific, hard-won anti-pattern; the plugin's §7 delegation economics discusses briefing-cost vs edit-cost but never this case.
3. *"Prefer editing existing files over creating new ones."*

**Fix.** Add all three to `playbook.md` §4 (subagent discipline) or a new "coordinator hygiene" bullet set in §7.

#### m4 — Cross-skill references with no resolvable path

**CONFIRMED.** `skills/product-discovery/SKILL.md:37` (*"see the precision-and-recall rule in the implementation-loop skill"*) and `skills/e2e-review/SKILL.md:44` (*"Gate-honesty rules 1, 3 and 5 from the implementation-loop skill apply unchanged"*).

Every playbook reference in this repo is a working relative link; these two are bare prose. A Stage-1 or Stage-5 reader has not loaded `implementation-loop` and is given no path to it.

**Failure scenario.** The e2e reviewer, told that "rules 1, 3 and 5 apply unchanged", cannot read rules 1, 3 and 5 — and either invents them or drops them. Given that §44 calls this "the highest-value sweep", losing it defeats the stage.

**Fix.** Link them (`../implementation-loop/SKILL.md`), or better — since the playbook already exists for exactly this purpose (`playbook.md:3`, *"Each skill points here rather than restating these rules"*) — move the six gate-honesty rules into `docs/playbook.md` as §10 and have implementation-loop point at them like everything else.

#### m5 — `claude plugin validate` is presented as verification but covers none of the content

**CONFIRMED by running it.**

```
$ claude plugin validate .
Validating marketplace manifest: …/.claude-plugin/marketplace.json
✔ Validation passed

$ claude plugin validate . --strict
Validating marketplace manifest: …/.claude-plugin/marketplace.json
✔ Validation passed

$ claude plugin validate .claude-plugin/plugin.json
Validating plugin manifest: …/.claude-plugin/plugin.json
✔ Validation passed
```

Note what it printed: *manifest*. It never opened `skills/`. `README.md:221` lists it under "Develop against it locally" with no caveat, implying a green check means the plugin is sound. It means two JSON files parse.

**Fix.** One line at `README.md:222`: *"`validate` checks the manifests only — it does not read `skills/`. Use `claude plugin details app-bootstrap` (with `--plugin-dir`) to confirm all five skills actually load."*

#### m6 — No version or update story

**CONFIRMED.** `.claude-plugin/marketplace.json:9-15` has no `version` field on the plugin entry; `README.md` never mentions `/plugin marketplace update`, `claude plugin tag`, or how a consumer pins or upgrades. `plugin.json` carries `0.1.0` but nothing surfaces it to a user and nothing states a stability policy — notable when one of five stages ships as an explicit STUB.

**Failure scenario.** A team wires the plugin into `.claude/settings.json` per `README.md:197-213`. The upstream repo changes the SHIP/ONE-MORE-ROUND semantics. Collaborators are on silently divergent doctrine with no version to compare and no documented refresh command.

**Fix.** Add `"version": "0.1.0"` to the marketplace entry, a one-line "Updating" subsection (`/plugin marketplace update claude-app-bootstrap` then `/reload-plugins`), and a sentence noting 0.x means the stage contracts may change — Stage 5 especially.

#### m7 — The universal reviewer template demands artifacts that only exist in the design loop

**CONFIRMED.** `docs/playbook.md:50`, scoped by `:43` (*"Every reviewer brief carries all six of these"*).

> `6. **Ledger obligations.** A requirement scorecard (R1..Rn…), **a verdict per Departure (uphold / reverse / amend)**…`

"Departures" is a Stage-1/Stage-3 construct (`product-discovery:47`, `design-loop:37`). An implementation-phase reviewer and an e2e-journey reviewer have no Departures section to adjudicate. In the source this obligation lived only in `design-review.md:37`, correctly scoped.

**Fix.** Mark it conditional: *"…and, where the artifact under review has a Departures section, a verdict per Departure."*

---

### NIT

- **n1 — `argument-hint` is a command-only frontmatter field.** All five SKILL.md files carry it (e.g. `design-loop:3`). Across all 60 installed skills on this machine the frontmatter keys are `name` (60), `description` (60), `metadata` (54), `allowed-tools` (3), `license` (1) — `argument-hint` appears **only** in `commands/*.md`. Harmless (the runtime tolerates it, and `$ARGUMENTS` interpolation *does* work in skills — verified, see G3), but non-conventional. Relatedly, `name:` is absent from all five while 60/60 installed skills carry it; the directory name is used as fallback, so this works, but it is a deviation.
- **n2 — `README.md:180`** gives `/plugin marketplace add ./claude-app-bootstrap`, which is wrong if the reader is standing inside the repo (should be `.`). Line 184 explains the general rule, but the copy-pasteable line is the one people paste.
- **n3 — `plugin.json` has no `homepage` or `repository` field.** `--strict` tolerates it; it means an installed user has no path back to the source.
- **n4 — The onboarding prompt is a 45-line paste presented as "copy and paste this" (`README.md:73-124`)** with no note about multi-line paste behavior in a terminal prompt. A novice pasting this may submit on the first newline and send only `I've installed the app-bootstrap Claude Code plugin…`. Worth one sentence.

---

## What it got right

- **G1 — The interface-consumer exercise survived intact, rationale and all.** `design-loop:51-55` preserves the mechanism, the "why reading isn't enough" argument, *and* the concrete BLOCKER anecdote from `design-review.md:40`. This was the single clause most at risk in a generalization pass and it came through stronger (generalized off "TypeScript" without losing force).
- **G2 — It resolved a real ambiguity in the source.** `design-review.md:32` says the reviewer is *continued across all rounds*; `subagent-loop-playbook.md:18` says the review subagent has *fresh context*. The source never reconciles these. `playbook.md:72-73` does, cleanly and correctly: *"The reviewer is persistent across rounds within a loop… A fresh reviewer starts each new loop or phase. Fresh eyes per unit of work; continuity within it."* That is an improvement on the source, not a port.
- **G3 — The mechanics actually work.** Verified against the running build (2.1.226) with `--plugin-dir`: all five skills load and namespace correctly (`app-bootstrap:product-discovery` … `app-bootstrap:e2e-review`); `$ARGUMENTS` **does** interpolate in a skill body (probe with `args='ZZTESTARGZZ'` returned `Run the full adversarial design-review workflow for a major design: **ZZTESTARGZZ**`, with no literal `$ARGUMENTS` remaining); and the relative playbook link resolves — the runtime prepends `Base directory for this skill: /…/claude-app-bootstrap/skills/design-loop`, so `../../docs/playbook.md` → `/…/claude-app-bootstrap/docs/playbook.md`, and the Read succeeded. Path arithmetic checks out: `skills/design-loop` → `..` = `skills/` → `../..` = repo root → `docs/playbook.md`. ✓
- **G4 — The README's UI strings are verbatim-accurate.** `Plugin is now active.`, `Run /reload-plugins to activate.`, `/reload-plugins --force`, `/plugin list`, `/plugin marketplace add <path/url>` all appear verbatim in the 2.1.226 binary. Someone checked rather than guessed. (M6 is the one exception, and it is a claim *about* output rather than a quotation of it.)
- **G5 — Zero chess leakage in the skills.** Receipt:
  ```
  $ grep -rniE "\b(chess|stockfish|fsrs|pgn|fen|elo|lichess|happylamp|multipv|blunder|opening line|postmortem|dynamodb|localstack|lerna|fastify|zustand|jest|npm run|nvm)\b" skills/
  EXIT=1   # no matches
  ```
  The only domain references anywhere are the two deliberate provenance notes (`README.md:248`, `docs/playbook.md:127`), which are the right call — they are what makes the rules credible.
- **G6 — The six gate-honesty rules are faithful to `HANDOFF.md` §5 and generalized without dilution.** Rule 1's `npx`-grandchild anecdote, the "five consecutive phases" count (Phases 2–6 — checked), rule 2's "two wrong rules reached the design doc as corrections", rule 3's vacuous-pin case, rule 5's three inversions — every specific traces to the source and every one survived the generalization with its teeth in. Rule 3's added paragraph on the fixture that makes the branch unreachable is a correct lift of the Phase 6 case.
- **G7 — The STUB banner on `e2e-review` is exemplary honesty.** `e2e-review:8-12` refuses to let the unvalidated stage masquerade as methodology, and §"Open questions" names five real ones. This is what rule 6 (label estimates as estimates) looks like applied to a whole skill.
- **G8 — The CLAUDE.md-preservation half of the onboarding prompt is genuinely defensive.** `README.md:114-121` — preserve everything, no-CLAUDE.md branch, show the exact diff, wait for approval, don't write until told yes. Two of the four defensive requirements are met well; M1 and M2 are what breaks the other two.

---

## Completion checklist

| # | Item | Status |
| :-- | :-- | :-- |
| 1 | Fidelity diff against all three source docs, per-clause receipts for dropped/weakened clauses | **PASS** — `design-review.md` diffed clause by clause (Phase 0–Exit; drops: M4 model requirement, provenance line — the latter deliberate and covered in README History); `subagent-loop-playbook.md` diffed (M3 scope inversion found; §5 reconciliation noted as an improvement, G2); chess `CLAUDE.md` Agent Workflow Policy diffed (m3, three dropped general rules); `HANDOFF.md` §5 diffed against the six gate-honesty rules (G6, faithful). |
| 2 | `claude plugin validate` + `--strict` run and quoted; playbook path resolution verified by actual arithmetic | **PASS** — all three invocations quoted in m5; both passed, and the output proves they cover manifests only. Path arithmetic done and confirmed empirically against the runtime's `Base directory` line (G3). |
| 3 | README walked step by step as a novice; every command checked for typeability; onboarding prompt assessed against its four defensive requirements | **PASS** — Steps 1–4 walked; Step 1 fails (B1), Step 3's guidance is inverted (M6), Steps 2 and 4 check out against verbatim binary strings (G4). Onboarding prompt: self-contained ✗ (M2), defensive re existing CLAUDE.md ✓ (G8), shows diff ✓, waits for approval ✓; plus an unperformable instruction (M1) and a paste-mechanics gap (n4). |
| 4 | Chess-leakage grep over `skills/` with pattern and result shown | **PASS** — pattern and `EXIT=1` result quoted in G5; a broader sweep over `docs/` and `README.md` surfaced only the two intentional provenance lines. |
| 5 | `REVIEW.md` written to the repo, newest-first, identical to the returned report | **PASS** — this file; Round 1 is the only round and the newest-first convention is stated at the top. |
| 6 | Verdict is exactly one of {SHIP, ONE MORE ROUND} | **PASS** — see below. |

---

## Verdict

**ONE MORE ROUND**
