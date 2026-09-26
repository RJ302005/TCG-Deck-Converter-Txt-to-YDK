# -*- mode: python ; coding: utf-8 -*-

import os
import customtkinter

# Obtener la ruta de instalación de customtkinter en tu equipo
ctk_path = os.path.dirname(customtkinter.__file__)

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluye la carpeta de assets de customtkinter dentro del paquete final
        (ctk_path, 'customtkinter/')
    ],
    hiddenimports=[],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YGO_Deck_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set a False para ocultar la consola negra de comandos detrás de la ventana
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='app_icon.ico' # Si deseas agregarle un icono .ico personalizado al ejecutable
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YGO_Deck_Converter',
)