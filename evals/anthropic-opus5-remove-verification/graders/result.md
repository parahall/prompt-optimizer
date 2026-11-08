---
type: llm
---
Look only at the rewritten prompt in the reply (not the explanation of changes).
PASS if the rewritten prompt no longer tells the model to double-check, re-verify, or add a final verification step, AND the reply explains that Claude Opus 5 already verifies its own work (or that such instructions cause over-verification).
FAIL if the rewritten prompt still contains a double-check or verification instruction, or if no rewritten prompt is given.
