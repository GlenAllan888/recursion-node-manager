#!/usr/bin/env bash
# ─── Activate venv (adjust path if needed) ─────────────────────────────────
cd /Users/chaosbookpro/recursion-node-manager
source ./.venv/bin/activate

# ─── Run the merge script ───────────────────────────────────────────────────
./merge_chaos_sessions.py \
  -d parsed_sessions/Anti-John/Transcripts/Markdown \
  -o parsed_sessions/Anti-John/all_anti-john_sessions.md