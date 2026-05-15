# Vault Slicer
A bundling tool to share "slice" of part of your vault that creates portable, self-contained bundles of selected knowledge subgraphs.

It recursively resolves:
- Folder-based note collections
- Wikilink relationships (`[[note]]`)
- Image and attachment dependencies

And will create an easily shareable output such as:
```
vault_bundle/
├── notes/
│   ├── note_1.md
│   ├── note_2.md
│   ├── note_3.md
│
└── images/
    ├── imageA.png
    ├── imageB.png
```

---


# Installation for Development
> **Note:** Before making changes to the pipeline, please verify with [act](https://github.com/nektos/act).

```bash
poetry install --with dev
poetry run lint = "ruff check ."
poetry run lint-fix = "ruff check . --fix"
poetry run format = "ruff format ."
poetry run format-check = "ruff format --check ."
poetry run typecheck = "pyright"
poetry run security = "bandit -r ."
test = "pytest"
```

# How to use it
## Basic Export
This will export a **single folder** _(`--target`)_ to the the destination location _(`--export`)_ based on the vault provided _(`--vault`)_:

```bash
python export.py \
  --vault ~/ObsidianVault \
  --export ~/exports/vault_bundle \
  --targets zettlekasten/virtualization
```
## Multiple Folders:
This will export a **mutiple folders** _(`--target`)_ to the the destination location _(`--export`)_ based on the vault provided _(`--vault`)_:
```bash
python export.py \
  --vault ~/ObsidianVault \
  --export ~/exports/bundle \
  --targets zettlekasten/virtualization zettlekasten/something_else
```
## Ignore system folders
You can also ignore folders, by adding the `--ignore` flag:
```bash
--ignore templates daily system
```
