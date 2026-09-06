# app-bootstrap

A Claude Code plugin that packages a five-stage methodology (six skills; stage 1 has two halves) for taking an app from an idea to shipped, reviewed code.

Most of its rules were adopted after a specific failure. The History section records which.

---

# Part 1: For everyone

Part 1 assumes no experience with git, plugins, or Claude Code. Part 2 is the [technical reference](#part-2-technical-reference).

## The five stages

The methodology has five stages. Each one ends when you approve its output.

1. **Product discovery.** Claude asks what the product does, who uses it, and what happens when things go wrong, then writes the answers up as a requirements document. Technical concepts are explained from first principles until you can challenge them. When you challenge a technical choice, Claude converts the objection into a question it can measure instead of arguing the point.
   - **1b. User journeys.** A second Claude, kept away from the product's own documents, writes down at least eight kinds of person who might use it (you are one of them, and so is someone using a screen reader) and what each of them walks through: the first run, the daily loop, the day the product is wrong. Those walks are then held against the requirements (or, on a product that already exists, against what is built) and every step is marked served, awkward or missing. A third Claude reviews the result adversarially. You get one page, a map, with every number counted from the register, and you decide what it changes about the plan. The map never changes the plan by itself.
2. **Wireframes.** Claude draws every screen of your app as a web page you can open in a browser, including the empty screens and the error screens. Each behavior the drawing does not make obvious gets a numbered note. Those notes are binding: later stages settle questions about the interface by reading this page.
3. **Design review.** Claude writes a technical design. A chain of fresh Claudes then reviews it adversarially, each fixing what it finds in place, until one changes nothing. Disagreements come to you as a written explanation with options and their costs. Implementation waits for your approval.
4. **Implementation.** The build runs in phases. In each phase one Claude writes the code, then a chain of fresh Claudes reviews it adversarially, each replaying the tests' injections and fixing what it finds, until one changes nothing. You see what shipped before the next phase starts.
5. **End-to-end review.** Claude drives the running app through the journeys defined in stage 2. This stage is a stub, and the skill file marks it as unvalidated.

Each stage ends with your approval before the next one begins. Requirements are signed off before design starts. The design is approved before implementation starts.

## Install the plugin

These steps require Claude Code, installed and working. Type the three commands below in a terminal, the same place you type `claude` to start Claude Code, rather than inside a Claude conversation. An alternative route from inside Claude Code follows them.

**Step 1. Tell Claude Code where to find this plugin.**

```
claude plugin marketplace add jasonou1994/claude-app-bootstrap
```

Expected output: `✔ Successfully added marketplace: claude-app-bootstrap (declared in user settings)`. If you get an error about the repository not being found, use the local-folder method: download or clone this repo somewhere, then run the same command with the folder's path instead, e.g. `claude plugin marketplace add ~/code/claude-app-bootstrap`.

**Step 2. Install the plugin.**

```
claude plugin install app-bootstrap@claude-app-bootstrap
```

Expected output: `✔ Successfully installed plugin: app-bootstrap@claude-app-bootstrap (scope: user)`. User scope makes the plugin available in all your projects.

**Step 3. Check it worked.**

```
claude plugin list
```

Expected output: `app-bootstrap@claude-app-bootstrap` with `Status: ✔ enabled`. For a detailed view of the six skills and their per-session token cost, run `claude plugin details app-bootstrap`.

Now start Claude Code in your project, or restart it. A session picks up newly installed plugins when it starts, so a conversation that was already open will not see the plugin until you begin a new one.

**Alternative: from inside Claude Code.** The same commands exist as slash commands at the conversation prompt: `/plugin marketplace add jasonou1994/claude-app-bootstrap`, then `/plugin install app-bootstrap@claude-app-bootstrap`, then `/plugin list` to confirm. These are interactive, so follow the prompts, and choose **User** if asked for a scope. On this route the install reports whether it took effect. If it says `Plugin is now active.`, the plugin is loaded. If it says `Run /reload-plugins to activate.`, type that command. Starting a new session also works.

The five stages are now available as slash commands, each prefixed with the plugin's name:

- `/app-bootstrap:product-discovery`
- `/app-bootstrap:user-journeys`
- `/app-bootstrap:wireframes`
- `/app-bootstrap:design-loop`
- `/app-bootstrap:implementation-loop`
- `/app-bootstrap:e2e-review`

Typing `/app` brings up the completions.

## Set up your project

A file named `CLAUDE.md` in your project is read by Claude at the start of every session in that folder. Recording the methodology there is what makes Claude follow the stages without being told each time.

Paste the block below into Claude Code inside your project. It is long and spans many lines, so paste it in one go. Most terminals handle a bracketed paste correctly. If yours submits at the first newline and sends only the opening sentence, press **Esc** to clear, then either paste it into an editor and use `/paste`, or save it to a file and tell Claude to read that file.

```text
I've installed the `app-bootstrap` Claude Code plugin and I want this repository set up to use it.

Do the following, in order:

1. Check the plugin is actually installed and enabled: run `claude plugin list` in
   the shell and tell me what you find. If `app-bootstrap` is not there, walk me
   through installing it one step at a time. Tell me exactly what to type in my
   terminal, wait for me to tell you what I saw, and only then give me the next
   step. The install steps are: add the marketplace (`claude plugin marketplace add
   jasonou1994/claude-app-bootstrap`, or a local folder path if I have the repo
   cloned), then `claude plugin install app-bootstrap@claude-app-bootstrap`, then
   confirm with `claude plugin list`. Remind me the skills only appear in sessions
   started after the install. Do not continue to step 2 until the plugin is
   confirmed installed.

2. Read this repository: its README, its existing CLAUDE.md if there is one, its
   folder structure, its package/build files, enough to describe what it actually
   is and how it's actually built. I want the next step tailored to THIS repo, not
   generic boilerplate. If the repository is brand-new, empty, or nearly so, say
   that plainly and ask me what it is going to be, then describe the intended
   project from what I tell you. Do NOT invent a characterization to satisfy this
   step.

3. Read the plugin's own docs before writing anything, and NOT from this
   repository, which does not contain them. Locate the installed copy by searching
   for the file itself, not for a directory:
       find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins -path '*app-bootstrap*' -name playbook.md
   Use that exact form. A hardcoded ~/.claude searches the wrong tree whenever
   CLAUDE_CONFIG_DIR is set, and can return a confident hit belonging to some
   other install. Two notes on reading the results:
     - Prefer a hit under plugins/cache/ over one under plugins/marketplaces/.
       The cache copy IS the installed plugin; the marketplaces copy is only the
       checkout of the catalog repo, and has no version directory.
     - The cache tree sits under a VERSION directory, like
       .../app-bootstrap/0.2.0/docs/playbook.md, so searching for a DIRECTORY
       named `app-bootstrap` lands one level too high and finds no `skills/`
       there. If several versions come back (each update adds one), take the
       highest.
   Read that playbook.md, then read the six SKILL.md files from its grandparent
   directory, at <version>/skills/*/SKILL.md. Use what they actually say. If you
   cannot find them, STOP and tell me. Do not write the next step from memory.

4. Propose an addition to this repository's CLAUDE.md: a section that references the
   six stage-skills by their exact slash-command names
   (/app-bootstrap:product-discovery, /app-bootstrap:user-journeys, /app-bootstrap:wireframes,
   /app-bootstrap:design-loop, /app-bootstrap:implementation-loop,
   /app-bootstrap:e2e-review), says what each one produces for THIS project
   specifically, and states the gate rules plainly:
     - every stage ends with my explicit sign-off before the next one starts;
     - the design loop must close (a pass that changes nothing) AND get my approval
       before any implementation begins;
     - implementation runs one author plus a chain of fresh adversarial passes per phase.
   Also add pointers to wherever this project's requirements doc and wireframe
   artifact will live.

IMPORTANT: how to handle my CLAUDE.md.
   - PRESERVE everything already in it. This is an addition, not a rewrite. Do not
     reorder, reword, condense, or "clean up" any existing content. If you think
     something in it is redundant or wrong, tell me and let me decide.
   - If there is no CLAUDE.md, say so and propose a new one containing only the new
     section plus a brief description of this repo.
   - SHOW ME THE EXACT DIFF before saving anything, meaning the precise lines you
     intend to add and where. Then WAIT for me to approve it. Do not write the file
     until I say yes.

Start with step 1 and tell me what you find.
```

## Running the stages

1. Open your project in Claude Code.
2. Paste the onboarding prompt above. Answer its questions, and approve the CLAUDE.md diff when it shows you one.
3. Type `/app-bootstrap:product-discovery` and describe your idea in your own words. Claude will ask what happens in the failure cases before it writes anything down.
4. Continue until Claude produces a requirements document. Read it, correct what is wrong, and sign it off.
5. Type `/app-bootstrap:user-journeys`, read the map it ends with, and rule on what it changes. Then type `/app-bootstrap:wireframes`, and review and sign off the same way.
6. Continue through `/app-bootstrap:design-loop` and the remaining stages in order.

Stage 1 takes longer than the stages that follow it.

---

# Part 2: Technical reference

## The five stages and their exit gates

| Stage | Skill | Produces | Exit gate |
| :-- | :-- | :-- | :-- |
| 1 | `/app-bootstrap:product-discovery` | Requirements doc: hard requirements `R1..Rn` split from the negotiable baseline, plus a dated product-decisions log | Maintainer signs off the requirements doc |
| 1b | `/app-bootstrap:user-journeys` | Personas, journeys and a tagged gap register written blind behind a firewall (greenfield: held against the R-list; brownfield: against the feature surface), plus a self-contained journey map whose every number is counted from the register | Plain **SHIP** from the adversarial reviewer, then the maintainer reads the map and rules on the roadmap; the skill never changes the roadmap itself |
| 2 | `/app-bootstrap:wireframes` | One published artifact covering every surface, with numbered callouts carrying binding semantics | Maintainer sign-off; artifact URL recorded in the project `CLAUDE.md` as the UI source of truth |
| 3 | `/app-bootstrap:design-loop` | Design doc + full review trail | A closing pass ("CODE CHANGED beyond line-level: no"), then a separate maintainer approval gate |
| 4 | `/app-bootstrap:implementation-loop` | Shipped code, phase by phase | A closing pass per phase, plus the coordinator's closure checks |
| 5 | `/app-bootstrap:e2e-review` | Browser-driven journey results | **STUB**. Shape defined, not yet validated |

Shared doctrine for all six lives in [`docs/playbook.md`](docs/playbook.md): two-loop sequencing, the adversarial briefing template, the adversarial-pass chain and its fresh-agent rule, the maintainer four-part walkthrough format, the verdict line, delegation economics, and background-agent hygiene. Each skill points at it rather than restating it.

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
│   ├── user-journeys/
│   │   ├── SKILL.md
│   │   └── assets/          # brief template, journey-map template, build-map.py
│   ├── wireframes/SKILL.md
│   ├── design-loop/SKILL.md
│   ├── implementation-loop/SKILL.md
│   └── e2e-review/SKILL.md
└── README.md
```

Per the [plugins reference](https://code.claude.com/docs/en/plugins-reference), only `plugin.json` lives inside `.claude-plugin/`; every component directory (`skills/`) sits at the plugin root. Skills are directories containing a `SKILL.md`, and the directory name becomes the skill name, namespaced by the plugin name, so `skills/design-loop/` surfaces as `/app-bootstrap:design-loop`.

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

The path may be any directory containing `.claude-plugin/marketplace.json`, absolute or relative, or a direct path to the `marketplace.json` file. Use `.` when standing inside the repository itself.

### Updating

Two commands, and you need both:

```
claude plugin marketplace update claude-app-bootstrap    # refresh the catalog
claude plugin update app-bootstrap@claude-app-bootstrap  # actually upgrade the plugin
```

The first refreshes marketplace metadata only. On its own it prints `✔ Successfully updated marketplace: claude-app-bootstrap` and leaves the installed plugin where it was, which is a success message for something that did not happen. The second performs the upgrade and prints `✔ Plugin "app-bootstrap" updated from 0.1.0 to 0.2.0 for scope user. Restart to apply changes.` Restart as instructed.

The plugin pins `"version"` in both `plugin.json` and its marketplace entry, so consumers stay on the version they installed until they run `claude plugin update`. That is the pin: upgrade is opt-in, and nothing changes under a running session or an untouched install.

Maintainers should note the corollary. Content pushed without bumping `version` in both manifests reaches nobody: existing installs run `claude plugin update`, are told they are current, and keep the old doctrine. Bump both manifests, then run `claude plugin tag`, which refuses to cut the release unless the two agree.

**Stability:** this is `0.x`. The stage contracts may change between versions, and Stage 5 (`e2e-review`) ships as an explicit stub. Releases are cut with `claude plugin tag`, which creates a `{name}--v{version}` git tag and validates that `plugin.json` and the marketplace entry agree on the version. This repo maintains those two manifests by hand, which is the disagreement that check catches.

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

Collaborators are prompted to install it when they trust the repository folder. Plugins load at session start, so a session that was already open when the plugin was installed will not see it until a new session begins.

### Develop against it locally

```
claude --plugin-dir ./claude-app-bootstrap
claude plugin validate ./claude-app-bootstrap/.claude-plugin/plugin.json --strict
claude --plugin-dir ./claude-app-bootstrap plugin details app-bootstrap
```

`--plugin-dir` loads the plugin without installing it and takes precedence over an installed copy of the same name for that session. Edits to skill files are picked up at the next session start.

Which check covers what, verified against Claude Code 2.1.226 by injecting two defects into a skill (an unparseable frontmatter colon, and a deleted `description:`) and re-running each form:

| Command | What it actually reads |
| :-- | :-- |
| `claude plugin validate .` (repo root) | **Marketplace manifest only.** Because this repo contains `.claude-plugin/marketplace.json`, `validate` resolves it as a marketplace and never opens `skills/`. It printed `✔ Validation passed` with a broken skill on disk. |
| `claude plugin validate .claude-plugin/plugin.json --strict` | Plugin manifest **and every skill's frontmatter**. This is the form that caught the injected defect: `❯ frontmatter: YAML frontmatter failed to parse`. Skill lines print only on error. **Keep `--strict`**: without it, a missing `description` is only a warning, printing `✔ Validation passed with warnings` at exit 0, so the default command greenlights a skill that has stopped surfacing. With `--strict` the same input exits 1. |
| `claude --plugin-dir . plugin details app-bootstrap` | What loads at runtime: the component inventory (`Skills (6) …`) and per-skill token cost. This is the only check that proves all six skills load. A broken skill still counts toward `Skills (6)`; the tell is the token column, where its always-on figure collapses to `< 20` against a healthy `~100`. |

A green `claude plugin validate .` on this repo means two JSON files parse. It is not evidence about the skills. A frontmatter error is otherwise silent, because the runtime loads the skill with empty metadata, dropping its description, after which the skill stops surfacing.

## Referencing the stages from a project's CLAUDE.md

A project adopting this methodology should carry a short section like:

```markdown
## Build methodology: app-bootstrap

This project is built with the `app-bootstrap` plugin's five stages. Each stage
exits only on the maintainer's explicit sign-off.

1. `/app-bootstrap:product-discovery` → requirements doc at `docs/requirements.md`
   (hard requirements R1..Rn vs. negotiable baseline; dated decisions log).
   1b. `/app-bootstrap:user-journeys` → personas, journeys, gap register and journey
   map in the project's docs tree; the maintainer rules on the roadmap from the map.
2. `/app-bootstrap:wireframes` → UI source of truth: <artifact URL>. Numbered
   callouts carry binding semantics.
3. `/app-bootstrap:design-loop` → design doc in `docs/`. Implementation begins only
   after the closing pass AND maintainer approval.
4. `/app-bootstrap:implementation-loop` → one author plus a chain of fresh adversarial
   passes per phase, each to a pass that changes nothing.
5. `/app-bootstrap:e2e-review` → browser journey testing (stub).

Doctrine: the plugin's `docs/playbook.md`. The only verdict inside a loop is the
line "CODE CHANGED beyond line-level: yes/no".
```

## History

Distilled from how the Postmortem chess-trainer project was built: a design loop of four adversarial rounds plus a product-coverage audit, then six implementation phases, with roughly 140 findings raised and closed.

Of the six gate-honesty rules in the implementation-loop skill, **five trace to a specific defect that a green gate certified.** Rule 1 traces to a fault-injection gate that killed a process shim while the real work ran uninterrupted in a grandchild, a failure class that recurred in five consecutive phases before the countermeasures went in. Rule 2 traces to two wrong detection rules that reached a design doc as "corrections" because someone measured how often they fired rather than whether the hits were right. Rule 3 traces to a pin that passed against the reverted code for an unrelated reason, and to a fixture that made the branch under test unreachable. Rule 5 traces to three inversions that each rendered through a path a gate had already certified. Rule 6 traces to a backfill projected at 14 hours from isolated per-position costs, which measured about 23 hours in-pipeline once real work ran through it.

**Rule 4 (subagent verification checklists) is the exception, and is stated as practice rather than as an incident.** Its second half, that self-certified "all PASS" is necessary but not sufficient, does have a trace: a checklist item reading "every question ends in ?" passed while the interrogative sentences it was meant to catch ended in a period. The requirement to attach a checklist at all is prophylactic, adopted because vague briefs produced shallow work, not because a specific checklist-less failure was recorded.

## License

MIT.
