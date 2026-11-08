---
type: llm
---
Look at the rewritten prompt in the reply.
PASS if the rewritten prompt no longer tells the model to think step by step or explain its reasoning before answering, and the reply explains that the model already reasons internally at this effort level (or that reasoning depth is controlled with the reasoning effort setting). Asking for a short justification of the recommendation is fine.
FAIL if the rewritten prompt still says "think step by step" or asks for detailed reasoning before the answer.
