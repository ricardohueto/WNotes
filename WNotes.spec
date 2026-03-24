# WNotes.spec
import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, BUNDLE, COLLECT

block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("styles/theme.qss", "styles"),
        ("assets/icons/icon.ico", "assets/icons"),
        ("assets/icons/icon.icns", "assets/icons"),
    ],
    hiddenimports=["PyQt6.QtCore", "PyQt6.QtWidgets", "PyQt6.QtGui"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if sys.platform == "win32":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name="WNotes",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        console=False,
        icon="assets/icons/icon.ico",
    )

elif sys.platform == "darwin":
    exe = EXE(
        pyz,
        a.scripts,
        [],
        name="WNotes",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon="assets/icons/icon.icns",
    )
    app = BUNDLE(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        name="WNotes.app",
        icon="assets/icons/icon.icns",
        bundle_identifier="com.wnotes.app",
    )