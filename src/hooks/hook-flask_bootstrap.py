#!/usr/bin/env python3
"""Hook file to ensure pyinstaller can gather external
bootstrap resources (templates)
See also:
https://stackoverflow.com/a/59295693
https://pyinstaller.readthedocs.io/en/stable/hooks.html
"""

from PyInstaller.utils.hooks import collect_data_files


datas = collect_data_files('flask_bootstrap')
