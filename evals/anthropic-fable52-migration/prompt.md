---
description: Moving a Fable 5.1 agent prompt to Fable 5.2 removes the "think less" line, keeps effort at medium or higher for the agentic work (lower only for easy turns), adds the Finishing work text for early stops, and keeps the hard requirements.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We're moving this system prompt from claude-fable-5-1 to claude-fable-5-2. We run it at medium effort. On Fable 5.2 the agent often ends its turn with a list of what's left or "want me to continue?" instead of finishing the migration.

You are a data-migration agent for Northwind Logistics.
Answer directly without deliberating.
Migrate the tables listed in migration-plan.md from the legacy database to the new warehouse.
Never touch tables marked "frozen" in the plan.
Ask before dropping any table.
