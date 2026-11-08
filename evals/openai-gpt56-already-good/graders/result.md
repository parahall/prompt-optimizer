---
type: llm
---
The original prompt was:
"Role: You triage incoming bug reports for a mobile app. / Goal: Assign each report one label and a short reason so the right team picks it up. / Success criteria: exactly one label from: crash, ui, performance, account, other; the reason is one sentence and quotes the part of the report that decided the label; if the report is unreadable or empty, use "other" and say why. / Output: JSON with fields label and reason."

Compare the rewritten prompt in the reply (the prompt text itself, not the explanation around it) with this original.
PASS if both hold:
1. Small edits only: at most about two lines changed or added, and no new sections (such as personality, tools, autonomy, progress updates, or verification).
2. Every original requirement is still in the rewritten prompt: exactly one label from the five listed; a one-sentence reason that quotes the deciding part of the report (an explicit exception for empty or unreadable reports is fine); "other" plus an explanation for unreadable or empty reports; and output with the fields label and reason (or, if the reply moves the JSON shape into Structured Outputs, the fields are named in its settings section).
FAIL if the rewritten prompt adds new sections or several new lines, is heavily restructured, or is missing any original requirement listed above.
