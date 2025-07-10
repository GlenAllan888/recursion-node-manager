#!/usr/bin/env python3
import argparse
from pathlib import Path

def merge_anti-john_markdown(anti-john_md_dir: Path, output_file: Path):
    md_files = sorted(anti-john_md_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {anti-john_md_dir}")
        return

    with output_file.open("w", encoding="utf-8") as out:
        for md in md_files:
            # Optional: add a section header for each file
            out.write(f"# {md.stem}\n\n")
            out.write(md.read_text(encoding="utf-8").rstrip())
            out.write("\n\n---\n\n")

    print(f"Merged {len(md_files)} files into {output_file}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Merge all Anti-John Markdown transcripts into one file"
    )
    p.add_argument(
        "-d", "--dir",
        default="parsed_sessions/Anti-John/Transcripts/Markdown",
        help="Directory containing Anti-John .md files"
    )
    p.add_argument(
        "-o", "--out",
        default="parsed_sessions/Anti-John/all_anti-john_transcripts.md",
        help="Path for the merged output file"
    )
    args = p.parse_args()

    md_dir = Path(args.dir)
    out_file = Path(args.out)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    merge_anti-john_markdown(md_dir, out_file)