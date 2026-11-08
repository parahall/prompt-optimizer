# GPT-6 family: GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, GPT-6 Sol

Checked against the docs on 2026-11-08.
Source: [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra) (section names below refer to this page).
API IDs `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`, `gpt-6-sol`. Settings: `api-settings.md`.

OpenAI writes one set of prompting advice for the whole family. It says the advice addresses behavior observed with **GPT-6 Astra** and should be evaluated with the chosen model. Say this in the report when the target is not Astra.

Contents: Family members · How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- The model stops to ask for clarification or approval where it should continue
- The prompt implies authorization, but the model only acknowledges or plans
- The app loads skills or AGENTS.md files and the model pauses or diverges
- Replies use more lists, tables, and Markdown than the product wants
- Technical writing is too jargon-heavy, or uses stock phrases
- The harness has subagents and the model delegates too little
- Messages between agents are hard to read
- Coding: tests broader than a small change needs

## Family members

- **GPT-6 Astra**: highest intelligence; most demanding reasoning, coding, computer use, professional work. Uses fewer output tokens than earlier models on many tasks. Effort `low` to `max`; **no `none`**. Default effort not stated in the docs.
- **GPT-6.1 Sol**: near-Astra quality at lower cost. Effort `low` to `max`, default `medium`; **no `none` or `minimal`**. Tool calling only in the Responses API.
- **GPT-6.1 Terra**: fast and efficient; visual reasoning, computer use, clear natural writing. Effort `none` to `max`, default `medium`; start at `medium`.
- **GPT-6 Luna**: fastest and cheapest, for focused high-volume tasks. Effort `none` to `max`, default `medium`.
- **GPT-6 Sol**: earlier Sol, for coding and agentic workflows; review migration guidance before moving to GPT-6.1 Sol.

## How it differs from GPT-5.6

- Stays coherent better during long tasks, but **asks for clarification more often** where earlier models made assumptions, and asks non-blocking questions while working. It can stop when the user expects it to assume and continue.
- **Stronger, more literal instruction following**, including instructions inside skills and files such as `AGENTS.md`. Unclear or conflicting guidance in a skill file may cause it to pause and block work early. OpenAI strongly recommends auditing such files.
- Tends toward **detailed, formatted replies** (lists, tables, Markdown) and may reuse the same phrases across sessions.
- **Delegates to subagents less** than some workflows want.
- On coding tasks, **tests thoroughly**, sometimes more broadly than a small change needs.
- New API features: async tool calling, mid-turn steering, changing effort mid-conversation with `configuration_update`.

## Remove from prompts

- **Unsolicited warning and approval language** carried over from older prompts (hypothetical-risk disclaimers, approval steps for reversible actions). The family already asks often; such lines add more stops. Keep real confirmation rules for external, destructive, or costly actions. ("Initiative and follow-through")
- **Conflicting or unclear instructions in skills and instruction files** the app loads: resolve the conflict or state which source wins. ("Instruction following")
- **`temperature`, `top_p`, `top_logprobs`** when effort is not `none`. ("Update API and model parameters")

## Add when you see this symptom

### The model stops to ask for clarification or approval where it should continue

> Quoted from OpenAI · "Using GPT-6" · "Initiative and follow-through"
```text
You should infer the user's intent and task scope from the instructions and prior conversation context. Your job is to bias towards action and carry the user's intended task to completion.

When the user expresses intent to perform new work or fix an existing issue, persist until the user's intended goal is complete. Progress autonomously towards the user's goal (e.g. creating isolated worktrees / checkouts if needed, resolving merge conflicts, read-only actions, creating draft PRs etc.) unless they are clearly destructive or irreversible.
```

