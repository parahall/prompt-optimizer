---
type: llm
---
PASS if the rewritten prompt gives the model the current date (for example a line like "The current date is {{current_date}}" or a placeholder the app fills in), AND either tells the model to search for facts that may have changed since its training (rules, fees, prices) or explains why the date helps it search.
FAIL if the rewritten prompt has no current-date line.
