# Where to find OpenAI's tested blocks

Checked against the docs on 2026-11-08.

OpenAI publishes its sample blocks per model family, so the quoted blocks live in the model files, each marked "Quoted from OpenAI" with its page and section. Insert a block word for word, and only when its symptom matches.

If the target family has no block for a symptom but another current family does, you may use the other family's block. Then say in the report that it was written for that other family and is untested on the target.

| Symptom | Block | File |
|---|---|---|
| Model stops to ask or get approval where it should continue | Initiative and follow-through blocks | `models/gpt-6.md` |
| Approval rules repeated, or agent acts beyond the request | Autonomy and approval policy | `models/gpt-5-6.md` |
| Unclear when to proceed or ask; instruction priority | `<default_follow_through_policy>`, `<instruction_priority>` | `models/gpt-5-4.md` |
| App loads skills or AGENTS.md; model pauses | Skill priority sentence | `models/gpt-6.md` |
| Prompt scripts steps instead of a goal | "Resolve the customer's issue end to end" | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Tool loops too long or too short | Stopping conditions | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Lookups skipped before actions | Prerequisite rule / `<dependency_checks>` | `models/gpt-5-6.md`, `models/gpt-5-4.md` |
| Grounded answers search too much | Retrieval budget | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Drafts invent facts | Creative drafting guardrails | `models/gpt-5-5.md` |
| Edits expand instead of polish | "Preserve the requested artifact…" | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Replies too short after migrating | What a short answer must keep | `models/gpt-5-6.md` |
| Too many lists and tables | Paragraph rule | `models/gpt-6.md` |
| Nested bullets | Flat-list rule | `models/gpt-5-4.md` |
| Stock phrases, jargon | Writing-style blocks | `models/gpt-6.md` |
| Customer-facing voice | Personality block | `models/gpt-5-5.md`, `<personality_and_writing_controls>` in `models/gpt-5-4.md` |
| Silent long tasks or over-narration | Preamble and update rules | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Work finished without validation | Validation blocks | `models/gpt-5-6.md`, `models/gpt-5-5.md` |
| Small-change coding gets broad tests | Testing calibration | `models/gpt-6.md` |
| Long tasks miss items | `<completeness_contract>` | `models/gpt-5-4.md` |
| Too little subagent delegation | Delegation sentence | `models/gpt-6.md` |
