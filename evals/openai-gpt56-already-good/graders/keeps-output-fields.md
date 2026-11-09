---
type: regex
target: last_message
pattern: "JSON[\\s\\S]{0,80}?(\\blabel\\b[\\s\\S]{0,40}\\breason\\b|\\breason\\b[\\s\\S]{0,40}\\blabel\\b)"
flags: i
---
