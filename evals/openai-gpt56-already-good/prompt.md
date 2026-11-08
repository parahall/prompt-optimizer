---
description: A good outcome-first prompt for GPT-5.6 should get very few changes.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this developer prompt for gpt-5.6-terra:

Role: You triage incoming bug reports for a mobile app.

Goal: Assign each report one label and a short reason so the right team picks it up.

Success criteria:
- exactly one label from: crash, ui, performance, account, other
- the reason is one sentence and quotes the part of the report that decided the label
- if the report is unreadable or empty, use "other" and say why

Output: JSON with fields label and reason.
