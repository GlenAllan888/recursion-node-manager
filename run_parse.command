#!/usr/bin/env bash
# ───────────────────────────────────────────────────────────────────────
# run_parse.command — Bootstraps venv, installs deps, and runs parser
# ───────────────────────────────────────────────────────────────────────

# 1) Jump into this script’s directory
cd "$(dirname "$0")"

# 2) Create a virtual env if it doesn't exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 3) Activate the virtual env
source .venv/bin/activate

# 4) Upgrade pip & install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 5) Invoke the parser with defaults
#    $1 → optional input JSON, defaulting to _UserData/conversations.json
#    $2 → optional output base,    defaulting to ParsedSessions
INPUT_FILE="${1:-_UserData/conversations.json}"
OUTPUT_DIR="${2:-parsed_sessions}"

python parse_sessions.py \
  -i "$INPUT_FILE" \
  -o "$OUTPUT_DIR"

# 6) Pause so user can see success message
echo
read -n 1 -r -p "🎉 Done! Press any key to close…"