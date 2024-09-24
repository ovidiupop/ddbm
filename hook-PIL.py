from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('PIL')
hiddenimports.append('PIL._tkinter_finder')