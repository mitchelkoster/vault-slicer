import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Export Obsidian sub-vault with dependency resolution")

    parser.add_argument("--vault", required=True, help="Path to Obsidian vault")
    parser.add_argument("--export", required=True, help="Export output folder")

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
    print(args)
