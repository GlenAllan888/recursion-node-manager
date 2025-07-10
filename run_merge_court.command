#!/usr/bin/env bash
# ─── Activate venv (adjust path if needed) ─────────────────────────────────
cd /Users/chaosbookpro/recursion-node-manager
source ./.venv/bin/activate

# ─── Run the merge script ───────────────────────────────────────────────────
./merge_court_sessions.py \
  -d parsed_sessions/CourtGPT/Transcripts/Markdown \
  -o parsed_sessions/CourtGPT/all_court_sessions.md