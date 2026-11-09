# Plan: a skill that optimizes prompts for a specific Claude model

Written 2026-11-08. Research is based on Anthropic's documentation as it stood on that date.

## 1. What we are building, in one paragraph

A Claude Code skill is a folder with a file called `SKILL.md` inside it. The file holds instructions that Claude loads when a task needs them. This repository will hold one skill. You give it a prompt (for example the system prompt of an app, the instructions for an agent, a `CLAUDE.md` file, or a one-off task prompt) and you name the Claude model that will run it. The skill rewrites the prompt so it follows Anthropic's official advice for that exact model. It also explains every change, recommends the API settings that go with the prompt, and says what to measure afterwards. The skill is general: it is not tied to any project. It is installed once for your user, and later published on GitHub so other people can install it.

The first version covers Claude models only. OpenAI models and Google's Gemini models come next, so the skill is built around "providers" (the company that makes the model) from the start: each provider gets its own folder of knowledge with the same parts, and the workflow does not change when a provider is added.

## Decisions so far (2026-11-08)

1. Names: `prompt-optimizer` for the repository and plugin, `optimize-prompt` for the skill. Approved.
2. Models: the eight Claude models that have their own page, plus one shared `legacy.md` for older Claude models. Approved. OpenAI and Gemini follow in a later phase (section 7).
3. When it runs: both. Claude may start it on its own when you write or edit a prompt, and you can start it with `/optimize-prompt`. The description must be narrow so it does not start by accident.
4. Where the result goes: decided by the input. If the prompt came from a file, write the result to new files next to it (`<name>.optimized.<ext>` and `<name>.optimized.report.md`) and show a short summary in the chat. If the prompt was pasted into the chat, show the full result in the chat. In both cases, when the Artifact tool is available in the session, also create a private side-by-side page (old prompt, new prompt, list of changes) without asking. The original file is never overwritten unless the user asks.
5. Quoting: approved. Anthropic's tested sample blocks are quoted word for word with the page and section named; everything else is in our own words; the README states the source and that the project is independent. An example is on the same Artifact page.

## 2. What the research found

### 2.1 The structure of Anthropic's prompting guide

The guide you linked ("Prompting best practices") is one page with three parts:

1. **A table of model-specific pages.** Each current model has its own page that lists only how it behaves *differently* from the model before it, and what to change in a prompt because of that. There are eight such pages today: Claude Fable 5.1 (shared with Claude Mythos 5.1), Claude Fable 5 (shared with Claude Mythos 5), Claude Opus 5.5, Claude Opus 5, Claude Opus 4.8, Claude Sonnet 5.5, Claude Sonnet 5, and Claude Haiku 5.5.
2. **General techniques for all current models.** Be clear and direct; explain *why* an instruction exists; use 3 to 5 examples inside `<example>` tags; separate parts of a prompt with XML tags (labels in angle brackets like `<instructions>` and `<documents>`); give a role; put long documents at the top and the question at the end; say what to do instead of what not to do; and patterns for tool use, thinking, agents, research, and front-end design.
3. **Migration advice** for prompts written for older model generations.

Three supporting pages matter as much as the guide itself:

- **Effort.** "Effort" is an API setting (`output_config.effort`) with five levels: `low`, `medium`, `high`, `xhigh`, `max`. It controls how much the model thinks and works. The docs repeat many times that effort, not prompt wording, is the first control to change. The default is `medium` on Opus 5.5 and Haiku 5.5 and `high` on the others.
- **Steering thinking.** "Thinking" is the model's private reasoning before it answers. On current models it is "adaptive": the model decides how much to think. On Fable 5.1, Fable 5 and Opus 5.5 it cannot be turned off.
- **Refusals.** Newer models run safety filters. One filter category, called `reasoning_extraction`, declines prompts that ask the model to write its reasoning into the answer (for example "think step by step inside `<thinking>` tags first", or a `reasoning` field in JSON output). Old prompt-engineering advice recommended exactly this, so it is the single most important thing the skill must detect and remove.

### 2.2 The key insight: the advice is organized by symptom

Every model page starts with "start with the section that matches what you observe". Most model-specific snippets fix a behavior you have *seen*, for example "the agent stops before the task is done" or "chat replies look silent". This has a big consequence for the skill:

