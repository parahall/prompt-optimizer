---
description: An unattended agent on Fable 5.1 should get guidance to finish the whole task instead of stopping to ask.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

This agent runs overnight with nobody watching. It uses claude-fable-5-1 with file and shell tools. Users complain they wake up to "Shall I continue?" messages and half-done work. Optimize the system prompt:

You are a migration agent. Migrate the repository's tests from Jest to Vitest.
Work carefully. Ask the user if anything is unclear.
