---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if the rewritten prompt no longer contains "CRITICAL", "MUST ALWAYS", "NO EXCEPTIONS", or other all-capital emphasis, states the tool rule in calm wording, and still keeps the user's requirement to use the case_law_search tool for every message (the requirement may be restated, not removed or narrowed). Suggesting in the explanation that the user might narrow the rule is fine.
FAIL if the rewritten prompt still contains all-capital emphasis, or if it narrows the rule so the tool is used only in some cases.