> The skill must **not** paste every recommended snippet into every prompt. That makes prompts long and can cause new problems. It should add a model-specific block only when the prompt's situation clearly matches the problem that block solves, and offer the rest as optional additions.

### 2.3 The same instruction can help one model and hurt another

These conflicts are the reason a per-model skill is worth building. Examples from the docs:

| Instruction in a prompt | Effect depends on the model |
|---|---|
| "Verify your answer before finishing" / "double-check your work" | Recommended in general. **Remove it for Opus 5**: it already verifies itself, and the instruction causes over-verification. **Add a specific one for Sonnet 5.5 and Haiku 5.5** at low effort, which sometimes skip checks. |
| A block against markdown, bullets and bold | Recommended for older models. **Remove or soften it for Fable 5.1**, which already formats too little. |
| "Be concise" | Opus 5 writes long by default and lowering effort does not shorten replies, so the prompt must ask for it. Fable 5.1 needs the opposite: ask it for progress updates and remove "keep updates brief" rules. |
| "Think carefully before answering" | Remove it in Opus 5.5 chat prompts (slower replies, no quality gain). Useful on Sonnet 5.5 for JSON answers that need several steps of working out. |
| "Think less" / "answer directly" | Does **not** work on Sonnet 5.5 or Haiku 5.5. Recommend a lower effort level instead. |
| "CRITICAL: You MUST use this tool" | Newer models are more obedient and now use the tool too often. Soften to "Use this tool when...". |
| "Only report high-severity issues" in a code-review prompt | Opus 4.8, Opus 5 and Sonnet 5 follow it literally and report fewer real bugs. Replace with "report everything, with confidence and severity, and filter later". |
| "Write your reasoning in `<thinking>` tags" | Can trigger a `reasoning_extraction` refusal on Fable 5.1, Fable 5, Opus 5.5, Opus 5, Sonnet 5.5. Remove it; read the reasoning from the API's summarized thinking instead. |
| A rule that tells the model not to think, when thinking is off | Makes internal tags leak into the visible answer on Opus 5 and Sonnet 5.5. Remove it. |

### 2.4 Things that are API settings, not prompt text

