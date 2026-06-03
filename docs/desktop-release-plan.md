# Desktop Release Plan

MidiPainter is intended to ship as a desktop application for Windows and macOS.

## MVP Runtime

The current UI MVP uses Python `tkinter`.

Why this is a good first step:

- ships with standard Python on most distributions
- avoids a browser/web runtime
- keeps the codebase small while product behavior is still changing
- can be packaged into portable builds later

Tradeoffs:

- visual polish is more limited than Qt, Flutter, or Electron
- advanced UI components may require custom work
- macOS packaging and signing still need a dedicated release step

## Portable Version

A portable build means the user receives a folder or archive that contains:

- the MidiPainter app executable
- the Python runtime bundled by the packager
- required libraries
- application assets

The user should be able to unzip and run it without installing Python.

Likely packaging tool:

```text
PyInstaller
```

## Installer Version

An installer can come later, once the app behavior is stable.

Windows options:

- Inno Setup
- NSIS
- MSIX

macOS options:

- `.app` bundle inside `.dmg`
- code signing and notarization for smooth Gatekeeper behavior

## Future UI Stack Decision

If `tkinter` becomes limiting, likely upgrade paths are:

- PySide6 / Qt for a more native desktop application
- Tauri for a small webview-based desktop shell
- Electron only if rich web UI needs outweigh bundle size

For now, the best path is to validate the product workflow with the smallest desktop stack.
