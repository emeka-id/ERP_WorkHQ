@echo off
setlocal

echo Building ERPSuite Lite executable...
python -m pip install pyinstaller
if errorlevel 1 (
  echo Failed to install PyInstaller.
  exit /b 1
)

pyinstaller --noconfirm --windowed --onefile --name "ERPSuite Lite" app.py
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo.
echo Build complete.
echo Executable: dist\ERPSuite Lite.exe
echo.
echo To launch from Desktop, copy dist\ERPSuite Lite.exe to your Desktop.

endlocal
