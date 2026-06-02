# VTT Studio

A browser-based **subtitle editor + translator** for WebVTT (`.vtt`) and SubRip (`.srt`) files. Single static HTML file — no build, no server, no dependencies. Everything runs in your browser; subtitles, video and API keys never leave the page except for the translation provider you choose.

**▶ Live app:** _enable GitHub Pages, then the URL appears here_

## Features

- **Edit** cue text and start/end times inline; add, delete, split-at-playhead and merge cues; undo/redo.
- **Video preview** — load any local video/audio and see captions live, with a playhead, click-to-seek and adjustable playback rate.
- **Timing** — global shift, shift/nudge selected cues, extend/shorten, set fixed duration, close gaps.
- **Timeline** — zoomable strip; drag blocks to move (whole selection together), drag edges to retime, rubber-band multi-select.
- **Speed rescale** — re-time captions when a video was sped up/slowed down (% change, raw factor, or map old→new duration, around a fixed pivot).
- **Find & replace** — plain or regex, case / whole-word / selection-only.
- **Translate** — DeepL, Microsoft (Azure), Google, LibreTranslate, or any OpenAI-compatible LLM. Translations are stored alongside the original until you commit. Irish (`ga`) via Microsoft/Google/LLM; Hiberno-English (`en-IE`) localisation via the LLM provider.

## Use it

Just open `index.html` — locally (double-click) or via the GitHub Pages URL above. No install.

## Translation notes

- You paste your own API key into the UI; it is never committed or sent anywhere but the chosen provider.
- **DeepL** blocks direct browser calls — paste a CORS-proxy prefix in the field provided. DeepL has no Irish.
- **Microsoft** needs your Azure region; **Google** uses an API key in the URL; **LibreTranslate** can be the public host or your own.

## Also included

`vttShift.py` — a tiny standalone CLI for headless/batch shifting:

```bash
python3 vttShift.py input.vtt output.vtt   # shifts by SHIFT_MS (edit the constant)
```

## Hosting on GitHub Pages

The repo root contains `index.html`, so: **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`**. Done.
