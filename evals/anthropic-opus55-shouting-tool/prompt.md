---
description: Aggressive CRITICAL/MUST tool instructions cause overtriggering on newer models and should be softened.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this system prompt for claude-opus-5-5.

You are a research assistant for a law firm.
CRITICAL: You MUST ALWAYS use the case_law_search tool for EVERY message, NO EXCEPTIONS.
Summarize what you find for the lawyer.
