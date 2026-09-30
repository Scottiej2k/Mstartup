# The Marriage Startup

A first-person novel about a late-20s founder in Silicon Valley, the woman who
reshapes his life, and the uncomfortable, useful overlap between building a
company and building a marriage.

**Author:** Scott (creative director, final say on everything)
**Co-writer:** Claude (drafts, proposes, pushes back, asks questions)

## How we work

1. **Scott's direction wins.** Everything in this repo marked `PROPOSED` is a
   suggestion until Scott marks it `APPROVED`.
2. **Bible first, prose second.** We lock characters, world, themes and the
   stage map before drafting chapters.
3. **Everything lives here.** Decisions get recorded in `decisions.md` so we
   never re-litigate them.
4. **Status tags** used across files: `PROPOSED`, `APPROVED`, `REVISE`, `CUT`.

## Repo map

| Path | What it holds |
|---|---|
| `00-premise.md` | Logline, structure, the chapter-ending device, sequel hook |
| `themes.md` | Core themes and the startup-to-marriage principles |
| `characters/` | Narrator, Maya, Uncle, supporting cast |
| `characters/voice/` | Voice guides and sample dialogue |
| `characters/backstories/` | Full backstories, family and inner circle, timeline |
| `world/` | Setting, era, locations |
| `startup/company.md` | The company: options, stages, key events |
| `startup/product.md` | The product bible: the check-in, the five rules, signals, the ladder, the opt-in, the pharmacy pitch |
| `outline/stage-map.md` | The five-stage arc (search, courting, going serious, breakthrough, grind): company and marriage side by side, with chapter list |
| `outline/beat-sheets.md` | Beat sheets for all 24 chapters, calendar, the transfer ledger, trackers |
| `style-guide.md` | Voice, tone, rules for the narrator and the reflections |
| `open-questions.md` | What we need Scott to decide |
| `decisions.md` | Running log of locked decisions |
| `reader/` | Built reading page (published as an Artifact). Rebuild with `python3 tools/build_reader.py` after any chapter change, then republish |
| `tools/` | `build_reader.py` and its template |
| `process/` | Working procedures: `edit-queue.md` (how Claude processes reader edit requests), `publish-update.md` (how chapter changes reach the reader and its Update button) |
| `chapters/` | Drafted chapters (Ch 1 approved; Ch 2-6 drafted, awaiting review) |

## Review agents

| Agent | Where | What it does |
|---|---|---|
| `reference-checker` | `.claude/agents/reference-checker.md` | Reads the chapters as a first-time reader and flags references, callbacks, running jokes and jargon that the text never established. Read-only; run it after every chapter draft or revision. |

## Reading and commenting

The manuscript is published as an Artifact: https://claude.ai/artifact/1ro4H4yHP486qFYgePcT2Z
The **Update** button (top right) pulls the latest text without a reload. Select any passage and tap **Comment** to tell Claude what to change or ask a question. It joins the Queue tab in the sidebar (Submitted, Working, Completed, then you press Resolve). To change the wording yourself, turn on **Edit text** at the top right and type straight into the paragraph. See `process/edit-queue.md`. After
editing any chapter, run `python3 tools/build_reader.py` and republish `reader/the-marriage-startup.html`.

## Status

Phase 1: Story bible. Major decisions are locked in `decisions.md` (20 as of
2026-09-29), including the core cast names and the company name, Loopback.health.
Supporting-cast names remain placeholders.
