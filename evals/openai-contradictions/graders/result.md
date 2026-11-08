---
type: llm
---
PASS if all of these hold:
- The reply names the conflict between "never create a reservation without explicit confirmation" and "book automatically".
- The reply asks the user which of these two booking rules should win (it may recommend one). Keeping both rules in the prompt until the user answers is correct.
- The reply names the conflict between "be brief" and "give complete details in every reply", and the rewritten prompt resolves it with one clear length rule.
FAIL if the reply does not mention the contradictions, if it settles the booking conflict on its own (dropping either booking rule) without asking the user which should win, or if the length conflict is left unresolved.
