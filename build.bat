@echo off
setlocal
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Nepodarilo sa nainstalovat zavislosti.
  pause
  exit /b 1
)
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ULTIMATE-QUIZ --add-data "quizzes.json;." main.py
if errorlevel 1 (
  echo Zostavenie EXE zlyhalo.
  pause
  exit /b 1
)
echo.
echo Hotovo! Program najdes v priecinku dist\ULTIMATE-QUIZ.exe
pause
