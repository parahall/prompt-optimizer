---
type: llm
---
Look at the rewritten prompt in the reply.
PASS if the rewritten prompt no longer mentions Claude-specific settings ("adaptive thinking", Claude effort levels) and no longer asks for reasoning inside <thinking> tags, and the reply explains that such settings belong in the API request (for GPT, reasoning.effort) rather than in the prompt.
FAIL if the rewritten prompt still mentions adaptive thinking or asks for reasoning inside <thinking> tags.
