---
description: Verification and double-check instructions must be removed for Claude Opus 5, which already checks its own work.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We are moving this system prompt to claude-opus-5. Please optimize it for that model.

You are a senior data analyst. Answer questions about the sales data the user provides.
Before every answer, double-check your numbers.
For any non-trivial task, include a final verification step and re-verify before responding.
Give your answer as a short report.
