# Claude Fable 5.2 (also Claude Mythos 5.2)

Checked against the docs on 2026-11-10.
Source: [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2) (section names below refer to this page).
API IDs `claude-fable-5-2` (Mythos 5.2: `claude-mythos-5-2`; the two share this prompting guidance but are separate models, and Mythos 5.2 is offered only to organizations verified through Anthropic's Cyber and Life Sciences Verification Programs). Default effort `high`. Thinking is always on (adaptive only; `enabled` and `disabled` return a 400 error). Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Agentic turns end before the work is done (more often at `low` and `medium`)
- Approval rules hold back routine work
- Agents ask for approvals they don't need, or hold back routine work, because cautions piled up in memory, notes, or messages between agents
- A coding agent repeats existing code instead of merging it, or reports nearby problems without fixing them
- Long agentic turns look silent, or the first tool call comes with no word to the user
- Agent sessions start more subagents than the task needs
- Final reports or handoffs are hard to follow for someone who did not watch the work
- Easy requests take too long or cost too much

## How it differs from earlier models

- The page does not say Fable 5.1's advice still applies, so this file does not inherit it; do not load `fable-5-1.md`. Instead, the page lists habits from Fable 5.1 and Opus 5.5 prompts to remove (see "Remove from prompts").
- At `high` and above it **thinks before almost every reply**, even a greeting. An instruction to answer directly does not stop it at `medium` and above (Fable 5.1 usually followed such a line). Effort is the control.
- **Effort barely changes reply length.** Use the prompt for length and tone.
- More likely to **stop early** on long multistep tasks, mostly at `low` and `medium`.
- **Follows instructions closely**: applies approval rules as written, holds back when cautious notes pile up in context, and turns hard style limits into choppy prose.
- **Responds to what the prompt says about who owns the code**: without an ownership statement it adds to the existing structure and reports nearby problems instead of fixing them.
- Writes **little user-facing text** during long runs of tool calls, and may make its first tool call without saying what it is about to do.
- Delegation depends on the harness: rarely with a minimal subagent tool, readily where prompts invite it. At `xhigh` and `max` it may start subagents to review its own work (Fable 5.1 did not). Early testers had good results using it as planner and orchestrator for other models.
- The API enforces the prefix check for every account: changing `system`, `tools`, or an earlier message and then sending thinking blocks back can return a 400 error.
- Works well on long-running asynchronous tasks, where the user comes back for the result.

## Remove from prompts

- **Instructions to think less** ("answer directly without deliberating"): no effect at `medium` and above; recommend a lower effort level instead. ("Review instructions written for earlier models", "Calibrate effort")
- **Requests to write reasoning in the reply** (`reasoning_extraction` refusals). To see how the model reasoned, recommend `display: "summarized"` and reading the thinking blocks. ("Safeguard refusals")
- **The Opus 5.5 "treat that answer as done" lines** for chat: on Fable 5.2 they reduced thinking on follow-ups but made the model far less likely to point out mistakes in its earlier answers. Remove them where the model should keep re-checking earlier answers; elsewhere, keep them only after testing. ("Review instructions written for earlier models")
- **Standing instructions to delegate** in system prompts, skills, and agent files, when the model starts more subagents than the tasks need. ("Review instructions written for earlier models")
- **A token budget that the harness writes into the prompt** (how many tokens the task may use and how many are left): recommend testing without it; removing a large budget lowered cost at `high` and `xhigh` with equivalent performance. This is about prompt text, not the API's task budgets. ("Review instructions written for earlier models")
- **Hard style rules for writing** ("one instruction per sentence, in 20 words or fewer"): they make the prose choppy. Remove the ones no longer needed before adding the "Communicating clearly" block. ("Review instructions written for earlier models")
- **Cautions in memory files, notes, and instruction files whose reason no longer holds.** Rewrite absolute rules so they state their scope and reason. ("Keep caution from piling up")

## Add when you see this symptom

### Agentic turns end before the work is done (more often at `low` and `medium`)
Add for agentic work at `low` or `medium`, or when early stops are seen. The page calls this text a starting point: insert it as written unless the product needs changes, and when adapting, keep its distinction between ordinary obstacles (diagnose and work through them) and deliberate blockers (leave them alone and report them). Expect about 30 percent more output tokens. It removed most endings that ask permission or offer to continue, but not endings that list what remains and then stop. Because the model asks less with this text, keep the product's own confirmation step for risky or irreversible actions.

> Quoted from Anthropic · "Finish the whole task"
```text
# Finishing work
Please avoid stopping while you still owe work the user asked for. Be persistent and do not stop unless needed.

While status notes are welcome, as is clarifying with the user on open decisions, carry on with work that does not depend on the user's answer without unnecessary stops.

If you notice yourself inviting the user to redirect you or offering to wait, instead proceed on the next part of the task. You may meet ordinary obstacles like errors, timeouts, locked files, empty results or failing tools. Diagnose them first, and when they are not real blockers, work through them with the access you have (wait and retry, fix the request, use another tool or source) rather than stopping unnecessarily.

If someone clearly decided something is a hard blocker, such as a file marked not to be touched, access that was intentionally withheld, or a safety guardrail, leave it alone, say plainly what you found, and look for another safe way to finish the task. Stopping before the task is complete is very rarely merited, as in when the task can't move forward without user input, or where the blocker is deliberate and should not be worked past. This does not override the need for confirmation on risky or destructive actions.
```

### Approval rules hold back routine work
Rewrite the rule so it names the exact actions it covers; the model applies approval rules as written. In Anthropic's testing, a rule that listed "sending messages to people outside this conversation" among steps needing approval made the model hold back about half of its routine requests to colleagues. Report a harness note too: when approving, say what is approved ("Yes, run the migration on the staging database") instead of a bare "continue" or thumbs-up. ("Approvals")

### Agents ask for approvals they don't need, or hold back routine work, because cautions piled up in memory, notes, or messages between agents
Mostly context and harness cleanup; report these as recommendations. ("Keep caution from piling up")
- Remove notes that are no longer needed (one old "never retry" note among a dozen cut retries from nearly all tries to about four in ten).
- Name the steps that need no approval, for example listing retries (only for calls that are safe to repeat). A general instruction to act more freely changed nothing.
- Check what reviewer agents attach to the context (a reviewer's "stop at the first error" blocked retries that a prompt line allowed).
- Write the exception into the rule itself ("get a go-ahead first, then …"); a separate line saying an approved step has its go-ahead barely helped.
- Keep the product's own confirmation step for risky or irreversible actions.

### A coding agent repeats existing code instead of merging it, or reports nearby problems without fixing them
Only where the model should own and improve the code. Leave it out where the user owns the code and wants it changed as little as possible; a scope-limiting rule elsewhere in the prompt does not cancel this sentence. Costs to report: about 1.5 times the output tokens, unrequested changes (often new tests and documentation), a changed behavior of an existing feature in one try in six to ten (more at higher effort), and closing summaries that skip small changes, so the diff should be reviewed.

> Quoted from Anthropic · "Say who owns the code"
```text
This codebase is yours: what it's for and how it's built are your call, and you'll keep building on it.
```

### Long agentic turns look silent, or the first tool call comes with no word to the user
First the client, before any prompt change: set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) or `"summarized"`, and render the non-empty `thinking` blocks between tool calls; at the default `"omitted"` their text is empty. Then, only where users watch the work live, use one or more of these. ("Keep users informed during long turns")

If the harness can change and the platform supports mid-conversation system messages: count consecutive tool-calling steps that give the user nothing to read (count with `display` at `"updates"` or `"summarized"`). After several in a row, append this reminder after the latest tool results as a turn-scoped system message (`clear_at: "next_user_message"`, beta header `mid-conversation-system-clear-at-2026-08-21`). Leave each reminder in `messages` on later requests; removing or rewording one invalidates later thinking blocks.

> Quoted from Anthropic · "Keep users informed during long turns"
```text
The user hasn't heard from you in a while: say in a few words what you're doing, then continue.
```

For an opening line before the first tool call, brief updates, and a closing recap, where a human is directly in the loop (about 20 percent more output tokens), add to the system prompt:

> Quoted from Anthropic · "Keep users informed during long turns"
```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own (what you found, what you did, and what's next), so a reader who only sees the last message has the full picture.
```

If the harness cannot change, or the platform has no mid-conversation system messages, add instead:

> Quoted from Anthropic · "Keep users informed during long turns"
```text
Every few tool calls, give the user a one-line update on where things stand.
```

Even with these, expect several tool calls between updates. For asynchronous work, where the user comes back for the result, gaps matter less.

### Agent sessions start more subagents than the task needs
First review the lines in system prompts, skills, and agent files that ask for delegation. Change the description of the tool that starts subagents only if the model still over-delegates. The page does not print Anthropic's tested description; it says the description does three things, cost first: states what a subagent adds to the cost of a session, says when delegation is worth it and when it isn't, and tells the model how to brief a subagent. Write such a description in your own words, mark it as untested wording, and suggest testing; more text about cost means less delegation. At `xhigh` and `max` the model may start subagents to review its own work, so recommend checking which model the harness runs subagents on. ("Set expectations for subagents")

### Final reports or handoffs are hard to follow for someone who did not watch the work
Add where the model writes final reports or handoffs. The page says to adjust the text to the readers and the product, so it may be adapted; remove hard style rules first. It made reports less dense, and on workflow tasks it shortened sentences. Length or required details can be added as separate instructions.

> Quoted from Anthropic · "Make reports easy to follow"
```text
# Communicating clearly
Write for an intelligent but low-context reader. The person reading has not seen your tool calls, your reasoning or the files you opened, and may be switching in from other work. Messages should generally be self-contained: the reader should understand what you mean without having to dig for other context. Put the key points in the first few sentences. Practice progressive disclosure in your sentence order, and do not use undefined references and ideas in line 1 that won't make sense until the reader reaches line 12.

Use plain words, and write in clear, understandable full sentences. Do not use a term or abbreviation that you made up during the work. Say what the thing is in a way any reader would understand. Write mostly in the style of ASD-STE100 Simplified Technical English: short sentences, one idea per sentence, active voice, and consistently using the same word for the same thing. Use a paragraph of flowing prose where ideas connect, and keep bullets for lists of separate items. Leave out unnecessary details unless the reader asks and practice concision, but do ensure that your messages have the key context. Aim to make your user-facing text as human-readable and clear as possible.
```

### Easy requests take too long or cost too much
A setting, not wording: run those turns at a lower effort level, with the per-message effort change where available (see API settings). Prompt instructions to answer directly do not work at `medium` and above. ("Calibrate effort")

## API settings

- Set `effort` to `high` explicitly, then run evals at `medium` and `xhigh` too. `low`: quick back-and-forth, well-specified tasks, high-volume work such as fast subagents. `medium`: interactive coding, chat, everyday knowledge work. `high`: hard coding, research, agentic work, long unattended runs. `xhigh`: hardest long-running coding and agentic work, only with a measured gain. `max`: measuring the ceiling, or open-ended problems where time and tokens don't matter. Re-run the sweep instead of copying a level from Fable 5.1 or Opus 5.5.
- At `high` and above, set a large `max_tokens` (it caps thinking plus reply).
- Mixing levels in one workflow (for example plan at `medium`, run the long unattended part higher): per-message effort change (beta header `mid-conversation-output-config-2026-07-01`; on Amazon Bedrock's InvokeModel API, in the body's `anthropic_beta` array) where the platform supports it, which keeps the prompt cache; otherwise a new top-level `effort`, which restarts the cache.
- Apply prompt changes to **new conversations only**. Mid-conversation, put new instructions in the newest turn, or in a mid-conversation system message where available. Keep history append-only; to shorten it, use context editing or compaction that keeps no earlier turns after the summary. `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta header `thinking-binding-controls-2026-08-01`) drops invalid thinking blocks instead of erroring, but the model then thinks again and uses more output tokens.

## Known traps

- "Think less" lines and effort levels copied from Fable 5.1 or Opus 5.5.
- The ownership sentence is not cancelled by a scope rule elsewhere in the prompt.
- The "Finishing work" text makes the model ask less, so the product's own confirmation for risky actions must stay.
- Approval and "never" rules are applied literally; vague rules hold back routine work.
