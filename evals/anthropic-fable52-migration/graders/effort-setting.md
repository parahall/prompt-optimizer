---
type: llm
---
Find the effort recommendation in the reply (usually under "Recommended API settings"). The agent in question is a long-running data-migration agent.
PASS if the reply recommends running the migration agent at `medium` or a higher effort level (for example `high`). Suggesting a lower level only for short, easy turns is fine.
FAIL if the reply recommends `low` effort for the migration work itself, gives no effort level at all, or tells the user to keep or add prompt wording that makes the model think less.
