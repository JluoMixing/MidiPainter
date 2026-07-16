# Release Packaging

This document describes how to produce downloadable MidiPainter release artifacts.

## Release Artifacts

For Windows releases, publish both files when possible:

- `MidiPainter-<version>-win64-portable.zip`
- `MidiPainter-<version>-win64-setup.exe`

The portable zip can be extracted and run without installing Python. The installer uses the same bundled application folder and adds Start Menu / optional desktop shortcuts.

## Windows Portable Build

Requirements:

- Windows 10/11
- Python 3.9+
- Project dependencies installed
- PyInstaller installed: `python -m pip install pyinstaller`

Build:

```powershell
.\scripts\build_windows_release.ps1 -Version 0.2.0
```

Skip tests when doing a quick local packaging check:

```powershell
.\scripts\build_windows_release.ps1 -Version 0.2.0 -SkipTests
```

The script writes:

```text
dist/MidiPainter-0.2.0-win64-portable/
dist/MidiPainter-0.2.0-win64-portable.zip
```

## Windows Installer

Install Inno Setup and ensure `iscc.exe` is available in `PATH`, then run:

```powershell
.\scripts\build_windows_release.ps1 -Version 0.2.0 -BuildInstaller
```

The installer script is:

```text
packaging/windows/MidiPainter.iss
```

Expected output:

```text
dist/MidiPainter-0.2.0-win64-setup.exe
```

## Manual Smoke Test

After building, test the portable folder before uploading a release:

1. Open `dist/MidiPainter-<version>-win64-portable/MidiPainter.exe`.
2. Load a sample image.
3. Drop an image into the input preview and confirm the piano-roll preview appears without creating a PNG file.
4. Change Aspect or Min Pitch and confirm the preview updates automatically.
5. Click Convert MIDI, choose a destination, and confirm the `.mid` file is written.
5. Open the generated `.mid` in a DAW or MIDI editor.

## GitHub Release Checklist

1. Update version references if needed.
2. Run tests: `python -m pytest`.
3. Build portable zip.
4. Build installer if Inno Setup is available.
5. Smoke test the portable app.
6. Create a GitHub release tag, for example `v0.2.0`.
7. Upload the portable zip and installer.
8. Add a short release note with highlights, known limitations, and installation instructions.

## macOS Notes

macOS packaging should be built on macOS. A future release script can use PyInstaller to create a `.app` bundle, then package it into a `.dmg`. Code signing and notarization are recommended for public releases.
