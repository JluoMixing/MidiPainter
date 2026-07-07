# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import site

from PyInstaller.utils.hooks import collect_dynamic_libs

ROOT = Path(SPECPATH).parents[1]
ENTRY = ROOT / "packaging" / "pyinstaller_entry.py"


def collect_numpy_libs():
    libs = []
    for site_dir in site.getsitepackages():
        numpy_libs = Path(site_dir) / "numpy.libs"
        if numpy_libs.exists():
            libs.extend((str(path), ".") for path in numpy_libs.glob("*.dll"))
    return libs


binaries = collect_dynamic_libs("numpy") + collect_dynamic_libs("cv2") + collect_numpy_libs()


a = Analysis(
    [str(ENTRY)],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=[
        (str(ROOT / "LICENSE"), "."),
        (str(ROOT / "README.md"), "."),
        (str(ROOT / "README.zh-CN.md"), "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "tests", "matplotlib.tests", "numpy.tests", "PIL.ImageQt"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MidiPainter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MidiPainter",
)