# API settings for OpenAI GPT models

Checked against the docs on 2026-11-08. Sources: [Models](https://developers.openai.com/api/docs/models) and each model's catalog page, [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning), [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra), [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.6), [Upgrading to GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/upgrading-to-gpt-5p6-sol), [Using GPT-5.5](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5), [Using GPT-5.4](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.4).

Many problems are fixed by settings, not wording. Always report recommended settings next to the rewritten prompt, and only settings the target model accepts.

Contents
1. The controls
2. Per-model table
3. Starting effort by kind of work
4. Settings that return errors or break things
5. Rules that affect how the prompt may change

## 1. The controls

- **Reasoning effort** (`reasoning.effort` in the Responses API, `reasoning_effort` in Chat Completions): `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`; which values exist depends on the model. OpenAI calls it a "last-mile knob": fix the prompt first (success criteria, stop rules, verification), then change effort one step at a time.
- **Verbosity** (`text.verbosity` in the Responses API, top-level `verbosity` in Chat Completions): `low`, `medium` (default), `high`. Sets the default length of the visible answer, not the thinking. Task-specific length rules in the prompt still apply on top.
- **Reasoning mode** (`reasoning.mode: "pro"`, GPT-5.6 and GPT-6, Responses API only): more model work for one final answer; costs more and is slower. Chosen separately from effort. The docs disagree on which efforts Pro accepts: the GPT-5.6 upgrade guide says "supported Pro efforts begin at `medium`", while the GPT-5.6 model guide says Pro works with any supported effort. Recommend `medium` or higher with Pro and say the docs disagree. Do not ask for it in the prompt ("think harder", "generate several candidates").
- **Persisted reasoning** (`reasoning.context`: `auto`, `current_turn`, `all_turns`): whether reasoning from earlier turns stays available. GPT-5.6 defaults to `all_turns`; earlier models to `current_turn`.
- **`phase`** on assistant messages (`commentary` for progress updates, `final_answer` for the answer), GPT-5.3-Codex and later in the Responses API. Required for GPT-5.3-Codex, highly recommended for later models when the app replays history itself. Never on user messages.
- **`configuration_update`** input item (supported GPT-6 and later models): changes effort (and `text.format`) mid-conversation without breaking the prompt cache. Limits: standard, single-agent mode only; do not combine with automatic compaction or automatic truncation; `/responses/compact` rejects histories that contain it; after an explicit compaction, send a fresh update. Mention these limits whenever you recommend it.
- **Prompt caching**: `prompt_cache_key`; on GPT-5.6 and GPT-6, `prompt_cache_options` (`mode`, `ttl`) replaces `prompt_cache_retention`. Cache writes cost more than uncached input: 1.25× at 30-minute retention on GPT-5.6 and GPT-6, more with longer retention (GPT-6.1 Terra lists $1.25 per million tokens for 30-minute and $2.50 for 12-hour retention against $1 input). Check the model's catalog page for exact prices.

## 2. Per-model table

| Model | API ID | Effort values | Default effort | Context / max output |
|---|---|---|---|---|
| GPT-6 Astra | `gpt-6-astra` | low, medium, high, xhigh, max (**no `none`**) | not stated in the docs | 1.05M / 128K |
| GPT-6.1 Sol | `gpt-6.1-sol` | low, medium, high, xhigh, max (**no `none` or `minimal`**) | medium | 1.05M / 128K |
| GPT-6.1 Terra | `gpt-6.1-terra` | none, low, medium, high, xhigh, max | medium | 1.05M / 128K |
| GPT-6 Luna | `gpt-6-luna` | none, low, medium, high, xhigh, max | medium | 1.05M / 128K |
| GPT-6 Sol | `gpt-6-sol` | none, low, medium, high, xhigh, max | medium | 1.05M / 128K |
| GPT-5.6 Sol (alias `gpt-5.6`) | `gpt-5.6-sol` | none, low, medium, high, xhigh, max | medium | 1.05M / 128K |
| GPT-5.6 Terra | `gpt-5.6-terra` | none, low, medium, high, xhigh, max | medium | 1.05M / 128K |
| GPT-5.6 Luna | `gpt-5.6-luna` | none, low, medium, high, xhigh, max | medium | the docs disagree: catalog page 1.05M, upgrade guide 400K; 128K output |
| GPT-5.5 | `gpt-5.5` | none, low, medium, high, xhigh | medium | 1.05M / 128K |
| GPT-5.4 | `gpt-5.4` | none, low, medium, high, xhigh | **none** | 1.05M / 128K |
| GPT-5.4 Mini | `gpt-5.4-mini` | none, low, medium, high, xhigh | **none** | 400K / 128K |
| GPT-5.3-Codex | `gpt-5.3-codex` | low, medium, high, xhigh (**no `none`**) | not stated; `medium` recommended | Responses API only |
| GPT-5.2 | `gpt-5.2` | none, low, medium, high, xhigh | **none** | 400K / 128K |
| GPT-5.1 | `gpt-5.1` | none, low, medium, high | **none** | |
| GPT-5 | `gpt-5` | minimal, low, medium, high | medium | |

Endpoint limits:
- GPT-6 Astra and GPT-6.1 Sol: tool calling only in the Responses API, not Chat Completions.
- GPT-6.1 Terra: tool calling requires the Responses API.
- GPT-6 Sol, GPT-6 Luna, and the GPT-5.6 family: in Chat Completions, function tools work only with effort `none`; use the Responses API for reasoning with tools.

## 3. Starting effort by kind of work

From the effort table in "Reasoning models" and the model pages. Always say: start here, then test one level lower on real requests.

| Work | Start |
|---|---|
| Migrating a working setup to a newer model | **the old effective effort** (including its default), then test one level lower |
| Classification, extraction, fast retrieval, voice | `none` where supported (`low` on Astra and 6.1 Sol); try `low` first on GPT-5.5 |
| Chat, support, drafting, tool use that must stay fast | `low` |
| Agentic coding, research, planning, judgment | `medium` |
| Hard debugging, long-horizon agents | `high` (compare with `medium`) |
| Deep research, long asynchronous work | `xhigh` only with a measured gain |
| Hardest quality-first work | `max` (GPT-5.6, GPT-6) only with a measured gain; never as a global default |

Before raising effort, check whether the prompt is missing a success criterion, dependency rule, tool-routing rule, or verification step (GPT-5.6 prompting page, "Reasoning effort").

## 4. Settings that return errors or break things

Report any of these found in the user's code or described setup:

- `temperature`, `top_p`, `logprobs` (and `top_logprobs`) with any effort other than `none`: error on GPT-5.4, GPT-5.2, and GPT-6; must be removed. On GPT-6 in the Responses API, also remove `message.output_text.logprobs` from `include`. On older GPT-5 models (`gpt-5`, `gpt-5-mini`, `gpt-5-nano`) they error at every setting. Use effort, `text.verbosity`, and `max_output_tokens` instead.
- Effort `none` on GPT-6 Astra or GPT-6.1 Sol: HTTP 400; use `low`. Effort `none` on GPT-5.3-Codex: not supported.
- Effort `minimal` on GPT-6 models: start with `low` instead.
- Function tools in Chat Completions on GPT-6 Astra or GPT-6.1 Sol: not supported; on GPT-5.6, GPT-6 Sol, and GPT-6 Luna only with effort `none`.
- Moving from GPT-5.4, Mini, or Nano (default `none`) to GPT-5.6, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, or GPT-6 Sol (default `medium`) with effort omitted, or to GPT-6 Astra (default not stated in the docs): requests silently become slower and more expensive, and Chat Completions function tools stop working. Set the old effort explicitly where the new model supports it; GPT-6 Astra and GPT-6.1 Sol reject `none`, so use `low` there and compare.
- `prompt_cache_retention` on GPT-5.6 and GPT-6: replace with `prompt_cache_options.ttl`.
- A separate "Pro" model name for GPT-5.6: there is none; use `reasoning.mode: "pro"` on the same model.

## 5. Rules that affect how the prompt may change

- **Keep reusable prefixes stable.** Put static instructions first and per-request content last; avoid timestamps, request IDs, or changing tool lists near the top of a large system prompt. GPT-5.6 places its cache breakpoint near the latest message, so a stable prefix followed by a changing suffix can lose cache hits.
- **Do not edit earlier turns.** On newer models, changing history before a reasoning item can make the API drop that reasoning. Change effort with `configuration_update` (GPT-6, with the limits in section 1), not by changing the request-level value.
- **Preserve `phase` values** when the app replays assistant messages itself; dropped `phase` can make progress updates count as final answers.
- **JSON shapes described in prose**: recommend Structured Outputs (`text.format` with a JSON schema) instead, at least for GPT-5.5 and later. Keep a short description of fields only where the schema cannot express a rule.
- **`instructions` parameter**: applies only to the current request; with `previous_response_id`, send it again on every call.
