---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if all of these hold: it tells the agent to give the user short updates while it works; it no longer tells the agent to stay silent (no "do not narrate" or "hold all findings for the final response" instruction remains next to the update instruction); and it still keeps the Meridian Analytics research-agent role, the search and read_file tools, and the rule to cite every source.
FAIL if the prompt contains both an instruction to stay silent and an instruction to give updates, if it has no update instruction, or if the role, the tools, or the citation rule is dropped.
