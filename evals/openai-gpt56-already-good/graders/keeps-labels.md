---
type: regex
target: last_message
pattern: "\\blabels?\\b(?=[\\s\\S]{0,200}\\bcrash\\b)(?=[\\s\\S]{0,200}\\bui\\b)(?=[\\s\\S]{0,200}\\bperformance\\b)(?=[\\s\\S]{0,200}\\baccount\\b)(?=[\\s\\S]{0,200}\\bother\\b)"
flags: i
---