Many problems are fixed by settings, not words. The skill should output these next to the prompt: the effort level to start with, the thinking mode (`adaptive`, `disabled`, or Sonnet 5.5's special `between_tools`), a large enough `max_tokens` (thinking counts toward it), and warnings about settings that now return errors (manual thinking budgets `budget_tokens`, `temperature` on Sonnet 5, prefilled assistant replies, `thinking: disabled` on Opus 5.5). It must also warn when a change to the system prompt in the middle of a conversation would break stored thinking blocks on the newest models.

### 2.5 The docs change often

In about a year Anthropic released many models, and each new one gets a new page. A skill that hard-codes all knowledge goes out of date fast. So the plan includes (a) one file per model, each with a "checked against the docs on <date>" line, (b) a maintainer script that downloads the pages again and shows what changed, and (c) a live-lookup fallback inside the skill for models it does not know yet. The docs are available as plain Markdown by adding `.md` to any page address, which makes (b) and (c) easy.

### 2.6 Rules for writing the skill itself

From Anthropic's "Skill authoring best practices" and the Claude Code skills page:

- The `name` field: lowercase letters, numbers and hyphens, at most 64 characters, and it **may not contain the words "claude" or "anthropic"**. The `description` field: at most 1,024 characters for claude.ai and the API (Claude Code allows 1,536), written in the third person, saying both what the skill does and when to use it.
- Keep `SKILL.md` under 500 lines. Put detail in reference files that `SKILL.md` links to directly (one level deep, never a chain of links). Any reference file longer than 100 lines starts with a table of contents.
- Write evaluations (automatic tests) before writing much text. Test with Haiku, Sonnet and Opus.
- The skill must follow its own advice: no shouting in capitals, no "show your reasoning" instructions, and the reason behind each rule.

## 3. What the skill does, step by step

This is the workflow that `SKILL.md` will describe.

1. **Collect the inputs.**
   - The prompt: pasted text or a file path.
   - The target model. If it is missing, ask. The skill finds the provider from the model name using `reference/providers.md` (for example `claude-…` → `anthropic`). If the provider has no folder yet, the skill says so plainly and stops, instead of applying Claude advice to another company's model. If the provider is known but the model has no file, say so, try to fetch its page live (see step 2), and otherwise fall back to the closest model in the same family plus the provider's general rules.
   - The kind of prompt, because the advice differs: a system prompt for a chat app, a system prompt for an autonomous agent, a one-off task prompt, a `CLAUDE.md` / skill / subagent definition, or a tool description.
   - Facts about how it runs, asked only when they change the advice: Is thinking on? What effort? Does it have tools (search, subagents)? Does a person watch it work, or does it run alone? Is the output shown to end users?
   - Optional: the model the prompt was written for (if this is a migration), and any bad behavior the user has already seen.
2. **Load only the knowledge that is needed.** From the target provider's folder: always its general-techniques file and its audit checklist, then the target model's file. If this is a migration, also the source model's file; if the source model is from a different provider (for example a GPT prompt moving to Claude), the source provider's audit checklist too, to find habits that only made sense for the old model. For an unknown Claude model, download `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-<model>.md`. Each provider folder records its own docs address pattern for this.
3. **Audit the prompt.** Produce a list of findings. Each finding names the problem, quotes the line, gives the rule, and links the documentation section.
4. **Rewrite the prompt.** Keep the author's intent and every hard requirement. Change as little as possible. Do three kinds of changes, in this order:
   1. Remove or replace what hurts the target model (section 2.3).
   2. Apply general structure where it is missing (context and reasons, XML sections, documents before the question, examples).
   3. Add a model-specific block only when the situation matches its symptom. List other blocks as "optional, add if you see X".
5. **Report.** The output always has the same five parts:
   1. The optimized prompt, placed as decision 4 says: new files for a file input, the chat for a pasted input, plus a side-by-side Artifact page when that tool is available.
   2. A change list: what changed, why, and the source link.
   3. Recommended API settings: effort, thinking mode, `max_tokens`, and settings to remove.
   4. What to test: two or three concrete checks the user should run on their real traffic, because the docs say every change must be measured.
   5. Open questions, if any facts were guessed.

## 4. Repository layout

```
prompt-optimizer/
├── .claude-plugin/
│   ├── plugin.json            # the plugin's ID card: name, description, version, author
│   └── marketplace.json       # makes this repo installable with /plugin marketplace add
├── skills/
│   └── optimize-prompt/
│       ├── SKILL.md           # the workflow from section 3, under ~250 lines
│       └── reference/
│           ├── providers.md                # model name patterns → provider folder; lists which providers exist
│           ├── anthropic/
│           │   ├── general-techniques.md   # rules for all current Claude models (from the main guide)
│           │   ├── audit-checklist.md      # patterns to find, with per-model verdicts (section 2.3 grown into a full list)
│           │   ├── api-settings.md         # per-model table: effort levels, default, starting level, thinking modes, max_tokens, removed parameters
│           │   ├── snippets.md             # tested text blocks shared by many Claude models (parallel tool calls, safe actions, pasted text, and so on)
│           │   └── models/
│           │       ├── fable-5-1.md        # also covers Mythos 5.1
│           │       ├── fable-5.md          # also covers Mythos 5
│           │       ├── opus-5-5.md
│           │       ├── opus-5.md
│           │       ├── opus-4-8.md
│           │       ├── sonnet-5-5.md
│           │       ├── sonnet-5.md
│           │       ├── haiku-5-5.md
│           │       └── legacy.md           # Opus 4.7, 4.6, 4.5, Sonnet 4.6, Haiku 4.5: only what the general guide says about them
│           ├── openai/                     # later phase: the same parts as anthropic/
│           └── google/                     # later phase: the same parts as anthropic/ (Gemini)
├── evals/                     # automatic tests, run with `claude plugin eval .`
│   └── <provider>-<case-name>/prompt.md + graders/*.md
├── tools/
│   ├── refresh-docs.sh        # maintainer script: downloads the doc pages, shows what changed since last time
│   └── sources/
│       └── anthropic.txt      # the list of doc page addresses for each provider; openai.txt and google.txt later
├── README.md                  # what it does, how to install, an example
└── LICENSE
```

Notes on this layout:

- **Every provider folder has the same four parts** (general techniques, audit checklist, API settings, one file per model). `SKILL.md` refers to them by these roles, never by Claude-specific names, so adding OpenAI or Gemini means adding a folder and a line in `providers.md`, not changing the workflow. API settings differ by provider (Claude has "effort", other providers have their own controls), so each provider's `api-settings.md` describes its own controls.
- **Links stay one level deep** even with provider folders: `SKILL.md` tells Claude which file to open by path after the provider is known, rather than chaining links from file to file.
- **Each model file has the same sections**, so Claude reads them the same way: date checked and source link; "how it differs from the model before it"; "remove from prompts"; "add when you see this symptom" (each item: symptom, block of text, source); "API settings"; "known traps". Each model file is complete together with the general files; the skill never loads older model files to fill gaps. Where Anthropic's page says the earlier model's patterns "remain a reasonable starting point" (Opus 5.5 from Opus 5, Sonnet 5.5 from Sonnet 5), the still-valid earlier blocks are copied into an "Inherited from …" section of the newer file. A page that only says old prompts "perform well" on the new model does not count. For a topic the target's files do not cover, `SKILL.md` allows reading that one topic in the model one step back, reported as unconfirmed for the target; OpenAI models are excluded: the GPT-5.5 guide says to start from a fresh baseline, and the older guides that say earlier advice carries over (GPT-5.2 over GPT-5 and 5.1) are already merged in `openai/models/legacy.md`.
- **Every link from `SKILL.md` goes straight to a file**, so the model files are one level deep, as the authoring rules require.
- **The skill's description claims only what exists.** In the first version it says Claude models. When the OpenAI or Gemini folder is added, the description is updated in the same change.
- **The downloaded docs are not committed.** `tools/refresh-docs.sh` saves them in a git-ignored folder. The reference files contain our own condensed wording plus short quoted sample blocks with links to the source. (Please read open question 5 about this.)
- **One repository is both the plugin and the marketplace.** Other people install it with `/plugin marketplace add <your-github-user>/prompt-optimizer` and then `/plugin install prompt-optimizer@<marketplace-name>`. The exact `"source"` value for a plugin at the root of its own marketplace was not confirmed in the docs; we check it with `claude plugin validate .` before publishing.
- **For your own user, before publishing**, we make a symlink (a shortcut on disk) from `~/.claude/skills/optimize-prompt` to `skills/optimize-prompt` in this repo. The Claude Code docs confirm symlinks work there. Edits in the repo are then live in every project at once. You run it as `/optimize-prompt`; through the plugin it becomes `/prompt-optimizer:optimize-prompt`.
- **Names.** Plugin and repository: `prompt-optimizer`. Skill: `optimize-prompt`. Neither contains "claude", so the same folder can also be uploaded to claude.ai or the API later.

## 5. Build order

Each step has a check that proves it is done.

1. **Set up the repository.** `git init`, `.gitignore`, `LICENSE`, the two `.claude-plugin` files, an empty skill folder.
   → Check: `claude plugin validate .` passes.
2. **Write the evaluations first** (about ten cases, listed in section 6), and run them with no skill to see the baseline.
   → Check: the baseline run finishes and shows which cases fail without the skill.
3. **Write `tools/refresh-docs.sh`.** It downloads the main guide, the eight model pages, effort, steering thinking, refusals, and the models overview, into a git-ignored folder, and prints a diff against the last download.
   → Check: running it twice in a row reports "no changes".
4. **Write the reference files**, starting with `audit-checklist.md` and `api-settings.md` (they carry most of the value), then the eight model files, then `general-techniques.md`, `snippets.md` and `legacy.md`. Every rule gets a source link.
   → Check: a script confirms every link in the reference files points to a page that exists, and every model in the guide's table has a file.
5. **Write `SKILL.md`** with the workflow from section 3.
   → Check: under 500 lines; frontmatter passes validation; the evaluations from step 2 now pass (target: at least 8 of 10).
6. **Install for your user** with the symlink, and try it on three real prompts from your other repositories.
   → Check: the output has all five report parts each time, and you agree with the changes.
7. **Test across models.** Run the evaluations with the skill running on Haiku, Sonnet and Opus.
   → Check: Haiku still produces correct output (it may need clearer steps).
8. **Publish.** Write the README with an example before and after, push to GitHub, and install it on a clean machine or account through the marketplace commands.
   → Check: the install works from the public repo with no local files.

## 6. Evaluation cases

Each case is a folder with a prompt and graders (automatic checks: a text search, or a short judgment by a model). Each runs with and without the skill, and the report shows the difference.

1. An Opus 5 prompt that says "double-check your answer" and "add a final verification step" → the skill removes both.
2. A prompt for Opus 5.5 that asks for reasoning inside `<thinking>` tags → removed, and the report recommends summarized thinking instead.
3. A chat prompt with a long anti-markdown block, target Fable 5.1 → replaced with the shorter rule from the Fable 5.1 page.
4. A Haiku 5.5 support bot with a search tool and no date → the date line and the search nudge are added.
5. A code-review prompt that says "only report high-severity issues", target Opus 4.8 → replaced with "report everything, with confidence and severity".
6. A Sonnet 5.5 prompt that says "keep your thinking short" → the line is removed and the report recommends a lower effort level.
7. A prompt with "CRITICAL: You MUST use the search tool" → softened.
8. An autonomous overnight agent prompt for Fable 5.1 → the "finish the whole task" block is added.
9. A prompt that is already good, target Sonnet 5 → very few changes, and no snippets added "just because".
10. A target model the skill does not know → the skill says so and fetches the page or asks, instead of inventing advice.
11. A target model from a provider that has no folder yet (for example a GPT model in the first version) → the skill says it does not support that provider yet and does not apply Claude advice to it.

## 7. Out of scope for the first version

- **Running the prompt against the real API to compare old and new versions.** This would be the strongest proof that a rewrite helps, but it needs an API key, costs money, and needs test inputs. We can add it later as an optional script.
- **Automatic updates.** The refresh script tells the maintainer what changed; a person still edits the reference files.

## 8. Phase 2: OpenAI GPT models (research done 2026-11-08)

Gemini follows later with the same steps.

### 8.1 What OpenAI publishes

All pages are on developers.openai.com and, like Anthropic's, have a plain Markdown copy when `.md` is added to the address. The list is in `tools/sources/openai.txt` (51 pages, downloaded and read).

- **One "Using GPT-X" page per model family**: what's new, prompting best practices, migration. Families: GPT-6, GPT-5.6, 5.5, 5.4, 5.3-Codex, 5.2, 5.1, 5, 4.1.
- **Extra pages for some families**: "Prompting guidance for GPT-5.6 Sol" (the most detailed page), "Upgrading to GPT-5.4 / 5.5 / 5.6 Sol", a front-end prompt page written for GPT-5.5, and older cookbook prompting guides (GPT-5, 5.1, 5.2, 4.1, Codex). The cookbook guides for GPT-5 and 5.1 are marked "archived".
- **General pages**: Prompt engineering (message roles, Markdown and XML sections, examples), Reasoning models (the `reasoning.effort` setting and its table), Reasoning best practices (older, written for the o-series models).
- **Model catalog pages**: effort levels, context window, knowledge cutoff, price, endpoints.

### 8.2 How it differs from Anthropic's docs

1. **The advice is written per family, not per model.** The GPT-6 prompting section covers GPT-6 Astra, 6.1 Sol, 6.1 Terra, 6 Luna, and 6 Sol together; it says the advice was observed on Astra and should be checked on the others. The members differ only in settings. Same for GPT-5.6 (Sol, Terra, Luna).
2. **OpenAI's main message for current models is "remove, don't add".** GPT-5.6 docs report that leaner system prompts scored 10–15% higher with 41–66% fewer tokens in OpenAI's coding-agent tests. They say: state each rule once, remove repeated rules and examples that do not change behavior, describe the outcome instead of every step, and change a working prompt only for a measured failure. So for OpenAI the skill's main job is simplifying, more than inserting blocks.
3. **Contradictions are the biggest risk.** OpenAI says GPT-5-class models spend reasoning trying to reconcile conflicting rules, and that this hurts them more than other models. Finding contradictions is the first audit item for OpenAI.
4. **The settings are different**: `reasoning.effort` (`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`; which ones exist depends on the model), `text.verbosity` (`low`, `medium`, `high`), `reasoning.mode: "pro"`, `reasoning.context`, `phase` on assistant messages, `configuration_update` for changing effort mid-conversation, and `prompt_cache_options`.
5. **The API you call matters.** On several models, tool calling with reasoning works only in the Responses API, not in Chat Completions. `temperature` and `top_p` work only at effort `none`.
6. **Advice that helps one GPT model and hurts another**, the same kind of conflict as for Claude. Examples:
   - Step-by-step process instructions: remove them for GPT-5.5 and 5.6 (they make answers mechanical); give the full step order for GPT-5.4 Mini (it is literal and needs it).
   - "Think step by step": remove at effort `low` or higher (the model reasons on its own); asking it to plan helps at `none` and `minimal`.
   - "Be concise": GPT-5.6 is already concise and the line can make answers too short; use `text.verbosity` instead.
   - Formatting: GPT-6 Astra and 5.4 lean on lists and tables; 5.5 defaults to paragraphs.
   - Asking before acting: GPT-6 Astra asks for clarification more often and may stop early; GPT-5.4 Mini asks follow-up questions unless told not to; repeated "ask first" lines on 5.6 cause needless approval stops.
   - Schema in the prompt: GPT-5.5 says move it to Structured Outputs; GPT-5.2 extraction says always give a schema.
   - The current date: GPT-5.5 says drop it (the model knows the UTC date).
7. **GPT-6 Astra follows skill files and `AGENTS.md` more closely**, so unclear or conflicting guidance in them can stop its work. OpenAI recommends one sentence that gives the user's instructions priority over skill instructions.

### 8.3 Files

Change from what I first proposed: one file per **family**, not per model, because the docs are written that way. Where family members differ, the file says so.

```
skills/optimize-prompt/reference/openai/
├── general-techniques.md   # roles, sections, examples, outcome-first prompts, stop rules, tool descriptions, prompt caching layout
├── audit-checklist.md      # patterns to find, with a verdict per family (contradictions first)
├── api-settings.md         # per model: effort levels and default, verbosity, endpoint limits, parameters that error
├── snippets.md             # tested blocks shared by several families
└── models/
    ├── gpt-6.md            # GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, GPT-6 Sol
    ├── gpt-5-6.md          # GPT-5.6 Sol, Terra, Luna (with the 5.6 Sol prompting page)
    ├── gpt-5-5.md          # GPT-5.5 (rich own guidance, still widely used)
    ├── gpt-5-4.md          # GPT-5.4 and 5.4 Mini (rich own guidance; Mini needs the opposite style)
    └── legacy.md           # GPT-5.3-Codex, 5.2, 5.1, 5, 4.1: short notes, mainly to recognize old habits when migrating
```

Out of scope for OpenAI in this phase: voice models (GPT-Live, Realtime), image models (GPT-Image), open-weight models (gpt-oss), and the cybersecurity models. The skill says it does not cover them.

### 8.4 Changes to the shared parts

- `providers.md`: mark `openai/` as supported; list the name patterns (`gpt-6…`, `gpt-5…`, `gpt-4.1`); state the out-of-scope models.
- `SKILL.md`: Step 2 names files by their role, not by Anthropic paths, so it works for any provider folder. Step 4 gains one provider-neutral rule: when the provider's guidance prefers lean prompts (OpenAI does), removing repeated and conflicting rules comes before adding anything. The description says "Claude and OpenAI GPT models".
- Quoted blocks are marked "Quoted from OpenAI", the same way as Anthropic's. `tools/check-references.py` checks quotes and links for every provider folder.
- README: OpenAI added to "Supported now" and to the credit note.
- Cross-provider migration (for example a GPT prompt moving to Claude, or a Claude prompt moving to GPT-6): the skill loads the source provider's checklist to remove habits that belong only to the old model (for example Claude's effort wording, or GPT's `phase` or `<persistence>` blocks).

### 8.5 Test cases to add

1. GPT-6 Astra agent that keeps asking for approval → the initiative and follow-through blocks are added.
2. GPT-6 Astra prompt with no rule on skill priority, in an app that loads skills → the priority sentence is added.
3. GPT-5.6 prompt with the same rule stated three times and examples that change nothing → repeats removed; the prompt gets shorter.
4. GPT-5.6 prompt with "Be concise. Keep it short." → removed or replaced, and `text.verbosity` recommended.
5. GPT-5.5 prompt with a step-by-step process script → rewritten as an outcome with success criteria and stop rules.
6. GPT-5.4 Mini prompt that relies on implied steps → explicit step order kept or added (the opposite of case 5).
7. Prompt with contradictory rules (for example "always ask before booking" and "book automatically") → the conflict is named and resolved, not left in.
8. Settings: a request that sends `temperature` with effort `medium`, or effort `none` to GPT-6 Astra → the report flags both as errors.
9. "Think step by step" for GPT-6.1 Sol at `medium` → removed; kept as planning at effort `none` on GPT-6 Luna.
10. A good prompt for GPT-5.6 → almost no changes.
11. Unknown OpenAI model (for example `gpt-7`) → says so; does not invent advice.
12. Cross-provider: a Claude-tuned prompt moving to GPT-6 Astra, and a GPT-tuned prompt moving to Claude Opus 5.5 → each side's model-specific habits are removed.
13. Replace the current "OpenAI not supported" case with "Gemini not supported".

### 8.6 Build order

1. Write the OpenAI reference files, quotes first checked by the script → check: all quotes match the docs, every family in the catalog that is in scope has a file, all links work.
2. Generalize `SKILL.md` and `providers.md` → check: the existing 12 Claude cases still pass.
3. Write the OpenAI test cases and run them with and without the skill, then with Sonnet and Haiku → check: at least 11 of 13 pass with the skill; a clear difference from the run without it.
4. Update README and this plan; commit and push → check: the GitHub repository shows the new folder.

Expected test cost: about $20–30, similar to the Claude phase.

## 9. Progress (2026-11-08)

- Steps 1 to 7 are done. Step 8 (publishing on GitHub) is not started.
- The skill is installed for the user through a symlink: `~/.claude/skills/optimize-prompt` points to `skills/optimize-prompt` in this repository. A live run from another folder worked.
- `python3 tools/check-references.py` passes: all 82 quoted blocks match Anthropic's pages word for word, every model in the guide has a file, and all links work.
- Test results, 12 cases, one run each:
  - Default model, with and without the skill (run 2): with the skill 10 of 12 passed (the 2 failures were checks I wrote badly, fixed afterwards); without it every case but one scored lower; average difference +0.66 on a 0-to-1 score.
  - After the fixes, with the skill: default model 12 of 12, Haiku 12 of 12, Sonnet 11 of 12. The Sonnet failure is Sonnet 5.5's safety filter declining to read a test prompt that asks for written-out reasoning; it is listed under "Known limits" in the README.
- What the comparison showed: without the skill, the model already knows the well-known fixes, but makes subtle mistakes (removed a scope line Sonnet 5 needs; told the user to update the date on every request), adds unrequested content, and cites no sources.
- Total test cost so far: about $25.

## 10. Open questions for you

The repository is parahall/prompt-optimizer (private). None open at the moment.

## 11. Progress of the OpenAI phase (2026-11-08)

- Built as planned in section 8, with one file per model family (approved by the user).
- `python3 tools/check-references.py` passes for both providers: 82 Anthropic and 53 OpenAI quoted blocks match the docs word for word, every OpenAI model family in the source list is covered, and all 32 links work.
- The refresh script had a bug found during this phase: pages with the same final name overwrote each other (the GPT-6 guide and the GPT-6 Astra catalog page). Files are now named by the last two parts of the address.
- Tests (26 cases, one run each unless noted):
  - Default model, with and without the skill: all 26 pass with the skill. Without it, every case except the two unknown-model cases scores lower; the average difference is +0.71. Without the skill, the model gets GPT-6 settings wrong (GPT-6 is newer than its knowledge).
  - Sonnet running the skill: all OpenAI and cross-provider cases pass except one refused by Sonnet 5.5's safety filter (the test prompt asks for reasoning in `<thinking>` tags; the known limit in the README).
  - Haiku running the skill: after three small `SKILL.md` fixes (pasted prompts after a description, source links for settings, `text.verbosity` for length problems), 7 of 8 reruns of its weak cases pass. Remaining weak spot: Haiku sometimes reads a pasted step script as a description and asks for the prompt.
- Test cost of the OpenAI phase: about $20.
