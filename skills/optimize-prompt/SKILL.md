---
name: optimize-prompt
description: Rewrites a prompt (an app's system prompt, agent instructions, a CLAUDE.md or skill file, a tool description, or a one-off task prompt) so it follows the official prompting guidance for the specific model that will run it. Explains every change with a link to its source, and recommends matching API settings such as effort and thinking. Use when the user asks to optimize, improve, review, audit, or migrate a prompt for a named model, or is writing or editing a prompt meant for a specific Claude model. Currently supports Claude models only.
argument-hint: "[prompt file or pasted text] for [target model]"
---

# Optimize a prompt for a specific model

The goal is a prompt that works better on one named model, changed no more than needed, with every change explained so the user can judge it. The knowledge lives in `reference/`; this file is the workflow.

Arguments, if any: $ARGUMENTS

## Step 1: Collect the inputs

You need these. Take them from the request, the arguments, or the files; ask only for what is missing and changes the advice. Ask all questions in one message.

1. **The prompt.** A file path (read the file) or pasted text.
2. **The target model.** If missing, ask. Find the provider with [reference/providers.md](reference/providers.md). If the provider is not supported, say so and follow that file's "When the provider is not supported" section; do not continue to Step 2.
3. **What kind of prompt it is**, inferred when obvious: system prompt for a chat product; system prompt for an agent (tools, many steps); one-off task prompt; instructions file (CLAUDE.md, skill, subagent definition); tool description.
4. **How it runs**, asked only when it changes the advice: thinking on or off; effort level; tools available (search, subagents, file editing); does a person watch while it works, or does it run unattended; is the output shown to end users.
5. **Optional:** the model the prompt was written for (a migration), and any bad behavior the user has already seen. Observed behavior is the strongest signal of which model-specific blocks to add.

If the user cannot answer a question, choose the most likely answer, continue, and list the assumption in the report.

## Step 2: Load only what is needed

For the `anthropic` provider, read:

- [reference/anthropic/audit-checklist.md](reference/anthropic/audit-checklist.md): always.
- [reference/anthropic/general-techniques.md](reference/anthropic/general-techniques.md): always.
- [reference/anthropic/api-settings.md](reference/anthropic/api-settings.md): always.
- The target model's file in `reference/anthropic/models/`: `fable-5-1.md` (also Mythos 5.1), `fable-5.md` (also Mythos 5), `opus-5-5.md`, `opus-5.md`, `opus-4-8.md`, `sonnet-5-5.md`, `sonnet-5.md`, `haiku-5-5.md`, or `legacy.md` (Opus 4.7, 4.6, 4.5, Sonnet 4.6, Haiku 4.5, Sonnet 4.5).
- For a migration, also the source model's file.
- [reference/anthropic/snippets.md](reference/anthropic/snippets.md): when the checklist or model file points to a block in it.

**Unknown Claude model** (a newer name with no file): say so first. If web access is available, fetch `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-<model-id-without-claude->.md` (for example `prompting-claude-opus-5-5.md`). If the page exists, use it as the model file and tell the user the advice comes from a live page the skill has not been checked against. If it does not exist, apply only the general files plus the closest model in the same family, say which one, and never present guesses about the unknown model as facts.

## Step 3: Audit

Go through every item of the audit checklist and the target model's "Remove from prompts" list. For each problem found, record: the quoted line, the problem, the rule, and the source link. Also note what the prompt already does well; a good prompt should be left mostly alone.

## Step 4: Rewrite

Rules for the rewrite:

- **Keep the author's intent and every hard requirement** (facts, constraints, output contracts, safety rules, template variables like `{{NAME}}`). If a requirement conflicts with model guidance, keep the requirement and say so in the report.
- **Change as little as possible.** Keep the author's voice and structure unless the structure itself is a problem. Every change must trace to a finding from Step 3. Ideas that do not fix a finding (new field definitions, extra examples, new sections) go under "Open questions and assumptions" in the report, not into the prompt. If the audit found little, the new prompt stays nearly identical to the old one; that is a good result.
- Make changes in this order:
  1. Remove or replace what hurts the target model.
  2. Apply missing general structure: the reason behind rules, what to do instead of what not to do, separated sections for mixed content, long documents before the question, examples where format matters.
  3. Add a model-specific block **only when the prompt's situation matches that block's symptom** (from the user's report, or clearly implied by the kind of prompt; for example an unattended agent, or a user-facing chat on Opus 5). List other relevant blocks under "Optional additions" in the report instead of adding them.
- **When the checklist or a model file names a replacement block, use that block** instead of writing your own version of the fix. Insert quoted blocks word for word. Fill in placeholders only where a block says to. Text you write yourself is not tested by the model maker; keep it short.
- **Recommend settings instead of wording** where the docs say a setting is the better lever (effort, thinking mode, `max_tokens`).
- Never add instructions that ask the model to write out its reasoning, and never keep a `<thinking>`, `<reasoning>`, or `<scratchpad>` section in the output format, even renamed to "short explanation". If the app needs an explanation, ask for it after the answer in a tag such as `<explanation>`.

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
- Effort: <level to start with, and what to compare it against>
- Thinking: <mode, or "leave as is">
- max_tokens: <guidance>
- Remove: <settings that now return errors, if any>

## 4. What to test
<two or three concrete checks on real traffic, each tied to a change above>

## 5. Open questions and assumptions
<facts that were guessed, and optional additions the user may want if they see a listed symptom; "None" if empty>
```

Write the report in plain language: short sentences, no unexplained jargon, and say what each setting or term means the first time it appears.

## When the skill starts on its own

If you started this skill because the user is writing or editing a prompt (not because they asked for an optimization), first confirm the target model if it is not stated, then present the audit findings and offer the rewrite. Do not write new files or publish a page until the user agrees.
