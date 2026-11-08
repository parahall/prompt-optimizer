# GPT-5.6 family: GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna

Checked against the docs on 2026-11-08.
Sources: [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) (P56), [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.6) (U56), [Upgrading to GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p6-sol) (UP56). The prompting page covers "GPT-5.6 Sol or the GPT-5.6 family".
API IDs `gpt-5.6-sol` (alias `gpt-5.6`), `gpt-5.6-terra`, `gpt-5.6-luna`. Default effort `medium`. Settings: `api-settings.md`.

Contents: Family members · How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- The prompt scripts every step instead of stating the goal
- Agentic loops search or call tools too long, or stop too early
- Replies are too short after migrating, or length varies
- Tone labels ("friendly", "empathetic") give inconsistent results
- Edits and rewrites add claims, sections, or a promotional tone
- The agent asks for approval too often, or acts beyond what was asked
- The agent skips a lookup it needed before acting
- Grounded answers search too much or cite poorly
- Long tool-heavy tasks: silent, or narrating every call
- Coding or visual work finished without validation
- Programmatic Tool Calling is enabled without clear routing

## Family members

- **Sol**: flagship; replaces unsuffixed GPT-5, GPT-5.5, and GPT-5.4 flagship roles.
- **Terra**: balance of intelligence and cost; replaces mini-like roles.
- **Luna**: efficient, high-volume; replaces nano-like roles (classification, extraction, routing, strict latency). Its context size is reported differently on two pages (1.05M on the catalog page, 400K in the upgrade guide).

The upgrade guide warns against moving every old model to Sol: map each workload by its role.

## How it differs from GPT-5.5

- **Token-efficient**: reaches flagship quality with fewer output tokens. Leaner prompts did better: in OpenAI's coding-agent tests, configurations with leaner system prompts scored roughly 10–15% higher with 41–66% fewer total tokens.
- **More concise by default**; broad brevity instructions can make replies too short.
- **Better at inferring intent** and the intended amount of work, so prompts need not prescribe every step. Still give domain context, hard constraints, approval boundaries, success criteria, and when an ambiguity should trigger a question.
- **Follows prompt contracts closely**, so conflicting rules cause more instability than missing detail.
- **Proactive and persistent** on multi-step tasks.
- Stronger frontend layout and design judgment.
- New: Programmatic Tool Calling, multi-agent (beta), explicit prompt caching, persisted reasoning, `max` effort, pro mode.
- Real-time cyber and biology safety classifiers can block or pause some outputs.

## Remove from prompts (P56 "Simplify prompts first"; UP56 "Prompt migration judgment")

Remove one group at a time, and keep what encodes a product requirement:
- **Repeated statements of the same rule**, and repeated style or process instructions that do not change behavior.
- **Examples that do not change behavior.**
- **Process instructions for behavior the model already does reliably**, and step-by-step scripts where only the outcome matters.
- **Tools and tool descriptions unrelated to the task.**
- **Generic "be brief", "be thorough", or "think step by step" instructions.**
- **Blanket language rules** such as "always respond in the user's language", unless that is the real requirement; they can cause unwanted language switching.
- **Repeated "ask first" / "wait for approval" / "do not mutate" lines**; they block safe, expected work.
- **"Minimize tool loops" without a correctness floor.**
- **Unnecessary absolute words** (ALWAYS, NEVER, must, only) for judgment calls; keep them for true invariants.
- **Universal defaults, keyword maps, and broad semantic shortcuts** where the right value is implicit; give decision criteria instead.

Keep: the user-visible outcome; success criteria and stop rules; safety, business, evidence, and permission constraints; context-dependent tool-routing rules; required output shape and validation.

## Add when you see this symptom

### The prompt scripts every step instead of stating the goal
Rewrite as outcome plus success criteria. Example from P56 ("Outcome-first prompts and stopping conditions"):

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Outcome-first prompts and stopping conditions"
```text
Resolve the customer's issue end to end.

Success means:
- make the eligibility decision from available policy and account evidence
- complete any allowed action before responding
- return completed_actions, customer_message, and blockers
- if required evidence is missing, ask for the smallest missing field
```

### Agentic loops search or call tools too long, or stop too early

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Outcome-first prompts and stopping conditions"
```text
Resolve the request in the fewest useful tool loops, but do not let loop
minimization outrank correctness, required evidence, calculations, or
required citations.

After each result, ask whether the core request can now be answered with
useful evidence. If yes, answer. If required evidence is still missing,
name the missing fact and use the smallest useful fallback.
```

### Replies are too short after migrating, or length varies
First check whether "Be concise" / "Keep it short" lines are still needed; remove them if replies are too short. Set the default with `text.verbosity`. When a task needs short answers, say what must stay:

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Personality, collaboration, and response length"
```text
Lead with the conclusion. Include the evidence needed to support it, any material
caveat, and the next action. Omit secondary detail and repetition.

Keep all required facts, decisions, caveats, and next steps. Trim introductions,
repetition, generic reassurance, and optional background first.
```

### Tone labels ("friendly", "empathetic") give inconsistent results
Describe the writing choices instead. Keep personality and collaboration style short.

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Personality, collaboration, and response length"
```text
State the answer directly. If the user reports a problem, acknowledge the
specific issue before giving the next step. Use reassurance only when it is
relevant. Omit generic praise and unnecessary sign-offs.
```

