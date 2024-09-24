pyinstaller --onefile --add-data "icons:icons" --add-data "help/info.txt:help" --add-data "backup:backup" --hidden-import PIL._tkinter_finder --additional-hooks-dir=. main.py
