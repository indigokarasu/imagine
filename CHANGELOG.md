# Changelog

## [1.0.3] - 2026-04-14

### Changed
- Split `references/default_styles.md` into one file per style: `soma.md`, `noir.md`, `hiro.md`, `comic.md`, `candy.md`, `vaporware.md`. `default_styles.md` is now a thin index pointing to each file.
- Updated Support File Map in SKILL.md to list each style file individually.

### Added
- Guidance in `default_styles.md` for adding a new default style (file naming, section shape, index entry).

## [1.0.2] - 2026-04-14

### Added
- `README.md` and `CHANGELOG.md` per `spec-ocas-skill-publishing.md`.
- `references/journal.md` defining the Imagine journal record schema.
- System-skill sections in SKILL.md: Responsibility Boundary, Optional Skill Cooperation, Ontology Mapping, Journal Outputs, Visibility, Background Tasks, Validation Rules.
- Storage Layout section referencing `~/openclaw/` paths.

### Changed
- Storage paths migrated from `{agent_root}/commons/data|journals/ocas-imagine/` to `~/openclaw/data/ocas-imagine/` and `~/openclaw/journals/ocas-imagine/` to match `spec-ocas-storage-conventions.md`.
- Frontmatter `filesystem.read` and `filesystem.write` entries updated to the `~/openclaw/` root.
- Description refined for routing (explicit trigger / non-trigger language differentiating Imagine from `ocas-look`).

### Fixed
- Support File Map previously referenced `references/journal.md`, which did not exist in the package. File now added.

## [1.0.1] - Prior

### Added
- Initial release of the Style/Content separation methodology.
- `imagine.generate`, `imagine.extract`, `imagine.library.list`, `imagine.style.save`, `imagine.journal` commands.
- `references/style_prompt_guide.md`, `references/default_styles.md`, `references/api_reference.md`.
