---
description: At reasoning effort none, prompting a plan before tool calls helps; the skill must not remove it.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this agent prompt for gpt-6-luna. It runs with reasoning effort "none" for speed, and has tools for searching a product catalog and checking stock.

You are a shopping assistant. Before calling any tool, briefly plan which tools you need and in what order. Then answer the customer.
