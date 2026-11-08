---
type: llm
---
PASS if the rewritten prompt tells the model that it is working autonomously and the user is not watching, that it should proceed with reversible steps that follow from the request instead of asking permission, and that it should stop only for destructive actions or input only the user can give. Replacing "Ask the user if anything is unclear" with "state assumptions and continue" also counts.
FAIL if the rewritten prompt still tells the model to ask the user whenever anything is unclear, or adds nothing about finishing the task without stopping.
