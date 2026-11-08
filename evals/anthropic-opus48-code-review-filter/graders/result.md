---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if the rewritten prompt no longer contains "be conservative" or "only report high-severity issues", and instead does either of these: (a) tells the model to report every issue, including uncertain or low-severity ones, or (b) gives a concrete threshold such as "report any bug that could cause incorrect behavior, a test failure, or a misleading result; omit only style or naming nits". Either (a) or (b) is enough.
FAIL if the rewritten prompt still says "be conservative" or "only report high-severity issues", or has no replacement rule at all.
