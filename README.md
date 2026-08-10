# app-bootstrap

A Claude Code plugin that packages a five-stage methodology for taking an app from an idea to shipped, reviewed code.

It is opinionated on purpose. Every rule in it exists because something went wrong without it.

---

# Part 1 — For everyone

*No git, plugin, or Claude Code experience assumed. If you know all that already, skip to [Part 2](#part-2--technical-reference).*

## What this gives you

Five stages, in order. Think of it as five conversations with Claude, each one ending with **you** saying yes.

1. **Talk through your product idea.** Claude interrogates the idea with you — what it does, who it's for, what happens when things go wrong — and writes it up as a requirements document. Technical concepts get explained to you from scratch until you can argue with them. When you push back, Claude doesn't debate you about taste; it turns your objection into a question it can go measure.
2. **See what it will look like.** Claude draws every screen of your app as a web page you can open in your browser: the main screens, the empty ones, the error ones. Every rule that isn't obvious from the picture gets a numbered note next to it. Those notes become binding — later on, "the app does X here" is settled by looking at this page.
3. **Approve an engineering design.** Claude writes a technical design, then a *second* Claude attacks it looking for holes. They go back and forth until the attacker says the design is sound. Anything they disagree about comes to you as a plain-language explanation with options. Then you approve it — or you don't.
4. **Watch it get built, in reviewed phases.** The build is split into phases. Each phase: one Claude writes it, a fresh Claude attacks it, they iterate until it holds up. Then you see what shipped before the next phase starts.
5. **Final testing in a real browser.** Claude drives your actual running app through the journeys from step 2. *(This stage is still a work in progress — see the note in the skill.)*

**The one rule that matters: each stage ends with you approving it before the next one begins.** Nothing gets designed before you sign off on the requirements. Nothing gets built before you sign off on the design. That is the whole point — the methodology's job is to make sure you're never surprised by what got built.

## Install it, step by step

You need Claude Code installed and working. The three commands below get typed in a **terminal** (the same place you'd type `claude` to start Claude Code) — not inside a Claude conversation. This route is fully verified; an alternative from inside Claude Code follows.

**Step 1 — Tell Claude Code where to find this plugin.**

```
claude plugin marketplace add jasonou1994/claude-app-bootstrap
```

*What you should see:* `✔ Successfully added marketplace: claude-app-bootstrap`. If you get an error about the repository not being found, use the local-folder method: download or clone this repo somewhere, then run the same command with the folder's path instead, e.g. `claude plugin marketplace add ~/code/claude-app-bootstrap`.

**Step 2 — Install the plugin.**

```
claude plugin install app-bootstrap@claude-app-bootstrap
```

*What you should see:* `✔ Successfully installed plugin: app-bootstrap@claude-app-bootstrap (scope: user)`. User scope means it's available in all your projects, which is what you want.

**Step 3 — Check it worked.**

```
claude plugin list
```

*What you should see:* `app-bootstrap@claude-app-bootstrap` with `Status: ✔ enabled`. (For a detailed view — its five skills and what they cost per session — `claude plugin details app-bootstrap`.)

Now start (or restart) Claude Code in your project: a session picks up newly installed plugins when it starts, so a conversation that was already open won't see it until you begin a new one.

**Alternative — from inside Claude Code:** the same commands exist as *slash commands* at the conversation prompt: `/plugin marketplace add jasonou1994/claude-app-bootstrap`, then `/plugin install app-bootstrap@claude-app-bootstrap`, then `/plugin list` to confirm. These are interactive — follow the prompts, and if asked to choose a scope, pick **User**.

The five stages are now available as slash commands. They're named with the plugin's name in front, like this:

- `/app-bootstrap:product-discovery`
- `/app-bootstrap:wireframes`
- `/app-bootstrap:design-loop`
- `/app-bootstrap:implementation-loop`
- `/app-bootstrap:e2e-review`

Type `/app` and Claude Code will offer to complete them for you, so you don't have to memorize this.

## Set up your project (copy and paste this)

Your project can have a file called `CLAUDE.md` — a note that Claude reads automatically every time it works in that folder. Adding the methodology to it means Claude follows these stages without you having to remind it.

**Paste this into Claude Code inside your project.** It is long and multi-line: paste the whole block in one go. Most terminals handle a bracketed paste correctly, but if yours submits at the first newline and sends only the opening sentence, press **Esc** to clear, then either paste it into an editor and use `/paste`, or save it to a file and tell Claude to read that file.

```text
I've installed the `app-bootstrap` Claude Code plugin and I want this repository set up to use it.

Do the following, in order:

1. Check the plugin is actually installed and enabled: run `claude plugin list` in
   the shell and tell me what you find. If `app-bootstrap` is not there, walk me
   through installing it one step at a time — tell me exactly what to type in my
   terminal, wait for me to tell you what I saw, and only then give me the next
   step. The install steps are: add the marketplace (`claude plugin marketplace add
   jasonou1994/claude-app-bootstrap`, or a local folder path if I have the repo
   cloned), then `claude plugin install app-bootstrap@claude-app-bootstrap`, then
   confirm with `claude plugin list`. Remind me the skills only appear in sessions
   started after the install. Do not continue to step 2 until the plugin is
   confirmed installed.

2. Read this repository — its README, its existing CLAUDE.md if there is one, its
   folder structure, its package/build files — enough to describe what it actually
   is and how it's actually built. I want the next step tailored to THIS repo, not
   generic boilerplate.

3. Read the plugin's own docs before writing anything — NOT from this repository,
   which does not contain them. Find the installed plugin first: search under
   ~/.claude/plugins/ for a directory named `app-bootstrap` that contains
   `skills/` and `docs/playbook.md` (e.g. `find ~/.claude/plugins -type d -name
   app-bootstrap`). Then read its five `skills/*/SKILL.md` files and its
   `docs/playbook.md` from there, and use what they actually say. If you cannot
   find them, STOP and tell me — do not write the next step from memory.

4. Propose an addition to this repository's CLAUDE.md: a section that references the
   five stage-skills by their exact slash-command names
   (/app-bootstrap:product-discovery, /app-bootstrap:wireframes,
   /app-bootstrap:design-loop, /app-bootstrap:implementation-loop,
   /app-bootstrap:e2e-review), says what each one produces for THIS project
   specifically, and states the gate rules plainly:
     - every stage ends with my explicit sign-off before the next one starts;
     - the design loop must reach a plain SHIP verdict AND my approval before any
       implementation begins;
     - implementation runs one author-plus-adversarial-reviewer loop per phase.
   Also add pointers to wherever this project's requirements doc and wireframe
   artifact will live.

IMPORTANT — how to handle my CLAUDE.md:
   - PRESERVE everything already in it. This is an addition, not a rewrite. Do not
     reorder, reword, condense, or "clean up" any existing content, even if you think
     it's redundant or wrong — tell me about it instead and let me decide.
   - If there is no CLAUDE.md, say so and propose a new one containing only the new
     section plus a brief description of this repo.
   - SHOW ME THE EXACT DIFF before saving anything — the precise lines you intend to
     add and where. Then WAIT for me to approve it. Do not write the file until I say yes.

Start with step 1 and tell me what you find.
```

## Your typical first session

1. Open your project in Claude Code.
2. Paste the onboarding prompt above. Answer its questions; approve the CLAUDE.md diff when it shows you one.
3. Type `/app-bootstrap:product-discovery` and start describing your idea in your own words. Claude will start asking you questions — including annoying ones about what happens when things go wrong. That's the stage working.
4. Keep going until Claude hands you a requirements document. Read it. Argue with it. Sign it off when it's right.
5. Type `/app-bootstrap:wireframes` and repeat: look at the drawings, argue, sign off.
6. Then `/app-bootstrap:design-loop`, and so on down the list.

Expect stage 1 to take longer than you think it should. That's where the value is.

---

# Part 2 — Technical reference

## The five stages and their exit gates

| Stage | Skill | Produces | Exit gate |
| :-- | :-- | :-- | :-- |
| 1 | `/app-bootstrap:product-discovery` | Requirements doc: hard requirements `R1..Rn` split from the negotiable baseline, plus a dated product-decisions log | Maintainer signs off the requirements doc |
| 2 | `/app-bootstrap:wireframes` | One published artifact covering every surface, with numbered callouts carrying binding semantics | Maintainer sign-off; artifact URL recorded in the project `CLAUDE.md` as the UI source of truth |
| 3 | `/app-bootstrap:design-loop` | Design doc + full review trail | Plain **SHIP** from the adversarial reviewer, then a separate maintainer approval gate |
| 4 | `/app-bootstrap:implementation-loop` | Shipped code, phase by phase | Plain **SHIP** per phase, plus the coordinator's independent spot-check |
| 5 | `/app-bootstrap:e2e-review` | Browser-driven journey results | **STUB** — shape defined, not yet validated |

Shared doctrine for all five lives in [`docs/playbook.md`](docs/playbook.md): two-loop sequencing, the adversarial briefing template, persistent-author/reviewer continuation rules, the maintainer four-part walkthrough format, the SHIP / ONE MORE ROUND verdict vocabulary, delegation economics, and background-agent hygiene. Each skill points at it rather than restating it.

## Repository layout

```
claude-app-bootstrap/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest
│   └── marketplace.json     # makes this repo its own single-plugin marketplace
├── docs/
│   └── playbook.md          # shared doctrine, referenced by every skill
├── skills/
│   ├── product-discovery/SKILL.md
│   ├── wireframes/SKILL.md
│   ├── design-loop/SKILL.md
│   ├── implementation-loop/SKILL.md
│   └── e2e-review/SKILL.md
└── README.md
```

Per the [plugins reference](https://code.claude.com/docs/en/plugins-reference), only `plugin.json` lives inside `.claude-plugin/`; every component directory (`skills/`) sits at the plugin root. Skills are directories containing a `SKILL.md`, and the directory name becomes the skill name, namespaced by the plugin name — so `skills/design-loop/` surfaces as `/app-bootstrap:design-loop`.

The marketplace entry uses `"source": "./"`, the documented pattern for a repository that is both the marketplace and the plugin.

## Install

Both forms exist as terminal commands (`claude plugin …`) and as slash commands (`/plugin …`) inside a session. The terminal form is non-interactive and is what the step-by-step guide above uses.

### From GitHub

```
claude plugin marketplace add jasonou1994/claude-app-bootstrap
claude plugin install app-bootstrap@claude-app-bootstrap
```

Other git hosts take the full URL including the `https://` prefix and the `.git` suffix, e.g. `claude plugin marketplace add https://gitlab.com/you/claude-app-bootstrap.git`.

### From a local path

```
claude plugin marketplace add ./claude-app-bootstrap
claude plugin install app-bootstrap@claude-app-bootstrap
```

The path may be any directory containing `.claude-plugin/marketplace.json`, absolute or relative — use `.` if you are standing inside the repository itself — or a direct path to the `marketplace.json` file.

### Updating

```
claude plugin marketplace update claude-app-bootstrap
```

Then start a new session to pick up the new version. The plugin pins `"version"` in both `plugin.json` and its marketplace entry, so consumers only move when that field is bumped.

**Stability:** this is `0.x`. The stage contracts may change between versions — Stage 5 (`e2e-review`) especially, which ships as an explicit stub. No release tags have been cut yet, so there is currently nothing to pin to; a team that needs doctrine which cannot move under them should vendor the repo and add it from a local path.

### Enable in a project

`/plugin install` offers **User**, **Project**, and **Local** scope; **Project** scope writes the plugin into the repository's `.claude/settings.json` so collaborators get it. To wire it up for a team without an interactive install, declare the marketplace and the plugin in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "claude-app-bootstrap": {
      "source": {
        "source": "github",
        "repo": "jasonou1994/claude-app-bootstrap"
      }
    }
  },
  "enabledPlugins": {
    "app-bootstrap@claude-app-bootstrap": true
  }
}
```

Collaborators are prompted to install it when they trust the repository folder. Plugins load at session start, so a session that was already open when the plugin was installed won't see it — start a new session.

### Develop against it locally

```
claude --plugin-dir ./claude-app-bootstrap
claude plugin validate ./claude-app-bootstrap/.claude-plugin/plugin.json
claude --plugin-dir ./claude-app-bootstrap plugin details app-bootstrap
```

`--plugin-dir` loads the plugin without installing it and takes precedence over an installed copy of the same name for that session. Edits to skill files are picked up at the next session start.

**Which check covers what** — verified against Claude Code 2.1.226 by injecting a YAML frontmatter defect into a skill and re-running each form:

| Command | What it actually reads |
| :-- | :-- |
| `claude plugin validate .` (repo root) | **Marketplace manifest only.** Because this repo contains `.claude-plugin/marketplace.json`, `validate` resolves it as a marketplace and never opens `skills/`. It printed `✔ Validation passed` with a broken skill on disk. |
| `claude plugin validate .claude-plugin/plugin.json` | Plugin manifest **and every skill's frontmatter**. This is the form that caught the injected defect: `❯ frontmatter: YAML frontmatter failed to parse`. Skill lines print only on error. |
| `claude --plugin-dir . plugin details app-bootstrap` | What actually loads at runtime — the component inventory (`Skills (5) …`) and per-skill token cost. The only check that proves all five skills load. |

The trap worth knowing: a green `claude plugin validate .` on this repo means two JSON files parse. It is not evidence about the skills. A frontmatter error is otherwise silent — the runtime loads the skill with *empty metadata*, dropping its description, so it simply stops surfacing.

## Referencing the stages from a project's CLAUDE.md

A project adopting this methodology should carry a short section like:

```markdown
## Build methodology — app-bootstrap

This project is built with the `app-bootstrap` plugin's five stages. Each stage
exits only on the maintainer's explicit sign-off.

1. `/app-bootstrap:product-discovery` → requirements doc at `docs/requirements.md`
   (hard requirements R1..Rn vs. negotiable baseline; dated decisions log).
2. `/app-bootstrap:wireframes` → UI source of truth: <artifact URL>. Numbered
   callouts carry binding semantics.
3. `/app-bootstrap:design-loop` → design doc in `docs/`. Implementation begins only
   after a plain SHIP verdict AND maintainer approval.
4. `/app-bootstrap:implementation-loop` → one author + adversarial-reviewer loop per
   phase, each to a plain SHIP.
5. `/app-bootstrap:e2e-review` → browser journey testing (stub).

Doctrine: the plugin's `docs/playbook.md`. Verdict vocabulary is SHIP or ONE MORE
ROUND, nothing else.
```

## History

Distilled from how the Postmortem chess-trainer project was actually built: a design loop of four adversarial rounds plus a product-coverage audit, then six implementation phases, ~140 findings raised and closed. The six gate-honesty rules in the implementation-loop skill each trace to a specific defect that a green gate certified — most notably a fault-injection gate that killed a process shim while the real work ran uninterrupted in a grandchild, a failure class that recurred in five consecutive phases before the countermeasures went in.

## License

MIT.
