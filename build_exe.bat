@echo off
title Building YouTube Downloader Executable
echo.
echo ========================================
echo   Building YouTube Downloader EXE
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/updating required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Building AllVideoDownloader executable with PyInstaller...
echo This may take several minutes...
echo.

pyinstaller --onefile --windowed --name AllVideoDownloader "v2\combined_gui.py"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo          BUILD SUCCESSFUL!
echo ========================================
echo.
echo The executable has been created in the 'dist' folder:
echo   dist\AllVideoDownloader.exe
echo.
echo You can now distribute this single file to users.
echo No Python installation required on target machines.
echo.

if exist "dist\AllVideoDownloader.exe" (
    echo Testing the executable...
    echo.
    start "" "dist\AllVideoDownloader.exe"
    echo.
    echo If the application starts successfully, the build is complete!
) else (
    echo WARNING: Executable not found in expected location.
)

echo.
pause
