# Art-Direction Output Schema

Use this schema when Flow 1 art-direction output is consumed programmatically (another skill or script parsing the prompt package) rather than being sent straight to generation.

```json
{
  "prompt": "<Style Prompt + Content Prompt concatenated, style first>",
  "style_slug": "noir",
  "style_weights": {"mood": 0.8, "composition": 0.7, "color": 0.9, "texture": 0.6},
  "negative_prompt": "blurry, low quality, distorted, watermark",
  "content_summary": "a detective standing under a streetlight at night"
}
```

## Rules

- `style_weights` are normalized 0.0–1.0 relative weights per standard style section.
- `negative_prompt` carries the style library's default exclusions unless explicitly overridden.
- `prompt` is always the executable style+content concatenation (Flow 1 step 3) — style first.
- `content_summary` is style-free: it describes only what is in the scene.
