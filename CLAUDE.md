# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

VTT Studio — a browser-based subtitle **editor + translator**. Two deliverables:

- **`index.html`** — the app. A single self-contained file (no build, no deps, no server). Open directly or serve via MAMP at `http://localhost:8888/VTTshift/`. All logic — parsing, editing, timeline, video sync, translation — lives in one inline `<script>` IIFE. Everything runs client-side; the only outbound calls are to whichever translation provider the user picks.
- **`vttShift.py`** — the original standalone CLI (`python3 vttShift.py in.vtt out.vtt`), kept for headless/batch shifting. Shift amount is the hardcoded `SHIFT_MS` constant; WebVTT-only.

## index.html architecture

Single global `App` state object holds `cues` (`{id,start,end,text,settings,ident,trans}`, times in **ms**), selection set, undo/redo stacks, format, and timeline zoom. Key pieces:

- **Parse/serialize** — `loadText` detects VTT vs SRT, preserves the `WEBVTT` header, cue identifiers, and cue settings (e.g. `line:90%`); `toVTT`/`toSRT` round-trip them. `RANGE` regex matches both `.mmm` and `,mmm`; `parseTime` accepts `HH:MM:SS.mmm` or `MM:SS.mmm` with either separator.
- **History** — `snapshot()` deep-clones `cues` to a JSON stack before every mutation; undo/redo swap between `history`/`future`. Any new mutating op MUST call `snapshot()` first or it won't be undoable.
- **Render** — `renderTable` (editable cue grid) and `renderTimeline` (zoomable DOM-block strip) are the only re-render paths; call `renderAll()` after mutations. During timeline drag, `paintDrag()` updates block positions live without history, then `mouseup` commits one clean snapshot.
- **Selection** — `App.selection` (Set of ids) is the shared currency for "selected" across table rows and timeline blocks. Shift/Ctrl-click ranges, rubber-band on empty timeline. Most timing/text/translate ops take a `scope` of `'all'` or `'sel'`.
- **Video sync** — `timeupdate` → `syncVideo()` finds the active cue, drives the overlay, highlights the row, moves the playhead. Times are ms throughout; video API is seconds (×1000).
- **Translation** — `callProvider(texts)` dispatches per provider; `translate(scope)` batches cues and writes results to `cue.trans` (kept separate from `cue.text` until the user commits). `resolveTarget` maps UI language codes to each provider's quirks.

## Translation provider notes (when touching `callProvider`)

- **DeepL** — blocks browser CORS (use the proxy-prefix field); free keys end in `:fx` (→ `api-free` host); has **no Irish (ga)** — `resolveTarget` flags it.
- **Microsoft (Azure)** — needs the region header; supports `ga`. **Google** v2 — key in URL. **LibreTranslate** — per-line, not batched.
- **Custom LLM** — any OpenAI-compatible `/chat/completions`; returns a JSON array. This is the only path that does real **Hiberno-English (en-IE)** localisation; MT engines fall back to plain English for `en-IE`.
- Keys are pasted in the UI and never persisted server-side. Don't add code that logs or transmits them anywhere but the chosen provider.

## Conventions

- All cue times are integer **milliseconds** internally; format only at render/serialize via `fmt(ms,sep)`.
- Negative times clamp to 0 (`clamp0`) — matches the Python tool's behaviour.
- No external libraries — keep it dependency-free and single-file. Validate JS edits with `node --check` after extracting the `<script>` block.
