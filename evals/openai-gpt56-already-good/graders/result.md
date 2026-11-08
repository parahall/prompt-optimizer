---
type: llm
---
The original prompt was:
"Role: You triage incoming bug reports for a mobile app. / Goal: Assign each report one label and a short reason so the right team picks it up. / Success criteria: exactly one label from: crash, ui, performance, account, other; the reason is one sentence and quotes the part of the report that decided the label; if the report is unreadable or empty, use "other" and say why. / Output: JSON with fields label and reason."

Compare the rewritten prompt in the reply with this original.
PASS if the rewritten prompt differs from the original only by small edits: at most about two lines changed or added, and no new sections (such as personality, tools, autonomy, progress updates, or verification).
FAIL if the rewritten prompt adds new sections or several new lines, or is heavily restructured.
