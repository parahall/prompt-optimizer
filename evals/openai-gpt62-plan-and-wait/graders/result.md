---
type: llm
---
Look only at the rewritten prompt inside the reply.
PASS if it tells the agent to keep working instead of ending its turn with a plan or a question for routine decisions, and it still keeps the ReleaseBot role, the three tasks (update the changelog, bump the version, open a draft pull request), the rule never to push to main, and the rule never to delete a branch.
FAIL if any of those requirements is dropped or weakened, or if there is no instruction to keep working.
