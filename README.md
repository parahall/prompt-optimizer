# prompt-optimizer

A [Claude Code](https://code.claude.com) skill that rewrites a prompt for the specific model that will run it.

You give it a prompt (an app's system prompt, agent instructions, a `CLAUDE.md` or skill file, a tool description, or a one-off task prompt) and name the target model. The skill:

1. checks the prompt against the model maker's official prompting guidance for that exact model,
2. rewrites it with as few changes as possible,
3. explains every change with a link to the documentation section it comes from,
4. recommends matching API settings (for Claude: effort level, thinking mode, `max_tokens`; for OpenAI: reasoning effort, `text.verbosity`, which API to call),
5. says what to test on real traffic.

It also moves prompts between providers, for example a prompt tuned for Claude that will now run on GPT-6, removing the habits that only made sense for the old model.

Why per model: the same instruction can help one model and hurt another. "Double-check your answer" helps most Claude models but causes wasted re-checking on Claude Opus 5. A rule against bullet points helps older models but suppresses needed structure on Claude Fable 5.1. Asking for reasoning inside `<thinking>` tags, once common advice, can make the newest Claude models decline the request. On the OpenAI side, a step-by-step process script makes GPT-5.5 mechanical but is exactly what GPT-5.4 Mini needs, and "Be concise" can make GPT-5.6 answers too short.

**Supported now:**
- Claude models: Fable 5.1, Fable 5, Opus 5.5, Opus 5, Opus 4.8, Sonnet 5.5, Sonnet 5, Haiku 5.5, and short notes for older models.
- OpenAI GPT text models: the GPT-6 family (Astra, 6.1 Sol, 6.1 Terra, Luna, 6 Sol), the GPT-5.6 family (Sol, Terra, Luna), GPT-5.5, GPT-5.4 and 5.4 Mini, and short notes for 5.3-Codex, 5.2, 5.1, 5, and 4.1. Voice, image, and open-weight models are not covered.

**Planned:** Google Gemini models.

## Example

Input, a support-bot system prompt moving to Claude Opus 5:

```text
You are a support assistant for the Tidewater Transit app.
CRITICAL: You MUST ALWAYS use the search_help_center tool before answering.
Think step by step inside <thinking> tags before every answer.
Double-check your answer before responding.
NEVER use markdown.
```

Output (prompt part):

```text
You are a support assistant for the Tidewater Transit app.

Before every answer, search the help center with the search_help_center tool.

Write in plain text. Do not use Markdown formatting.

Keep responses focused, brief, and concise. Keep disclaimers and caveats short,
and spend most of the response on the main answer. When asked to explain
something, give a high-level summary unless an in-depth explanation is
specifically requested.
```

Plus the reasons: the `<thinking>` request can trigger refusals on this model; Opus 5 already checks its own work, so the double-check line goes; capital-letter "MUST ALWAYS" makes newer models over-use a tool, so the rule is kept but said calmly; Opus 5 writes long replies by default and lowering effort does not shorten them, so Anthropic's conciseness block is added word for word. And settings: start at `low` or `medium` effort for chat.

## Where the result goes

- Prompt from a file: new files next to it (`<name>.optimized.<ext>` and `<name>.optimized.report.md`). The original is never overwritten unless you ask.
- Prompt pasted into the chat: the full result in the chat.
- If the Artifact tool is available in your session: also a private side-by-side page comparing old and new.

## Install

### As a plugin (recommended)

In Claude Code:

```
/plugin marketplace add parahall/prompt-optimizer
/plugin install prompt-optimizer@prompt-optimizer
```

Run it with `/prompt-optimizer:optimize-prompt`, or just ask Claude to optimize a prompt for a named model.

### Updating the plugin

The plugin has no fixed version number, so every change merged to `main` counts as a new version. Claude Code does not update plugins from this marketplace automatically unless you turn it on:

- **Automatic:** run `/plugin`, open the Marketplaces tab, select `prompt-optimizer`, and choose "Enable auto-update". Claude Code then checks for updates in the background during your sessions.
- **Manual:** run `claude plugin update prompt-optimizer@prompt-optimizer`, or choose "Update now" for the plugin in `/plugin`.

A running session keeps the version it started with. Run `/reload-plugins` or start a new session to use the update.

### As a personal skill from a clone

```bash
git clone https://github.com/parahall/prompt-optimizer.git
ln -s "$PWD/prompt-optimizer/skills/optimize-prompt" ~/.claude/skills/optimize-prompt
```

Run it with `/optimize-prompt`.

## Usage

```
/optimize-prompt prompts/system.md for claude-sonnet-5-5
```

Or in plain words: "Optimize this system prompt for Claude Haiku 5.5. It's a support chatbot with a web search tool." Mentioning problems you have already seen ("the agent stops halfway", "replies are too long") helps the skill choose the right fixes.

## Known limits

- **A prompt can be refused before the skill sees it.** The newest Claude models run safety filters on their input. If the prompt you want to optimize asks for written-out reasoning (for example "write your full reasoning inside `<thinking>` tags"), the model running Claude Code may decline the whole request with the `reasoning_extraction` category. In testing this happened with Claude Sonnet 5.5 as the session model, not with Opus 5.5 or Haiku 5.5. Workaround: switch the session to another model for that one prompt.
- **The skill follows the docs, not your traffic.** Every change is a well-sourced starting point. Measure it on real requests before shipping, as the report's "What to test" section suggests.

## How it is built

```
skills/optimize-prompt/
├── SKILL.md                     # the workflow
└── reference/
    ├── providers.md             # model name → provider folder
    ├── anthropic/
    │   ├── audit-checklist.md   # patterns to find, with a verdict per model
    │   ├── api-settings.md      # effort, thinking, max_tokens per model
    │   ├── general-techniques.md
    │   ├── snippets.md          # tested text blocks shared by several models
    │   └── models/              # one file per model
    └── openai/
        ├── audit-checklist.md   # contradictions first, then repetition, scripts, ...
        ├── api-settings.md      # reasoning effort, verbosity, endpoint limits per model
        ├── general-techniques.md
        ├── snippets.md          # which model file holds the block for each symptom
        └── models/              # one file per model family (OpenAI writes its advice per family)
```

Each provider folder has the same parts, so adding a provider does not change the workflow.

## Maintaining

Model makers update their guides often. Two scripts help:

- `tools/refresh-docs.sh` downloads the documentation pages listed in `tools/sources/<provider>.txt` into `docs-cache/` (not committed) and prints what changed since the last download.
- `python3 tools/check-references.py` confirms, for every provider folder, that every quoted block still appears word for word in the docs, that every model or model family in the docs has a file, and that every link works.

Tests: `claude plugin eval .` runs the cases in `evals/`, each with and without the skill. The case that tests file output needs `--scaffold --allow-tools Write`.

## Sources and credit

The rules in `skills/optimize-prompt/reference/anthropic/` summarize, in our own words, Anthropic's public prompting documentation at [platform.claude.com/docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Text blocks marked "Quoted from Anthropic" are copied word for word from those pages, with a link to the exact section, so the skill can insert the tested wording unchanged. The quoted text remains the work of Anthropic.

The rules in `skills/optimize-prompt/reference/openai/` do the same for OpenAI's public documentation at [developers.openai.com](https://developers.openai.com/api/docs/guides/prompt-engineering). Text blocks marked "Quoted from OpenAI" are copied word for word, with the page and section named. The quoted text remains the work of OpenAI.

This project is independent and is not made or endorsed by Anthropic, OpenAI, or Google.

## License

MIT for the original content of this repository. See [LICENSE](LICENSE).
