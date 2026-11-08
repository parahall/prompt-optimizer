# General techniques for all current Claude models

Checked against the docs on 2026-11-08. Source: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Section names below match that page.

These are structural improvements for any Claude prompt. The model file for the target model wins where it disagrees.

Contents
1. Clarity and context
2. Examples
3. Structure and long inputs
4. Output format
5. Tools and actions
6. Thinking
7. Agents and long tasks
8. Migrating from older models

## 1. Clarity and context ("Be clear and direct", "Add context")

- Write as if briefing a brilliant new colleague who knows nothing about your norms. Test: would a colleague with no context understand it?
- State the output format and constraints explicitly. Use numbered steps when order or completeness matters.
- If you want more than the minimum ("go beyond the basics", "include as many relevant features as possible"), ask for it; current models do what is asked, not more.
- Give the reason behind each rule. The model generalizes from the reason to cases the rule did not name.
- For agents with many workstreams, state the larger goal: who the work is for and what it enables.
- A one-sentence role in the system prompt focuses tone and behavior.

## 2. Examples ("Use examples effectively")

- 3 to 5 examples are the most reliable way to steer format, tone, and structure.
- Make them relevant (close to real use), diverse (cover edge cases, avoid accidental patterns), and wrapped in `<example>` tags (several inside `<examples>`).
- With thinking on, a worked example (problem, method, answer) also shapes how the model reasons.
- Positive examples of the wanted style work better than lists of things to avoid.

## 3. Structure and long inputs ("Structure prompts with XML tags", "Long context prompting")

- When a prompt mixes instructions, context, examples, and variable input, put each in its own XML tag (`<instructions>`, `<context>`, `<input>`). Use consistent, descriptive tag names; nest when content is hierarchical.
- With long inputs (about 20,000 tokens or more), put the documents at the top and the question and instructions at the end. This improved answer quality by up to 30 percent in Anthropic's tests.
- Wrap each document in `<document index="n">` with `<source>` and `<document_content>` inside `<documents>`.
- For long-document tasks, ask the model to first pull out the relevant quotes (in `<quotes>` tags), then answer from them.
- Mark text the user pasted from elsewhere so instructions inside it are not followed; see the pasted-content block in `models/opus-5-5.md`, which applies to other models as a general guardrail.

## 4. Output format ("Control the format of responses")

- Say what to do, not what not to do ("write in flowing prose paragraphs", not "no markdown").
- XML format indicators help ("write the prose sections inside `<prose>` tags").
- The prompt's own style leaks into the output: a prompt full of markdown gets markdown back.
- Prefill (writing the start of the model's answer) no longer works on Claude 4.6 models and later. Use structured outputs for strict formats, tools with an enum for classification, and "Respond directly without preamble" to skip intros.

## 5. Tools and actions ("Tool usage", "Optimize parallel tool calling")

- Models act on the exact verb: "can you suggest changes" gets suggestions; "change this function" gets changes. Match the verbs to the wanted behavior, or set a default with a block from `snippets.md`.
- Say when to use each tool and why, in calm language. Strong wording ("CRITICAL", "MUST") causes over-use on current models.
- Parallel tool calls are steerable to near 100 percent with the block in `snippets.md`.

## 6. Thinking ("Leverage thinking")

- Effort is the main control for how much the model thinks; prompt wording is the second lever. See `api-settings.md`.
- A general instruction ("think thoroughly") usually beats a hand-written plan of reasoning steps.
- Do not ask for reasoning written into the answer on current models; see `audit-checklist.md`, item 1.
- A closing self-check against stated criteria helps coding and math, except on Opus 5.

## 7. Agents and long tasks ("Agentic systems")

- Give the full task, intent, and constraints in the first turn; drip-fed requirements cost tokens and quality.
- For work that spans several context windows: set up tests and an `init.sh` in the first window; track test status in structured files (for example `tests.json`) and progress in free-text notes; use git as the log; tell a fresh window how to re-orient ("Review progress.txt, tests.json, and the git logs").
- Tell the model never to remove or edit tests to make them pass.
- Give verification tools (browser, computer use) for long autonomous work.
- Define research success criteria and ask for checking across several sources.

## 8. Migrating from older models ("Migration considerations")

- Remove anti-laziness wording ("be thorough", "use tools aggressively", "if in doubt, use X"); current models over-trigger on it.
- Move thinking control from `budget_tokens` to adaptive thinking plus effort.
- Remove prefill.
- On the newest models, keep conversation history append-only: change instructions with a mid-conversation system message, not by rewriting the system prompt.
- Ask explicitly for features you want (animations, interactivity); do not rely on the model to infer them.
