---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if the rewritten prompt contains a <medical_guidance> block about children's medicine doses, and still keeps the CareCorner pharmacy identity, the three tasks (finding products, store opening hours, prescription refills), and the web_search tool.
FAIL if there is no medicine-dosing block, or if any of those requirements is dropped.
