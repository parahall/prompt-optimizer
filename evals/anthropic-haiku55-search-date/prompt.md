---
description: A Haiku 5.5 bot with a search tool should get the current date, and a search nudge when the prompt is long.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

This is the system prompt for our travel-visa help bot. It runs on claude-haiku-5-5 and has a web_search tool. Optimize it for that model.

You are VisaHelper. You answer questions about visa rules, fees, and processing times for travelers.
Be accurate and friendly. Use the web_search tool when needed.
