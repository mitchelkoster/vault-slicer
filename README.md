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

# How to use it

## Installation
```bash
poetry install
poetry run vault-slicer -h
````

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
