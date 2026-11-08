# General techniques for OpenAI GPT models

Checked against the docs on 2026-11-08. Sources: [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering), [Prompting](https://developers.openai.com/api/docs/guides/prompting), [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning), [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices), and the model pages linked from `models/`.

These are structural improvements for any GPT prompt. The model file for the target family wins where it disagrees.

Contents
1. Roles and priority
2. Structure
3. Outcome, success criteria, and stop rules
4. Examples
5. Tools
6. Grounding and long inputs
7. Agents and long tasks
8. Changing a working prompt

## 1. Roles and priority ("Message roles and instruction following")

- `developer` messages (or the `instructions` parameter) outrank `user` messages. Put rules, business logic, and tone there; put the task and its inputs in the user message. Reasoning models use `developer`, not `system`.
- The `instructions` parameter applies only to the current request; with `previous_response_id`, send it again each call.
- Make priority explicit when sources can conflict: user instructions vs. defaults, skills, or earlier instructions (blocks in `models/gpt-5-4.md` and `models/gpt-6.md`).

## 2. Structure ("Message formatting with Markdown and XML", "Suggested prompt structure")

- Use Markdown headers and lists to show sections; use XML tags to mark where a piece of content (a document, an example, user data) starts and ends. XML attributes can carry metadata (`<doc id="2">`).
- Classic order: Identity → Instructions → Examples → Context (context near the end, because it changes per request).
- For GPT-5.5 and later, OpenAI suggests: Role, Personality, Goal, Success criteria, Constraints, Tools, Output, Stop rules. Keep each section short; add detail only where it changes behavior.
- Personality (tone) and collaboration style (when to ask, assume, take initiative, check work) are separate and both short; neither replaces goals or stop rules.

## 3. Outcome, success criteria, and stop rules

- Describe the destination, not every step: what good looks like, which constraints matter, what evidence is available, what the final answer must contain.
- Add a completion bar ("Success means: …") and stop rules (when to retry, fall back, abstain, ask, or stop).
- Use decision rules for judgment calls; keep absolute words for true invariants.
- Preserve explicit user values; where the right value is implicit, give decision criteria instead of universal defaults or keyword maps.

## 4. Examples ("Few-shot learning")

- Show a diverse range of inputs with the desired outputs, marked with XML tags or a compact block.
- Examples must agree with the rules; a mismatch produces poor results. Any behavior shown in an example should also be stated as a rule.
- For reasoning models, try zero examples first and add them only if needed. For GPT-5.4 Mini, include one correct example of the full flow.

## 5. Tools

- Pass tools in the `tools` field, not as text in the prompt. Name each tool clearly; the `description` says what it does, when to use it, inputs, side effects, and errors.
- System-prompt tool rules only for cross-tool policy: prerequisites before actions, parallel independent reads, which tool wins in which case.
- For risky tools (payments, deletes, external writes) set a lower threshold for asking the user than for read-only tools.
- Prefer OpenAI's hosted tools where they fit (web search, file search, code interpreter, computer use, `apply_patch`, shell).

## 6. Grounding and long inputs

- For grounded answers, say what needs a citation, what counts as enough evidence, and what to do when evidence is missing; cite only retrieved sources; label inference separately from supported facts.
- Give a retrieval budget (when to search again and when to stop).
- GPT-4.1 guidance for long context: instructions at both the start and end of the context work best; if only once, put them above.

## 7. Agents and long tasks

- Define what each request authorizes: answer/review/plan vs. change/build/fix vs. actions that need confirmation (external writes, destructive actions, purchases, scope expansion). Keep the policy in one place.
- Ask for a short visible preamble before the first tool call and sparse updates at phase changes, not narration of every call.
- Define the current layer of work (research, design, implementation, review) for long work.
- Ask for real validation before finishing (tests, type checks, build, render checks) and an explanation when validation cannot run.
- Work plans for long tasks (staged plans, a plan tool, the current phase) help at any effort. Asking the model to reason out loud before answering is unnecessary at effort `low` or higher; at effort `none`, outlining steps first is documented to help on GPT-5.1, 5.2, and 5.4.

## 8. Changing a working prompt ("Prompt migration workflow")

- OpenAI's migration order: switch the model and keep the current effort; run representative evals; remove obsolete scaffolding, repeated instructions, and irrelevant tools; add only the smallest targeted instruction that fixes a measured regression; re-run evals after each change.
- Do not rewrite a working prompt stack all at once; you cannot tell what caused a change.
- When fixing a regression: find the instruction or contradiction that likely caused it, make a surgical edit, and re-run the same cases.
