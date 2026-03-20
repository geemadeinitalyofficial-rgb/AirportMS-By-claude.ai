"""
setup.py – py2exe build script for AirportMS
Usage:  python setup.py py2exe
"""

from distutils.core import setup
import py2exe
import sys
import os

# Make sure the current directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------------------ #
#  py2exe options                                                      #
# ------------------------------------------------------------------ #
options = {
    "py2exe": {
        # Bundle level 1 = everything into the .exe (largest but most portable)
        # Bundle level 2 = DLLs separate
        # Bundle level 3 = nothing bundled (default)
        "bundle_files": 2,

        # Compress the library archive
        "compressed": True,

        # Optimize: 0=none, 1=assert removed, 2=docstrings removed
        "optimize": 2,

        # Modules to explicitly include (py2exe sometimes misses these)
        "includes": [
            "PyQt5",
            "PyQt5.QtWidgets",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "PyQt5.QtSql",
            "sqlite3",
            "pyttsx3",
            "pyttsx3.drivers",
            "pyttsx3.drivers.sapi5",   # Windows SAPI5 TTS
            "csv",
            "json",
            "threading",
            "logging",
            "random",
            "datetime",
        ],

        # Packages to pull in completely
        "packages": [
            "PyQt5",
            "pyttsx3",
            "sqlite3",
            "encodings",
        ],

        # DLLs/files to exclude (reduces size)
        "excludes": [
            "tkinter",
            "unittest",
            "email",
            "html",
            "http",
            "urllib",
            "xml",
            "pydoc",
            "doctest",
            "argparse",
            "calendar",
            "ftplib",
        ],

        # Skip these DLLs (they will be found at runtime)
        "dll_excludes": [
            "MSVCP90.dll",
            "w9xpopen.exe",
        ],

        # Destination directory
        "dist_dir": "dist",
    }
}

# ------------------------------------------------------------------ #
#  Data files to include alongside the .exe                           #
# ------------------------------------------------------------------ #
data_files = [
    # Include the db directory (empty, will be created on first run)
    ("db", []),

    # Include any Qt platform plugins needed (important for PyQt5!)
    # These paths assume a standard Python/PyQt5 installation
    # Adjust if your PyQt5 is installed elsewhere
]

# Try to find Qt platform plugins automatically
try:
    import PyQt5
    qt_path = os.path.dirname(PyQt5.__file__)
    platforms_path = os.path.join(qt_path, "Qt5", "plugins", "platforms")
    if os.path.exists(platforms_path):
        platform_files = [os.path.join(platforms_path, f)
                          for f in os.listdir(platforms_path)
                          if f.endswith(".dll")]
        if platform_files:
            data_files.append(("platforms", platform_files))

    # Qt styles plugins (for dark theme)
    styles_path = os.path.join(qt_path, "Qt5", "plugins", "styles")
    if os.path.exists(styles_path):
        style_files = [os.path.join(styles_path, f)
                       for f in os.listdir(styles_path)
                       if f.endswith(".dll")]
        if style_files:
            data_files.append(("styles", style_files))
except Exception as e:
    print(f"Warning: Could not auto-detect Qt plugins: {e}")
    print("You may need to manually copy the 'platforms' folder next to the .exe")

# ------------------------------------------------------------------ #
#  Main setup call                                                     #
# ------------------------------------------------------------------ #
setup(
    name="AirportMS",
    version="1.0.0",
    description="Airport Management System",
    author="AirportMS",

    # GUI application (no console window)
    windows=[{
        "script": "main.py",
        "dest_base": "AirportMS",        # Output .exe name
        "icon_resources": [],             # Add: [(1, "assets/icon.ico")] if you have an icon
    }],

    # Console version (useful for debugging — comment out 'windows' above and use this)
    # console=[{
    #     "script": "main.py",
    #     "dest_base": "AirportMS_debug",
    # }],

    data_files=data_files,
    options=options,

    # Required for py2exe to find packages
    zipfile="library.zip",
)
