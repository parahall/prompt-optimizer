---
name: optimize-prompt
description: Rewrites a prompt (an app's system prompt, agent instructions, a CLAUDE.md or skill file, a tool description, or a one-off task prompt) so it follows the official prompting guidance for the specific model that will run it. Explains every change with a link to its source, and recommends matching API settings such as effort, thinking, and verbosity. Use when the user asks to optimize, improve, review, audit, or migrate a prompt for a named model, including moving a prompt between Claude and GPT, or is writing or editing a prompt meant for a specific Claude or GPT model. Supports Anthropic Claude models and OpenAI GPT text models (GPT-6, GPT-5.x, GPT-4.1).
argument-hint: "[prompt file or pasted text] for [target model]"
---

# Optimize a prompt for a specific model

The goal is a prompt that works better on one named model, changed no more than needed, with every change explained so the user can judge it. The knowledge lives in `reference/`; this file is the workflow.

Arguments, if any: $ARGUMENTS

## Step 1: Collect the inputs

You need these. Take them from the request, the arguments, or the files; ask only for what is missing and changes the advice. Ask all questions in one message.

1. **The prompt.** A file path (read the file) or pasted text. Users often describe the app first and then paste the prompt in the same message; treat the instruction-like text (the part addressed to the model) as the prompt instead of asking for it again.
2. **The target model.** If missing, ask. Find the provider with [reference/providers.md](reference/providers.md). If the provider is not supported, say so and follow that file's "When the provider is not supported" section; do not continue to Step 2.
3. **What kind of prompt it is**, inferred when obvious: system prompt for a chat product; system prompt for an agent (tools, many steps); one-off task prompt; instructions file (CLAUDE.md, skill, subagent definition); tool description.
4. **How it runs**, asked only when it changes the advice: effort level (and for Claude, thinking on or off; for OpenAI, the Responses API or Chat Completions); tools available (search, subagents, file editing); does a person watch while it works, or does it run unattended; is the output shown to end users.
5. **Optional:** the model the prompt was written for (a migration), and any bad behavior the user has already seen. Observed behavior is the strongest signal of which model-specific blocks to add.

If the user cannot answer a question, choose the most likely answer, continue, and list the assumption in the report.

## Step 2: Load only what is needed

From the target provider's folder, `reference/<provider>/` next to this file, read (with the file-reading tool):

- `audit-checklist.md`: always.
- `general-techniques.md`: always.
- `api-settings.md`: always.
- The target model's file in `models/`:
  - `anthropic/models/`: `fable-5-1.md` (also Mythos 5.1), `fable-5.md` (also Mythos 5), `opus-5-5.md`, `opus-5.md`, `opus-4-8.md`, `sonnet-5-5.md`, `sonnet-5.md`, `haiku-5-5.md`, or `legacy.md` (Opus 4.7, 4.6, 4.5, Sonnet 4.6, Haiku 4.5, Sonnet 4.5).
  - `openai/models/`: `gpt-6.md` (GPT-6 Astra, 6.1 Sol, 6.1 Terra, 6 Luna, 6 Sol), `gpt-5-6.md` (GPT-5.6 Sol, Terra, Luna), `gpt-5-5.md`, `gpt-5-4.md` (also 5.4 Mini and Nano), or `legacy.md` (GPT-5.3-Codex, 5.2, 5.1, 5, 4.1).
- `snippets.md`: when the checklist or model file points to a block in it.
- Never load older model files to "fill in" the target model. Each model file is complete together with the general files; where Anthropic says an older model's advice still applies (Opus 5.5, Sonnet 5.5), it is already copied into the newer file.
- **Narrow fallback, Claude only:** if the prompt's main topic (for example code review, frontend design, tool triggering, tone, computer use) is not covered by the target model's file or the general files, you may read only that topic's section in the file of the one model the target's file says it differs from (its "How it differs from …" heading). Never go further back. Do not put that advice into the prompt; list it under "Optional additions" in the report, labeled "documented for <older model>, not confirmed for <target model>; test it". Not for OpenAI models: their guides do not say older advice carries over, and the GPT-5.5 guide says to start from a fresh baseline.
- **For a migration**, also the source model's file. If the source model is from another provider, also that provider's `audit-checklist.md`, to find habits that belong only to the old model.

**Unknown model of a supported provider** (a newer name with no file): say so first. If web access is available, fetch the provider's page for it and use it as the model file, telling the user the advice comes from a live page the skill has not been checked against:
- Claude: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-<model-id-without-claude->.md` (for example `prompting-claude-opus-5-5.md`).
- OpenAI: find the model's "Using …" and "Prompting guidance …" pages in `https://developers.openai.com/api/docs/llms.txt` and fetch the addresses as listed (they already end in `.md`; add `.md` only to an address that lacks it).

If no page exists, apply only the general files plus the closest model in the same family, say which one, and never present guesses about the unknown model as facts.

## Step 3: Audit

Go through every item of the audit checklist and the target model's "Remove from prompts" list. For each problem found, record: the quoted line, the problem, the rule, and the source link. Also note what the prompt already does well; a good prompt should be left mostly alone.

## Step 4: Rewrite

Rules for the rewrite:

- **Keep the author's intent and every hard requirement** (facts, constraints, output contracts, safety rules, template variables like `{{NAME}}`). If a requirement conflicts with model guidance, keep the requirement and say so in the report.
- **Change as little as possible.** Keep the author's voice and structure unless the structure itself is a problem. Every change must trace to a finding from Step 3. Ideas that do not fix a finding (new field definitions, extra examples, new sections) go under "Open questions and assumptions" in the report, not into the prompt. If the audit found little, the new prompt stays nearly identical to the old one; that is a good result.
- Make changes in this order:
  1. Remove or replace what hurts the target model. Resolve contradictions between rules: when one side is a soft preference (style, tone, length, a default), settle it yourself and say how. When both sides are hard requirements (for example "delete records after 30 days" and "keep records for 90 days", or "never book without confirmation" and "book automatically"), do not pick one: keep both in the prompt, name the conflict in the report, and ask the user which wins. When the target model's guidance prefers lean prompts (OpenAI's GPT-6, GPT-5.6, and GPT-5.5), removing repeated rules, examples that change nothing, and step scripts comes before adding anything. This does not apply where the model file asks for explicit steps (GPT-5.4 Mini and Nano, GPT-4.1).
  2. Apply missing general structure: the reason behind rules, what to do instead of what not to do, separated sections for mixed content, long documents before the question, examples where format matters.
  3. Add a model-specific block **only when the prompt's situation matches that block's symptom** (from the user's report, or clearly implied by the kind of prompt; for example an unattended agent, or a user-facing chat on Opus 5). List other relevant blocks under "Optional additions" in the report instead of adding them.
- **When the checklist or a model file names a replacement block, use that block** instead of writing your own version of the fix. Insert quoted blocks word for word. Fill in placeholders only where a block says to. Text you write yourself is not tested by the model maker; keep it short.
- **Exception: blocks the docs present as examples of a pattern** (the model file says "Example", "example from", or "adapt"; or the block names a specific scenario such as a customer eligibility decision, fixed output fields, or a sample website). Copy the pattern, replace the scenario-specific parts with the user's own task, fields, and constraints, and say in the report that the block was adapted. Never put the example's task or fields into a prompt for a different task.
- **Recommend settings instead of wording** where the docs say a setting is the better lever (effort, thinking mode, verbosity, token limits).
- Never add instructions that ask a reasoning model to write out its reasoning. For Claude, never keep a `<thinking>`, `<reasoning>`, or `<scratchpad>` section in the output format, even renamed to "short explanation"; if the app needs an explanation, ask for it after the answer in a tag such as `<explanation>`. The one exception is Opus 4.8, Sonnet 5, and older Claude models running with thinking off, where manual chain of thought is the documented fallback and may stay (see the Anthropic checklist, item 1). For GPT models, follow the checklist item on thinking step by step: asking the model to reason out loud is unnecessary at effort `low` or higher; outlining steps first is documented to help at effort `none` on GPT-5.1, 5.2, and 5.4, at `minimal` on GPT-5, and on GPT-4.1. Work plans for long tasks (staged plans, a plan tool) are a different thing and stay.

## Step 5: Deliver

Where the result goes depends on where the prompt came from:

- **From a file:** write the new prompt to a new file next to the original, named `<name>.optimized.<ext>` (for example `support-bot.optimized.md`), and the report to `<name>.optimized.report.md`. Never overwrite the original unless the user asks. In the chat, give a short summary: the files written, the number of changes, the most important change, and the recommended effort.
- **Pasted into the chat:** show the full report in the chat, with the new prompt in a code block.
- **In both cases, if the Artifact tool is available:** also publish a private side-by-side page: the old prompt and the new prompt next to each other with removed and added text marked, then the change list and the recommended settings. Follow the Artifact tool's own rules for the page. Give the user the link.

The report always has these five parts, in this order:

```markdown
## 1. Optimized prompt
<the full rewritten prompt, or the path of the new file>

## 2. What changed and why
- <Removed | Changed | Added>: <what>. Why: <one or two plain sentences; for a model-specific change, say what this model does differently>. Source: <link to the docs section>.
(Then "Kept as is": the strong parts left unchanged, in one or two lines.)

## 3. Recommended API settings
- Effort: <the provider's effort setting: level to start with, and what to compare it against>
- Other settings that matter here: <for Claude: thinking mode, max_tokens; for OpenAI: text.verbosity (always when answer length is an issue), Responses API vs Chat Completions, Structured Outputs; or "leave as is">
- Remove: <settings that now return errors, if any>
(Each setting line ends with its source link, like the changes above.)

## 4. What to test
<two or three concrete checks on real traffic, each tied to a change above>

## 5. Open questions and assumptions
<facts that were guessed, and optional additions the user may want if they see a listed symptom; "None" if empty>
```

Write the report in plain language: short sentences, no unexplained jargon, and say what each setting or term means the first time it appears.

## When the skill starts on its own

If you started this skill because the user is writing or editing a prompt (not because they asked for an optimization), first confirm the target model if it is not stated, then present the audit findings and offer the rewrite. Do not write new files or publish a page until the user agrees.
