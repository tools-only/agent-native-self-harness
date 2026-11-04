# Agent-native Self-Harness demo

A static project page introducing the quality-led, agent-owned self-harness loop, the real JPMorgan Chase Q3 2021 HTML presentation run, and two original GPT-6.1 Sol generated videos.

## Contents
- `index.html`, `styles.css`, `app.js`: static page source; no build step or external assets.
- `assets/presentation.html`: delivered 15-slide deck.
- `assets/*.png`: selected render evidence.
- `assets/codex-baseline-gpt-6.1-sol.mp4`: original baseline Codex generated video.
- `assets/agent-native-gpt-6.1-sol.mp4`: original Agent self-evolution generated video.
- `assets/*-poster.jpg`: still frames used only as video preview posters.
- `components/`: task-created reviewer, skill, validator, and quality map.

The video files are byte-for-byte copies of the supplied MP4s. The page embeds and plays those original files with native HTML video controls; they are not recompressed or transcoded. Posters are separate still frames and do not replace the videos. Both files are 15 seconds, 1920×1080 H.264 with AAC audio.

The PPT demo began with generic harness-learning guidance and no task-specific criteria, methods, or components preloaded. The Agent created the quality map and three components shown here during the task. The single run demonstrates the workflow and recorded evidence; it does not establish causal quality gain or cross-task net benefit.

The presentation uses JPMorgan Chase's publicly available Third-Quarter 2021 earnings release: https://www.sec.gov/Archives/edgar/data/19617/000001961721000446/a3q21erfexhibit991narrative.htm

## Local preview
Open `index.html` directly in a browser. The site is static and uses relative links, so it also works as a GitHub Pages project site.
