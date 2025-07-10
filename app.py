#!/usr/bin/env python3
import os
import re
import shutil
from datetime import datetime

import ujson
import markdown2
from weasyprint import HTML
import gradio as gr

# ─── CONFIG ────────────────────────────────────────────────────────────────

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
JSON_PATH   = os.path.join(BASE_DIR, "_UserData", "conversations.json")
OUTPUT_BASE = os.path.join(BASE_DIR, "parsed_sessions")

# These are the subfolders we want:
FOLDERS = {
    "pdfs":           os.path.join(OUTPUT_BASE, "PDFs", "Sessions"),
    "image_archives": os.path.join(OUTPUT_BASE, "PDFs", "ImageArchives"),
    "md":             os.path.join(OUTPUT_BASE, "Transcripts", "Markdown"),
}


# ─── CORE PARSING LOGIC ────────────────────────────────────────────────────

def get_conversation_messages(conv):
    """
    Walk the JSON tree back from `current_node` → root,
    safely handling missing fields so we never do None.get(...)
    """
    msgs = []
    current = conv.get("current_node")
    mapping = conv.get("mapping") or {}

    while current:
        node = mapping.get(current)
        if not node:
            break
        message = node.get("message") or {}
        content = message.get("content") or {}
        parts  = content.get("parts") or []
        author = message.get("author", {}).get("role", "")

        # skip any “tool:” status messages
        if author == "tool":
            current = node.get("parent")
            continue

        if parts:
            text = parts[0]
            prefix = {
                "assistant": "**ChatGPT:**",
                "user":      "**You:**",
                "system":    "**System:**"
            }.get(author, f"**{author}:**")

            msgs.append({
                "author": author,
                "text":   text,
                "md":     f"> {prefix} {text}"
            })

        current = node.get("parent")

    return list(reversed(msgs))


def parse_sessions(json_path, output_base):
    """
    1) Clears previous output_base
    2) Creates our fixed folder structure
    3) Walks each conversation, dumping:
       - .md → Transcripts/Markdown
       - .pdf → PDFs/Sessions
       (Image-Archives reserved for future)
    """
    # rebuild output dirs
    if os.path.exists(output_base):
        shutil.rmtree(output_base)
    for path in FOLDERS.values():
        os.makedirs(path, exist_ok=True)

    # load all sessions
    with open(json_path, "r", encoding="utf-8") as f:
        data = ujson.load(f)

    for conv in data:
        ct = conv.get("create_time")
        ut = conv.get("update_time")
        if not (ct and ut):
            continue

        # safe filename
        dt = datetime.fromtimestamp(ut)
        safe_title = re.sub(r"[^0-9A-Za-z_]", "_", conv.get("title", "Untitled"))[:80]
        ts_str     = dt.strftime("%d_%m_%Y_%H_%M_%S")
        base       = f"{safe_title}_{ts_str}"

        msgs = get_conversation_messages(conv)

        # Markdown transcript
        md_path = os.path.join(FOLDERS["md"], base + ".md")
        with open(md_path, "w", encoding="utf-8") as out_md:
            for m in msgs:
                out_md.write(m["md"] + "\n\n")

        # PDF version of the transcript
        html     = markdown2.markdown_path(md_path)
        pdf_path = os.path.join(FOLDERS["pdfs"], base + ".pdf")
        HTML(string=html).write_pdf(pdf_path)

    return output_base


# ─── GRADIO UI ─────────────────────────────────────────────────────────────

def run_parse():
    out = parse_sessions(JSON_PATH, OUTPUT_BASE)
    return f"✅ Done — all sessions in → {out}"


with gr.Blocks(title="Recursion Node Manager ▶ Session Parser") as demo:
    gr.Markdown("## 📂  Parse your ChatGPT export")
    parse_btn  = gr.Button("Parse All Sessions")
    status_box = gr.Textbox(interactive=False, label="Status")
    parse_btn.click(fn=run_parse, inputs=None, outputs=status_box)

# launch on 0.0.0.0 so your run_recursion_manager.command URL will work as expected
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    inbrowser=True
)