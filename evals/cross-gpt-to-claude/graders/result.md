---
type: llm
---
PASS if the reply removes or replaces the GPT-specific settings wording in the prompt (reasoning_effort, text.verbosity), recommends Claude's own settings instead (for example the effort parameter or adaptive thinking), and does not keep "think step by step" as a written-out reasoning instruction.
FAIL if the rewritten prompt still tells the model to set reasoning_effort or text.verbosity, or the reply recommends OpenAI settings for Claude.
