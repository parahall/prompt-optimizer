---
description: "Settings that fail on GPT-6 Astra must be flagged: effort none, and temperature with reasoning."
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

We're moving this integration to gpt-6-astra. Our request currently sends reasoning effort "none" and temperature 0.2 through Chat Completions with function tools. Optimize the system prompt and tell us what to change in the settings:

You are a data assistant. Answer questions about our sales database using the run_sql tool.
