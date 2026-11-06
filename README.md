# Agent-native Self-Harness demo

A static project page introducing Agent-native self-evolution with a PPT run, a Kaggle run and a video comparison.

## Demo sources

Demo 1 (PPT) and Demo 2 (Kaggle) share one layout: six stage tiles, then a stage studio with three panes — Agent trace, workspace and the harness file tree. Each demo is one JSON file:

- `data/demo1.json`: the PPT run — stages, Agent trace, harness components, contact-sheet renders and the slide 14 comparison.
- `data/kaggle.json`: the Kaggle run — stages, Agent trace, harness components (skills, memory, reflections and the Python scripts in `work/`), and the CV / public LB points drawn in the workspace score chart.
- `tools/build_demos.py`: renders each JSON into `index.html` between its `<!-- MARKER:START -->` and `<!-- MARKER:END -->` comments (`DEMO1`, `KAGGLE`).
- `demo.css` and `demo.js`: shared styles and interaction for both sections.
- `assets/demo1/deck.html`: the requested `exports/v004/deck.html` deliverable from `ppt-jpm-imagegen-20261104-r2`.
- `assets/demo1/v001-contact-sheet.png`, `v003-contact-sheet.png`, `v004-contact-sheet.png`: selected intermediate and final renders.
- `components/`: the persisted Agent, prompt, skill, and tools from the PPT run.
- The PPT trajectory view includes only execution batches 1–12 of 328.

### Regenerating the demos

Run from the site root (Python 3.8+, no extra packages):

```
python tools/build_demos.py                    # rebuild every demo in index.html
python tools/build_demos.py data/kaggle.json   # rebuild only the Kaggle demo
python tools/build_demos.py --sync             # first copy files listed in each sync block
python tools/build_demos.py --watch            # rebuild on every change to data/, assets/ or components/
```

To update a demo, edit its JSON. Each stage picks a tile scene (`loop`, `tool`, `review`, `extend`, `gate`, `auditor`), lists its four loop steps, its events, the state of every component (`new`, `updated`, `used`, `kept`, or an empty string for a component that is present but idle) and its workspace. A workspace shows a contact-sheet `image`, or the score `chart` defined at the top of the file; `files` adds a short deliverable list under it. Components with `"counted": false` (runtime-provided prompt, skills or roles, inline snippets) are listed but not counted as Agent components; a `summary` given as a list renders as bullet notes. A lane with `"fold": true` folds earlier, untouched files into one row of names. For a running Kaggle job, add the new chart points, components and a stage, then rebuild. The script stops with a list of problems if a scene, component, chart stage or asset path is wrong.

## Video demo source
- `assets/codex-baseline-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied baseline Codex video.
- `assets/agent-native-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied Agent-native video.
- The MP4 files are embedded and played directly with native HTML video controls. They are not recompressed or transcoded. Poster images are separate preview frames.

Both demo videos are 15 seconds, 1920×1080 H.264 with AAC audio. The PPT source is JPMorgan Chase's public Third-Quarter 2021 earnings release: https://www.sec.gov/Archives/edgar/data/19617/000001961721000446/a3q21erfexhibit991narrative.htm

Open `index.html` directly for a local preview, or publish the repository root on GitHub Pages.
