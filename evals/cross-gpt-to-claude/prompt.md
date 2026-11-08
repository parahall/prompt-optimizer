---
description: A GPT-tuned prompt moving to Claude Opus 5.5 should lose GPT-specific habits.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We're moving this agent prompt from gpt-5.2 to claude-opus-5-5. Optimize it for the new model:

<solution_persistence>
- Persist until the task is fully handled end-to-end.
</solution_persistence>
Set reasoning_effort to none for speed and think step by step before each tool call.
Use text.verbosity low.
You are a coding agent for our backend services.
