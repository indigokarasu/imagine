---
name: ocas-imagine
description: 'Imagine: an art-direction engine for text-to-image generation. Separates
  Style from Content to keep aesthetic identity consistent across an image series.
  Use when the user asks to generate, render, or illustrate an image (especially across
  a series), to capture the style of a reference image for reuse, or to produce an
  image in a named/saved style. Not for captioning, image analysis for decisions (that
  is ocas-look), or photo editing.

  '
license: MIT
metadata:
  author: Indigo Karasu
  version: 1.0.4
---

# Imagine

Imagine is an art-direction engine that treats image generation as a two-part process: **Style Prompting** and **Content Prompting**. Decoupling aesthetic DNA from subject matter lets a series of images share one visual identity while their content varies.

## When to use

- Create a series of images with a consistent visual identity (comics, storyboards, concept art).
- Translate a specific artistic style from a reference image into a reusable Style Prompt.
- Generate images using the Flux model via the Pollinations.ai API.
- Art-direct an LLM to produce a prompt that is style-pure (no content bleed).

## Responsibility Boundary

**Imagine does:** style library management, style extraction from reference images, art-directed prompt synthesis, image generation via Pollinations.ai, journaling of every generation and extraction run.

**Imagine does not:** analyze user-provided images to drive downstream decisions (that is `ocas-look`), perform general web research on aesthetics (that is `ocas-sift`), or edit/post-process existing images.

Adjacent responsibility: `ocas-look` consumes images as decision inputs; Imagine produces images as creative output. If a request is "look at this image and do X with the info," route to Look; if it is "make an image that looks like this," route to Imagine.

## Optional Skill Cooperation

Imagine functions standalone. When present it may cooperate with:

- **ocas-sift** — research on a referenced artist, movement, or visual vocabulary before extraction.
- **ocas-weave** — resolving references to known people (portrait subjects) for identity context.

Imagine never depends on these skills and must run normally if they are absent.

## Ontology Mapping

Imagine extracts no Chronicle entities and emits no entity signals. Styles are internal artifacts of this skill only.

## Journal Outputs

- **Action Journal** — emitted by `imagine.generate` and `imagine.style.save` (external HTTP side effect or persistent state write).
- **Observation Journal** — emitted by `imagine.extract` and `imagine.library.list` (analysis or read-only enumeration, no side effects).

Every run produces exactly one journal file. See `references/journal.md` for the record schema.

## The Core Methodology: Style-Content Separation

The fundamental invariant of Imagine is that **Style** and **Content** must never be mashed into a single descriptive paragraph.

1. **Style Prompt:** a high-detail technical description of the aesthetic — Perspective, Lighting, Color Palette, Brushwork/Texture, Framing.
2. **Content Prompt:** a pure description of objects, relative scale, placement, and narrative components.

**The Rule:** if a Content Prompt describes a color, material, or lighting effect that the Style Prompt already handles, it is an overspecification and must be removed to avoid confusing the model.

## Operational Flows

### Flow 1: Image Generation (existing style)

Use when the user wants an image in a known or predefined style.

1. **Select Style:** retrieve a style definition from `references/default_styles.md` or a previously saved Style Prompt in `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
2. **Expand Content:** turn the user's subject request into a detailed Content Prompt.
   - *Constraint:* describe what is in the scene, never how it looks (no colors, no style keywords, no lighting direction).
3. **Synthesis:** concatenate Style + Content into the final API call.
4. **Execute:** call the Pollinations.ai endpoint.
5. **Journal:** write an Action Journal record with the final synthesized prompt and the resulting image URL.

### Flow 2: Style Extraction (image → style)

Use when the user provides an image and wants to capture its soul for future use.

1. **Visual Analysis:** use a multi-modal LLM (via `vision_analyze` or equivalent) to analyze the reference image.
2. **Exhaustive Extraction:** apply the extraction prompt in `references/style_prompt_guide.md`.
   - *Requirement:* describe the style in exhaustive detail without naming any object or content.
3. **Semantic Organization:** organize the raw description into the five standard sections:
   - Perspective & Composition
   - Lighting & Shadow
   - Color Palette
   - Brushwork & Technique
   - Image Framing & Balance
4. **Verification:** generate a Style Test image of an unrelated, simple subject to confirm the prompt is robust and free of content bleed.
5. **Save:** append the resulting Style Prompt to `{agent_root}/commons/data/ocas-imagine/styles.jsonl`.
6. **Journal:** write an Observation Journal record for the extraction.

## Commands

- `imagine.generate --style <name|prompt> --content <description>` — generate an image in a specific style.
- `imagine.extract --image <path|url>` — analyze an image and produce a structured Style Prompt.
- `imagine.library.list` — list all available predefined and saved styles.
- `imagine.style.save --name <name> --prompt <prompt>` — save a new custom style to the library.
- `imagine.journal` — read the most recent run record (final prompt + resulting image URL).

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every generation/extraction run writes an evidence record to `{agent_root}/commons/data/ocas-imagine/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: Not applicable — on-demand only.
- **Degraded mode**: When Pollinations.ai API is unavailable, logs `degraded: pollinations_api` and returns error with fallback suggestion.
- **Log compaction**: Evidence and history logs older than 30 days compacted. Last 7 days retained.

