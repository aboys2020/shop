# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec：轻量 CLI（无图表、无 pandas、无 Web 框架）。"""

import os

block_cipher = None

ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))

a = Analysis(
    [os.path.join(ROOT, "cli.py")],
    pathex=[ROOT],
    binaries=[],
    datas=[],
    hiddenimports=["core.scrapers.jd", "core.scrapers.taobao", "core.scrapers.pdd", "core.scrapers.demo"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pandas",
        "numpy",
        "matplotlib",
        "plotly",
        "fastapi",
        "uvicorn",
        "starlette",
        "pydantic",
        "python_multipart",
        "jinja2",
        "email_validator",
        "itsdangerous",
        "orjson",
        "ujson",
        "sqlalchemy",
        "tortoise",
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
    name="price_scraper_cli",
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
