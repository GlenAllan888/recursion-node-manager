#!/usr/bin/env python3
import re
import argparse
from pathlib import Path
from datetime import datetime
import ujson as json
from collections import defaultdict

#------------------------------------------------------------------------------
GPT_MAP = {
    None: "ChatGPT",
    "g-67fa9758dbec819185984c7de374285d": "TheChaosSystem",
    "g-jt4zig6Zx":                         "CourtGPT",
    "g-681c359ff61081918977af4bc625e6ac": "Zero-Omega",
    "g-686de2cbf93881919f1616a678277a87": "Anti-John",
    
}
USER_LABEL = "Glen Allan"

def md_escape(text: str) -> str:
    return "" if not isinstance(text, str) else text.replace("_", "\\_").replace("*", "\\*")

def sanitize_filename(text: str) -> str:
    s = re.sub(r"\s+", "_", text)
    s = re.sub(r"[^\w\-]", "", s)
    return s[:100] or "untitled"

def extract_model_slug(conv: dict) -> str:
    for node in (conv.get("mapping") or {}).values():
        if not isinstance(node, dict): continue
        slug = (node.get("message") or {}).get("metadata", {}).get("model_slug")
        if slug: return slug
    return "unknown-model"

def extract_raw_messages(conv: dict) -> list:
    out = []
    for node in (conv.get("mapping") or {}).values():
        if not isinstance(node, dict): continue
        msg = node.get("message") or {}
        role = msg.get("author", {}).get("role")
        content = msg.get("content") or {}
        ctype = content.get("content_type")
        ts = msg.get("create_time") or msg.get("update_time") or 0

        if role == "user" and ctype == "text":
            txt = "\n".join(p.strip() for p in content.get("parts", []) if isinstance(p, str)).strip()
            if txt: out.append((ts, role, "text", txt))

        elif role == "assistant":
            if ctype == "thoughts":
                for th in content.get("thoughts", []):
                    t = th.get("content", "").strip()
                    if t: out.append((ts, role, "thoughts", t))
            elif ctype == "text":
                txt = "\n".join(p.strip() for p in content.get("parts", []) if isinstance(p, str)).strip()
                if txt: out.append((ts, role, "text", txt))

    return sorted(out, key=lambda x: x[0])

def main(input_json: Path, output_base: Path):
    data = json.loads(input_json.read_text(encoding="utf-8"))
    convs = list(data.values()) if isinstance(data, dict) else data

    # group by GPT name
    buckets = defaultdict(list)
    for conv in convs:
        tpl = conv.get("conversation_template_id")
        name = GPT_MAP.get(tpl, "ChatGPT")
        ts = conv.get("update_time") or conv.get("create_time") or 0
        buckets[name].append((ts, conv))

    for gpt_name, items in buckets.items():
        items.sort(key=lambda x: x[0])  # chronological
        md_dir = output_base / gpt_name / "Transcripts" / "Markdown"
        md_dir.mkdir(parents=True, exist_ok=True)

        for idx, (ts, conv) in enumerate(items, start=1):
            raw_title = conv.get("title") or "untitled"
            safe_title = sanitize_filename(raw_title)
            ts_str = datetime.fromtimestamp(ts).strftime("%Y%m%d_%I%M%S%p")
            num_str = f"{idx:03d}"

            filename = f"{num_str}_{ts_str}_{safe_title}.md"
            out_path = md_dir / filename

            model_slug = extract_model_slug(conv)

            lines = [
                f"# {num_str}. {raw_title}",
                f"- **Session #:** {idx}",
                f"- **Date / Time:** {datetime.fromtimestamp(ts).strftime('%Y-%m-%d %I:%M:%S %p')}",
                f"- **Custom GPT Name:** {gpt_name}",
                f"- **Model Used:** {model_slug}",
                ""
            ]
            for _, role, ctype, text in extract_raw_messages(conv):
                esc = md_escape(text)
                if role == "user" and ctype == "text":
                    lines.append(f"{USER_LABEL} said: {esc}")
                elif role == "assistant" and ctype == "thoughts":
                    lines.append(f"[{gpt_name} thinking]: {esc}")
                elif role == "assistant" and ctype == "text":
                    lines.append(f"{gpt_name} said: {esc}")
                lines.append("")

            out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
            print(f"Wrote {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Export all sessions, numbered and grouped, as Markdown"
    )
    p.add_argument("-i","--input",
                   default="_UserData/conversations.json",
                   help="Path to conversations.json")
    p.add_argument("-o","--output",
                   default="parsed_sessions",
                   help="Base directory for parsed sessions")
    args = p.parse_args()
    main(Path(args.input), Path(args.output))