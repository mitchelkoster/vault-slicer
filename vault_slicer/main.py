import argparse
from pathlib import Path

from .obsidian_parser import ObsidianParser


def parse_args():
    parser = argparse.ArgumentParser(description="Export Obsidian sub-vault with dependency resolution")

    parser.add_argument("--vault", required=True, help="Path to Obsidian vault")
    parser.add_argument("--export", required=True, help="Export output folder")
    parser.add_argument(
        "--attachments",
        default="attachments",
        help="Obsidian attachment folder inside the vault",
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        required=True,
        help="Root folders to export (multiple allowed)",
    )

    parser.add_argument("--ignore", nargs="*", default=[], help="Folders to ignore")

    parser.add_argument("--max-depth", type=int, default=10, help="Safety limit for recursion depth")

    return parser.parse_args()


def main():
    args = parse_args()
    vault = Path(args.vault).resolve()
    export_path = Path(args.export).resolve()

    if vault == export_path:
        raise ValueError("Export path cannot be inside vault")

    parser = ObsidianParser(
        vault=vault, targets=args.targets, ignore=args.ignore, export_path=export_path, attachments=args.attachments
    )
    parser.export()
