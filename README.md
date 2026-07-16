# MidiPainter

**Turn image contours into MIDI piano-roll drawings.**

MidiPainter converts the visible outlines of an image into a standard `.mid` file. Open the exported MIDI in your DAW, and the notes appear as a piano-roll pattern based on the original picture.

[中文说明](README.zh-CN.md)

## Preview

![MidiPainter UI](docs/assets/ui.png)


## What It Does

- Converts images into MIDI piano-roll patterns.
- Exports standard `.mid` files for DAWs and MIDI editors.
- Shows a piano-roll preview before you open your DAW.
- Lets you drop an image directly into the input preview, or choose it from a file picker.
- Preserves image proportions with `contain` mode, or fills the full piano-roll range with `stretch` mode.
- Lets you adjust pitch range, timeline length, and visual detail from a simple desktop interface.


## Quick Start

1. Open `MidiPainter.exe`.
2. Drop a PNG, JPG, JPEG, WEBP, or BMP image into the input area, or click **Open Image**.
3. Adjust **Aspect**, **Pitch Range**, **Total Beats**, and **Detail** if needed.
4. Click **Preview Only** to update the in-app piano-roll preview; setting changes update it automatically.
5. Click **Convert MIDI**, then choose the destination in the save dialog (which opens beside the input image).
6. Import the `.mid` file into your DAW.

## Tips For Better Results

- Use high-contrast images with clear outlines.
- Simple logos, icons, drawings, and portraits usually work better than busy photos.
- Use `contain` mode when you want to preserve the original image shape.
- Use `stretch` mode when you want the result to fill the full piano-roll area.
- Increase Detail for more contour information; reduce it for fewer notes and cleaner shapes.
- If your DAW view looks wider or taller than the preview, adjust zoom or try a different timeline length.

## Desktop App

The desktop app is the recommended way to use MidiPainter. It includes:

- input image preview
- piano-roll preview
- MIDI export
- drag-and-drop image input
- in-app preview with no preview image files written
- export save dialog, opening in the input image's folder
- aspect mode selection
- pitch range and timeline controls
- a Detail slider for balancing clean output and dense contour detail
- conversion stats such as contour count and note count

## Command Line Usage

MidiPainter also includes a CLI for repeatable conversion.

Basic conversion:

```powershell
python -m midipainter input.png output.mid
```

Generate MIDI plus preview images:

```powershell
python -m midipainter input.png output.mid `
  --preview piano_roll.png `
  --edge-preview edges.png
```

Common parameters:

```powershell
python -m midipainter input.png output.mid `
  --preview piano_roll.png `
  --edge-preview edges.png `
  --min-pitch 36 `
  --max-pitch 96 `
  --total-beats 64 `
  --note-beats 0.125 `
  --quantize-beats 0.125 `
  --velocity 84 `
  --aspect-mode contain `
  --display-aspect 2.012 `
  --max-width 512 `
  --canny-low 80 `
  --canny-high 180 `
  --min-contour-points 4 `
  --min-contour-area 8 `
  --max-contours 512 `
  --simplify-epsilon 1.5 `
  --sample-step 2 `
  --max-notes 5000
```

## Run From Source

Requirements:

- Python 3.9 or newer
- Windows or macOS
- A DAW or MIDI editor for opening exported `.mid` files

Install and run:

```powershell
python -m pip install -e .
python -m midipainter.app
```

Run tests:

```powershell
python -m pytest
```

## Current Limitations

- Very detailed images can produce many notes and may be heavy for some DAWs.
- Background clutter can create unwanted contours.
- The visual result may vary depending on DAW zoom, note height, and piano-roll display settings.
- Windows is the first packaged target; macOS packaging is not included yet.

## Roadmap

- Better background cleanup and subject isolation.
- SVG/path input for cleaner source artwork.
- Optional musical mapping features such as scale snapping and velocity mapping.
- Color-aware or multi-track MIDI export.
- macOS packaged builds.


## License

MIT License. See [LICENSE](LICENSE).
