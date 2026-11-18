# GPT-6.2 family: GPT-6.2 Astra, GPT-6.2 Sol

Checked against the docs on 2026-11-18.
Sources: [Using GPT-6.2](https://developers.openai.com/api/docs/guides/latest-model/gpt-6.2-astra) (section names below refer to this page) and [Keep the prefix unchanged](https://developers.openai.com/api/docs/guides/keep-prefix-unchanged).
API IDs `gpt-6.2-astra`, `gpt-6.2-sol`. Settings: `api-settings.md`.

OpenAI writes one set of prompting advice for both models; it says the prompts are a starting point and address behavior seen with GPT-6.2 Astra and Sol. The page does not say the GPT-6 advice still applies, so this file does not inherit it; do not load `gpt-6.md` to fill in this family.

Contents: Family members · How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- The model proposes a next step or a plan and waits, where it should continue
- Long tasks end before every part is done or checked
- The model stops on an unclear detail it could reasonably assume
- Day-to-day collaboration: the writing is too thin or hard to follow
- Drafts for an outside audience lack background, or edits change the author's wording
- The final answer carries shorthand from the work, or reads like a continuation of progress updates
- Code ignores project conventions, adds needless tests, or is too dense or too abstract
- Frontend output uses the wrong kind of visuals or filler text

## Family members

- **GPT-6.2 Astra**: OpenAI's most capable model, for the hardest projects. Builds and revises software, uses a computer, works with documents.
- **GPT-6.2 Sol**: the go-to model for everyday work, from coding to agents at scale, at a quarter of Astra's token price.
- Both: text and image input, text output; 1.05M context, 128K max output; effort `none` is rejected. The pages checked do not list the other effort levels or the default.

## How it differs from GPT-6

The page describes GPT-6.2 Astra's behavior ("GPT-6.2 Astra behavior"):
- **More concise and direct by default** than earlier models; its tone can be tuned from professional colleague to conversational assistant.
- **When the user's intent is unclear, it may propose a next step and wait for confirmation.** For longer tasks it needs room to make reasonable assumptions and keep working.
- Tends to write **more efficient, high-quality code** than its predecessors; it needs the project's conventions described.
- Frontend: needs the imagery and typography specified when the interface must have a particular look.
- During longer tasks it can **carry shorthand from its reasoning or from other agents into its final answer**.
- API changes that affect prompts ("What's new"): the Responses API **drops reasoning items after edits to earlier conversation history** (prefix edits), certain model changes, or changes to the end user or organization; and top-level `instructions` are now **appended after `input`**.

## Remove from prompts

- **"Be concise" and similar brevity lines** carried over from older models: the page says to revisit them, because the model is already concise and direct. Keep one only if the product needs a fixed length. ("GPT-6.2 Astra behavior")
- **`temperature`, `top_p`, `logprobs`, `top_logprobs`**; in the Responses API also `message.output_text.logprobs` in `include`. ("Update API and model parameters")

## Add when you see this symptom

### The model proposes a next step or a plan and waits, where it should continue
For work that can proceed without supervision. The page says to specify the outcome to complete and which decisions need the user's input, so keep the product's own rules about what needs approval. The block's first paragraph contains the typo "maketo"; it is OpenAI's.

> Quoted from OpenAI · "Using GPT-6.2" · "Task completion"
```text
Avoid stopping to end the turn while the task is incomplete or if there is an authorized next step you can take, and instead take the next steps within task scope to progress the user's request. If your final response before ending the turn is a suggested next step, a plan, a request to the user for a routine decision, instructions for a task to execute, or similar handoff to the user, take these steps yourself to make progress towards what the user asked for. Make sure that you have authorization to do so, and flag any assumptions or decisions you maketo the user.

Only stop to clarify with the user if there is significant change in task scope, you are concretely blocked, have a decision that the user needs to resolve, or before irreversible or destructive actions.
```

### Long tasks end before every part is done or checked
Higher reasoning effort also helps the model persist through final checks on complex or long-running tasks; recommend it with the block.

> Quoted from OpenAI · "Using GPT-6.2" · "Task completion"
```text
Bias towards action, and persist until you've completed the task the user asked for. Avoid stopping to end the turn while the task is incomplete or if there is an authorized next step you can take, and instead take the next steps within task scope to progress the user's request. Make sure that you have accounted for every part of the user's request, and persist until you've delivered a result that fully satisfies the user's goal. If a task requires sustained work, do all the necessary work until the intended outcome is completely fulfilled.

Progress autonomously towards the user's goal (e.g. creating isolated worktrees / checkouts if needed, resolving merge conflicts, creating draft PRs etc) unless they are clearly destructive or irreversible. Before ending a turn or calling your work complete, check that your work fully satisfies what the user asked for. If any steps remain or any part of the result still needs verification, follow through on this work before finishing.
```

### The model stops on an unclear detail it could reasonably assume

> Quoted from OpenAI · "Using GPT-6.2" · "Task completion"
```text
Make reasonable, reversible assumptions to carry work forward and state them if it progresses the task within scope. Do not second guess yourself, stop after describing what you could do, offer to do the work, or provide a partial answer unless there is no way you can proceed.
```

If the application can add an async tool such as `request_user_input_async`, the model can ask the user and continue work that does not depend on the answer; report this as a harness option.

### Day-to-day collaboration: the writing is too thin or hard to follow
For using the model as a collaborator and thought partner.

> Quoted from OpenAI · "Using GPT-6.2" · "Writing style"
```text
Write using terminology the user and sources use. Keep technical details and use domain-specific language when they make the explanation more precise. Use the active voice and keep closely related details together. Cover the key points up front, and avoid references that the reader can only make sense of later in the response. Give the user enough context to follow your reasoning.
```

### Drafts for an outside audience lack background, or edits change the author's wording
For documents, emails, messages, and external posts.

> Quoted from OpenAI · "Using GPT-6.2" · "Writing style"
```text
When drafting a message or any other material on behalf of the user to be sent to an external audience, consider who will read it and tailor the content to that intended audience. The intended audience likely does not have the same context as the user, so ensure that you provide the background information or reasoning required for the audience to understand the content. When reviewing or editing existing content, preserve the author’s content and wording, and follow the user's instruction carefully for what edits they want.
```

### The final answer carries shorthand from the work, or reads like a continuation of progress updates

> Quoted from OpenAI · "Using GPT-6.2" · "Writing style"
```text
Treat your final answer as the user's first look at your work, and not as a continuation of intermediate commentary. The final answer must always be fully self-contained: users should never need to read earlier commentary updates for context, since they are collapsed when the final answer is shown to the user.

Write the final answer and all other human-facing material anew for the intended reader. Do not copy or closely paraphrase your reasoning or adopt its writing style. Do not carry over working shorthand, jargon, or abbreviations from your reasoning, tool calls, or instructions to subagents and automations.
```

### Code ignores project conventions, adds needless tests, or is too dense or too abstract
The page says to describe the codebase's conventions and the behavior existing callers rely on: when to reuse logic, how narrowly to scope a change, when to add a test. Replace or extend the points with the user's own conventions where they have them.

> Quoted from OpenAI · "Using GPT-6.2" · "Coding style"
```text
Above all, be thorough in producing high-quality, correct code that completely fulfills the user's task. Keep the code easy to read and verify that the user-requested outcome works as they intend. Follow these instructions when coding:

(a) Reuse existing logic in the user's repo when you can. You should reuse existing classes, methods, representations, and APIs in the codebase as long as they preserve correctness. Before consolidating or removing code, preserve the behavior its callers rely on unless the task requires changing it.
(b) Skip new tests unless requested, required by the repo, or needed to catch a specific regression existing tests would miss.
(c) Make sure that code is human readable. Do not use fewer lines, shorter variable names, minified formatting, or dense one-liners as substitutes for simplicity. Ensure that comments and variable names are readable and understandable to a human. Code-golfed expressions count as overly complex when they encode many branches, conditions, or hidden assumptions.
(d) Avoid unnecessary indirection and abstraction. Helper functions, utility functions, and class abstractions can add cognitive complexity even when they do not add branches.
```

### Frontend output uses the wrong kind of visuals or filler text
First have the prompt describe the visual style the application depends on: the kinds of images and the typography, including a typeface when it matters. Then:

> Quoted from OpenAI · "Using GPT-6.2" · "Frontend design"
```text
When generating webpages or apps with a frontend user interface, follow these instructions:

- When choosing visuals, generally prefer realistic images from ImageGen or image search that suit the project's style and purpose. Use SVGs when the user specifically asks for them.
- Include a text element only when it provides information the user needs, helps them navigate or act, or fulfills an explicit content request. Remove decorative numbering, filler badges, redundant headings, and explanatory copy that merely restates what the surrounding interface already makes clear, while preserving necessary labels, instructions, and status feedback.
```

For visual work the page also suggests sharing a reference image, or giving the model the image generation tool to create one, then asking it to build, render, and refine against the reference.

## API settings

- Effort: start with `medium` for a new integration. If the old request used `none` or `minimal`, use `low`. ("Update API and model parameters")
- Tool calling: use the Responses API. Both models support Chat Completions, but tool calling requires Responses.
- **Where the prompt goes:** put reusable instructions in a `developer` message as the first item in `input`, so they can be cached. Top-level `instructions` is appended after `input` on these models, billed at the uncached rate, and meant for guidance that applies only to the current request.
- **Keep the conversation prefix unchanged.** Changing earlier history (rewriting a developer message, shortening a tool result, summarizing older turns) makes the API drop the reasoning items after the change; quality can drop and tokens rise. To update instructions mid-conversation, append a new `developer` message at the end. To change effort or the output schema, append a `configuration_update` item and keep the request-level setting the same. To add tools, append an `additional_tools` item. Apply an optimized prompt to new conversations, or append it. ("Keep the prefix unchanged")
- From GPT-5.5 or earlier: replace `prompt_cache_retention` with `prompt_cache_options.ttl` (`"30m"`).

## Known traps

- The autonomy blocks make the model act more; keep explicit confirmation rules for external, destructive, or costly actions.
- Advice from the GPT-6 or GPT-5.6 files is not documented for this family; if used, label it so.
