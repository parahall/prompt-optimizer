---
type: llm
---
Look at the recommended API settings in the reply. The user runs this migration agent at medium effort, and on Claude Fable 5.2 it stops early; Anthropic's page says early stops are more common at low and medium effort.
PASS if the reply recommends an explicit effort level that does not make early stops more likely for the agentic work (for example keeping medium, or raising to high), treats effort rather than prompt wording as the way to control thinking, and lowers effort, if at all, only for easy turns.
FAIL if it gives no effort recommendation, lowers effort for the whole agentic workload (for example to low), or tells the user to keep or add prompt wording to make the model think less.
