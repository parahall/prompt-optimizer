---
type: llm
---
Find the effort recommendation in the reply (usually under "Recommended API settings").
PASS if the reply says that reasoning effort `none` is rejected or not supported on GPT-6.2 Sol and recommends `low` or a higher level instead.
FAIL if it keeps `none`, or does not mention that `none` must change.
