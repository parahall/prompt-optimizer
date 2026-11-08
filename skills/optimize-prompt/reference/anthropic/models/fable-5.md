# Claude Fable 5 (also Claude Mythos 5)

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) (section names below refer to this page).
API ID `claude-fable-5`. Default effort `high`. Thinking is always on (adaptive only, summarized output only). Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Overplanning or long surveys of options on ambiguous tasks
- Unrequested tidying or refactoring at higher effort
- Output elaborates beyond what is needed
- It pauses for the user too often in long workflows
- Long autonomous runs: progress reports must be trustworthy
- Unrequested actions
- Autonomous pipelines: turns end with "I'll now run X" or permission questions
- The harness must show context budgets, and the model offers to stop or hand off
- Final summaries after long work are hard to read
- The request lacks its purpose
- Subagents: wanted, and the lead should keep working
- The agent can keep notes between runs (memory)
- Long asynchronous agents must show content verbatim mid-task
- Long runs need self-verification

## How it differs from Opus 4.8

- Built for hard, long, ambiguous end-to-end work (hours to weeks for a person). Turns can run many minutes; autonomous runs can last hours.
- **Strong instruction following**: one short instruction steers a behavior; there is no need to list every case.
- At higher effort it can over-gather context and over-explain on routine work.
- Can take unrequested actions (drafting an email nobody asked for, defensive git branches).
- Can occasionally fabricate progress reports on long runs unless told to ground them.
- Dispatches parallel subagents readily and well.
- Does better when told the reason behind a request.
- In long agentic sessions, its text to the user can become hard to follow (arrow chains, private labels).
- Rarely, ends a turn with a statement of intent instead of the tool call, or suggests a new session because of context budget.
- **Skills and prompts written for earlier models are often too prescriptive** and can lower quality.

## Remove from prompts

- **Over-prescriptive instructions and long lists of banned behaviors**; one short instruction does the job. Review older skill text and remove what default behavior already does better. ("Strong instruction following", "Recommended scaffolding changes")
- **Requests to echo, transcribe, or explain internal reasoning in the reply** (`reasoning_extraction`; server-side fallback does not retry it).
- **Remaining-token countdowns shown to the model**, where the harness can avoid them. ("Rare cases of context-budget concern")

## Add when you see this symptom

### Overplanning or long surveys of options on ambiguous tasks

> Quoted from Anthropic · "Longer turns by default"
```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

### Unrequested tidying or refactoring at higher effort

> Quoted from Anthropic · "Consider all effort levels"
```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use feature flags or backwards-compatibility shims when you can just change the code.
```

### Output elaborates beyond what is needed

> Quoted from Anthropic · "Strong instruction following"
```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail and reasoning come after. Being readable and being concise are different things, and readability matters more.

The way to keep output short is to be selective about what you include (drop details that don't change what the reader would do next), not to compress the writing into fragments, abbreviations, arrow chains like A → B → fails, or jargon.
```

### It pauses for the user too often in long workflows

> Quoted from Anthropic · "Strong instruction following"
```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

### Long autonomous runs: progress reports must be trustworthy

> Quoted from Anthropic · "Ground progress claims during long runs"
```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

### Unrequested actions

> Quoted from Anthropic · "State the boundaries"
```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one. Before running a command that changes system state (restarts, deletes, config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

### Autonomous pipelines: turns end with "I'll now run X" or permission questions

> Quoted from Anthropic · "Rare cases of early stopping"
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking "Want me to…?" or "Shall I…?" will block the work. For reversible actions that follow from the original request, proceed without asking. Offering follow-ups after the task is done is fine; asking permission after already discussing with the user before doing the work is not. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ("I'll…", "let me know when…"), do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

### The harness must show context budgets, and the model offers to stop or hand off

> Quoted from Anthropic · "Rare cases of context-budget concern"
```text
You have ample context remaining. Do not stop, summarize, or suggest a new session on account of context limits. Continue the work.
```

### Final summaries after long work are hard to read

> Quoted from Anthropic · "Readability when communicating with the user"
```text
Terse shorthand is fine between tool calls. Your final summary is different: it's for a reader who didn't see any of that.

If you've been working for a while without the user watching (overnight, across many tool calls, since they last spoke), your final message is their first look at any of it. Write it as a re-grounding, not a continuation of your working thread: the outcome first, then the one or two things you need from them, each explained as if new. The vocabulary you built up while working is yours, not theirs; leave it behind unless you re-introduce it.

When you write the summary at the end, drop the working shorthand. Write complete sentences. Spell out terms. Don't use arrow chains, hyphen-stacked compounds, or labels you made up earlier. When you mention files, commits, flags, or other identifiers, give each one its own plain-language clause. Open with the outcome: one sentence on what happened or what you found. Then the supporting detail. If you have to choose between short and clear, choose clear.
```

### The request lacks its purpose
Fill in the brackets from what the user told you; ask if unknown.

> Quoted from Anthropic · "Give the reason, not only the request"
```text
I'm working on [the larger task] for [who it's for]. They need [what the output enables]. With that in mind: [request].
```

### Subagents: wanted, and the lead should keep working

> Quoted from Anthropic · "Parallel subagents"
```text
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.
```

### The agent can keep notes between runs (memory)

> Quoted from Anthropic · "Construct a memory system"
```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

### Long asynchronous agents must show content verbatim mid-task
Recommend a `send_to_user` tool (the page has the definition, "Create a send-to-user tool") plus this instruction; without the instruction the model rarely calls it.

> Quoted from Anthropic · "Create a send-to-user tool"
```text
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.
```

### Long runs need self-verification
Fresh-context verifier subagents beat self-critique. Fill in the interval.

> Quoted from Anthropic · "Recommended scaffolding changes"
```text
Establish a method for checking your own work at an interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the specification.
```

## API settings

- `high` for most tasks, `xhigh` for the most capability-sensitive, `medium`/`low` for routine work.
- At `high`/`xhigh`: large `max_tokens`. Adjust client timeouts and streaming for long turns.
- Safety classifiers cover offensive cybersecurity, biology and life sciences, and extraction of summarized thinking; configure fallback to Opus 4.8 if needed.
