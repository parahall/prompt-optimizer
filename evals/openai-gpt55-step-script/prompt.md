---
description: GPT-5.5 prefers outcome-first prompts; a step-by-step script should become an outcome with success criteria and stop rules.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this agent prompt for gpt-5.5. It handles refund requests with tools for order lookup, refund policy lookup, and issuing refunds.

First look up the order. Then look up the refund policy. Then compare every field of the order with every rule in the policy. Then think through all possible exceptions. Then decide which tool to call. Then call the tool. Then explain the entire process to the customer step by step.
