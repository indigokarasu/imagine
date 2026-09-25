---
name: ocas-imagine
license: MIT
description: 'Art-direction engine for text-to-image generation. Separates Style from Content to keep aesthetic identity consistent across an image series. Use when generating, rendering, or illustrating images (especially across a series), capturing the style of a reference image for reuse, or producing an image in a named/saved style. Not for captioning, image analysis for decisions (use ocas-look), or photo editing.'
source: https://github.com/<agent-handle>/imagine
includes:
- references/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "1.1.1"
  hermes:
    category: creative
    tags:
    - image-generation
    - art-direction
    - text-to-image
    - creative
triggers:
- generate image
- text to image
- ai art
- image generation
- illustrate
---

# Imagine

An art-direction engine that treats image generation as a two-part process: **Style Prompting** + **Content Prompting**. Decoupling aesthetic DNA from subject matter lets a series of images share one visual identity while content varies.

## Interactive Menu

When invoked interactively, present the two-level menu (uses the `clarify` tool). Full structure: `references/interactive-menu.md`.

## When to Use

- Create a series of images with a consistent visual identity (comics, storyboards, concept art).
- Translate a specific artistic style from a reference image into a reusable Style Prompt.
- Generate images using the current active text-to-image mode exposed by Hermes.
- Art-direct an LLM to produce a prompt that is style-pure (no content bleed).

## When NOT to Use

- Analyzing user-provided images to drive downstream decisions → use `ocas-look`
- General web research on aesthetics or art history → use `ocas-sift`
- Editing or post-processing existing images → use an image editor
- Image captioning or description → use `ocas-look`

## RULE — Read the Skill End-to-End Before Any Generation Run

Before ANY imagine run, read this SKILL.md and `references/api_reference.md` in full; never reconstruct the methodology from memory or guess the generation path. If you catch yourself hand-rolling a substitute (hand-coded SVGs, a separate model, ad-hoc scripts), STOP — that is the signature of not having read the skill; fix the blocker instead. **Why:** content bleed and concatenation-order failures are non-obvious, and memory-based reconstruction reliably gets them wrong.

## Responsibility Boundary

**Imagine does:** style library management, style extraction from reference images, art-directed prompt synthesis, image generation through the current active conversation model (when text-to-image capable), and journaling of every run.

**Imagine does not:** call the separate `image_generate` tool, bypass the active model via Pollinations/Pollination, FAL, or direct provider endpoints (unless <operator> explicitly requests one), edit/post-process images, or do general web research.

Routing: `ocas-look` consumes images as decision inputs; Imagine produces images as creative output. "Look at this image and do X with the info" → Look. "Make an image that looks like this" → Imagine.

## Optional Skill Cooperation

Imagine runs standalone; these are optional and must not block a run:

- **ocas-sift** — research a referenced artist or movement before extraction.
- **ocas-weave** — resolve portrait references to known people.

## Journal Outputs

- **Action** — `imagine.generate`, `imagine.style.save` (external side effect or persistent state write).
- **Observation** — `imagine.extract`, `imagine.library.list` (analysis or read-only enumeration).

Every run produces exactly one journal file. See `references/journal.md` for the record schema.

## Core Methodology

See `references/style_prompt_guide.md` for the full Style-Content separation methodology, the five standard style sections, and the overspecification rule.

## Operational Flows

### Flow 1: Image Generation (existing style)

Use when the user wants an image in a known or predefined style.

**Checklist:**
- [ ] Style selected from default_styles.md or styles.jsonl
- [ ] Content Prompt describes only what is in the scene (no style/color/lighting keywords)
- [ ] Final prompt = Style Prompt + Content Prompt (style first)
- [ ] API call succeeded
- [ ] Action Journal record written with final prompt + image URL