### Edits, rewrites, summaries, or drafts add claims, sections, or a promotional tone

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Personality, collaboration, and response length"
```text
Preserve the requested artifact, length, structure, genre, and factual claims
first. Improve clarity, flow, and correctness without adding new claims,
sections, or a more promotional tone unless requested.
```

### The agent asks for approval too often, or acts beyond what was asked
State each rule once, in one place; name the safe local actions.

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Define autonomy and approval boundaries"
```text
For requests to answer, explain, review, diagnose, or plan, inspect the
relevant materials and report the result. Do not implement changes unless
the request also asks for them.

For requests to change, build, or fix, make the requested in-scope local
changes and run relevant non-destructive validation without asking first.

Require confirmation for external writes, destructive actions, purchases,
or a material expansion of scope.
```

For long work, also name the current layer (research, design, implementation, review, external coordination) so the model does not silently move to another.

### The agent skips a lookup it needed before acting

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Tool routing"
```text
Before taking an action, resolve required discovery, retrieval, and
validation steps. Do not skip a prerequisite because the intended final
state seems obvious.
```

### Grounded answers search too much or cite poorly
Define what needs support, what is enough evidence, and what to do when evidence is missing ("absence of evidence should not automatically become a factual 'no'").

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Grounding, citations, and retrieval budgets"
```text
For ordinary Q&A, start with one broad search using short, discriminative
keywords. If the top results contain enough support for the core request,
answer from those results.

Make another retrieval call only when a required fact, owner, date, ID, or
source is missing; the user asked for exhaustive coverage or comparison; a
specific artifact must be read; or an important claim would otherwise be
unsupported.

Do not search again only to improve phrasing, add examples, or support
nonessential detail.
```

### Long tool-heavy tasks: silent, or narrating every call

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Long-running workflows and state"
```text
Before tool calls for a multi-step task, send a one- or two-sentence
user-visible update that states the first step. During the task, update only
when a major phase begins or a finding changes the plan. Each update should
state one concrete outcome and the next step.
```

### Coding or visual work finished without validation

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Check work before finishing"
```text
After making changes, run the most relevant validation available:
- targeted tests for changed behavior
- type checks or lint checks when applicable
- build checks for affected packages
- a minimal smoke test when full validation is too expensive

If validation cannot be run, explain why and describe the next best check.
```

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Check work before finishing"
```text
Render the artifact before finalizing. Inspect layout, clipping, spacing,
missing content, and visual consistency. Revise until the rendered output
matches the requirements.
```

For coding migrations, also:

> Quoted from OpenAI · "Upgrading to GPT-5.6 Sol" · "Prompt migration judgment"
```text
Preserve existing functionality, routes, outputs, and user-visible behavior.
Do not delete or disable required behavior merely to make the build pass.
Before finishing, run the relevant build, tests, type checks, render or smoke
checks, and report the evidence.
```

### Programmatic Tool Calling is enabled without clear routing
Generic lines like "use Programmatic Tool Calling efficiently" do not work. State the bounded stage, eligible tools, output schema, retry limit, stop condition, and handoff:

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Programmatic Tool Calling"
```text
Use Programmatic Tool Calling only for the bounded record-reduction stage.
Call only the documented read-only tools. Filter and deduplicate the
intermediate results, then emit exactly the required compact schema with
evidence fields. Retry transient failures at most twice. Use direct tool
calls for approval, semantic judgment, citations, and final validation.
```

## Suggested structure for complex prompts

Keep each section short; add detail only where it changes behavior.

> Quoted from OpenAI · "Prompting guidance for GPT-5.6 Sol" · "Suggested prompt structure"
```text
Role: [the model's function and context]

Personality: [tone and collaboration style]

Goal: [user-visible outcome]

Success criteria: [what must be true before the final answer]

Constraints: [policy, safety, business, evidence, and side-effect limits]

Tools: [which tools to use, when, and what not to use]

Output: [sections, length, format, and tone]

Stop rules: [when to retry, fallback, abstain, ask, or stop]
```

## API settings

- Default effort `medium`. Migrating from GPT-5.5 or 5.4: keep the old effective effort, then test one level lower. GPT-5.4, Mini, and Nano defaulted to `none`; omitting effort on 5.6 silently raises it to `medium`.
- `low` for latency-sensitive work; `high`/`xhigh` only with measured gains; `max` only for the hardest quality-first work, never globally.
- Set default length with `text.verbosity`; task-specific length goes in the prompt.
- Pro mode: `reasoning.mode: "pro"` on the same model (no separate Pro model); do not ask for "think harder" in the prompt.
- Persisted reasoning defaults to `all_turns`; use `current_turn` when earlier reasoning is stale.
- Chat Completions with function tools only at effort `none`; use the Responses API for reasoning with tools.
- Image and PDF inputs: omitted or `auto` detail can keep original size and raise token use; set detail explicitly when cost matters.

## Known traps

- Rewriting a working prompt stack all at once makes it impossible to tell what caused a change; OpenAI recommends one change at a time, each tied to a measured failure.
- Do not add Pro mode, persisted reasoning, explicit caching, Programmatic Tool Calling, or multi-agent as part of a plain migration.
