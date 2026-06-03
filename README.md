# MidiPainter

**MidiPainter converts image contours into MIDI piano roll patterns.**

This project is currently in MVP stage with continued refinement planned.

[中文说明](README.zh-CN.md)

## Preview

![UI screenshot](docs/assets/ui.png)

## Features

- Import an image and extract visual contours.
- Convert contours into MIDI notes.
- Export `.mid` files for DAWs.
- Generate a piano roll preview image before opening a DAW.
- Generate an edge-detection preview for debugging.
- Control note density, pitch range, time length, contour filtering, and aspect ratio.
- Preserve image proportions with `contain` mode, or fill the full piano roll with `stretch` mode.

## Desktop MVP

Run the desktop app:

```powershell
python -m midipainter.app
```

The desktop MVP provides:

- image selection
- input image preview
- piano roll preview
- MIDI export
- edge preview export
- core conversion parameters
- conversion diagnostics

## CLI Usage

```powershell
python -m midipainter input.png output.mid --preview piano_roll.png --edge-preview edges.png
```

Example with common options:

```powershell
python -m midipainter input.png output.mid `
  --preview piano_roll.png `
  --edge-preview edges.png `
  --min-pitch 36 `
  --max-pitch 96 `
  --total-beats 64 `
  --note-beats 0.125 `
  --quantize-beats 0.125 `
  --aspect-mode contain `
  --display-aspect 2.012 `
  --min-contour-area 8 `
  --max-contours 512 `
  --simplify-epsilon 1.5 `
  --sample-step 2 `
  --max-notes 5000
```

## Aspect Modes

`contain` preserves the input image shape inside the piano roll viewport. Tall images get horizontal padding, and wide images get vertical padding. This is the default.

`stretch` fills the full configured time and pitch range. It uses space efficiently but may distort the source image.

`display-aspect` controls the physical width/height ratio used by `contain` mode. Adjust it if your DAW piano roll zoom differs from MidiPainter's preview.

## Development

Install dependencies in your preferred Python environment:

```powershell
python -m pip install numpy opencv-python Pillow matplotlib pytest
```

Run tests:

```powershell
python -m pytest
```

Run a syntax check:

```powershell
python -m compileall midipainter
```

## Roadmap

- Improve continuous line rendering in the piano roll.
- Add quality presets.
- Add better background removal and subject isolation.
- Add SVG input support.
- Add multi-track and color-aware MIDI export.
- Package portable Windows/macOS builds.

## Status

MidiPainter is currently an MVP. The core conversion pipeline works, but image processing and visual quality are still being refined.
