# Older Claude models without their own prompting page

Checked against the docs on 2026-11-08.
Sources: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (BP) and [Effort](https://platform.claude.com/docs/en/build-with-claude/effort). These models have only the notes below; apply `general-techniques.md` and `audit-checklist.md` with the verdicts for "thinking off" where relevant.

When the user is migrating a prompt **from** one of these models to a current model, use this file to recognize habits written for the old model, then follow the target model's file.

## Claude Opus 4.7 (`claude-opus-4-7`)

- Effort guidance is the same as Opus 4.8: `xhigh` for coding and agentic work, at least `high` for intelligence-sensitive work. At `low`, pair the prompt with an explicit checklist if the task has several sections. `max` can over-think structured-output tasks.
- Respects effort strictly; at low effort it does only what was asked. If reasoning is shallow, raise effort rather than prompting around it.
- Thinking off by default; adaptive only (manual `budget_tokens` returns a 400 error).
- Most Opus 4.8 notes (literal instruction following, design defaults) are described as shared with it.

## Claude Opus 4.6 (`claude-opus-4-6`)

- Does more up-front exploration, especially at higher effort; can over-think and over-gather. Replace blanket defaults ("Default to using [tool]") with targeted ones ("Use [tool] when it would enhance your understanding of the problem"); remove "If in doubt, use [tool]"; lower effort as a fallback.
- Very responsive to the system prompt: aggressive tool wording ("CRITICAL: You MUST use this tool") now over-triggers; soften it.
- Strong tendency to spawn subagents where a direct approach would do; add "When to use subagents" from `snippets.md`.
- May take hard-to-reverse actions without guidance; add "Confirm before risky actions" from `snippets.md`.
- Tends to over-engineer; add "Over-engineering" from `snippets.md`.
- Effort levels: low, medium, high, max (no `xhigh`). Manual `budget_tokens` still works but is deprecated.

If it thinks too long:

> Quoted from Anthropic · BP · "Overthinking and excessive thoroughness"
```text
When you're deciding how to approach a problem, choose an approach and commit to it.
Avoid revisiting decisions unless you encounter new information that directly
contradicts your reasoning. If you're weighing two approaches, pick one and see it
through. You can always course-correct later if the chosen approach fails.
```

## Claude Opus 4.5 (`claude-opus-4-5`)

- **With thinking disabled, it is especially sensitive to the word "think"** and its variants. Use "consider", "evaluate", or "reason through" instead.
- Over-engineers (extra files, abstractions, flexibility); add "Over-engineering" from `snippets.md`.
- Responsive to the system prompt; soften aggressive tool wording.
- Extended thinking only (`budget_tokens`); effort levels low, medium, high, used together with the budget.
- Front ends drift to a generic look without guidance. For Opus 4.5 and 4.6 the long aesthetics block applies:

> Quoted from Anthropic · BP · "Frontend design"
```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this
creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive
frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic
fonts like Arial and Inter; opt instead for distinctive choices that elevate the
frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency.
Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw
from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only
solutions for HTML. Use Motion library for React when available. Focus on high-impact
moments: one well-orchestrated page load with staggered reveals (animation-delay)
creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer
CSS gradients, use geometric patterns, or add contextual effects that match the overall
aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the
context. Vary between light and dark themes, different fonts, different aesthetics. You
still tend to converge on common choices (Space Grotesk, for example) across
generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## Claude Sonnet 4.6 (`claude-sonnet-4-6`)

- Set effort explicitly; `medium` is the recommended default (agentic coding, tool-heavy work), `low` for chat and high volume, `high` for complex reasoning. No `xhigh`.
- Thinking off by default; adaptive available; manual `budget_tokens` deprecated.
- Tracks its remaining context window (context awareness); in a harness that compacts context, add "Context will be compacted, do not stop early" from `snippets.md`.
- More proactive than earlier models; reduce anti-laziness wording.

## Claude Haiku 4.5 (`claude-haiku-4-5`)

- No effort setting. Extended thinking only (`budget_tokens`); thinking off by default.
- Context awareness, as for Sonnet 4.6.
- Manual chain of thought (reason first, final answer in `<answer>` tags) is a valid fallback when thinking is off.

## Claude Sonnet 4.5 (deprecated)

Extended thinking only. Recommend migrating; treat prompts as "written for an older model" and follow the target model's file.
