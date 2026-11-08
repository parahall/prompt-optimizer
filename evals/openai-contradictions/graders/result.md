---
type: llm
---
PASS if the reply names the conflict between "never create a reservation without explicit confirmation" and "book automatically", and the conflict between "be brief" and "give complete details in every reply", and the rewritten prompt resolves both. The booking resolution must keep the guest's explicit confirmation before a reservation is created (for example: collect date and time, then confirm, then book), or the reply must ask the user which booking policy they want instead of deciding it silently. The length resolution must be one clear rule.
FAIL if the rewritten prompt still contains both conflicting booking rules or both conflicting length rules, if it resolves the booking conflict by dropping the confirmation requirement without asking the user, or if the reply does not mention the contradictions.
