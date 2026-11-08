# GPT-5.5

Checked against the docs on 2026-11-08.
Sources: [Using GPT-5.5](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5) (section names below refer to this page) and [Upgrading to GPT-5.5](https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p5).
API ID `gpt-5.5`. Default effort `medium`. Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- Customer-facing replies feel curt or lack warmth
- Streaming apps feel slow before the first visible text
- The prompt scripts every step instead of stating the goal
- Tool loops run too long, or evidence rules are unclear
- Replies are over-formatted, or length and audience are unspecified
- Edits and rewrites expand instead of polishing
- Grounded answers search too much
- Drafts invent facts to sound stronger
- Coding or visual work finished without validation

## How it differs from GPT-5.4

- Strong results with **fewer reasoning tokens** at the same effort.
- **Strongest with outcome-first prompts**; step-by-step process guidance adds noise, narrows the model's search, or makes answers mechanical. Legacy prompt stacks often over-specify process.
- **Literal and thorough** instruction following.
- **More concise and direct** by default; conversational products may need explicit personality, warmth, and formatting guidance. On GPT-5.5, `text.verbosity: "low"` is proportionally shorter than on GPT-5.4.
- More precise tool selection and arguments.
- **Knows the current UTC date.**
- Higher effort is not automatically better: with conflicting instructions, weak stop rules, or open-ended tool access it can over-think and over-search.
- OpenAI calls it a new model family to tune for, not a drop-in replacement for 5.2 or 5.4.

## Remove from prompts ("Migration quickstart › Prompting", "Prompting best practices")

- **Detailed step-by-step process guidance**, unless the product needs that exact path. Example of the style to avoid:

> Quoted from OpenAI · "Using GPT-5.5" · "Outcome-first prompts and stopping conditions"
```text
First inspect A, then inspect B, then compare every field, then think through
all possible exceptions, then decide which tool to call, then call the tool,
then explain the entire process to the user.
```

- **Output schema definitions in the prompt**, "where possible": use Structured Outputs instead. Delete the prose schema only when the app sends an equivalent schema in the request; otherwise keep it and recommend the change (see `audit-checklist.md`, item 9).
- **The current date**: the model already knows the UTC date. Keep a date only for a business timezone, policy-effective date, user-local date, or other non-UTC reference.
- **Unnecessary absolute rules** (ALWAYS, NEVER, must, only) for judgment calls; keep them for true invariants and use decision rules otherwise.
- **Tool-specific guidance in the system prompt** that belongs in the tool's own description (what it does, when to use it, inputs, side effects, retry safety, errors).

## Add when you see this symptom

### Customer-facing replies feel curt or lack warmth
Define a short personality and collaboration style. Example for a steady, task-focused assistant (the page also has an "expressive collaborative" variant):

> Quoted from OpenAI · "Using GPT-5.5" · "Personality and behavior"
```text
# Personality
You are a capable collaborator: approachable, steady, and direct. Assume the user is competent and acting in good faith, and respond with patience, respect, and practical helpfulness.

Prefer making progress over stopping for clarification when the request is already clear enough to attempt. Use context and reasonable assumptions to move forward. Ask for clarification only when the missing information would materially change the answer or create meaningful risk, and keep any question narrow.

Stay concise without becoming curt. Give enough context for the user to understand and trust the answer, then stop. Use examples, comparisons, or simple analogies when they make the point easier to grasp. When correcting the user or disagreeing, be candid but constructive. When an error is pointed out, acknowledge it plainly and focus on fixing it.

Match the user's tone within professional bounds. Avoid emojis and profanity by default, unless the user explicitly asks for that style or has clearly established it as appropriate for the conversation.
```

### Streaming apps feel slow before the first visible text

> Quoted from OpenAI · "Using GPT-5.5" · "Improve time to first visible token with a preamble"
```text
Before any tool calls for a multi-step task, send a short user-visible update that acknowledges the request and states the first step. Keep it to one or two sentences.
```

### The prompt scripts every step instead of stating the goal
Example of the pattern; adapt the task and the output fields to the user's prompt, do not copy them:

> Quoted from OpenAI · "Using GPT-5.5" · "Outcome-first prompts and stopping conditions"
```text
Resolve the customer's issue end to end.

Success means:
- the eligibility decision is made from the available policy and account data
- any allowed action is completed before responding
- the final answer includes completed_actions, customer_message, and blockers
- if evidence is missing, ask for the smallest missing field
```

### Tool loops run too long, or evidence rules are unclear

> Quoted from OpenAI · "Using GPT-5.5" · "Outcome-first prompts and stopping conditions"
```text
Resolve the user query in the fewest useful tool loops, but do not let loop minimization outrank correctness, accessible fallback evidence, calculations, or required citation tags for factual claims.

After each result, ask: "Can I answer the user's core request now with useful evidence and citations for the factual claims?" If yes, answer.
```

