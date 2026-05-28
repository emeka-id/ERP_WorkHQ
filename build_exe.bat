@echo off
setlocal

echo Installing ERPSuite Lite build dependencies...

python -m pip install -r requirements.txt

if errorlevel 1 (
  echo Failed to install requirements.
  exit /b 1
)

echo Building ERPSuite Lite executable...

python -m PyInstaller ^
--noconfirm ^
--windowed ^
--name "ERPSuite Lite" ^
app.py

if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo.
echo Build complete.
echo Executable:
echo dist\ERPSuite Lite\ERPSuite Lite.exe
echo.

endlocal