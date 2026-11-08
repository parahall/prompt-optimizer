---
description: An agent on GPT-6 Astra that keeps stopping for approval should get the initiative and follow-through guidance.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Our internal ops agent runs on gpt-6-astra with file, shell, and ticketing tools. Engineers complain it keeps stopping to ask "Should I proceed?" even for simple fixes they asked for. Optimize its system prompt for that model:

You are OpsBot. You help engineers fix issues in our infrastructure repos.
Be careful. Before doing anything, explain your plan and ask the engineer to confirm.
Always warn about possible risks before every change.
