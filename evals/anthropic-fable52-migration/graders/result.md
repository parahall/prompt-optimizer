---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if all of these hold: the line "Answer directly without deliberating." is gone; the prompt contains a "Finishing work" section that tells the agent not to stop while work is still owed; and it still keeps the Northwind Logistics data-migration role, the instruction to migrate the tables in migration-plan.md, the rule never to touch tables marked "frozen", and the rule to ask before dropping any table.
FAIL if the think-less line remains, if there is no finishing-work instruction, or if any of the four requirements is dropped or weakened.