1. **Select Style:** load a style from `references/default_styles.md` or a saved Style Prompt in `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
2. **Expand Content:** turn the user's subject request into a detailed Content Prompt.
   - *Constraint:* describe what is in the scene, never how it looks (no colors, no style keywords, no lighting direction) — style keywords in a Content Prompt break the style/content split.
3. **Synthesis:** concatenate Style + Content into the final prompt, style first, because reversing the order makes the model prioritize subject over aesthetics.
4. **Execute:** submit the synthesized prompt to the current active conversation model when it is text-to-image capable. Do not call the separate `image_generate` tool, Pollinations/Pollination, FAL, or any direct provider endpoint unless <operator> explicitly asks for that backend.
5. **Journal:** write an Action Journal record with the final synthesized prompt and the resulting image URL.

**I/O Example:**
- Input: `imagine.generate --style NOIR --content "a detective standing under a streetlight at night"`
- Output: `{"status": "ok", "image": "<active-mode image URL or file path>", "journal_id": "r_a7f2c1"}`

When art-direction output is consumed programmatically, emit the structured JSON (prompt, style_weights, negative_prompt, content_summary) defined in `references/output-schema.md`.

### Flow 2: Style Extraction (image → style)

Use when the user provides an image and wants to capture its soul for future use.

**Checklist:**
- [ ] Reference image loaded (path or URL)
- [ ] Multi-modal analysis completed
- [ ] Style extracted in exhaustive detail (no object/content names)
- [ ] Organized into five standard sections
- [ ] Style Test image generated and verified (no content bleed)
- [ ] Style Prompt saved to styles.jsonl
- [ ] Observation Journal record written

1. **Visual Analysis:** use a multi-modal LLM (via `vision_analyze` or equivalent) to analyze the reference image.
2. **Exhaustive Extraction:** apply the extraction prompt in `references/style_prompt_guide.md`.
   - *Requirement:* describe the style in exhaustive detail without naming any object or content.
3. **Semantic Organization:** organize the raw description into the five standard sections: Perspective & Composition; Lighting & Shadow; Color Palette; Brushwork & Technique; Image Framing & Balance.
4. **Verification:** generate a Style Test image of an unrelated simple subject to confirm the prompt is robust and content-bleed-free (bleed produces inconsistent results across subjects).
5. **Save:** append the resulting Style Prompt to `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
6. **Journal:** write an Observation Journal record for the extraction.

**I/O Example:**
- Input: `imagine.extract --image https://example.com/ref-photo.jpg`
- Output: `{"status": "ok", "style_name": "extracted-noir", "style_prompt": "...", "test_image_url": "...", "journal_id": "r_9c3e02"}`

## Commands

- `imagine.generate --style <name|prompt> --content <description>` — generate an image in a specific style.
- `imagine.extract --image <path|url>` — analyze an image into a structured Style Prompt.
- `imagine.library.list` — list all predefined and saved styles.
- `imagine.style.save --name <name> --prompt <prompt>` — save a custom style to the library.
- `imagine.journal` — read the most recent run record (final prompt + image URL).

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every generation/extraction run writes an evidence record to `{agent_root}/commons/data/ocas-imagine/evidence.jsonl`, including no-op runs (`not_activity_reason` mandatory when no side effects occur).
- **Gap detection**: Not applicable — on-demand only.
- **Degraded mode**: If the active model cannot emit image attachments through the current surface, log `degraded: current_model_t2i_unavailable` and return the interface error; no fallback backends.
- **Log compaction**: Evidence and history logs older than 30 days compacted; last 7 days retained.

## Storage Layout

All state lives under `{agent_root}/commons/` — layout tree, ConfigBase notes, and pending-spec pointers: `references/storage-layout.md`. Never write skill state inside the skill directory.

## Implementation Details

See `references/api_reference.md` for the current-model execution contract and failure handling.

## Background Tasks

Imagine has no operational background tasks — it runs purely on invocation, so a generation failure is not retried automatically.

## Self-Update

Self-update is handled centrally by the `skills:update-fleet` cron. This skill intentionally ships no in-skill updater or update script — do not re-add one.

## Visibility

