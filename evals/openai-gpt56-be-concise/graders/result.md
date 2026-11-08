---
type: llm
---
PASS if the reply removes or softens the broad brevity rules ("Be concise", "Keep it short", "as few words as possible"), recommends setting the text.verbosity parameter, and the rewritten prompt says what an answer must keep (for example the next step or required facts).
FAIL if the rewritten prompt keeps "Use as few words as possible", or the reply never mentions text.verbosity.
