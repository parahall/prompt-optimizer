---
type: llm
---
PASS if all of these hold:
- The reply names the conflict between "never create a reservation without explicit confirmation" and "book automatically".
- The reply names the conflict between "be brief" and "give complete details in every reply".
- The length conflict is resolved in the rewritten prompt with one clear length rule.
- The booking conflict is handled in one of these two acceptable ways: (a) the rewritten prompt keeps the guest's explicit confirmation before a reservation is created and drops automatic booking; or (b) the reply asks the user which booking rule should win (keeping both in the prompt until they answer is fine in this case).
FAIL if the reply does not mention the contradictions, if the length conflict is left unresolved, or if the booking conflict is resolved by dropping the confirmation requirement without asking the user.
