---
description: A prompt that is already good should get very few changes and no snippets added just because they exist.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Optimize this prompt for claude-sonnet-5. It is a one-off extraction prompt sent through the API with structured outputs.

You extract invoice data for an accounting system. The invoices below come from many suppliers and formats.

<invoices>
{{INVOICES}}
</invoices>

For each invoice, extract the supplier name, invoice number, issue date (ISO 8601), currency, and total amount. If a field is missing, use null rather than guessing, because the accounting team reviews nulls by hand and a wrong guess goes unnoticed. Apply these rules to every invoice, not just the first one.
