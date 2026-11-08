# Claude Sonnet 5

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5) (section names below refer to this page).
API ID `claude-sonnet-5`. Default effort `high`. Thinking: adaptive **on by default** (a change from Sonnet 4.6); `disabled` accepted. Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- A rule should apply broadly
- Replies are too long
- Shallow reasoning at `low` effort that must stay low
- Thinking triggers more often than wanted (large system prompts)
- Tools unused, especially with thinking disabled
- Warmer voice needed
- Code review reports too few bugs
- Frontend output always looks the same

## How it differs from Sonnet 4.6

- Strong at coding and agentic tasks; Sonnet 4.6 prompts work without changes.
- Reply length follows task complexity.
- Respects effort strictly; at `low`/`medium` it does only what was asked and can under-think moderately complex tasks. Sonnet 5 at `medium` is about Sonnet 4.6 at `high`; at `high` about Sonnet 4.6 at `max`.
- More agentic: reaches for tools and self-verification more readily. With thinking disabled it is less likely to use tools or search.
- Gives regular, good progress updates without scaffolding.
- **Follows instructions literally**, especially at low effort; does not generalize a rule from one item to others.
- New tokenizer: about 30 percent more tokens for the same text, so old `max_tokens` limits can truncate.
- `temperature`, `top_p`, `top_k` return a 400 error.
- Settles into a default visual style on open-ended design briefs.
- Follows severity filters in review prompts literally.

## Remove from prompts

- **Forced status scaffolding** ("after every 3 tool calls, summarize progress"). ("User-facing progress updates")
- **Severity filters in review prompts**. ("Code review harnesses")
- **Generic design instructions** ("make it clean and minimal"). ("Design and frontend defaults")
- **Reliance on `temperature` for variety**: move variety into the prompt (for example "propose 4 distinct directions"). ("Tone and writing style")

## Add when you see this symptom

### A rule should apply broadly
State the scope explicitly, for example "Apply this formatting to every section, not just the first one." ("More literal instruction following")

### Replies are too long

> Quoted from Anthropic · "Response length and verbosity"
```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

### Shallow reasoning at `low` effort that must stay low
Raise effort first; otherwise:

> Quoted from Anthropic · "Calibrating effort and thinking depth"
```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

### Thinking triggers more often than wanted (large system prompts)

> Quoted from Anthropic · "Calibrating effort and thinking depth"
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

### Tools unused, especially with thinking disabled
Add an explicit instruction on when and why to use the tool; raise effort to `high`/`xhigh`. ("Tool use triggering")

### Warmer voice needed

> Quoted from Anthropic · "Tone and writing style"
```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### Code review reports too few bugs
Use "Report every issue" in `snippets.md`.

### Frontend output always looks the same
Give a concrete spec (palette hex values, type, layout, radius), or:

> Quoted from Anthropic · "Design and frontend defaults"
```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

> Quoted from Anthropic · "Design and frontend defaults"
```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## API settings

- `high` default; `xhigh` for the hardest coding and agentic work; `medium` for cost-sensitive; `low` for short, latency-sensitive tasks.
- At `high` and above leave headroom in `max_tokens`; revisit limits tuned for Sonnet 4.6 (new tokenizer, thinking now on).
- Manual extended thinking (`budget_tokens`) returns a 400 error.
- Coding products: `xhigh` or `high`, an autonomous mode, and the full task in the first turn.
- Computer use: 1080p screenshots balance cost and quality; 720p or 1366×768 for cost-sensitive work.
