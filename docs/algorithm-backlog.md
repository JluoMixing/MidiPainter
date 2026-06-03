# Algorithm Backlog

These items are intentionally deferred while the project moves into the desktop UI MVP.

## Line Continuity

- Interpolate contour paths into denser, visually continuous note runs.
- Optionally connect nearby contour fragments before MIDI mapping.
- Add a "line mode" that favors short adjacent notes over isolated scatter points.

## Shape Quality

- Add adaptive thresholding and background removal presets.
- Add subject-focused filtering to reduce background contour noise.
- Add SVG input support for cleaner path-based conversion.

## Note Control

- Improve density limiting so important contours survive aggressive note caps.
- Add per-region simplification instead of global sampling only.
- Add quality presets: Draft, Balanced, Detailed, DAW-safe.

## Musicality

- Add optional pitch scale snapping.
- Add velocity mapping from edge strength or image brightness.
- Add multi-track export based on color or contour groups.
