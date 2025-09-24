# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import whisper  # importa il pacchetto per trovare la cartella assets

# path dinamico alla cartella "assets" di whisper
whisper_assets = os.path.join(os.path.dirname(whisper.__file__), "assets")

# base datas (comuni a tutti i sistemi)
datas = [
    ('icons/logo.icns', '.'),
    (whisper_assets, 'whisper/assets')
]
binaries = []

# aggiungi solo su Windows le dipendenze di Kivy
if sys.platform.startswith("win"):
    import kivy_deps.sdl2 as sdl2
    import kivy_deps.glew as glew
    import kivy_deps.angle as angle
    binaries = [
        *sdl2.dep_bins,
        *glew.dep_bins,
        *angle.dep_bins,   # occhio: è dep_bins, non includes
    ]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
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
