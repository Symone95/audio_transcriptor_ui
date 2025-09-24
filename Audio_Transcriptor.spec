# -*- mode: python ; coding: utf-8 -*-

import os
from kivy_deps import sdl2, glew
from kivy_deps.angle import includes as angle_includes
import whisper  # importa il pacchetto per trovare la cartella assets

# path dinamico alla cartella "assets" di whisper
whisper_assets = os.path.join(os.path.dirname(whisper.__file__), "assets")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icons/logo.icns', '.'),
           (whisper_assets, 'whisper/assets'),
            *sdl2.dep_bins,
            *glew.dep_bins,
            *angle_includes,
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Audio_Transcriptor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/logo.icns'],
)
app = BUNDLE(
    exe,
    name='Audio_Transcriptor.app',
    icon='icons/logo.icns',
    bundle_identifier=None,
)
