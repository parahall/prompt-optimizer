# Providers

A provider is the company that makes the model. Find the provider from the target model's name, then open only that provider's folder.

| Model name looks like | Provider folder | Status |
|---|---|---|
| `claude-…`, "Claude …", "Opus", "Sonnet", "Haiku", "Fable", "Mythos" | `anthropic/` | Supported |
| `gpt-…`, `o1`, `o3`, `o4-…`, "ChatGPT", "OpenAI" | `openai/` | Not supported yet |
| `gemini-…`, "Gemini", "Google" | `google/` | Not supported yet |

Model names arrive in many shapes: API IDs (`claude-opus-5-5`), display names ("Claude Opus 5.5"), cloud IDs (`anthropic.claude-opus-5-5`, `claude-opus-5-5@…`), or short forms ("opus 5.5"). Normalize to the API ID before looking up a model file.

## Every provider folder has the same parts

| File | Role |
|---|---|
| `general-techniques.md` | Rules that apply to all of the provider's current models |
| `audit-checklist.md` | Patterns to find in a prompt, with a verdict for each model |
| `api-settings.md` | The provider's request settings per model, and settings that now fail |
| `snippets.md` | Tested text blocks shared by several models |
| `models/<model>.md` | How one model differs, what to remove, what to add for which symptom |
| `models/legacy.md` | Short notes on older models without their own page |

## When the provider is not supported

Say plainly that this skill has no guidance for that provider yet. Do not apply one provider's model-specific advice (effort levels, thinking modes, refusal categories, model behaviors) to another provider's model. You may offer provider-neutral improvements (clear task, context and reasons, examples, separated sections), labeled as general advice, not official guidance for that model.
