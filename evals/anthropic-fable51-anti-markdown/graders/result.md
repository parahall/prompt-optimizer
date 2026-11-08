---
type: llm
---
PASS if the reply removes the long anti-formatting block or replaces it with a shorter rule that allows lists when the content needs them (for example lists for recipe ingredients or steps), AND explains that Claude Fable 5.1 already uses little formatting, so the block can suppress structure the content needs.
FAIL if the rewritten prompt keeps the full ban on lists, bold, and headers, or gives no model-specific reason.
