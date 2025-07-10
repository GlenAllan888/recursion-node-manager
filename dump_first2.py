#!/usr/bin/env python3
import json, os, re
from pathlib import Path
from datetime import datetime

# where your raw export lives
IN_JSON = Path("_UserData/conversations.json")
OUT_DIR = Path("SessionSummaries/BySession")

# sanitize a title into a safe filename
def sanitize(text):
    # collapse whitespace, remove non-alnum, truncate to 80 chars
    s = re.sub(r"\s+", "_", text)
    s = re.sub(r"[^\w\-]", "", s)
    return s[:80] or "untitled"

# walk mapping to reconstruct ordered messages
def extract_messages(conv):
    mapping = conv.get("mapping", {})
    cur = conv.get("current_node")
    seq = []
    while cur:
        node = mapping.get(cur, {})
        msg  = node.get("message", {}) or {}
        role = msg.get("author", {}).get("role", "")
        parts = msg.get("content", {}).get("parts", []) or []
        # only keep string parts
        text = "\n".join(p.strip() for p in parts if isinstance(p, str))
        label = "You" if role=="user" else "Assistant"
        seq.append((label, text))
        cur = node.get("parent")
    return list(reversed(seq))

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(IN_JSON.read_text(encoding="utf-8"))
    for conv in data:
        # sanitize filename
        title_raw = conv.get("title","")
        fname = sanitize(title_raw)
        # which GPT
        tpl = conv.get("conversation_template_id") or "null"
        # extract first two messages
        msgs = extract_messages(conv)[:2]
        # write out
        out_path = OUT_DIR / f"{fname}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"title: \"{title_raw}\"\n")
            f.write(f"gpt_id: {tpl}\n")
            f.write(f"---\n\n")
            for role, text in msgs:
                f.write(f"**{role}:** {text}\n\n")
        print("Wrote", out_path)

if __name__=="__main__":
    main()