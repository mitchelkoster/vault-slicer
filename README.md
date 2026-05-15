# Vault Slicer
A bundling tool for exporting portable “slices” of your Obsidian vault and exports it to a new fault so you can easily share information.

It recursively resolves:
- Folder-based note collections
- Wikilink relationships ([[note]])
- Image and attachment dependencies


**Example Usage**
```bash
poetry run vault-slicer \
  --vault '/home/mitchel/Documents/obsidian' \
  --export '/tmp/radio' \
  --targets 'Zettlekasten/Radio' \
  --ignore 'Aviation' \
  --attachments 'Files'
```

Or when using Docker:
```bash
docker build -t vault-slicer .
docker run --rm -it \
  --user $(id -u):$(id -g) \
  -v /home/mitchel/Documents/obsidian:/vault \
  -v ~/exports/radio:/export \
  vault-slicer \
  --vault /vault \
  --export /export \
  --targets Zettlekasten/Radio \
  --ignore Aviation \
  --attachments Files
```

**Example output:**
```
vault_bundle/
├── .obsidian/
│   └── app.json
├── notes/
│   ├── note_1.md
│   ├── note_2.md
│   └── note_3.md
└── attachments/
    ├── imageA.png
    └── imageB.png
```


# Installation for Development
> **Note:** Before making changes to the pipeline, please verify with [act](https://github.com/nektos/act) and set secrets `act --secret-file .secrets`.

Install dependencies:
```bash
poetry install --with dev
```
Development commands:
```bash
poetry run lint = "ruff check ."
poetry run lint-fix = "ruff check . --fix"
poetry run format = "ruff format ."
poetry run format-check = "ruff format --check ."
poetry run typecheck = "pyright"
poetry run security = "bandit -r ."
test = "pytest"
```

# Usage Instructions
## Basic Export
Export a folder from your vault into a portable Obsidian bundle:

```bash
poetry run vault-slicer \
  --vault ~/ObsidianVault \
  --export ~/exports/vault_bundle \
  --targets Zettlekasten/Radio
```
## Multiple Targets:
This will export a **mutiple folders** _(`--target`)_ to the the destination location _(`--export`)_ based on the vault provided _(`--vault`)_:
```bash
poetry run vault-slicer \
  --vault ~/ObsidianVault \
  --export ~/exports/vault_bundle \
  --targets \
    Zettlekasten/Radio \
    Zettlekasten/Aviation
```
## Ignore Folders
Exclude folders from traversal:
```bash
poetry run vault-slicer \
  --vault ~/ObsidianVault \
  --export ~/exports/vault_bundle \
  --targets Zettlekasten \
  --ignore Templates Daily System
```
## Custom Attachment Folder
If your Obsidian vault stores attachments in a custom directory:
```bash
poetry run vault-slicer \
  --vault ~/ObsidianVault \
  --export ~/exports/vault_bundle \
  --targets Zettlekasten/Radio \
  --attachments Files
```

This configures the exported vault to use `attachments/` as the Obsidian attachment directory internally.