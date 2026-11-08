# Claude Opus 5

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) (section names below refer to this page).
API ID `claude-opus-5`. Default effort `high`. Thinking on by default; can be disabled only at `high` or below. Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Replies are longer than the product needs (user-facing output)
- Too much narration during agentic work
- Written documents (reports, Markdown files) are padded
- A narrow task gets widened or transformed
- Too many subagents (cost-sensitive harness)
- Users see it correcting trivial slips
- The integration must keep thinking disabled, and tool calls appear as text or internal tags leak

## How it differs from Opus 4.8

- Strongest on hard multi-file coding; finishes whole tasks without stubs. Works best with the full specification up front and then left to run.
- Code review with high precision and recall, even at lower effort, but follows "only report high-severity issues" literally.
- **Writes longer replies** than earlier Opus models, and lowering effort does **not** shorten them. Files it writes are long too.
- **Narrates a lot** during agentic work.
- **Verifies and self-corrects without being told**; extra verification instructions cause over-verification. Narrates its own corrections more than earlier models.
- Can widen a task's scope with its own judgment.
- Delegates to subagents more readily.
- 1M-token context window with steady quality across it.

## Remove from prompts

- **Verification and double-check instructions** ("include a final verification step", "use a subagent to verify", "double-check your answer", "re-verify before responding"). Remove them rather than rewrite them; also remove harness steps that add separate verification. ("Task scope and over-verification", "Self-correction")
- **Severity or confidence filters in review prompts** ("only report high-severity issues", "be conservative"); ask it to report everything and filter in a separate pass. ("Capability improvements")
- **Requests to write reasoning in the reply** (`reasoning_extraction`). ("Reasoning in the response")
- **With thinking disabled: any rule telling the model not to think or reason**; it increases internal tag leakage. ("Running with thinking disabled")
- **Vision workarounds tuned for earlier models**: re-validate them.

## Add when you see this symptom

### Replies are longer than the product needs (user-facing output)
This is the usual case on Opus 5; add it to user-facing prompts unless length is already specified.

> Quoted from Anthropic · "Response length and verbosity"
```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

In a long system prompt, also add this reminder near the end:

> Quoted from Anthropic · "Response length and verbosity"
```text
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

### Too much narration during agentic work

> Quoted from Anthropic · "User-facing progress updates"
```text
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

To tune narration up instead, describe what updates should look like and give positive examples.

### Written documents (reports, Markdown files) are padded

> Quoted from Anthropic · "Written deliverable length"
```text
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

### A narrow task gets widened or transformed

> Quoted from Anthropic · "Task scope and over-verification"
```text
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

### Too many subagents (cost-sensitive harness)
With Claude Code or the Agent SDK, also mention the hard caps `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, and the SDK's `max_budget_usd`.

> Quoted from Anthropic · "Controlling subagent spawning"
```text
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

### Users see it correcting trivial slips

> Quoted from Anthropic · "Self-correction"
```text
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

### The integration must keep thinking disabled, and tool calls appear as text or internal tags leak
Do not name thinking tags specifically; the general form works better.

> Quoted from Anthropic · "Running with thinking disabled"
```text
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

## API settings

- Start at `high`; use `low` and `medium` liberally where quality holds; `xhigh` for demanding coding and agentic work. Re-run an effort sweep if levels were copied from an older model.
- Effort does not control reply length; prompt for length.
- Prefer thinking on at `low` effort over thinking disabled at similar cost.
- At `xhigh`/`max`: `max_tokens` about 64,000 to start; `disabled` returns a 400 error at those levels.

## Known traps

- Do not stack verification instructions on top of its own checking.
- Claude Code adds its own delegation instruction for Opus 5 only with the `claude_code` system prompt preset; with a custom prompt, add one yourself.
