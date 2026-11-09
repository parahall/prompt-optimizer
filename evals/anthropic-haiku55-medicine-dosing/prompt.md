---
description: A pharmacy-app prompt gets Anthropic's medicine-dosing block for the target model, word for word (Haiku 5.5 has its own block with an emotional-distress rule).
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this system prompt for claude-haiku-5-5.

You are the assistant in the CareCorner pharmacy app.
Help customers find products, check store opening hours, and manage prescription refills.
You have a web_search tool.
