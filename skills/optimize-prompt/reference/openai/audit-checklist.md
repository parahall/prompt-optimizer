# Audit checklist for OpenAI GPT prompts

Checked against the docs on 2026-11-08. Sources: the model files in `models/` (each links its pages), [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning), [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices).

Go through every item, in this order. For each pattern found, apply the verdict for the target family. "Current families" means GPT-6, GPT-5.6, and GPT-5.5. OpenAI's main advice for current families is to **simplify**: removing repeated and conflicting rules usually helps more than adding blocks.

Contents
1. Contradictions
2. Repetition and dead weight
3. Step-by-step process scripts
4. Requests to think step by step
5. Absolute words and capitals
6. Length and brevity rules
7. Formatting defaults
8. Asking, approval, and autonomy rules
9. Output schemas written in prose
10. The current date
11. Tool guidance placement and tool lists
12. Tone labels and language rules
13. Skill and instruction-file conflicts (GPT-6)
14. Habits from older GPT models
15. Habits from other providers
16. Layout for prompt caching

---

## 1. Contradictions (check first)

**Spot it:** two rules that cannot both hold, or hold without saying which wins: "always look up X first" next to "in an emergency, act immediately"; "never act without consent" next to "do it automatically"; "be concise" next to "err on the side of completeness"; a formal tone next to "use emojis sometimes"; examples that show behavior the rules forbid.

**Verdict, all families: resolve every conflict.** Say which rule wins and when (an explicit exception), or delete one, when at least one side is a soft preference. When both sides are hard requirements (safety, permissions, legal or business rules), do not choose: keep both, name the conflict, and ask the user which wins (see `SKILL.md`, Step 4). GPT-5-class models follow prompt contracts closely and spend reasoning trying to reconcile conflicts, which OpenAI says hurts them more than missing detail. GPT-4.1 tends to follow whichever conflicting rule comes last. Name each conflict in the report.

Sources: GPT-5.6 prompting page, "Simplify prompts first"; Using GPT-5, "Instruction following"; Using GPT-4.1, "Recommended Workflow".

## 2. Repetition and dead weight

**Spot it:** the same rule stated several times; style or process lines that do not change behavior; examples that add nothing; process instructions for things the model already does; tools unrelated to the task.

