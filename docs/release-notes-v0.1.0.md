# MidiPainter 0.1.0

First packaged desktop release of MidiPainter.

## Highlights

- Desktop app for converting image contours into MIDI piano-roll patterns.
- Input image preview and generated piano-roll preview.
- MIDI export for DAWs.
- Optional edge-detection preview for checking contour extraction.
- Aspect-ratio preservation with `contain` mode and full-range mapping with `stretch` mode.
- Detail control for balancing cleaner output and denser contour detail.
- Windows portable package and installer-ready release workflow.

## Downloads

- `MidiPainter-0.1.0-win64-portable.zip`: unzip and run `MidiPainter.exe`.
- `MidiPainter-0.1.0-win64-setup.exe`: run the installer and launch from the Start Menu.

## Known Notes

- Windows is the first packaged target.
- macOS packaging is planned separately and should be built on macOS.
- Some DAWs may display piano-roll spacing differently depending on zoom and note height; adjust aspect mode and display aspect if needed.