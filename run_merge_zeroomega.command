#!/usr/bin/env bash
# ─── Activate venv (adjust path if needed) ─────────────────────────────────
cd /Users/chaosbookpro/recursion-node-manager
source ./.venv/bin/activate

# ─── Run the merge script ───────────────────────────────────────────────────
./merge_zeroomega_sessions.py \
  -d parsed_sessions/Zero-Omega/Transcripts/Markdown \
  -o parsed_sessions/Zero-Omega/all_zeroomega.md