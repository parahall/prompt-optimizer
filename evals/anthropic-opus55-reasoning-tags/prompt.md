---
description: Requests to write reasoning in tags must be removed for Claude Opus 5.5 (reasoning_extraction refusals).
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Improve this prompt for claude-opus-5-5. It is the system prompt of an internal tool that classifies support tickets.

You classify customer support tickets into one of: billing, bug, feature_request, other.
First, think step by step and write your full reasoning inside <thinking> tags.
Then output the label inside <label> tags.