To have it ask only after preparing a concrete result (adjust to the product's level of autonomy):

> Quoted from OpenAI · "Using GPT-6" · "Initiative and follow-through"
```text
Before asking the user clarifying questions, you should complete the work that is already authorized from context and necessary to make the proposed action concrete and reviewable. The user should be approving a concrete, reviewable result. For example, before deploying a change, writing to an external application, merging a PR or publishing a site, do all the required work first so that user approval is the final step. You don't need user permission for reversible tasks, read-only actions, reviews or fixes, or anything for which authorization is provided earlier in the session or strongly implied from the task instruction.

Do not introduce unsolicited warnings, disclaimers, approval flows, or safety/compliance checklists due to hypothetical risk.
```

### The prompt implies authorization ("can you…", "help me…"), but the model only acknowledges or plans

> Quoted from OpenAI · "Using GPT-6" · "Initiative and follow-through"
```text
When the user's prompt indicates a request for action, such as "can you...", "I want to...", "help me..." and similar expressions, treat these as instructions to do the work and take action. Do not stop at acknowledging capability (e.g. "Yes…"), proposing a plan, or offering to continue. Do not settle for a partial or "helpful enough" solution that does not fully satisfy the user's task to save time, effort or tokens. If a task requires sustained work, complete all the necessary work until the intended outcome is fulfilled.
```

### The app loads skills or `AGENTS.md` files, and the model pauses or diverges

> Quoted from OpenAI · "Using GPT-6" · "Instruction following"
```text
The user's instructions take precedence over guidelines provided in a skill. If explicit user instructions conflict with a skill's instructions, prioritize the user's instructions.
```

For transparency while debugging which file caused a pause:

> Quoted from OpenAI · "Using GPT-6" · "Instruction following"
```text
If a skill causes you to ask for permission or confirmation, pause, leave requested work unfinished, or diverge from the user's intent, name and link to the exact SKILL.md file you read, quote the relevant instruction, and briefly explain how it applies. Distinguish explicit skill requirements from your interpretation of guidelines.
```

### Replies use more lists, tables, and Markdown than the product wants

> Quoted from OpenAI · "Using GPT-6" · "Personality and writing style"
```text
Default to using clear, concise paragraphs, each developing one main idea. Use lists only when the information is genuinely parallel, sequential, or easier to compare, and avoid nested lists unless the hierarchy cannot be expressed clearly in prose. Use plain, simple language: familiar words, concrete examples, and precise verbs. Prefer active voice and direct statements.

Make sure to state the main point clearly and early, then develop it with the explanation and detail the reader needs. Let each sentence build on what came before. Develop the points that matter and provide enough support to be useful.
```

### Technical writing is too jargon-heavy, or uses stock phrases

> Quoted from OpenAI · "Using GPT-6" · "Personality and writing style"
```text
Use plain language over jargon, and reference technical details only to the degree that it helps illustrate an idea or your work to the user. Communicate complex concepts in a clear and cohesive manner, and calibrate your writing to the level of background knowledge assumed from the user's prompt and context.
```

> Quoted from OpenAI · "Using GPT-6" · "Personality and writing style"
```text
Avoid using slop words or phrases like "Bottom Line:" in conclusions, "delve," "foster," "leverage," "it's worth noting," "importantly," "Question? Answer." or "This isn't about X. It's about Y.", "genuinely" or hyphenated compound descriptions and adjectives. Do not use concluding summary statements such as "In short:..", "The simplest mental model is:...".

State the intended action directly. Avoid adding what you won't do, what will remain unchanged, or how you'll separate or categorize results. Do not use contrastive framing such as "X, not Y" that introduces an unprompted alternative that the user didn't ask about. Avoid invented compound labels like "exact-head checks" and "editorial-row layouts", vague qualifiers, and canned transitions; use plain verbs and prepositions to state the actual relationship directly.
```

### The harness has subagents and the model delegates too little

> Quoted from OpenAI · "Using GPT-6" · "Subagent delegation"
```text
If at any point you can parallelize work by delegating tasks to another agent (no matter if you are the root or subagent), you should do so using collaboration tools if it could save time or improve quality.
```

### Messages between agents are hard to read

> Quoted from OpenAI · "Using GPT-6" · "Subagent delegation"
```text
Messages that you send to other agents and your final answer may be read by a human, so ensure they are legible. Always put proper spaces between words and/or numbers.
```

### Coding: tests broader than a small change needs

> Quoted from OpenAI · "Using GPT-6" · "Testing and verification"
```text
Do not write tests for reversible, low-impact changes that mirror the implementation. If you do choose to verify your work with tests, make sure that the tests are meaningful and necessary to verify implementation.

Run tests appropriate to the change and complete required checks. Once those pass, broaden or repeat testing only when new changes, failures, or unresolved concerns justify it; otherwise, continue toward completing the task.
```

## API settings

- Preserve the current effective effort when migrating; Astra and 6.1 Sol do not accept `none` (use `low`); if the old request used `minimal`, start with `low`.
- Tool calling: use the Responses API. GPT-6 Sol and Luna allow Chat Completions function calling only with effort `none`.
- When effort is not `none`: remove `temperature`, `top_p`, `top_logprobs` (and `logprobs` in Chat Completions).
- Changing effort between responses: use `configuration_update` items and keep the request-level effort fixed, to keep the prompt cache. Only in standard, single-agent requests; not together with automatic compaction or truncation (see `api-settings.md`).
- From GPT-5.5 or earlier: replace `prompt_cache_retention` with `prompt_cache_options.ttl` (`"30m"`).

## Known traps

- The prompting advice was measured on Astra; the cheaper members may need different tuning.
- Autonomy blocks make the model act more; keep explicit confirmation rules for external, destructive, or costly actions.
