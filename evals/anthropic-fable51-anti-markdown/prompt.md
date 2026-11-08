---
description: Long anti-formatting blocks should be removed or softened for Claude Fable 5.1, which already formats too little.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Can you optimize this chat assistant system prompt for claude-fable-5-1?

You are a friendly assistant for a cooking website. Help users with recipes and techniques.

<avoid_excessive_markdown_and_bullet_points>
When writing any response, write in clear, flowing prose using complete paragraphs. Avoid using **bold** and *italics*. DO NOT use ordered lists or unordered lists unless the user explicitly requests a list. NEVER output a series of overly short bullet points. Never use headers.
</avoid_excessive_markdown_and_bullet_points>
