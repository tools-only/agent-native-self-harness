---
name: acceptance_check
description: "Read-only release gate for the current offline HTML earnings deck."
---
Before delivery, validate the current latest rendered deck. Require exactly 15 slides, source citations on every slide containing sourced financial figures, no scene-bound warnings, functional previous/next and keyboard navigation, print pagination with one slide per page, and at least 2 embedded self-contained images. Return a pass/fail result with evidence. Never alter the presentation.