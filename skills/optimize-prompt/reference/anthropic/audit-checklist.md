# Audit checklist for Claude prompts

Checked against the docs on 2026-11-08. Main source: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and the per-model pages linked from each item.

Go through every item. For each pattern found in the prompt, apply the verdict for the target model. "Current models" means every model with a file in `models/`. Model files can add model-only items; this file holds the patterns that appear across models.

Contents
1. Requests for written-out reasoning
2. Verification and double-check instructions
3. Thinking instructions ("think carefully", "think less")
4. Shouting and blanket tool rules
5. Anti-formatting blocks
6. Rules that suppress or force progress updates
7. Length and verbosity
8. Severity filters in review prompts
9. Rules that discourage or force tool use and search
10. Negative-only instructions and missing reasons
11. Scope that relies on the model to generalize
12. Scope creep and over-engineering
13. Subagent rules
14. Generic design instructions
15. Prefill and other removed features
16. Phrasings that trigger safety false positives
17. Medicine dosing questions

---

## 1. Requests for written-out reasoning

**Spot it:** a `<thinking>`, `<reasoning>`, `<scratchpad>` section to fill before answering; "think step by step and write it down"; a `reasoning`, `thinking`, `rationale` or `trace` field in requested JSON or in a tool input schema; "show your full reasoning"; "explain your thinking verbatim"; a running log of private notes. Check tool descriptions and skill text too, not only the main prompt.

**Verdict:**
- Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Sonnet 5.5: **remove.** These models can decline such requests with the `reasoning_extraction` refusal category, which is billed and is not retried by server-side fallback.
- Haiku 5.5: **remove.** Thinking is on by default, so the reasoning already happens in thinking blocks; written-out reasoning in replies is a known problem on this model.
- Opus 4.8, Sonnet 5 and legacy models **with thinking off**: manual chain of thought (reason first, then the answer in `<answer>` tags) is the documented fallback and may stay. With thinking on, prefer removing it.

**Instead:** ask for "a short explanation of the answer", "the evidence behind the result", or "a summary of the actions taken", placed after the answer in a tag that does not suggest reasoning, such as `<explanation>`. Do not keep a `<thinking>` or `<reasoning>` tag in the output format, even for a short explanation. If the application needs to see the reasoning, recommend the API setting `thinking.display: "summarized"` and reading the thinking blocks.

Sources: [Refusals: keep reasoning in thinking blocks](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks); best practices, "Leverage thinking"; each model page's refusal section.

## 2. Verification and double-check instructions

**Spot it:** "double-check your answer", "re-verify before responding", "include a final verification step", "use a subagent to verify your work", harness steps that add a separate check.

**Verdict:**
- Opus 5, and Opus 5.5 (inherited from Opus 5): **remove, do not rewrite.** It verifies on its own; these lines cause over-verification and cost tokens with no quality gain. Same for "double-check" style self-correction requests.
- Sonnet 5.5 and Haiku 5.5 **coding agents**: at low effort (Haiku also at medium) they sometimes report a change as done without running a check. If the prompt is for a coding agent, a specific verification paragraph helps; see `snippets.md`, "Run a real check before reporting code done". Vague "double-check" lines do not do this job.
- Sonnet 5.5 at `xhigh`/`max`: it starts its own review rounds; if that is unwanted, use the "stop when checks pass" block in `models/sonnet-5-5.md`.
- Other current models: a short self-check against stated criteria ("Before you finish, verify your answer against [criteria]") is recommended for coding and math.