**Verdict:**
- GPT-6, GPT-5.6, GPT-5.5: **remove** (leaner prompts scored higher with far fewer tokens in OpenAI's tests). State each rule once. Keep examples and style rules that encode a real product requirement.
- GPT-5.4 Mini and Nano, GPT-4.1: be careful; small and older models need more explicit structure (see item 3). Remove only true duplicates.

## 3. Step-by-step process scripts

**Spot it:** "First do A, then B, then compare every field, then…" for a task where only the result matters.

**Verdict:**
- GPT-6, GPT-5.6, GPT-5.5: **rewrite as outcome + success criteria + stop rules** (GPT-5.6 and GPT-5.5: use the "Resolve the customer's issue end to end" block in their model file; GPT-6 has no such block, so write the outcome, success criteria, and stop rules in your own words). Keep a fixed order only where the exact path is a real requirement (safety steps, required lookups before an action).
- GPT-5.4 Mini and Nano: **keep or add** the full execution order when tools or side effects matter; this model is literal and weak at implied steps.
- GPT-4.1: an ordered list of workflow steps is the recommended pattern.

## 4. Requests to think step by step

**Spot it:** "think step by step", "explain your reasoning before answering", "show your work", a "reasoning" section to fill before the answer.

This item is about asking the model to reason out loud. It is not about work plans: staged plans, a plan tool, or naming the current phase of long work are still recommended for current families (GPT-5.6 upgrade guide: "staged plans, current-layer awareness, and concise handoffs for long work").

**Verdict:**
- GPT-5-class and GPT-6 models at effort `low` or higher: **remove.** They reason internally; OpenAI says such instructions are unnecessary and can hurt. Control depth with `reasoning.effort`; put success criteria in the prompt instead.
- At effort `none`: OpenAI documents that asking the model to **plan or outline its steps** helps on GPT-5.1, GPT-5.2, and GPT-5.4 (and at `minimal` on GPT-5). Keep such an instruction on those models. For other models that accept `none` (GPT-5.6, GPT-6.1 Terra, GPT-6 Luna, GPT-6 Sol), the docs do not say; keep an existing planning instruction, and say the benefit is documented only for the older models.
- GPT-4.1 (not a reasoning model): prompted chain of thought helps; keep it.
- "Think harder" / "use pro mode" / "generate several candidates": remove; use `reasoning.mode: "pro"` (GPT-5.6, GPT-6) if more work is wanted.

## 5. Absolute words and capitals

**Spot it:** ALWAYS, NEVER, MUST, ONLY, CRITICAL in capitals; "you must call a tool before responding".

**Verdict:**
- GPT-6, GPT-5.6, GPT-5.5: keep absolutes **only for true invariants** (safety rules, required fields, actions that must never happen); turn judgment calls (when to search, ask, use a tool, keep going) into decision rules.
- GPT-5.4 Mini: "you MUST" alone does not work; add structure (numbered steps, decision rules, explicit action definitions).
- GPT-4.1: capitals and incentives are usually unnecessary and can make it apply a rule too strictly.
- Any family: "always call tool X first" can make the model invent tool inputs when information is missing; add "if you don't have enough information to call the tool, ask the user for what you need".

## 6. Length and brevity rules

- GPT-5.6: already concise; "Be concise" / "Keep it short" can make answers **too short**. Remove if so, set `text.verbosity`, and say what a short answer must keep (block in `models/gpt-5-6.md`).
- GPT-5.5: concise and direct by default; for concise output prefer `text.verbosity: "low"`; conversational products may need warmth and rationale added.
- GPT-6: tends toward detailed, formatted replies; explicit length and structure guidance is useful.
- All: concrete limits (sentences, words, sections) work better than "brief".

## 7. Formatting defaults

- GPT-6 and GPT-5.4: lean on lists, tables, Markdown. If the product wants prose, add the paragraph rule in `models/gpt-6.md` or flatten lists with the rule in `models/gpt-5-4.md`.
- GPT-5.5: the docs give a recommended formatting block that makes paragraphs the default and uses lists sparingly (in `models/gpt-5-5.md`); they do not say the model writes paragraphs without being told.
- A prompt written in heavy Markdown tends to get Markdown back.

## 8. Asking, approval, and autonomy rules

- GPT-6: **asks for clarification and approval more often** than earlier models. If the product wants autonomy, add the initiative blocks in `models/gpt-6.md`; remove hypothetical-risk warnings and approval steps for reversible actions.
- GPT-5.6: "ask first" / "wait for approval" repeated in several places blocks safe work. **Keep one compact policy** (the autonomy block in `models/gpt-5-6.md`) and name safe local actions.
- GPT-5.4 Mini: asks follow-up questions by default; say explicitly whether to ask one.
- Customer-facing or risky-action agents (payments, deletes, external writes): **keep real confirmation rules**. Never paste GPT-5's `<persistence>` block ("Do not ask the human to confirm or clarify assumptions") into such agents on any model.

## 9. Output schemas written in prose

- GPT-5.5 and later: OpenAI says to remove schema definitions from the prompt "where possible" and use Structured Outputs (`text.format` with a JSON schema) instead. The rewritten prompt is only half of the change, so **remove the prose schema only if the user confirms the app already sends, or will send, an equivalent schema in the request**. Otherwise keep the prose schema in the prompt and recommend Structured Outputs in the settings part of the report, saying the prose schema can be deleted once the request carries the schema.
- GPT-5.4 Mini: a schema alone is not enough for tool workflows; show the correct flow too.
- GPT-5.2 extraction: "Always provide a schema or JSON shape for the output. You can use structured outputs for strict schema adherence." When migrating, first check how the app supplies the shape today (prompt text or Structured Outputs), then apply the GPT-5.5 rule above.

## 10. The current date

- GPT-5.5: **remove** a plain current-date line; the model knows the UTC date. Keep a date only for a business timezone, policy-effective date, user-local date, or other non-UTC reference.
- Other families: the docs do not say; leave existing date lines alone.

## 11. Tool guidance placement and tool lists

- Put what a tool does, when to use it, inputs, side effects, and errors in the tool's own `description`; keep only cross-tool policy in the system prompt (GPT-5.5).
- Expose only task-relevant tools (GPT-5.6).
- Say when a lookup must happen before an action (dependency rule), and when independent reads can run in parallel.
- Programmatic Tool Calling (GPT-5.6, GPT-6): generic "use it efficiently" lines do not work; state the bounded stage, tools, output schema, retries, and handoff.

## 12. Tone labels and language rules

- "Be friendly / empathetic / professional" alone is ambiguous (GPT-5.6): describe the writing choices (how directly to answer, when to acknowledge a problem, whether to reassure or sign off).
- "Always respond in the user's language": keep only if it is the real requirement; it can cause unwanted language switching (GPT-5.6). Say which output language and when it changes.
- Personality must not override required formats (if the user asks for JSON, return JSON).

## 13. Skill and instruction-file conflicts (GPT-6)

GPT-6 follows skills and files like `AGENTS.md` closely; unclear or conflicting guidance there can stop work. If the prompt runs in an app that loads skills or instruction files, add the priority sentence in `models/gpt-6.md` and point out conflicts between the prompt and those files.

## 14. Habits from older GPT models

When migrating to a current family, look for and usually remove or rewrite:
- GPT-5 `<persistence>` / `<maximize_context_understanding>` style blocks and shouting thoroughness language (caused over-searching on GPT-5).
- GPT-5.1/5.2 long procedural XML stacks (`<solution_persistence>`, `<output_verbosity_spec>` with fixed sentence counts) where the current family is concise by default.
- "After every N tool calls, summarize progress" and narrate-every-step preamble rules; current guidance is sparse updates at phase changes.
- The o1-era `system` role: use the `developer` role for reasoning models.
- `temperature` / `top_p` settings: they fail once effort is above `none`.
- Old effort values: `minimal` → start at `low` on GPT-6; an omitted effort that used to mean `none` (GPT-5.1–5.4) now means `medium` on 5.6 and 6.

## 15. Habits from other providers

When the prompt was tuned for Claude: remove Claude API wording (effort levels described as Claude's, "adaptive thinking", requests for reasoning inside `<thinking>` tags meant for Claude's extended thinking) and Claude model names; XML-tagged sections themselves are fine on GPT models.

## 16. Layout for prompt caching

Static content first (role, rules, examples, tool definitions), dynamic content last (user data, retrieved documents, timestamps). Changing text near the top of a large prompt on every request loses cache hits; on GPT-5.6 and GPT-6 cache writes also cost extra.
