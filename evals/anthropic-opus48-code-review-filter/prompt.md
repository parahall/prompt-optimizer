---
description: Severity filters in a code-review prompt reduce recall on Claude Opus 4.8; replace with report-everything language.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Please optimize our automated code review prompt for claude-opus-4-8.

You are a code reviewer. Review the diff below.
Be conservative. Only report high-severity issues. Don't nitpick.
For each issue, give the file, line, and a one-sentence description.
