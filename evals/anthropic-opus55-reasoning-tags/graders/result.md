---
type: llm
---
Look at the rewritten prompt in the reply.
PASS if the rewritten prompt no longer asks the model to write its reasoning in the response (no <thinking> section, no "write your reasoning"), AND the reply says why: asking for written reasoning can trigger a refusal (reasoning_extraction) on this model, or the reasoning should come from the API's thinking blocks instead.
FAIL if the rewritten prompt still asks for written-out reasoning, or the reply gives no reason for removing it.
