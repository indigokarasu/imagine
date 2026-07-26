# ⚙️ Imagine

  <img src="./assets/readme/hero.jpg" width="100%" alt="Imagine">

Art-direction engine for text-to-image generation. Separates Style from Content to keep aesthetic identity consistent across an image series. Use when generating, rendering, or illustrating images (especially across a series), capturing the style of a reference image for reuse, or producing an image in a named/saved style. Not for captioning, image analysis for decisions (use ocas-look), or photo editing.

**Skill name:** `ocas-imagine`
**Version:** 1.0.5
**Type:** 
**Layer:** creative
**Author:** <agent-name>

---

## 📖 Overview

Art-direction engine for text-to-image generation. Separates Style from Content to keep aesthetic identity consistent across an image series. Use when generating, rendering, or illustrating images (especially across a series), capturing the style of a reference image for reuse, or producing an image in a named/saved style. Not for captioning, image analysis for decisions (use ocas-look), or photo editing.

---

## 🔧 Commands

- `imagine.generate --style <name|prompt> --content <description>` — generate an image in a specific style.
- `imagine.extract --image <path|url>` — analyze an image and produce a structured Style Prompt.
- `imagine.library.list` — list all available predefined and saved styles.
- `imagine.style.save --name <name> --prompt <prompt>` — save a new custom style to the library.
- `imagine.journal` — read the most recent run record (final prompt + resulting image URL).

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [1.0.4] - 2026-04-14
- Changed
- [1.0.3] - 2026-04-14
- Changed
- Added
- [1.0.2] - 2026-04-14
- Added
- Changed

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
