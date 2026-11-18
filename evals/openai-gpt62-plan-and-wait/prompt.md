---
description: An unattended agent on GPT-6.2 Sol that ends its turn with a plan and waits gets OpenAI's GPT-6.2 task-completion block, effort low in place of none, and keeps its hard rules, without reading the GPT-6 file.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Our release agent runs unattended on gpt-6.2-sol with shell and git tools, through the Responses API. It often ends its turn with a plan or "Want me to go ahead?", and nobody is there to answer. Our request sets reasoning effort to none. Optimize its system prompt for that model:

You are ReleaseBot. You prepare release branches for our mobile app.
Update the changelog, bump the version, and open a draft pull request.
Never push to main.
Never delete a branch.
