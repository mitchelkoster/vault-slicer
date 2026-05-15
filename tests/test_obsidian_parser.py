import json
from pathlib import Path

from vault_slicer.obsidian_parser import ObsidianParser


def write_note(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_parser(tmp_path, ignore=None):
    vault = tmp_path / "vault"
    export = tmp_path / "export"

    vault.mkdir()
    export.mkdir()

    return ObsidianParser(
        vault=vault,
        targets=["."],
        ignore=ignore or [],
        export_path=export,
        attachments="attachments",
    )


def test_collect_notes_basic(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    write_note(vault / "A.md", "Hello world")
    write_note(vault / "B.md", "Hello world")

    notes = parser._collect_notes(vault, targets=["."], ignore=[])

    assert len(notes) == 2
    assert any(n.name == "A.md" for n in notes)
    assert any(n.name == "B.md" for n in notes)


def test_collect_notes_follows_wikilinks(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    write_note(vault / "A.md", "Links to [[B]]")
    write_note(vault / "B.md", "Links to [[C]]")
    write_note(vault / "C.md", "No links")

    notes = parser._collect_notes(vault, targets=["."], ignore=[])

    names = {n.name for n in notes}

    assert "A.md" in names
    assert "B.md" in names
    assert "C.md" in names


def test_collect_notes_resolves_alias(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    write_note(vault / "A.md", "Links to [[B|alias]]")
    write_note(vault / "B.md", "No links")

    notes = parser._collect_notes(vault, targets=["."], ignore=[])

    names = {n.name for n in notes}

    assert "B.md" in names


def test_collect_notes_avoids_cycles(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    write_note(vault / "A.md", "Links to [[B]]")
    write_note(vault / "B.md", "Links to [[A]]")

    notes = parser._collect_notes(vault, targets=["."], ignore=[])

    names = {n.name for n in notes}

    assert names == {"A.md", "B.md"}


def test_collect_notes_ignore_folder(tmp_path):
    parser = make_parser(tmp_path, ignore=["ignore_me"])
    vault = parser._vault

    ignored_dir = vault / "ignore_me"
    ignored_dir.mkdir()

    write_note(vault / "A.md", "Links to [[B]]")
    write_note(ignored_dir / "B.md", "Should be ignored")

    notes = parser._collect_notes(vault, targets=["."], ignore=["ignore_me"])

    names = {n.name for n in notes}

    assert "A.md" in names
    assert "B.md" not in names


def test_find_note(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    write_note(vault / "sub" / "Test.md", "content")

    found = parser._find_note(vault, "Test")

    assert found is not None
    assert found.name == "Test.md"


def test_build_note_map(tmp_path):
    parser = make_parser(tmp_path)
    vault = parser._vault

    n1 = vault / "NoteOne.md"
    n2 = vault / "NoteTwo.md"

    write_note(n1, "x")
    write_note(n2, "y")

    notes = {n1, n2}

    note_map = parser._build_note_map(notes)

    assert note_map["NoteOne"] == "NoteOne.md"
    assert note_map["NoteTwo"] == "NoteTwo.md"


def test_extract_images(tmp_path):
    parser = make_parser(tmp_path)

    text = """
    ![[image1.png]]
    ![](image2.jpg)
    """

    images = parser._extract_images(text)

    assert images == ["image1.png", "image2.jpg"]


def test_rewrite_links(tmp_path):
    parser = make_parser(tmp_path)

    text = "Link to [[MyNote]]"

    note_map = {"MyNote": "MyNote.md"}

    rewritten = parser._rewrite_links(text, note_map)

    assert rewritten == "Link to [MyNote](MyNote.md)"


def test_export_copies_notes_and_images(tmp_path):
    parser = make_parser(tmp_path)

    vault = parser._vault
    export = parser._export_path

    attachments = vault / "attachments"
    attachments.mkdir()

    write_note(vault / "A.md", "Link [[B]]\n\n![[image.png]]")

    write_note(vault / "B.md", "Hello")

    (attachments / "image.png").write_text("fake image")

    parser.export()

    exported_note = export / "notes" / "A.md"
    exported_image = export / "attachments" / "image.png"

    assert exported_note.exists()
    assert exported_image.exists()

    content = exported_note.read_text()

    assert "[B](B.md)" in content


def test_export_creates_obsidian_vault(tmp_path):
    parser = make_parser(tmp_path)

    vault = parser._vault
    export = parser._export_path

    write_note(vault / "A.md", "Hello")

    parser.export()

    obsidian_dir = export / ".obsidian"
    app_json = obsidian_dir / "app.json"

    assert obsidian_dir.exists()
    assert app_json.exists()

    config = json.loads(app_json.read_text())

    assert config["attachmentFolderPath"] == "attachments"
