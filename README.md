# 🎨 Imagine

An art-direction engine for text-to-image generation that separates Style from Content to keep aesthetic identity consistent across an image series.

Skill packages follow the [agentskills.io](https://agentskills.io/specification) open standard and are compatible with OpenClaw, Hermes Agent, and any agentskills.io-compliant client.

---

## Overview

Imagine treats image generation as a two-part process: a Style Prompt that fully describes aesthetic DNA (palette, lighting, composition, texture, framing) and a Content Prompt that describes only what is in the scene. Decoupling the two prevents style drift across a series and makes a captured style reusable as a named library entry.

The skill ships a curated library of baseline styles, extracts new styles from reference images via a multi-modal analysis prompt, and generates images through the Pollinations.ai Flux endpoint. Every run is journaled.

## Commands

| Command | Description |
|---|---|
| `imagine.generate` | Generate an image in a specific style. |
| `imagine.extract` | Analyze a reference image and produce a structured Style Prompt. |
| `imagine.library.list` | List all available predefined and saved styles. |
| `imagine.style.save` | Save a new custom style to the library. |
| `imagine.journal` | Read the most recent run record. |

## Setup

`imagine.init` runs on first use and creates `~/openclaw/data/ocas-imagine/` (with `config.json`, `styles.jsonl`, `history.jsonl`) and `~/openclaw/journals/ocas-imagine/`. No manual setup is required. No API keys, accounts, or credentials are needed — Pollinations.ai is used anonymously.

## Dependencies

**External**

- Pollinations.ai Flux endpoint (required) — zero-cost, no auth. See `references/api_reference.md`.
- Multi-modal LLM with image analysis (required for `imagine.extract`) — e.g. vision-capable Claude or GPT model.

## Changelog

### v1.0.3 — April 14, 2026
- Split `references/default_styles.md` into one file per style (`soma.md`, `noir.md`, `hiro.md`, `comic.md`, `candy.md`, `vaporware.md`); `default_styles.md` is now an index.
- Support File Map in SKILL.md lists each style file individually.

### v1.0.2 — April 14, 2026
- Moved storage from `{agent_root}/commons/…` to `~/openclaw/…` per `spec-ocas-storage-conventions.md`.
- Added required System-skill sections (Responsibility Boundary, Optional Skill Cooperation, Ontology Mapping, Journal Outputs, Visibility, Background Tasks, Validation Rules).
- Added `references/journal.md` (record schema).
- Added `README.md` and `CHANGELOG.md` per `spec-ocas-skill-publishing.md`.

### v1.0.1 — Prior
- Pre-compliance release.