> Quoted from OpenAI · "Using GPT-5.5" · "Outcome-first prompts and stopping conditions"
```text
Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop.
```

### Replies are over-formatted, or length and audience are unspecified
Set `text.verbosity` (`low` for concise), then:

> Quoted from OpenAI · "Using GPT-5.5" · "Formatting"
```text
Let formatting serve comprehension. Use plain paragraphs as the default format for normal conversation, explanations, reports, documentation, and technical writeups. Keep the presentation clean and readable without making the structure feel heavier than the content.

Use headers, bold text, bullets, and numbered lists sparingly. Reach for them when the user requests them, when the answer needs clear comparison or ranking, or when the information would be harder to scan as prose. Otherwise, favor short paragraphs and natural transitions.

Respect formatting preferences from the user. If they ask for a terse answer, minimal formatting, no bullets, no headers, or a specific structure, follow that preference unless there is a strong reason not to.
```

Audience and length example (adapt the numbers):

> Quoted from OpenAI · "Using GPT-5.5" · "Formatting"
```text
Write for a senior business audience. Keep the answer under 400 words. Use short paragraphs and only include bullets when they improve scannability. Prioritize the conclusion first, then the reasoning, then caveats.
```

### Edits and rewrites expand instead of polishing

> Quoted from OpenAI · "Using GPT-5.5" · "Formatting"
```text
Preserve the requested artifact, length, structure, and genre first. Quietly improve clarity, flow, and correctness. Do not add new claims, extra sections, or a more promotional tone unless explicitly requested.
```

### Grounded answers search too much

> Quoted from OpenAI · "Using GPT-5.5" · "Add an explicit retrieval budget"
```text
For ordinary Q&A, start with one broad search using short, discriminative keywords. If the top results contain enough citable support for the core request, answer from those results instead of searching again.

Make another retrieval call only when:
- The top results do not answer the core question.
- A required fact, parameter, owner, date, ID, or source is missing.
- The user asked for exhaustive coverage, a comparison, or a comprehensive list.
- A specific document, URL, email, meeting, record, or code artifact must be read.
- The answer would otherwise contain an important unsupported factual claim.

Do not search again to improve phrasing, add examples, cite nonessential details, or support wording that can safely be made more generic.
```

### Drafts (slides, launch copy, summaries) invent facts to sound stronger

> Quoted from OpenAI · "Using GPT-5.5" · "Creative drafting guardrails"
```text
For creative or generative requests such as slides, leadership blurbs, outbound copy, summaries for sharing, talk tracks, or narrative framing, distinguish source-backed facts from creative wording.

- Use retrieved or provided facts for concrete product, customer, metric, roadmap, date, capability, and competitive claims, and cite those claims.
- Do not invent specific names, first-party data claims, metrics, roadmap status, customer outcomes, or product capabilities to make the draft sound stronger.
- If there is little or no citable support, write a useful generic draft with placeholders or clearly labeled assumptions rather than unsupported specifics.
```

### Coding or visual work finished without validation

> Quoted from OpenAI · "Using GPT-5.5" · "Prompt the model to check its work"
```text
After making changes, run the most relevant validation available:
- targeted unit tests for changed behavior
- type checks or lint checks when applicable
- build checks for affected packages
- a minimal smoke test when full validation is too expensive

If validation cannot be run, explain why and describe the next best check.
```

## Suggested structure for complex prompts

> Quoted from OpenAI · "Using GPT-5.5" · "Suggested prompt structure"
```text
Role: [1-2 sentences defining the model's function, context, and job]

# Personality
[tone, demeanor, and collaboration style]

# Goal
[user-visible outcome]

# Success criteria
[what must be true before the final answer]

# Constraints
[policy, safety, business, evidence, and side-effect limits]

# Output
[sections, length, and tone]

# Stop rules
[when to retry, fallback, abstain, ask, or stop]
```

## API settings

- Default `medium`; many workloads do well at `low`. For latency-sensitive work with tools or planning, test `low` before `none`; `none` only for voice turns, fast retrieval, classification. `high`/`xhigh` only with measured gains.
- Use the Responses API for reasoning, tools, and multi-turn; preserve `phase` when replaying history.
- `text.verbosity`: default `medium`; `low` is often the better start for concise answers.
- Use a stable `prompt_cache_key`; static content first, dynamic content last.
- Image inputs: unset or `auto` detail now behaves as `original` (more tokens).

## Known traps

- Migrating from 5.4 with short, task-bounded prompts: change the model name only. Otherwise make light, workflow-specific prompt changes, one at a time, after a fresh baseline.
- Whether `temperature` is accepted at effort `none` is not stated for GPT-5.5 (it is for 5.4 and 5.2).
