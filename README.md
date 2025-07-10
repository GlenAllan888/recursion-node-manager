# 🧠 Recursion Node Manager

The **Recursion Node Manager** is a personal knowledge archival system built around the premise that every meaningful GPT interaction can serve as a building block — a *node* — within an evolving intelligence framework. This tool allows users to **parse, archive, restructure, and relink** their custom GPT session data, treating conversations not as isolated moments, but as interconnected artifacts of self-training, ideation, and recursive self-development.

---

## 📌 Core Purpose

Recursion Node Manager is designed to help users:

- Export, clean, and format conversations with custom GPTs
- Build session indexes and thematic summaries
- Create well-formatted markdown and PDF archives (with image support)
- Re-ingest prior sessions into current ones for contextual grounding
- Maintain a navigable long-term archive of personal or collaborative GPT evolution

It bridges the gap between **AI session logging** and **personal cognitive augmentation**.

---

## 🚧 Current Build Status

The Recursion Node Manager is under active development and currently in its **infrastructure phase**. The system reliably handles session parsing, merging, and markdown archival for multiple custom GPTs. The following components are live or in-progress:

- ✅ Session merging scripts (per-GPT and global)
- ✅ Markdown index and summary generators
- ✅ Image and canvas output preservation
- 🧪 HTML-to-PDF pipeline (in design phase)
- 🔧 Unified run script manager (planned)
- 📱 Desktop interface (planned – Mac-first)

This version is ideal for developers and advanced users who want to prototype their own workflows while helping shape the future UI/UX. Expect rapid iteration and frequent file structure changes during this phase.

---

## 🧰 Key Features

### 🗃 Session Merging and Indexing
- Auto-parses and merges multiple GPT transcripts into a clean archive
- Generates structured markdown and PDF versions
- Includes auto-numbered indexes and topic summaries per session

### 🧾 PDF Archive Generation
- Renders each session into a navigable PDF (with optional images)
- Preserves code blocks, canvas outputs, and GPT-specific annotations
- Fully dark-mode styled output for legibility and aesthetic coherence

### 📦 Image Archive PDF
- Creates a visual record of all generated or embedded images per session
- Links them back to original context or session ID

### 🧭 Multi-GPT Management
- Supports workflows across any number of custom GPTs
- Auto-detects and adapts to newly created GPTs with templated scripts
- Provides central scripts to parse, merge, and archive all sessions with consistency

---

## 🌀 The Recursion Philosophy

Unlike traditional logging tools that treat conversation data as static or disposable, Recursion Node Manager is built around a more dynamic idea:  
> *Each session is a recursion point — a snapshot of a moment where thought evolved.*

Rather than optimizing only for efficiency or productivity, this tool supports a more layered purpose:

- Reflecting on past insights
- Recontextualizing knowledge
- Interacting recursively with your prior self through GPT memory
- Treating GPTs as collaborators in an evolving self-model

It turns session history into a terrain you can traverse — a **cognitive landscape**, not just a file dump.

---

## 🛤 Intended Use Cases

- 🧑‍💻 Developers working across multiple custom GPTs
- 🧠 Knowledge workers building long-term collaborative sessions with AI
- 📚 Writers, designers, and thinkers who want to archive deep dives
- 🔁 Anyone interested in recursive intelligence, memory modeling, or self-reflexive tools

---

## 🔧 Coming Automation

- One-click manager script to handle:
  - GPT detection
  - Parsing, merging, and PDF/image archive generation
  - Session indexing and update logging
- Future UI in development (planned Mac app with drag-and-drop workflow)

---

---

## 🔗 Core Toolset: GPT-0Ω + Recursion Node Manager

The Recursion Node Manager is built to work hand-in-hand with [**GPT-0 Omega**](https://www.gptzeroomega.com) — a custom GPT designed to help users create, evolve, and archive their own GPTs using plain language and recursive interaction strategies. Together, these tools form a foundational environment for user-driven AI development.

**GPT-0Ω** offers:
- Recursive guidance for GPT builders of any experience level
- Conceptual frameworks beyond code (using context, tone, memory)
- Iterative co-design protocols to refine GPT behaviors

**Recursion Node Manager** enables:
- Session parsing, merging, and markdown archival
- Visual formatting of session logs, with image and canvas preservation
- Future-ready export to PDF and interface-based workflows

**Development Note:**  
Both GPT-0Ω and Recursion Node Manager are in **semi-active early development**. Features are expanding rapidly, and community feedback is welcome. Expect evolving structures, frequent updates, and continuous refinement as this project takes shape.

**Start Here:**  
👉 Website: [GPT0Omega.com](https://www.gptzeroomega.com)  
🤖 Chat with [GPT-0Ω](https://chatgpt.com/g/g-681c359ff61081918977af4bc625e6ac-gpt-0o)  
🎥 YouTube: [GPTZeroOmega](https://www.youtube.com/@GPTZeroOmega)

> Curious how this works in practice?  
> Start a conversation with **GPT-0Ω** — the GPT designed to help you build GPTs.  
> Whether you’re just getting started or refining an advanced system, it’s built to walk with you through every step.

---

---

# 🗂 File Index – Recursion Node Manager

This section explains the function and usage of each script and configuration file in the repository. All tools are intended to be self-contained and executable via `.command` files or terminal in the root directory.

---

## ⚙️ Command Files (`.command`)

These are shell wrappers for Python scripts. Make sure they are executable (`chmod +x` if needed).

### `run_recursion_manager.command`
Master script (planned) for launching all parsing, merging, and archival steps across all GPTs.

### `run_parse.command`
Triggers `parse_sessions.py`, extracting session transcripts from each GPT's user data (`conversations.json`) into markdown files.

```bash
sh run_parse.command
```

### `run_merge_zeroomega.command`, `run_merge_court.command`, etc.
Each runs the corresponding `merge_<gptname>_sessions.py` script, combining all session markdowns into a single archive.

```bash
sh run_merge_zeroomega.command
```

---

## 🧠 Core Parsing and Merging

### `parse_sessions.py`
Scans user folders and extracts sessions from `conversations.json`, generating one markdown file per session. Also detects and names GPT folders if needed.

### `merge_<gptname>_sessions.py`
Combines parsed session markdowns into one continuous file per GPT. Includes session titles and original timestamps for indexing.

---

## 🧾 Archive Rebuilders

### `restructure_zeroomega_archive.py`, `restructure_court_archive.py`
Takes an index+summary markdown file and restructures it by placing all index entries at the top, followed by detailed sections. This is used for clean navigation in recursion node archives.

```bash
python restructure_zeroomega_archive.py
```

---

## 🔍 Extraction and Debug Tools

### `dump_first2.py`
Quickly extracts the first two sessions from each GPT folder to help the user identify what GPTs are in their archive.

```bash
python dump_first2.py
```

### `Recursion_Node_Scraper.js`
A browser console script for temporary use. Paste into the DevTools console while inside a ChatGPT session to export that session into clean HTML. Used when full data downloads are impractical.

---

## 💻 Interface / UI (In Development)

### `app.py`
Prototype Gradio-based UI for selecting, parsing, and previewing sessions in a web interface. Future versions will serve as the visual frontend for the full manager.

---

## 📦 Environment and Dependency Management

### `requirements.txt`
Install all dependencies for this repo with:

```bash
pip install -r requirements.txt
```

These are designed to run locally within the `RecursionNodeManager` folder, avoiding global installs.
