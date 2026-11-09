---
type: regex
target: last_message
pattern: "\\bJSON\\b[\\s\\S]{0,200}?(\\blabel\\b[\\s\\S]{0,200}\\breason\\b|\\breason\\b[\\s\\S]{0,200}\\blabel\\b)|(\\blabel\\b[\\s\\S]{0,200}\\breason\\b|\\breason\\b[\\s\\S]{0,200}\\blabel\\b)[\\s\\S]{0,200}?\\bJSON\\b"
flags: i
---