Public.

## Gotchas

- **Content bleed invalidates a Style Prompt** — A Style Prompt naming specific objects or people produces inconsistent results across subjects. Always verify with a Style Test image of an unrelated, simple subject before saving.
- **Style-content concatenation order matters** — Style Prompt first, then Content Prompt. Reversing the order makes the model prioritize subject over aesthetics.
- **Current-model failures are terminal** — When the active model cannot emit image attachments through the current surface, there is no in-skill retry. Log degraded mode, report the interface problem; never route around it via `image_generate`, Pollinations/Pollination, FAL, or direct provider calls.
- **Validation triple is mandatory** — Every generation must produce entries in `history.jsonl`, a journal file, AND `evidence.jsonl`; a run missing any of these is invalid per the OKR data_integrity target.
- **On-demand only — no background tasks** — No cron jobs or heartbeat tasks; a missed run is never replayed.

## Error Handling

| Failure | Handling |
|---|---|
| Current model image path unavailable (interface/tooling error) | Log `degraded: current_model_t2i_unavailable` to evidence.jsonl, return the interface error; no fallback backends |
| vision_analyze fails on reference image | Retry once asking for a pure visual-style description; if still failing, report accepted image formats |
| styles.jsonl is corrupted or unreadable | Initialize fresh from built-in defaults in `references/default_styles.md`; log corruption to evidence.jsonl |
| Content Prompt accidentally contains style keywords | Halt generation, report content bleed to user, request pure content description |
| Style Test image shows content bleed | Do NOT save the Style Prompt; report extraction failure, suggest a cleaner reference image |
| Journal write fails (permissions/disk) | Log to stderr, still return the generation result, flag evidence record `journal_write_failed: true` |
| Invalid image path or URL in extract command | Return error listing accepted formats: local path, http(s) URL; never fetch unsupported schemes |

## Support File Map

| File | When to read |
|---|---|
| `references/style_prompt_guide.md` | During Flow 2 step 2 — when extracting style from a reference image |
| `references/default_styles.md` | During Flow 1 step 1 — before picking a style, to browse available presets |
| `references/output-schema.md` | When Flow 1 output is consumed programmatically (structured JSON) |
| `references/storage-layout.md` | Before writing any state file, or when verifying where data lives |
| `references/interactive-menu.md` | When invoked interactively via `/` — full two-level menu structure |
| `references/journal.md` | Before writing any journal file; contains the record schema |
| `references/api_reference.md` | When executing generation; contains the current-model routing contract |
| `references/indigo.md` | When a violet glitch-field / signal-decay aesthetic is requested |
| `references/soma.md` | When a soft luminous gradient aesthetic is requested or identified |
| `references/noir.md` | When a flat silhouette + low sun aesthetic is requested or identified |
| `references/hiro.md` | When a woodblock print aesthetic is requested or identified |
| `references/comic.md` | When an ink linework + warm ground aesthetic is requested or identified |
| `references/candy.md` | When a plein-air + opaque color field aesthetic is requested |
| `references/vaporware.md` | When a retro consumer electronics aesthetic is requested |
| `tests/test_skill_integrity.py` | When editing SKILL.md or support files — run `python3 -m unittest discover -s tests` before finishing |

## Validation Rules

- Every generation writes to `history.jsonl`, a journal file, AND `evidence.jsonl`. A run missing any record is invalid.
- Style Prompts must not reference specific objects, people, or scene content.
- Content Prompts must not reference colors, lighting, materials, or style keywords already covered by the selected Style Prompt.
- All filesystem writes stay within `{agent_root}/commons/data/ocas-imagine/` and `{agent_root}/commons/journals/ocas-imagine/`.

## OKRs

- **schedule_adherence**: 100% — on-demand only; every invocation completes or errors within timeout (measured via evidence.jsonl timestamps).
- **data_integrity**: 100% — every run produces valid history.jsonl + journal + evidence.jsonl records. A run missing any record is invalid.