Sources: [Opus 5: task scope and over-verification](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#task-scope-and-over-verification); best practices, "Ask Claude to self-check".

## 3. Thinking instructions

**Spot it, kind A, "think more":** "think carefully before answering", "think thoroughly", "take your time and reason".
- Opus 5.5 **chat** prompts: **remove.** Effort is the control; removing the line made replies start sooner with no clear quality loss.
- Sonnet 5.5 asked for a JSON answer that needs several steps of working out: **add** "Think the problem through before you answer." (with adaptive thinking).
- Opus 4.8 and Sonnet 5 at `low` effort on multistep problems: a targeted line is fine ("This task involves multistep reasoning. Think carefully through the problem before responding."), but recommend raising effort first.
- General: "think thoroughly" beats a hand-written step-by-step plan for how to reason.

**Spot it, kind B, "think less":** "keep your thinking short", "don't deliberate", "answer directly".
- Fable 5.2, Sonnet 5.5 and Haiku 5.5: **remove and recommend a lower effort level.** Prompt wording does not reliably reduce thinking on these models (on Fable 5.2, "answer directly without deliberating" did not stop thinking at `medium` and above).
- Opus 5.5: lower effort first; "Answer directly without deliberating." may be added at `low` effort if time to first token still matters, and quality must be measured.
- Opus 4.8, Sonnet 5, Fable 5 and 5.1: the steering line "Thinking adds latency and should only be used when it will meaningfully improve answer quality..." works; lowering effort is still the first lever.

**Spot it, kind C, "do not think" rules in an integration that runs with thinking off** (Opus 5 with `disabled`, Sonnet 5.5 with `between_tools`): **remove.** They increase leaking of internal XML tags into visible output.

Sources: [Steering thinking](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost); [Opus 5.5: thinking instructions in chat](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5#thinking-instructions-in-chat-system-prompts); [Sonnet 5.5: reasoning tasks with JSON](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5#reasoning-tasks-with-json-output); [Haiku 5.5: effort](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5#use-effort-to-control-thinking); [Fable 5.2: calibrate effort](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2#calibrate-effort).

## 4. Shouting and blanket tool rules

**Spot it:** "CRITICAL", "IMPORTANT", "You MUST", "ALWAYS", "NEVER" in capitals; "for EVERY message"; "If in doubt, use [tool]"; "Default to using [tool]".

**Verdict, all current models: soften the wording, keep the condition.** Newer models follow the system prompt closely, and wording written to fix under-use now causes over-use. Change only the tone, the way Anthropic's example turns "CRITICAL: You MUST use this tool when..." into "Use this tool when...": keep the author's own condition exactly, and add the reason. If the condition itself looks too broad (for example "for every message"), keep it in the prompt and suggest a narrower condition in the report's open questions; narrowing it is the user's decision. Keep real hard limits (safety, irreversible actions), stated calmly with the reason.

Source: best practices, "Tool usage" and "Overthinking and excessive thoroughness".

## 5. Anti-formatting blocks

**Spot it:** a long block banning markdown, bullets, bold, headers, or lists.

**Verdict:**
- Fable 5.1: **replace the whole block** with the "Formatting in chat" block in `models/fable-5-1.md`, word for word. Do not soften the old ban in your own words; a softened ban still suppresses lists and headers. It already formats less than earlier models, and the block suppresses structure the content needs. If the product truly cannot render markdown, keep one sentence saying so as the reason (for example "The chat window shows raw text"), in addition to the block.
- Other current models: keep if the product needs prose, but prefer saying what to do ("write in flowing prose paragraphs") and why ("the reply is shown in a widget that cannot render markdown").

Source: best practices, "Control the format of responses"; [Fable 5.1: formatting in chat](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#formatting-in-chat).

## 6. Rules that suppress or force progress updates

**Spot it, suppressing:** "hold all findings for the final response", "do not narrate", "keep updates to a minimum".
- Fable 5.1, Sonnet 5.5: **remove.** These models already write few user-facing updates; add a positive update instruction only if the product shows the model's work live.
- Fable 5.2 also writes little during long tool runs. Where users watch live, use the update text in `models/fable-5-2.md` ("Long agentic turns look silent"); its page does not discuss suppression rules, so flag any such rule in the report instead of silently keeping it.

**Spot it, forcing:** "after every 3 tool calls, summarize progress".
- Opus 4.8, Sonnet 5: **remove.** They give regular updates without it. Describe the wanted shape of updates instead, with an example, if needed.
- Opus 5: describe cadence and shape instead (it narrates a lot); see `models/opus-5.md`.

## 7. Length and verbosity

- Opus 5: replies run long by default and lowering effort does not shorten them. If the output is user-facing and no length guidance exists, **add** the conciseness block from `models/opus-5.md`. Files it writes are also long; add the document-length line if the product has written deliverables.
- Opus 5.5: uses fewer tokens than Opus 5; add the inherited conciseness block from `models/opus-5-5.md` only when replies are reported or clearly likely to be too long.
- Opus 4.8, Sonnet 5: length follows task complexity; add a conciseness line only if the product needs a fixed style. Positive examples of the right length work better than "do not" lists.
- Fable 5 and Fable 5.1: brevity and readability are steered by one short instruction; long lists of banned habits are unnecessary.

## 8. Severity filters in review prompts

**Spot it:** "only report high-severity issues", "be conservative", "don't nitpick", "only important bugs".

**Verdict:** Opus 4.8, Sonnet 5, Opus 5 (and Opus 5.5 and Sonnet 5.5, which inherit this) follow these literally and report fewer real bugs (lower recall). **Replace** with the coverage block in `snippets.md` ("Report every issue you find..."), or, for a single pass, a concrete threshold ("report any bug that could cause incorrect behavior, a test failure, or a misleading result; omit only pure style or naming nits"). Apply the same reasoning on other current models; the risk is documented for those three.

Sources: [Opus 4.8: code review harnesses](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8#code-review-harnesses); [Opus 5: capability improvements](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#capability-improvements).

## 9. Rules that discourage or force tool use and search

- "Only use tools when strictly necessary", "minimize tool calls": **remove** for Sonnet 5.5 in chat and knowledge work (it then answers from memory where a search would catch changed facts).
- "Search for any present-day factual question regardless of confidence": **remove** for Haiku 5.5 (it then searches on half of prompts that need no search, with no accuracy gain); use the targeted search nudge in `models/haiku-5-5.md`.
- A search tool with no current date in the prompt: **add the date** for Haiku 5.5; useful for every model with search.
- Fable 5.1 at `low` effort searches less; add the name-verification nudge in `models/fable-5-1.md` if the product depends on fresh facts.
- "Can you suggest changes" wording in an agent that should act: models take it literally and only suggest. Use direct verbs ("Change...", "Make these edits..."), or add the "default to action" block from `snippets.md`.

## 10. Negative-only instructions and missing reasons

- "Do not use X" with no alternative: rewrite as what to do instead.
- A rule with no reason: add the reason in one clause. Claude generalizes from the reason ("Your reply will be read aloud by a text-to-speech engine, so never use ellipses").
- These apply to every model and are part of every rewrite.

## 11. Scope that relies on the model to generalize

Opus 4.8 and Sonnet 5 (and Sonnet 5.5, which inherits this) follow instructions literally, especially at low effort, and do not stretch a rule from one item to others. If a rule should apply broadly, say so ("Apply this formatting to every section, not just the first one").

## 12. Scope creep and over-engineering

Symptom-driven: add a scope block only for coding or task agents where unrequested extras would hurt.
- Opus 5: scope block in `models/opus-5.md`. Opus 5.5: the same block, inherited, in `models/opus-5-5.md`.
- Fable 5: "don't add features, refactor..." block in `models/fable-5.md`.
- Fable 5.1: "keep changes and tests to what the task asks for" block in `models/fable-5-1.md`.
- Fable 5.2: the opposite lever exists. Its ownership sentence (`models/fable-5-2.md`) makes it restructure and fix nearby code; leave that sentence out where the user wants minimal changes, because a scope rule does not cancel it.
- Sonnet 5.5, Haiku 5.5: the "when the work is done and checked, stop and report" paragraph in their files.
- Legacy Opus 4.5/4.6: over-engineering block in `snippets.md`.

## 13. Subagent rules

- Opus 5 delegates readily. "Use subagents for everything" multiplies cost; add the damping block from `models/opus-5.md` for cost-sensitive harnesses (for Opus 5.5, the inherited copy in `models/opus-5-5.md`).
- Fable 5 also dispatches subagents readily, but its docs recommend using them, with guidance on when ("Parallel subagents" in `models/fable-5.md`), and recommend fresh-context verifier subagents for long runs. Do not copy Opus 5's block into a Fable 5 prompt: its "do not use subagents to verify" line contradicts Fable 5's guidance.
- Fable 5.2: delegation depends on the harness. Review existing "delegate" lines first; change the subagent tool description only if it still over-delegates (see `models/fable-5-2.md`). At `xhigh`/`max` it may start subagents to review its own work.
- Opus 4.8 spawns fewer subagents by default; add explicit "when to spawn" guidance only if more delegation is wanted.
- Never tell a model to use subagents to verify its own work on Opus 5.

## 14. Generic design instructions

"Avoid a generic AI look", "make it clean and minimal", "don't use that color" swap one default style for another on Opus 5.5, Opus 4.8 and Sonnet 5. **Replace** with a concrete spec (palette, type, layout, radius), with a list of named patterns to avoid, or with "propose 4 distinct visual directions and let the user pick". See the model files.

## 15. Prefill and other removed features

- A prompt that depends on a prefilled assistant reply (the app writes the start of Claude's answer) fails with a 400 error on Claude 4.6 models and later. Replace with: structured outputs for formats; "Respond directly without preamble" for skipping intros; continuation text moved into the user message.
- Settings that now fail are listed in `api-settings.md` ("Settings that now return errors").

## 16. Phrasings that trigger safety false positives

Fable 5.1: "Does this program compile without errors?" triggers more false refusals than "Are there any bugs in this program?". For a little-known programming language, add a short description of the language. Tools that return base64 data into context also raise false positives.

Source: [Fable 5.1: reduce safeguard false positives](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#reduce-safeguard-false-positives).

## 17. Medicine dosing questions

**Spot it:** the application could be asked about medicine doses: a health, pharmacy, or parenting product, or a general consumer assistant, whether or not the prompt mentions medicine.

**Verdict:** all models with a block: **add** the matching "Medicine dosing" block from `snippets.md`, word for word, even if nothing else changes. Fable 5.2 uses the same text as the Fable 5.1 group (Anthropic lists it under its own label). Haiku 5.5 has its own block (it adds a rule about emotional distress); Sonnet 4.6 and Haiku 4.5 have their own. If the application clearly cannot be asked about medicine (for example a code reviewer), skip it.

Source: [Best practices: medication dosing](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#medication-dosing).
