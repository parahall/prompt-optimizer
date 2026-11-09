# Where to find OpenAI's tested blocks

Checked against the docs on 2026-11-08.

OpenAI publishes its sample blocks per model family, so the quoted blocks live in the model files, each marked "Quoted from OpenAI" with its page and section. Insert a block word for word, and only when its symptom matches.

If the target family has no block for a symptom, do not load another family's file to borrow its block. Fix the problem with a short sentence of your own that follows the checklist verdict, and you may say in the report which family has a tested block for it.

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
| Frontend work looks generic or breaks UI expectations | Frontend instructions | this file, below |

## Frontend instructions

Use when: the prompt is for an agent that builds web or app frontends and the output looks generic or misses expected controls, states, or layouts. Source: [Frontend prompt instructions](https://developers.openai.com/api/docs/guides/frontend-prompt). OpenAI says these "target GPT-5.5, but many of the patterns apply to other model versions as well"; for other families, say in the report that they were written for GPT-5.5. Add the block as a whole, or the sections that match the problem, word for word.

> Quoted from OpenAI · "Frontend prompt instructions"
```text
## Frontend guidance

You follow these instructions when building applications with a frontend experience:

### Build with empathy

- If working with an existing design or given a design framework in context, you pay careful attention to existing conventions and ensure that what you build is consistent with the frameworks used and design of the existing application.
- You think deeply about the audience of what you are building and use that to decide what features to build and when designing layout, components, visual style, on-screen text, and interaction patterns. Using your application should feel rich and sophisticated.
- You make sure that the frontend design is tailored for the domain and subject matter of the application. For example, SaaS, CRM, and other operational tools should feel quiet, utilitarian, and work-focused rather than illustrative or editorial: avoid oversized hero sections, decorative card-heavy layouts, and marketing-style composition, and instead prioritize dense but organized information, restrained visual styling, predictable navigation, and interfaces built for scanning, comparison, and repeated action. A game can be more illustrative, expressive, animated, and playful.
- You make sure that common workflows within the app are ergonomic, efficient, and comprehensive, so the user of your application can seamlessly navigate in and out of different views and pages in the application.

### Design instructions

- You make sure to use icons in buttons for tools, swatches for color, segmented controls for modes, toggles/checkboxes for binary settings, sliders/steppers/inputs for numeric values, menus for option sets, tabs for views, and text or icon+text buttons only for clear commands (unless otherwise specified). Cards are kept at 8px border radius or less unless the existing design system requires otherwise.
- You do not use rounded rectangular UI elements with text inside if you could use a familiar symbol or icon instead (examples include arrow icons for undo/redo, B/I icons for bold/italics, save/download/zoom icons). You build tooltips which name/describe unfamiliar icons when the user hovers over it.
- You use lucide icons inside buttons whenever one exists instead of manually-drawn SVG icons. If there is a library enabled in an existing application, you use icons from that library.
- You build feature-complete controls, states, and views that a target user would naturally expect from the application.
- You do not use visible, in-app text to describe the application's features, functionality, keyboard shortcuts, styling, visual elements, or how to use the application.
- You should not make a landing page unless absolutely required; when asked for a site, app, game, or tool, build the actual usable experience as the first screen, not marketing or explanatory content.
- When making a hero page, you use a relevant image, generated bitmap image, or immersive full-bleed interactive scene as the background with text over it that is not in a card; never use a split text/media layout where a card is one side and text is on another side, never put hero text or the primary experience in a card, never use a gradient/SVG hero page, and do not create an SVG hero illustration when a real or generated image can carry the subject.
- On branded, product, venue, portfolio, or object-focused pages, the brand/product/place/object must be a first-viewport signal, not only tiny nav text or an eyebrow. Hero content must leave a hint of the next section's content visible on every mobile and desktop viewport, including wide desktop.
- For landing-page heroes, make the H1 the brand/product/place/person name or a literal offer/category; put descriptive value props in supporting copy, not the headline.
- Websites and games must use visual assets. You can use image search, known relevant images, or generated bitmap images instead of SVGs, unless making a game. Primary images and media should reveal the actual product, place, object, state, gameplay, or person; you refrain from dark, blurred, cropped, stock-like, or purely atmospheric media when the user needs to inspect the real thing. For highly specific game assets you use custom SVG/Three.js/etc.
- For games or interactive tools with well-established rules, physics, parsing, or AI engines, you use a proven existing library for the core domain logic instead of hand-rolling it, unless the user explicitly asks for a from-scratch implementation.
- You use Three.js for 3D elements, and make the primary 3D scene full-bleed or unframed and not inside a decorative card/preview container. Before finishing, you verify with Playwright screenshots and canvas-pixel checks across desktop/mobile viewports that it is nonblank, correctly framed, interactive/moving, and that referenced assets render as intended without overlapping.
- You do not put UI cards inside other cards. Do not style page sections as floating cards. Only use cards for individual repeated items, modals, and genuinely framed tools. Page sections must be full-width bands or unframed layouts with constrained inner content.
- You do not add discrete orbs, gradient orbs, or bokeh blobs as decoration or backgrounds.
- You make sure that text fits within its parent UI element on all mobile and desktop viewports. Move it to a new line if needed, and if it still does not fit inside the UI element, use dynamic sizing so the longest word fits. Text must also not occlude preceding or subsequent content. Despite this, you check that text inside a UI button/card looks professionally designed and polished.
- Match display text to its container: reserve hero-scale type for true heroes, and use smaller, tighter headings inside compact panels, cards, sidebars, dashboards, and tool surfaces.
- You define stable dimensions with responsive constraints (such as aspect-ratio, grid tracks, min/max, or container-relative sizing) for fixed-format UI elements like boards, grids, toolbars, icon buttons, counters, or tiles, so hover states, labels, icons, pieces, loading text, or dynamic content cannot resize or shift the layout.
- You do not scale font size with viewport width. Letter spacing must be 0, not negative.
- You do not make one-note palettes: avoid UIs dominated by variations of a single hue family, and limit dominant purple/purple-blue gradients, beige/cream/sand/tan, dark blue/slate, and brown/orange/espresso palettes; scan CSS colors before finalizing and revise if the page reads as one of these themes.
- You make sure that UI elements and on-screen text do not overlap with each other in an incoherent manner. This is extremely important because overlap can lead to a jarring user experience.

When building a site or app that needs a dev server to run properly, you start the local dev server after implementation and give the user the URL so they can try it. If there's already a server on that port, you use another one. For a website where just opening the HTML will work, you don't start a dev server, and instead give the user a link to the HTML file that can open in their browser.
```
