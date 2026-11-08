---
type: regex
target: { source: file, path: prompts/support-bot.optimized.md }
pattern: "<(thinking|reasoning|scratchpad)>"
flags: i
match: not_contains
---
