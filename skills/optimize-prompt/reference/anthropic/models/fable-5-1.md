# Claude Fable 5.1 (also Claude Mythos 5.1)

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) (section names below refer to this page).
API ID `claude-fable-5-1`. Default effort `high`. Thinking is always on. Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Chat replies need more structure than they get
- Long agentic turns are silent, or the final message covers only the last step
- Autonomous or asynchronous work stops early ("Next, I'll…", "Shall I apply this?")
- Unrequested fixes, extensions, or too many committed tests
- Prose is dense or mannered
- Summaries copy source wording without quotation marks
- At `low` effort, answers come from memory instead of search
- Whole files rewritten for small changes
- Agent loops issue one independent tool call per turn
- Long deliverables at `xhigh`/`max` take very long or hit `max_tokens`
- Client-side compaction summaries drop details

## How it differs from Fable 5

- Fable 5 prompts work without changes; the Fable 5 file still applies. The items below are the differences.
- **Writes fewer user-facing updates** during long tool-calling turns, more so at higher effort.
- **Formats less**: less bold, fewer headers, lists, and quotation marks.
- Prose has few stock phrases but can be **dense**: long sentences, few paragraph breaks.
- More likely to **reproduce source text without quotation marks** when summarizing.
- On long asynchronous work it can end a turn by describing the next step instead of doing it, or ask permission for work already requested.
- On open-ended features it may fix nearby code, extend behavior, or commit more tests than needed.
- At `low` effort it **searches less** and answers from memory more.
- More likely to **rewrite whole files** for small edits.
- At `xhigh`/`max` it may draft a long deliverable in its thinking and write it again.
- In coding and computer-use loops it may issue implied independent tool calls one per turn.
- At `low` it is often competitive on cost with Opus and Sonnet while scoring higher.

## Remove from prompts

- **Anti-formatting blocks** (long bans on markdown, bullets, bold). Remove, or replace with the formatting rule below. ("Formatting in chat")
- **Narration suppression** ("hold all findings for the final response", "keep updates brief"). Remove before adding anything. ("Ask for user-facing progress updates")
- **Requests to write reasoning in the reply** (`reasoning_extraction`).
- **"Does this compile?" phrasing**: use "Are there any bugs in this program?" ("Reduce safeguard false positives")

## Add when you see this symptom

### Chat replies need more structure than they get

> Quoted from Anthropic · "Formatting in chat"
```text
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

### Long agentic turns are silent, or the final message covers only the last step
First check the client receives progress updates (`display: "updates"`). Then, for human-in-the-loop work:

> Quoted from Anthropic · "Ask for user-facing progress updates"
```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

If the product hides tool output, the harness should send this after hidden output as a turn-scoped system message:

> Quoted from Anthropic · "Ask for user-facing progress updates"
```text
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

### Autonomous or asynchronous work stops early ("Next, I'll…", "Shall I apply this?")
Apply both blocks; if length is limited, the first alone keeps most of the effect. Keep the first sentence as written. Add a sentence after it listing any confirmations the product requires. It can make the model ask less about ambiguous requests.

> Quoted from Anthropic · "Finish the whole task"
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

> Quoted from Anthropic · "Finish the whole task"
```text
# Delivering work
The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it. Read ambiguity the way a careful colleague would: make routine judgment calls yourself, and check in only when different readings would lead to materially different work. If you see a real problem with the task as specified, say so in a sentence or two and keep building under stated assumptions; if the user hears the concern and reaffirms, that is their decision, so deliver the full request.

If a question comes up partway, first do everything that doesn't depend on the answer; then state the assumption you made, or — when going ahead on a wrong guess would be unsafe or would make the work useless — put the question at the end of a turn that also delivers that progress. If one part turns out to be blocked, complete every other part in full and say exactly what you left out and why — the whole task is the deliverable, and scaling it down is the user's call, not yours. A step you have decided on is something to run, not to announce: describing the next step and ending the turn leaves it undone until the user replies.

Keep changes to what the request needs. Something else you notice worth doing — cleanup or documentation the task didn't call for, a change to a file the task didn't require — is a suggestion to make at the end, not a change to make; actions clearly beyond what the ask implies, and risky or destructive ones, still need the user's go-ahead.
```

### Unrequested fixes, extensions, or too many committed tests

> Quoted from Anthropic · "Keep changes and tests to what the task asks for"
```text
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

### Prose is dense or mannered
Preferred in a user message; the system prompt also works. A short version also tends to work: "Please remove all mannered prose."

> Quoted from Anthropic · "Writing density"
```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

### Summaries copy source wording without quotation marks
Add one complete correct example to the system prompt: request, response, and why it is correct. The page has a full example ("Quoting retrieved sources"); adapt its tool lines to the product's tool names. Do not invent a new example without telling the user it is untested.

### At `low` effort, answers come from memory instead of search
Raising effort for those turns is often simplest. Otherwise:

> Quoted from Anthropic · "Search triggering at low effort"
```text
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

### Whole files rewritten for small changes

> Quoted from Anthropic · "Prefer targeted edits over whole-file rewrites"
```text
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

### Agent loops issue one independent tool call per turn
The harness appends this after each round of tool results as a turn-scoped system message (or as text after the tool results without the beta).

> Quoted from Anthropic · "Batch independent tool calls in agent loops"
```text
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

### Long deliverables at `xhigh`/`max` take very long or hit `max_tokens`
Prefer running such requests at `high`. If staying at `xhigh`/`max`, append this to the end of the user message and replace `[max_tokens]` with the request's real value.

> Quoted from Anthropic · "Leave room for long outputs at xhigh and max effort"
```text
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

### Client-side compaction summaries drop details
The page gives a full summarization instruction ("Tell the model what to preserve in compaction summaries"); use it for the summarizer prompt, not the main system prompt.

## API settings

- Start at `high`; test `low`, `medium`, `xhigh`, `max`. Re-run the sweep even if one was run on Fable 5.
- Keep the conversation history append-only: do not edit earlier turns, the system prompt, or the tool list mid-conversation. Use turn-scoped or mid-conversation system messages.
- Vision on dense images: give crop or image-processing tools.

## Known traps

- The anti-markdown block recommended for older models hurts here.
- Do not tell it to keep progress text brief.
