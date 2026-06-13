# FAL — API Key and Usage

## Key location

The FAL API key is stored in `config/web` (the Hermes web config). Do not hardcode it in scripts or skills.

## Usage

Use the `ocas-imagine` skill for all FAL image generation. The skill handles:
- Key retrieval from config
- Model selection
- Prompt engineering with style/content separation
- Image delivery

## Direct API access

If you need to call FAL directly (outside ocas-imagine), read the key from config at runtime:

```python
import yaml
config = yaml.safe_load(open('/root/.hermes/config/web'))
fal_key = config.get('fal', {}).get('key')
```

Never commit the key to any file, log, or output.
