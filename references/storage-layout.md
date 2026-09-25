# Storage Layout

All state lives under `{agent_root}/commons/` — never inside the skill directory.

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

Config follows `ConfigBase` from `spec-ocas-shared-schemas.md` (⚠️ pending spec — not yet authored). All paths use the `{agent_root}/commons/` root per `spec-ocas-storage-conventions.md` (⚠️ pending spec — not yet authored).
