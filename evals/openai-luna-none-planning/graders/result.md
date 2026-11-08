---
type: llm
---
PASS if the rewritten prompt keeps (or strengthens) the instruction to plan which tools to call before calling them, and the reply does not remove it on the grounds that the model reasons internally.
FAIL if the rewritten prompt removes the planning instruction.
