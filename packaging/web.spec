# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec：Web 服务（含前端静态文件，无图表库）。"""

import os
from pathlib import Path

block_cipher = None

ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))
static_dir = Path(ROOT) / "backend" / "static"
datas = [(str(static_dir), "backend/static")] if static_dir.exists() else []

a = Analysis(
    [os.path.join(ROOT, "run.py")],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "backend.main",
        "backend.services.search",
        "core.scrapers.jd",
        "core.scrapers.taobao",
        "core.scrapers.pdd",
        "core.scrapers.demo",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pandas",
        "numpy",
        "matplotlib",
        "plotly",
        "PIL",
        "setuptools",
        "pkg_resources",
        "pytest",
        "unittest",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="price_scraper_web",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
