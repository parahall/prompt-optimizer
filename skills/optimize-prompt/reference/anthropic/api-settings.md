# API settings for Claude models

Checked against the docs on 2026-11-08. Sources: [Effort](https://platform.claude.com/docs/en/build-with-claude/effort), [Thinking support by model](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#thinking-support-defaults-and-rejected-configurations-by-model), [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost), [Models overview](https://platform.claude.com/docs/en/models/overview), and each model's prompting page.

Many problems are fixed by settings, not wording. Always report recommended settings next to the rewritten prompt. Only recommend settings the target model accepts.

Contents
1. The controls
2. Per-model table
3. Starting effort by kind of work
4. Settings that now return errors
5. Rules that affect how the prompt may change

## 1. The controls

- **Effort** (`output_config.effort`): `low`, `medium`, `high`, `xhigh`, `max`. How much the model thinks and works on the whole reply. It is the first control to change for quality, speed, and cost; wording comes second. Level names do not mean the same amount of thinking across models, so never copy a level from another model without testing.
- **Thinking** (`thinking.type`): `adaptive` (the model decides how much to think), `disabled`, and on Sonnet 5.5 only `between_tools` (no thinking before the first tool call). Manual `enabled` with `budget_tokens` is the old mode.
- **Thinking display** (`thinking.display`): `omitted` (default on the newest models: thinking text comes back empty), `summarized` (a summary of the reasoning), `updates` (beta: summaries of the short user-facing notes the model writes between tool calls).
- **`max_tokens`**: a hard cap on thinking plus the reply, per request. Thinking counts toward it even when its text is not returned.

## 2. Per-model table

| Model | API ID | Default effort | Effort levels | Thinking when the field is omitted | Thinking can be turned off? |
|---|---|---|---|---|---|
| Fable 5.2 / Mythos 5.2 | `claude-fable-5-2` / `claude-mythos-5-2` | high | all five | adaptive, always on | No (`disabled` returns 400) |
| Fable 5.1 / Mythos 5.1 | `claude-fable-5-1` / `claude-mythos-5-1` | high | all five | adaptive, always on | No (`disabled` returns 400) |
| Fable 5 / Mythos 5 | `claude-fable-5` / `claude-mythos-5` | high | all five | adaptive, always on | No |
| Opus 5.5 | `claude-opus-5-5` | **medium** | all five | adaptive, always on | No |
| Opus 5 | `claude-opus-5` | high | all five | adaptive, on | `disabled` only at effort `high` or below |
| Opus 4.8 | `claude-opus-4-8` | high | all five | **off** (send `adaptive` to turn on) | Yes |
| Sonnet 5.5 | `claude-sonnet-5-5` | high | all five | adaptive, on | Use `between_tools` (not `disabled`), only at effort `high` or below |
| Sonnet 5 | `claude-sonnet-5` | high | all five | adaptive, on | Yes (`disabled`) |
| Haiku 5.5 | `claude-haiku-5-5` | **medium** | all five | adaptive, on | `disabled` only at effort `high` or below |
| Opus 4.7 | `claude-opus-4-7` | high | all five | off | Yes |
| Opus 4.6 | `claude-opus-4-6` | high | low, medium, high, max | off | Yes; manual budgets deprecated |
| Sonnet 4.6 | `claude-sonnet-4-6` | high | low, medium, high, max | off | Yes; manual budgets deprecated |
| Opus 4.5 | `claude-opus-4-5` | high | low, medium, high | off; manual `budget_tokens` only | Yes |
| Haiku 4.5 | `claude-haiku-4-5` | no effort setting | none | off; manual `budget_tokens` only | Yes |

All current models: 1M-token context window, 128K max output (synchronous API).

## 3. Starting effort by kind of work

Always say: start here, then compare two or three levels on real traffic.

| Model | Chat, latency-sensitive | Agentic coding, multistep tools | Knowledge work, hard reasoning |
|---|---|---|---|
| Fable 5.2 | `low` for quick, well-specified, high-volume work; `medium` for chat and interactive coding | `high`; `xhigh` only with a measured gain | `high` (most of the gain is already there) |
| Fable 5.1 | `medium` or `low` (at `low` it searches less) | `high`; `xhigh`/`max` only with a measured gain | `high` |
| Fable 5 | `medium` or `low` | `high`; `xhigh` for the most demanding | `high` |
| Opus 5.5 | `low` or `medium` | `medium` (matched Opus 5 at `high` in Anthropic's tests) | `medium`; test `high` |
| Opus 5 | `low` or `medium` | `high`; `xhigh` for demanding work | `high` |
| Opus 4.8 / 4.7 | `low` for short, scoped replies; `medium` otherwise | `xhigh` | at least `high` |
| Sonnet 5.5 | `medium` or `low` | `medium` for well-specified tasks, `high` for harder or longer ones | `high` |
| Sonnet 5 | `low` | `high`; `xhigh` for the hardest | `high` |
| Haiku 5.5 | `low` | `medium` | `high` (also for strict instruction following) |
| Sonnet 4.6 | `low` | `medium` (recommended default) | `high` |

`max_tokens`: leave room for thinking. Opus 5.5 and Sonnet 5.5 agentic coding: 128,000 (the maximum) with streaming. Opus 5, Opus 4.8, Opus 4.7 at `xhigh`/`max`: start at 64,000. Fable 5.1 long deliverables at `xhigh`/`max`: size for thinking plus the reply. Fable 5.2 at `high` and above: a large `max_tokens`.

## 4. Settings that now return errors

Report any of these found in the user's code or described setup:

- `thinking: {type: "enabled", budget_tokens: N}`: 400 error on Claude 4.7 and later models (deprecated on 4.6). Replace with `adaptive` plus an effort level.
- `thinking: {type: "disabled"}` on Fable 5.2, Fable 5.1, Fable 5, Opus 5.5, Sonnet 5.5 (use `between_tools`), and on Opus 5 / Haiku 5.5 at `xhigh` or `max`.
- `between_tools` on any model other than Sonnet 5.5, or on Sonnet 5.5 at `xhigh`/`max`. `between_tools` also rejects `display`, `budget_tokens`, and per-message effort changes.
- A prefilled last assistant message: 400 error on Claude 4.6 models and later.
- `temperature`, `top_p`, `top_k` on Sonnet 5: 400 error. The docs call this "new for Sonnet-class models"; check the target model's migration guide for other models. Use prompt instructions for tone and variety instead.

## 5. Rules that affect how the prompt may change

- **Keep the system prompt fixed within a conversation** on Fable 5.2 (the API enforces the prefix check for every account), Haiku 5.5, and the 5.1-generation models. Changing `system` or `tools` mid-conversation invalidates earlier thinking blocks (can return a 400 error). Put new instructions in a mid-conversation system message or the newest user turn instead. Tell the user to apply the optimized prompt to new conversations only.
- **Changing top-level effort between requests breaks the prompt cache.** For per-turn changes, recommend the per-message effort change (beta) on the models that support it: Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, and Haiku 5.5 (not Fable 5). It needs the beta header `mid-conversation-output-config-2026-07-01`; without it the request returns a 400 error. On Sonnet 5.5 with `between_tools` and on Haiku 5.5 with `thinking: {type: "disabled"}`, a per-message effort that differs from the level in effect also returns a 400 error; to vary effort per turn on those two models, use adaptive thinking.
- **Read responses by block type.** On models where thinking is on, a reply may start with a `thinking` block; code that reads `content[0].text` breaks.
- **Progress updates on Opus 5.5, Sonnet 5.5, Fable 5.2, Fable 5.1** arrive as thinking blocks that are empty at the default display. If the user says the agent "looks silent", recommend `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) before changing the prompt. Only with adaptive thinking: on Sonnet 5.5 with `between_tools` the notes already come back with their summary text, and sending `display` returns a 400 error.