## Storage Layout

```
{agent_root}/commons/data/ocas-imagine/
  config.json        # ConfigBase fields + Imagine defaults
  styles.jsonl       # Custom user-created style prompts (append-only)
  history.jsonl      # Append-only log of generation prompts and results
  intents.jsonl      # Append-only log of user intents per run
  evidence.jsonl     # Append-only evidence records (recovery contract)
{agent_root}/commons/journals/ocas-imagine/
  YYYY-MM-DD/
    {run_id}.json    # One journal file per run
```

Config follows `ConfigBase` from `spec-ocas-shared-schemas.md`. All paths use the `{agent_root}/commons/` root per `spec-ocas-storage-conventions.md`.

## Implementation Details

### API Integration

Primary endpoint — Pollinations.ai (zero-cost Flux):

```
https://image.pollinations.ai/prompt/{prompt}?width=1024&height=1024&model=flux&nologo=true
```

See `references/api_reference.md` for parameters, timeouts, and fallback endpoints.

## Background Tasks

Imagine has no operational background tasks. The universal `imagine:update` self-update cron is standard and is not enumerated here.

## Self-update

`imagine.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from SKILL.md frontmatter `metadata.version`
3. Fetch remote version from SKILL.md frontmatter: `gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1 | sed 's/.*\"\(.*\)\".*/\1/'`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Imagine from version {old} to {new}`

## Visibility

Public.

## Gotchas

- **Content bleed invalidates a Style Prompt** — If a Style Prompt references specific objects, people, or scene content, it will produce inconsistent results across subjects. Always verify with a Style Test image of an unrelated, simple subject before saving.
- **On-demand only — no background tasks** — Imagine has no scheduled cron jobs or heartbeat tasks. It runs purely on invocation. A generation failure won't be retried automatically.
- **Style-content concatenation order matters** — The final API prompt must be Style Prompt first, then Content Prompt. Reversing the order causes the model to prioritize subject over aesthetics.
- **API failures are terminal** — When Pollinations.ai is unavailable, there is no built-in retry in the skill itself. The degraded mode logs the error and returns a fallback suggestion to the user.
- **Validation triple is mandatory** — Every generation must produce entries in `history.jsonl`, a journal file, AND `evidence.jsonl`. A generation missing any of these is considered invalid per the OKR data_integrity target.

## Support File Map

| File | When to read |
|---|---|
| `references/style_prompt_guide.md` | During Flow 2 step 2 — when extracting style from a reference image |
| `references/default_styles.md` | During Flow 1 step 1 — before picking a style, to browse available presets |
| `references/soma.md` | When user requests or you identify a soft luminous gradient aesthetic |
| `references/noir.md` | When user requests or you identify a flat silhouette + low sun aesthetic |
| `references/hiro.md` | When user requests or you identify a woodblock print aesthetic |
| `references/comic.md` | When user requests or you identify an ink linework + warm ground aesthetic |
| `references/candy.md` | When user requests or you identify a plein-air + opaque color field aesthetic |
| `references/vaporware.md` | When user requests or you identify a retro consumer electronics aesthetic |
| `references/api_reference.md` | When tuning generation parameters or debugging API failures |
| `references/journal.md` | Before writing any journal file; contains the record schema |

## Validation Rules

- Every generation writes to both `history.jsonl` and a journal file. A generation with no journal is invalid.
- Style Prompts must not reference specific objects, people, or scene content.
- Content Prompts must not reference colors, lighting, materials, or style keywords already covered by the selected Style Prompt.
- All filesystem writes stay within `{agent_root}/commons/data/ocas-imagine/` and `{agent_root}/commons/journals/ocas-imagine/`.

## OKRs

### schedule_adherence
- **Target**: 100% — on-demand skill with no scheduled runs; every invocation completes or reports error within timeout.
- **Measurement**: Evidence records in `evidence.jsonl` with timestamps; no silent failures.

### data_integrity
- **Target**: 100% — every generation/extraction run produces valid `history.jsonl` + journal + evidence records.
- **Measurement**: Validation that all three record types exist and are well-formed after each run.
