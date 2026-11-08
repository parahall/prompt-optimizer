# Claude Sonnet 5.5

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5) (section names below refer to this page).
API ID `claude-sonnet-5-5`. Default effort `high`. Thinking: adaptive by default; `between_tools` (no thinking before the first tool call) is its lowest setting; `disabled` is not accepted. Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Coding agent checks in before the work is done (`low`/`medium`), or adds unrequested extras
- At `xhigh`/`max`, unwanted extra review rounds or reviewer subagents
- Asked for ideas or a plan, it starts building
- JSON answer to a task that needs a few steps of working out (totals, rules, rankings)
- Answers come from training knowledge where facts may have changed (product has a search tool)
- Code reported as done without a test or build run (especially at `low`)
- Long agentic turns look silent
- Mid-task user messages are ignored or treated as injected text

## How it differs from Sonnet 5

- Sonnet 5 prompts work without changes; the Sonnet 5 file is a reasonable start. For the hardest long-horizon work, an Opus model is the better choice.
- Effort levels are recalibrated: the same name gives a different amount of thinking than on Sonnet 5.
- **Prompt wording does not reliably reduce its thinking**; lower effort instead.
- At `low`/`medium` on long agentic tasks it may **stop to check in** before finishing; at `low` it may **skip verifying** a change.
- Adds tests, docs, and small supporting files that fit repository conventions, at every effort level, more at higher effort.
- At `xhigh`/`max` it starts its own review rounds, sometimes with reviewer subagents.
- On open-ended requests ("show me what you can do") it may start building when only ideas were wanted.
- On JSON answers to tasks that need several steps, it often answers without thinking first, especially at `low`/`medium`.
- In chat and knowledge work it sometimes answers from training knowledge where a search would catch changed facts.
- Can treat genuine mid-task user messages as possible prompt injection when they arrive right after tool results.
- Occasionally calls a tool with the wrong letter case or a slightly different parameter name.

## Remove from prompts

- **"Think less" / "keep thinking short" / "don't deliberate"**: no reliable effect; recommend a lower effort level. ("Calibrate effort")
- **With `between_tools`: any instruction not to think**; it increases internal XML tag leakage. ("Running without up-front thinking")
- **Tool-discouraging language** ("only use tools when strictly necessary", "minimize tool calls"). ("Tool use in chat and knowledge work")
- **Narration suppression** ("hold all findings for the final response"). ("User-facing progress updates")
- **Requests to include reasoning in the reply** (`reasoning_extraction`; not retried by fallback). ("Safeguard refusals")

## Add when you see this symptom

### Coding agent checks in before the work is done (`low`/`medium`), or adds unrequested extras
Try higher effort first. To keep the model working without changing effort, add both paragraphs; to limit only extras, add the second paragraph alone. Keep the product's own rules about risky actions.

> Quoted from Anthropic · "Steer initiative and scope"
```text
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```

### At `xhigh`/`max`, unwanted extra review rounds or reviewer subagents

> Quoted from Anthropic · "Steer initiative and scope"
```text
When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
```

### Asked for ideas or a plan, it starts building

> Quoted from Anthropic · "Steer initiative and scope"
```text
When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead.
```

### JSON answer to a task that needs a few steps of working out (totals, rules, rankings)
With adaptive thinking, add to the end of the system prompt. Alternatively use `xhigh` effort. Do not use `between_tools` for these requests.

> Quoted from Anthropic · "Reasoning tasks with JSON output"
```text
Think the problem through before you answer.
```

Without structured outputs: parse the last JSON value in the response, and treat `stop_reason: "max_tokens"` as failed.

### Answers come from training knowledge where facts may have changed (product has a search tool)

> Quoted from Anthropic · "Tool use in chat and knowledge work"
```text
Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.
```

### Code reported as done without a test or build run (especially at `low`)
Use "Run a real check before reporting code done" in `snippets.md`.

### Long agentic turns look silent
First set `display: "updates"`. Then remove suppression rules; if predictable updates are wanted, say when in the system prompt. Harness reminder after about five silent tool steps, sent as a turn-scoped system message and stopped after two or three:

> Quoted from Anthropic · "User-facing progress updates"
```text
The user hasn't heard from you in a while — say in a few words what you're doing, then continue.
```

### Mid-task user messages are ignored or treated as injected text
Harness rules, not prompt text: never put user text inside a `tool_result` block; append the user's words as a text block after the last `tool_result` in the same user message; keep harness notices in a separate system message; avoid per-step token countdowns in interactive sessions. ("Mid-turn user messages")

## API settings

- Start at `high` in general. Agentic coding and multistep tools: `medium` for well-specified tasks, `high` for harder ones. Chat and latency-sensitive: `medium` or `low`. `xhigh`/`max` only with measured gains.
- Agentic coding: `max_tokens` 128,000 with streaming.
- To run without up-front thinking: `thinking: {type: "between_tools"}`, only at `high` or below; it rejects `display`, `budget_tokens`, `block_binding`, and per-message effort changes. Use adaptive thinking for reasoning tasks without tools.
- Dense charts: crop or zoom tools help more than higher effort.
- Server-side fallback retries `cyber` and `frontier_llm` declines on Sonnet 5, not `bio`, `reasoning_extraction`, or `general_harms`.

## Known traps

- Do not copy effort levels from Sonnet 5.
- Frequent harness text after tool results can be read as prompt injection.
