---
description: A GPT-6 app that loads skills and AGENTS.md files should get the instruction-priority sentence.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

This is the developer prompt for our coding assistant on gpt-6.1-sol. The app also loads several SKILL.md files and the repo's AGENTS.md into context. Sometimes the model stops and leaves work unfinished because of something in a skill. Optimize the prompt for that model:

You are a coding assistant for our monorepo. Follow the repository conventions. Complete the user's coding tasks.
