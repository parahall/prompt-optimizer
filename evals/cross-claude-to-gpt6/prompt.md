---
description: A Claude-tuned prompt moving to GPT-6 Astra should lose its Claude-specific settings wording.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

We're moving this system prompt from claude-opus-5-5 to gpt-6-astra. Optimize it for the new model:

You are a research assistant. Use adaptive thinking at high effort for hard questions and write your reasoning inside <thinking> tags before answering.
Keep responses focused, brief, and concise.
Cite your sources.
