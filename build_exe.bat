@echo off
setlocal

echo Installing ERPSuite Lite build dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Failed to install build dependencies.
  exit /b 1
)

echo Building ERPSuite Lite executable...
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
