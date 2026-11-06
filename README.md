# Agent-native Self-Harness demo

A static project page introducing Agent-native self-evolution and two task demonstrations.

## Demo 1 source
- `data/demo1.json`: all Demo 1 content — stages, Agent trace, harness components, workspace images and the slide 14 comparison.
- `tools/build_demo1.py`: renders that JSON into `index.html` between `<!-- DEMO1:START -->` and `<!-- DEMO1:END -->`.
- `assets/demo1/deck.html`: the requested `exports/v004/deck.html` deliverable from `ppt-jpm-imagegen-20261104-r2`.
- `assets/demo1/v001-contact-sheet.png`, `v003-contact-sheet.png`, `v004-contact-sheet.png`: selected intermediate and final renders.
- `components/`: the persisted Agent, prompt, skill, and tools from the completed run.
- The trajectory view includes only execution batches 1–12 of 328. The v004 `deck.html` was exported in batch 6; the final acceptance result is reported separately from that 12-batch trajectory cutoff.

### Regenerating Demo 1

Run from the site root (Python 3.8+, no extra packages):

```
python tools/build_demo1.py           # rebuild index.html from data/demo1.json
python tools/build_demo1.py --sync    # first copy renders listed in sync.files from sync.source_root
python tools/build_demo1.py --watch   # rebuild on every change to data/, assets/ or components/
```

To swap in a new example, edit `data/demo1.json`: point `sync.source_root` at the new run and list its renders, then edit the `stages`. Each stage picks a tile scene (`loop`, `tool`, `review`, `extend`, `gate`, `auditor`), lists its four loop steps, its timestamped events, the state of every component (`new`, `updated`, `used`, `kept`, or an empty string for a component that is present but idle) and the workspace image. The script stops with a list of problems if a scene, component or asset path is wrong. `demo1.css` and `demo1.js` do not need changes.

## Demo 2 source
- `assets/codex-baseline-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied baseline Codex video.
- `assets/agent-native-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied Agent-native video.
- The MP4 files are embedded and played directly with native HTML video controls. They are not recompressed or transcoded. Poster images are separate preview frames.

Both demo videos are 15 seconds, 1920×1080 H.264 with AAC audio. The PPT source is JPMorgan Chase's public Third-Quarter 2021 earnings release: https://www.sec.gov/Archives/edgar/data/19617/000001961721000446/a3q21erfexhibit991narrative.htm

Open `index.html` directly for a local preview, or publish the repository root on GitHub Pages.
