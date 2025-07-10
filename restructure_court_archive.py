#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

# split wherever a line begins with "## "
SESSION_SPLIT = re.compile(r'(?m)^##\s+')

def load_blocks(text):
    """
    Split the entire file into blocks, each beginning with "## ",
    returning a list of (raw_header, body_text).
    """
    parts = SESSION_SPLIT.split(text)
    # drop anything before the first "## "
    blocks = []
    for part in parts[1:]:
        lines = part.splitlines()
        raw_header = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        blocks.append((raw_header, body))
    return blocks

def parse_header(raw):
    """
    Given a header token like "001_20240304_020117AM_Title_Parts",
    extract (idx, date_fmt, time_fmt, title).
    """
    # 1) split off the numeric index
    try:
        idx_str, rest = raw.split("_", 1)
    except ValueError:
        raise ValueError(f"Cannot split index from header: {raw!r}")

    # 2) rest should be "YYYYMMDD_HHMMSS[AM|PM]_Title_parts"
    parts = rest.split("_", 2)
    if len(parts) < 3:
        raise ValueError(f"Header has wrong format, expected date_time_title: {rest!r}")
    date_token, time_token, title_token = parts

    # parse date YYYYMMDD → YYYY-MM-DD
    if len(date_token) == 8 and date_token.isdigit():
        date_fmt = datetime.strptime(date_token, "%Y%m%d").strftime("%Y-%m-%d")
    else:
        date_fmt = date_token

    # parse time HHMMSS[AM|PM]
    m = re.match(r"^(\d{2})(\d{2})(\d{2})(AM|PM)?$", time_token)
    if m:
        hh, mm, ss, ampm = m.groups()
        time_fmt = f"{hh}:{mm}:{ss}" + (f" {ampm}" if ampm else "")
    else:
        time_fmt = time_token

    # human title: replace underscores with spaces
    title = title_token.replace("_", " ").strip()

    return idx_str, date_fmt, time_fmt, title

def main():
    p = argparse.ArgumentParser(
        description="Re-structure CourtGPT index+summaries into a full Markdown with ToC"
    )
    p.add_argument("-i", "--input", required=True,
                   help="Path to your CourtGPTArchive-IndexAndSummaries.md")
    p.add_argument("-o", "--output", required=True,
                   help="Path for the new restructured Markdown")
    args = p.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"ERROR: Input file not found: {inp}", file=sys.stderr)
        sys.exit(1)

    text = inp.read_text(encoding="utf-8")
    blocks = load_blocks(text)
    if not blocks:
        print("WARNING: No session blocks found—check your input formatting.", file=sys.stderr)

    out_lines = []

    # --- Build the Index (single-hash)
    out_lines.append("# Index\n")
    for raw_header, _ in blocks:
        idx, date_fmt, time_fmt, title = parse_header(raw_header)
        out_lines.append(f"{idx}. {title} ({date_fmt} {time_fmt})")
    out_lines.append("\n---\n")

    # --- Append each session in full, using single-hash section headers
    for raw_header, body in blocks:
        idx, date_fmt, time_fmt, title = parse_header(raw_header)
        out_lines.append(f"# {idx}. {title}")
        out_lines.append(f"*Date: {date_fmt}*  *Time: {time_fmt}*\n")
        out_lines.append(body)
        out_lines.append("\n---\n")

    Path(args.output).write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote restructured archive with ToC → {args.output}")

if __name__ == "__main__":
    main()