# Older OpenAI models: GPT-5.3-Codex, GPT-5.2, GPT-5.1, GPT-5, GPT-4.1

Checked against the docs on 2026-11-08.
Sources: [Using GPT-5.3-Codex](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.3-codex), [Using GPT-5.2](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.2), [Using GPT-5.1](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.1), [Using GPT-5](https://developers.openai.com/api/docs/guides/latest-model/gpt-5), [Using GPT-4.1](https://developers.openai.com/api/docs/guides/latest-model/gpt-4.1) and the matching cookbook guides (the GPT-5 and GPT-5.1 cookbook guides are marked "archived").

Use this file mainly to **recognize habits written for these models** when a prompt is migrating to a current model, then follow the target model's file. Many patterns that were right for these models hurt GPT-5.5 and later (long procedural blocks, "persistence" blocks, many MUST rules, schemas in the prompt).

## GPT-5.3-Codex (`gpt-5.3-codex`)

- Coding-agent model; Responses API only. Effort `low`, `medium`, `high`, `xhigh` (**no `none`**); `medium` recommended for interactive coding.
- **`phase` is required**: dropping assistant `phase` values when rebuilding history degrades performance significantly.
- Trained to follow `AGENTS.md` files closely.
- Tooling: use OpenAI's `apply_patch`, a `shell_command` tool taking a string, and `update_plan`; name custom tools after real terminal commands; truncate tool output to about 10K tokens.
- The page has a full starter system prompt ("Recommended Starter Prompt"). Its autonomy lines:

> Quoted from OpenAI · "Using GPT-5.3-Codex" · "Recommended Starter Prompt"
```text
- Bias to action: default to implementing with reasonable assumptions; do not end your turn with clarifications unless truly blocked.
- Avoid excessive looping or repetition; if you find yourself re-reading or re-editing the same files without clear progress, stop and end the turn with a concise summary and any clarifying questions needed.
```

- Known failure modes: overthinking before the first useful action, "loggy" status updates, repetitive tics ("Good catch", "Got it").

## GPT-5.2 (`gpt-5.2`)

- Effort `none` (**default**), `low`, `medium`, `high`, `xhigh`. `temperature`, `top_p`, `logprobs` only at `none`. 400K context.
- Compared with 5.1: more deliberate, lower verbosity, stronger instruction adherence, more tool actions in interactive flows, conservative grounding. GPT-5 and 5.1 guidance largely carries over.
- Prompts use many XML blocks: `<output_verbosity_spec>`, `<design_and_scope_constraints>`, `<long_context_handling>`, `<uncertainty_and_ambiguity>`, `<user_updates_spec>`, `<tool_usage_rules>`, `<extraction_spec>`, `<web_search_rules>`. Scope example:

> Quoted from OpenAI · "Using GPT-5.2" · "Preventing Scope drift"
```text
<design_and_scope_constraints>
- Explore any existing design systems and understand it deeply.
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no UX embellishments.
- Style aligned to the design system at hand.
- Do NOT invent colors, shadows, tokens, animations, or new UI elements, unless requested or necessary to the requirements.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>
```

- At effort `none`, ask the model to think or outline its steps before answering.
- 5.2 extraction guidance says: "Always provide a schema or JSON shape for the output. You can use structured outputs for strict schema adherence." When migrating to 5.5 or later, first check how the app supplies the shape (prompt text or Structured Outputs), then follow `audit-checklist.md`, item 9.

## GPT-5.1 (`gpt-5.1`)

- Effort `none` (**default**), `low`, `medium`, `high`. Can end too early or be too concise; its guide adds persistence and completeness blocks (`<solution_persistence>`), user-update specs, and length specs (`<output_verbosity_spec>`).
- At effort `none`, planning instructions help, for example:

> Quoted from OpenAI · "Using GPT-5.1" · "Using the “none” reasoning mode for improved efficiency"
```text
You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls, ensuring user's query is completely resolved. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully. In addition, ensure function calls have the correct arguments.
```

- Its guide recommends two-step metaprompting: first diagnose failure modes and the prompt lines that cause them, then make a surgical revision that keeps the structure and length.

## GPT-5 (`gpt-5`)

- Effort `minimal`, `low`, `medium` (default), `high`. Introduced `text.verbosity`, tool preambles, and custom tools.
- Its guide's best-known blocks: `<context_gathering>` (less eagerness), `<persistence>` (more eagerness: "Do not ask the human to confirm or clarify assumptions"), `<tool_preambles>`, `<self_reflection>`.
- **Contradictions hurt GPT-5 badly**: it spends reasoning trying to reconcile conflicting rules.
- Cursor's experience in the guide: shouting thoroughness language ("Be THOROUGH… FULL picture") made GPT-5 over-use search; softening it fixed that.
- Do not copy `<persistence>` into customer-facing or risky-action agents on any model; it tells the model never to ask.

## GPT-4.1 (`gpt-4.1`)

- **Not a reasoning model**: prompted chain of thought ("think carefully step by step") helps here, unlike on GPT-5-class models at effort `low` or higher.
- Follows instructions very literally; when instructions conflict, it tends to follow the one closer to the end of the prompt. All-caps and incentives are usually unnecessary and can make it over-apply a rule.
- Agent prompts used three reminders: persistence, tool use instead of guessing, and optional explicit planning.
- With long context, instructions at both the beginning and end of the context worked best; if only once, above the context.
- When migrating from GPT-4.1 to GPT-5.4 or later, start at effort `none` (5.4) or the lowest supported level, and remove chain-of-thought instructions once the model reasons on its own.
