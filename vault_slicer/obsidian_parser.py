import logging
import re
import shutil


class ObsidianParser:
    def __init__(self, vault, targets, ignore, export_path, attachments):
        self._logger = logging.getLogger(__name__)

        self._vault = vault
        self._targets = targets
        self._ignore = ignore
        self._export_path = export_path
        self._attachments = attachments

        # Wikilinks:
        # [[note]] or [[note|alias]]
        self._wikilink_pattern = re.compile(r"\[\[(.*?)\]\]")

        # Images:
        # ![[image.png]] or ![](image.png)
        self._image_pattern = re.compile(r"!\[\[(.*?)\]\]|!\[.*?\]\((.*?)\)")

    def _rewrite_links(self, text, note_map):
        def replacer(match):
            raw = match.group(1)
            target = raw.split("|")[0]

            if target in note_map:
                return f"[{target}]({note_map[target]})"

            return match.group(0)

        return self._wikilink_pattern.sub(replacer, text)

    def _extract_images(self, text):
        matches = self._image_pattern.findall(text)
        return [m[0] or m[1] for m in matches if m[0] or m[1]]

    def _is_ignored(self, path, ignore_list):
        return any(part in ignore_list for part in path.parts)

    def _extract_wikilinks(self, text):
        matches = self._wikilink_pattern.findall(text)
        return [m.split("|")[0] for m in matches]

    def _find_note(self, vault, name):
        results = list(vault.rglob(f"{name}.md"))
        return results[0] if results else None

    def _collect_notes(self, vault, targets, ignore):
        to_process = []
        collected = set()

        for t in targets:
            base = vault / t
            for md in base.rglob("*.md"):
                if not self._is_ignored(md, ignore):
                    to_process.append(md)
                    collected.add(md)

        while to_process:
            note = to_process.pop()
            text = ""

            try:
                text = note.read_text()
            except (OSError, UnicodeDecodeError) as e:
                self._logger.warning("Skipping unreadable note %s: %s", note, e)

            for link in self._extract_wikilinks(text):
                linked = self._find_note(vault, link)

                if linked and linked not in collected:
                    if not self._is_ignored(linked, ignore):
                        collected.add(linked)
                        to_process.append(linked)

        return collected

    def _build_note_map(self, notes):
        return {n.stem: n.name for n in notes}

    def export(self):
        notes = self._collect_notes(self._vault, self._targets, self._ignore)
        note_map = self._build_note_map(notes)

        # Create output directories
        out_notes = self._export_path / "notes"
        out_images = self._export_path / "images"
        out_notes.mkdir(parents=True, exist_ok=True)
        out_images.mkdir(parents=True, exist_ok=True)

        copied_images = set()
        for note in notes:
            note_text = note.read_text()

            # rewrite links BEFORE saving
            note_text = self._rewrite_links(note_text, note_map)

            # write exported note
            (out_notes / note.name).write_text(note_text)

            # Export Images
            for img in self._extract_images(note_text):
                img_path = self._vault / self._attachments / img

                if img_path.exists():
                    if img_path.name not in copied_images:
                        shutil.copy2(img_path, out_images / img_path.name)
                        copied_images.add(img_path.name)
