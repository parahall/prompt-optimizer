---
description: A Fable 5.2 agent that looks silent to users who watch it live gets the client display setting first, then Anthropic's update line for harnesses that cannot send reminders, without leaving a rule that suppresses updates next to it.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this system prompt for claude-fable-5-2. Analysts watch the agent work live in our app and complain that it goes silent for long stretches. We can't change the harness, and our platform has no mid-conversation system messages.

You are a research agent for Meridian Analytics.
Use the search and read_file tools to answer the analyst's question.
Do not narrate. Hold all findings for the final response.
Cite every source you use.
