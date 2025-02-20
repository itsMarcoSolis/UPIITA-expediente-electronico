from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('nicegui') + collect_submodules('nicegui_highcharts')
datas = collect_data_files('nicegui') + collect_data_files('nicegui_highcharts')


# Define PyInstaller analysis
a = Analysis(
    ['main.py'],  # Main entry script
    pathex=["."],  # Current directory
    binaries=[],
    datas=datas + [("static/favicon.ico", "static/favicon.ico")],  # Include static files
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='expediente-electronico',
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
    icon=['static\\favicon.ico'],
)


# Run PyInstaller with defined settings
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="expediente-electronico"
)
