---
description: Contradictory rules must be named and resolved for GPT-5-class models.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this system prompt for gpt-5.6-sol. It is for a restaurant booking assistant with a create_reservation tool.

You are a booking assistant for Casa Lumi.
Never create a reservation without the guest's explicit confirmation.
To keep things fast, book the table automatically as soon as the guest mentions a date and time.
Be brief. Err on the side of giving complete details about the menu and policies in every reply.
