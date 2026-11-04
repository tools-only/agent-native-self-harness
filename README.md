# Agent-native Self-Harness demo

A static project page introducing Agent-native self-evolution and two task demonstrations.

## Demo 1 source
- `assets/demo1/deck.html`: the requested `exports/v004/deck.html` deliverable from `ppt-jpm-imagegen-20261104-r2`.
- `assets/demo1/v001-contact-sheet.png`, `v003-contact-sheet.png`, `v004-contact-sheet.png`: selected intermediate and final renders.
- `components/`: the persisted Agent, prompt, skill, and tools at the delivery cutoff.
- The trajectory view intentionally includes only the first 12 lifecycle records and stops at the v004 `deck.html` delivery event.

## Demo 2 source
- `assets/codex-baseline-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied baseline Codex video.
- `assets/agent-native-gpt-6.1-sol.mp4`: byte-for-byte copy of the supplied Agent-native video.
- The MP4 files are embedded and played directly with native HTML video controls. They are not recompressed or transcoded. Poster images are separate preview frames.

Both demo videos are 15 seconds, 1920×1080 H.264 with AAC audio. The PPT source is JPMorgan Chase's public Third-Quarter 2021 earnings release: https://www.sec.gov/Archives/edgar/data/19617/000001961721000446/a3q21erfexhibit991narrative.htm

Open `index.html` directly for a local preview, or publish the repository root on GitHub Pages.
