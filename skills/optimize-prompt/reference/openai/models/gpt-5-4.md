# GPT-5.4 and GPT-5.4 Mini

Checked against the docs on 2026-11-08.
Sources: [Using GPT-5.4](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.4) (section names below refer to this page) and [Upgrading to GPT-5.4](https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p4).
API IDs `gpt-5.4`, `gpt-5.4-mini` (and `gpt-5.4-nano`). **Default effort `none`.** Settings: `api-settings.md`.

GPT-5.4 prompts use XML-tagged blocks; OpenAI says: "Start with the smallest prompt that passes your evals, and add blocks only when they fix a measured failure mode." Add a block below only for its symptom.

Contents: How it differs · GPT-5.4 Mini · Remove from prompts · Add when you see this symptom · API settings
Symptoms covered:
- Replies too long or structure drifts
- Unclear when to proceed and when to ask; mid-conversation changes ignored
- Tool use stops early or skips prerequisites
- Long tasks finish with items missing
- High-impact actions without checks; guessing when context is missing
- Final answers overuse or nest bullet lists
- Coding agent stops at analysis instead of implementing
- Stops at the first plausible answer
- Customer-facing writing lacks a clear voice

## How it differs from GPT-5.2

- Stronger: personality and tone with less drift; sticking with multi-step work and retrying; long-context synthesis; batched and parallel tool calls; following block-structured prompts when the contract is explicit.
- Still needs explicit help with: tool routing early in a session, dependent steps, choosing effort, research citations, irreversible actions, terminal tool boundaries.
- **Often defaults to more structured formatting and may overuse bullet lists.**
- More thorough end to end, so it often needs less "verify everything" prompting; keep a light verification clause for high-stakes changes.
- Meant as a drop-in replacement for 5.2 at default settings.

## GPT-5.4 Mini (and Nano) ("Small-model guidance")

