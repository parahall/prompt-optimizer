# Providers

A provider is the company that makes the model. Find the provider from the target model's name, then open only that provider's folder.

| Model name looks like | Provider folder | Status |
|---|---|---|
| `claude-…`, "Claude …", "Opus", "Sonnet", "Haiku", "Fable", "Mythos" | `anthropic/` | Supported |
| `gpt-6…`, `gpt-5…`, `gpt-4.1…`, "GPT-6 Astra", "GPT-5.6 Sol", "Sol", "Terra", "Luna" with a GPT version | `openai/` | Supported for text models |
| `gemini-…`, "Gemini", "Google" | `google/` | Not supported yet |

Model names arrive in many shapes: API IDs (`claude-opus-5-5`, `gpt-6.1-sol`), display names ("Claude Opus 5.5", "GPT-5.6 Sol"), aliases (`gpt-5.6` routes to `gpt-5.6-sol`), cloud IDs (`anthropic.claude-opus-5-5`), or short forms ("opus 5.5", "5.6 terra"). Normalize to the API ID before looking up a model file.

**OpenAI models this skill does not cover:** voice models (GPT-Live, GPT-Realtime), image models (GPT-Image), transcription models, open-weight models (gpt-oss), the cybersecurity models (GPT-5.6 Cyber, GPT-6-Cyber), and older non-GPT-5 models such as GPT-4o and the o-series. OpenAI has separate prompting guides for voice and image models; say so and treat them like an unsupported provider.

## Every provider folder has the same parts

| File | Role |
|---|---|
| `general-techniques.md` | Rules that apply to all of the provider's current models |
| `audit-checklist.md` | Patterns to find in a prompt, with a verdict for each model |
| `api-settings.md` | The provider's request settings per model, and settings that fail |
| `snippets.md` | Tested text blocks shared by several models, or where to find them |
| `models/<model or family>.md` | How one model or family differs, what to remove, what to add for which symptom |
| `models/legacy.md` | Short notes on older models without their own file |

## When the provider or model is not supported

Say plainly that this skill has no guidance for that provider or model yet. Do not apply one provider's model-specific advice (effort levels, thinking modes, refusal categories, model behaviors) to another provider's model. You may offer provider-neutral improvements (clear task, context and reasons, examples, separated sections), labeled as general advice, not official guidance for that model.
