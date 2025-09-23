import platform
import os

if platform.system() == "Windows":
    os.system(r".venv\Scripts\pyinstaller.exe --onefile --windowed --icon=icons/logo.ico --name=Audio_Transcriptor main.py")
elif platform.system() == "Darwin":  # macOS
    # togliere " --onefile" per farlo senza terminale
    os.system(".venv/bin/pyinstaller --onefile --windowed --name Audio_Transcriptor --icon=icons/logo.icns --add-data icons/logo.icns:. main.py")
else:  # Linux
    os.system(".venv/bin/pyinstaller --onefile --windowed --icon=icons/logo.png --name=Audio_Transcriptor main.py")
