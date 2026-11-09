---
type: llm
focus: { source: file, path: prompts/support-bot.optimized.md }
---
This file is a rewritten system prompt. The original was:
"You are a support assistant for the Tidewater Transit app. CRITICAL: You MUST ALWAYS use the search_help_center tool before answering. Think step by step inside <thinking> tags before every answer. Double-check your answer before responding. NEVER use markdown."
PASS if the rewritten prompt is a usable system prompt that still says it is a support assistant for the Tidewater Transit app, still requires using the search_help_center tool before every answer (calmer wording is fine; narrowing it to some questions is not), and still forbids Markdown formatting. It must not ask for reasoning written in tags or for a double-check step.
FAIL if any of these requirements is missing, narrowed, or contradicted, or if the file is not a usable prompt (for example only keywords).