Mini is **more literal, makes fewer assumptions, is weaker on implicit workflows and ambiguity**, and may keep the conversation going with a follow-up question unless told not to. Prompts for small models are often longer and more explicit, which is the opposite of the GPT-5.5/5.6 advice. Apply these rules (OpenAI's list):

- Put critical rules first.
- Specify the full execution order when tool use or side effects matter.
- Do not rely on "you MUST" alone; use numbered steps, decision rules, and explicit action definitions.
- Separate "do the action" from "report the action."
- Show the correct flow, not just the final format.
- Define when to ask, abstain, or proceed.
- Specify answer length, whether to ask a follow-up question, citation style, and section order.
- Prefer scoped endings ("after the final JSON, output nothing further") over "output nothing else".

Good default order for Mini prompts: task; critical rule; exact step order; edge cases or clarification behavior; output format; one correct example. Avoid implied next steps, unspecified edge cases, schema-only prompts for tool workflows, and generic instructions without structure.

Nano: only narrow tasks with closed outputs (labels, enums, short JSON); route ambiguous or planning-heavy tasks to a stronger model instead of over-prompting.

## Remove from prompts

- **Blanket "verify everything" scaffolding** on routine work (5.4 is already thorough); keep it for production, migration, or security changes.
- **`temperature`, `top_p`, `logprobs`** unless effort is `none` ("GPT-5.4 parameter compatibility").
- **Blocks that fix nothing measured** (each block should do real work).

## Add when you see this symptom

### Replies too long or structure drifts

> Quoted from OpenAI · "Using GPT-5.4" · "Keep outputs compact and structured"
```xml
<output_contract>
- Return exactly the sections requested, in the requested order.
- If the prompt defines a preamble, analysis block, or working section, do not treat it as extra output.
- Apply length limits only to the section they are intended for.
- If a format is required (JSON, Markdown, SQL, XML), output only that format.
</output_contract>

<verbosity_controls>
- Prefer concise, information-dense writing.
- Avoid repeating the user's request.
- Keep progress updates brief.
- Do not shorten the answer so aggressively that required evidence, reasoning, or completion checks are omitted.
</verbosity_controls>
```

### Unclear when to proceed and when to ask; mid-conversation changes ignored

> Quoted from OpenAI · "Using GPT-5.4" · "Set clear defaults for follow-through"
```xml
<default_follow_through_policy>
- If the user’s intent is clear and the next step is reversible and low-risk, proceed without asking.
- Ask permission only if the next step is:
  (a) irreversible,
  (b) has external side effects (for example sending, purchasing, deleting, or writing to production), or
  (c) requires missing sensitive information or a choice that would materially change the outcome.
- If proceeding, briefly state what you did and what remains optional.
</default_follow_through_policy>
```

> Quoted from OpenAI · "Using GPT-5.4" · "Set clear defaults for follow-through"
```xml
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

### Tool use stops early or skips prerequisites

> Quoted from OpenAI · "Using GPT-5.4" · "Make tool use persistent when correctness depends on it"
```xml
<tool_persistence_rules>
- Use tools whenever they materially improve correctness, completeness, or grounding.
- Do not stop early when another tool call is likely to materially improve correctness or completeness.
- Keep calling tools until:
  (1) the task is complete, and
  (2) verification passes (see <verification_loop>).
- If a tool returns empty or partial results, retry with a different strategy.
</tool_persistence_rules>
```

> Quoted from OpenAI · "Using GPT-5.4" · "Make tool use persistent when correctness depends on it"
```xml
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval steps are required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If the task depends on the output of a prior step, resolve that dependency first.
</dependency_checks>
```

### Long tasks finish with items missing

> Quoted from OpenAI · "Using GPT-5.4" · "Force completeness on long-horizon tasks"
```xml
<completeness_contract>
- Treat the task as incomplete until all requested items are covered or explicitly marked [blocked].
- Keep an internal checklist of required deliverables.
- For lists, batches, or paginated results:
  - determine expected scope when possible,
  - track processed items or pages,
  - confirm coverage before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly what is missing.
</completeness_contract>
```

### High-impact actions without checks; guessing when context is missing

> Quoted from OpenAI · "Using GPT-5.4" · "Add a verification loop before high-impact actions"
```xml
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by the provided context or tool outputs?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects, ask permission first.
</verification_loop>
```

> Quoted from OpenAI · "Using GPT-5.4" · "Add a verification loop before high-impact actions"
```xml
<missing_context_gating>
- If required context is missing, do NOT guess.
- Prefer the appropriate lookup tool when the missing context is retrievable; ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>
```

### Final answers overuse or nest bullet lists

> Quoted from OpenAI · "Using GPT-5.4" · "Prompting patterns for coding tasks"
```xml
Never use nested bullets. Keep lists flat (single level). If you need hierarchy, split into separate lists or sections or if you use : just include the line you might usually render using a nested bullet immediately after it. For numbered lists, only use the `1. 2. 3.` style markers (with a period), never `1)`.
```

### Coding agent stops at analysis instead of implementing

> Quoted from OpenAI · "Using GPT-5.4" · "Prompting patterns for coding tasks"
```xml
<autonomy_and_persistence>
Persist until the task is fully handled end-to-end within the current turn whenever feasible: do not stop at analysis or partial fixes; carry changes through implementation, verification, and a clear explanation of outcomes unless the user explicitly pauses or redirects you.

Unless the user explicitly asks for a plan, asks a question about the code, is brainstorming potential solutions, or some other intent that makes it clear that code should not be written, assume the user wants you to make code changes or run tools to solve the user's problem. In these cases, it's bad to output your proposed solution in a message, you should go ahead and actually implement the change. If you encounter challenges or blockers, you should attempt to resolve them yourself.
</autonomy_and_persistence>
```

### Stops at the first plausible answer (try before raising effort)

> Quoted from OpenAI · "Using GPT-5.4" · "Treat reasoning effort as a last-mile knob"
```xml
<dig_deeper_nudge>
- Don’t stop at the first plausible answer.
- Look for second-order issues, edge cases, and missing constraints.
- If the task is safety or accuracy critical, perform at least one verification step.
</dig_deeper_nudge>
```

### Customer-facing writing lacks a clear voice
Fill in the angle-bracket fields; personality must not override required formats (if the user asks for JSON, return JSON).

> Quoted from OpenAI · "Using GPT-5.4" · "Control personality for customer-facing workflows"
```xml
<personality_and_writing_controls>
- Persona: <one sentence>
- Channel: <Slack | email | memo | PRD | blog>
- Emotional register: <direct/calm/energized/etc.> + "not <overdo this>"
- Formatting: <ban bullets/headers/markdown if you want prose>
- Length: <hard limit, e.g. <=150 words or 3-5 sentences>
- Default follow-through: if the request is clear and low-risk, proceed without asking permission.
</personality_and_writing_controls>
```

## API settings

- Default effort `none`. Most teams should stay in `none`–`medium`: `none` for extraction, triage, short transforms; `low`/`medium` for nuanced interpretation; `medium`+ for research; `xhigh` not as a default. At `none`, asking the model to outline its steps first helps.
- Before raising effort, add `<completeness_contract>`, `<verification_loop>`, `<tool_persistence_rules>`, then `<dig_deeper_nudge>`.
- `temperature`, `top_p`, `logprobs` only at effort `none`.
- Preserve `phase` when replaying assistant items; set image `detail` explicitly for vision and computer use.
- Migration starts: from 5.2 or 5.3-Codex keep the effort; from GPT-4.1 or 4o start at `none`; research and long agents `medium` or `high`.
