# Claude Opus 4.8

Checked against the docs on 2026-11-08.
Source: [Prompting Claude Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8) (section names below refer to this page).
API ID `claude-opus-4-8`. Default effort `high`. **Thinking is off unless the request sends `thinking: {type: "adaptive"}`.** Settings: `api-settings.md`.

Contents: How it differs · Remove from prompts · Add when you see this symptom · API settings · Known traps
Symptoms covered:
- A rule should apply to many items but the model applies it to one
- Replies are too long for the product
- Shallow reasoning at `low` effort, and effort cannot be raised
- Thinking (adaptive) triggers more often than wanted, often with large system prompts
- Too few tool calls (for example web search unused)
- More subagents wanted
- A warmer product voice is needed
- Code review reports too few bugs
- Frontend output always has the same house style

## How it differs from Opus 4.7

- Strong at long agentic work, knowledge work, vision, and memory tasks. Opus 4.7 prompts work without changes.
- Reply length follows its estimate of task complexity: short for lookups, much longer for open analysis.
- Effort matters more than for any earlier Opus. It respects effort strictly; at `low`/`medium` it does only what was asked and can under-think moderately complex tasks.
- **Follows instructions literally**, especially at low effort: it does not stretch a rule from one item to others or infer requests you did not make.
- Prefers reasoning over tool calls; higher effort raises tool use.
- Gives regular progress updates without scaffolding.
- Spawns fewer subagents by default.
- Direct, opinionated tone with little validation and few emoji.
- Persistent default design style: cream/off-white backgrounds, serif display type, italic accents, terracotta accent.
- Better bug finding, but follows severity filters in review prompts literally.
- Uses more tokens in interactive sessions because it reasons after each user turn.

## Remove from prompts

- **Forced status scaffolding** ("after every 3 tool calls, summarize progress"). ("User-facing progress updates")
- **Severity filters in review prompts** ("only report high-severity issues", "be conservative", "don't nitpick"). ("Code review harnesses")
- **Generic design instructions** ("don't use cream", "make it clean and minimal"): they move the model to another fixed palette. ("Design and frontend defaults")
- Long frontend-aesthetics blocks written for earlier models; it needs less design prompting.

## Add when you see this symptom

### A rule should apply to many items but the model applies it to one
State the scope explicitly, in the prompt's own words, for example "Apply this formatting to every section, not just the first one." ("More literal instruction following")

### Replies are too long for the product

> Quoted from Anthropic · "Response length and verbosity"
```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

### Shallow reasoning at `low` effort, and effort cannot be raised
Raise effort first. If it must stay low:

> Quoted from Anthropic · "Calibrating effort and thinking depth"
```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

### Thinking (adaptive) triggers more often than wanted, often with large system prompts

> Quoted from Anthropic · "Calibrating effort and thinking depth"
```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multistep reasoning. When in doubt, respond directly.
```

### Too few tool calls (for example web search unused)
Raise effort to `high` or `xhigh`, and say in the prompt when and why to use the tool. ("Tool use triggering")

### More subagents wanted
Give explicit guidance about when to spawn. Example from the page (adapt it to the use case):

> Quoted from Anthropic · "Controlling subagent spawning"
```text
Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see).

Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

### A warmer product voice is needed

> Quoted from Anthropic · "Tone and writing style"
```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### Code review reports too few bugs
Use the "Report every issue" block in `snippets.md`, or a concrete single-pass threshold.

### Frontend output always has the same house style
Option 1: give a concrete visual spec (palette with hex values, typography, layout, corner radius, motion). Option 2:

> Quoted from Anthropic · "Design and frontend defaults"
```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface — one-line rationale). Ask the user to pick one, then implement only that direction.
```

Short aesthetics block that works with either option:

> Quoted from Anthropic · "Design and frontend defaults"
```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## API settings

- `xhigh` for coding and agentic work; at least `high` for intelligence-sensitive work; `medium`/`low` only where measured quality holds.
- At `xhigh`/`max`: `max_tokens` about 64,000 to start.
- Coding products: `xhigh` or `high`, an autonomous mode, and the full task in the first turn.

## Known traps

- Thinking is off by default; a prompt that assumes thinking needs `adaptive` set in the request.
- Underspecified requirements spread over many turns cost tokens and quality; put the task, intent, and constraints in the first turn.
