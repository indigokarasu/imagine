# imagine

<p align="center">
<img src="./assets/readme/hero.jpg" width="100%" alt="Imagine: art-direction engine for text-to-image generation.">
</p>

An art-direction engine for text-to-image generation. Imagine separates **Style** from **Content** so a series of images can share one visual identity while the subject matter varies — it is not a prompt wrapper.

## What it does

- Generates images in a named or saved style through the current active text-to-image model.
- Extracts a reusable, content-pure Style Prompt from a reference image.
- Maintains a style library: predefined defaults plus user-saved styles.
- Journals every generation and extraction run for provenance.

## Layout

- `SKILL.md` — agent procedure, routing, and operational flows
- `references/` — style methodology, default style library, schemas
- `tests/` — integrity tests (`python3 -m unittest discover -s tests`)
- `evals/` — evaluation cases

## Usage

Load the skill and ask for an image, a style extraction, or a style listing. See `SKILL.md` for the full workflow.

## License

MIT — see `LICENSE`. Part of the OCAS Agent Suite.
