# Desktop Release Plan

MidiPainter ships as a desktop-first application for Windows and macOS, with Windows as the first packaged target.

## Current Runtime

The current desktop UI uses Python `tkinter` with a small native-feeling interface. The app is packaged with PyInstaller so users do not need to install Python.

## Release Artifacts

Windows releases should provide two download options:

- Portable zip: `MidiPainter-<version>-win64-portable.zip`
- Installer: `MidiPainter-<version>-win64-setup.exe`

The portable build is the primary artifact. The installer wraps the same bundled application folder with Start Menu and optional desktop shortcuts.

## Build Tools

- PyInstaller for the portable app bundle.
- Inno Setup for the Windows installer.
- GitHub Releases for publishing downloadable artifacts.

## Build Commands

Portable only:

```powershell
.\scripts\build_windows_release.ps1 -Version 0.1.0
```

Portable plus installer:

```powershell
.\scripts\build_windows_release.ps1 -Version 0.1.0 -BuildInstaller
```

The Inno Setup compiler `iscc.exe` must be available in `PATH` for installer builds.

## macOS Plan

macOS packaging should be built on macOS. The intended path is:

1. Use PyInstaller to create a `.app` bundle.
2. Package the app into a `.dmg`.
3. Add code signing and notarization before public distribution.

## Future UI Stack Decision

The current `tkinter` UI is enough for the first packaged release. If the app later needs richer native controls, likely upgrade paths are:

- PySide6 / Qt for a more native desktop application.
- Tauri for a small webview-based desktop shell.
- Electron only if rich web UI features become more important than bundle size.