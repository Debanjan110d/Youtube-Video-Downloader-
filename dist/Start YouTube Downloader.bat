@echo off
title YouTube Video Downloader

echo.
echo ==========================================
echo     YouTube Video Downloader v1.0
echo ==========================================
echo.
echo Starting the application...
echo.

:: Start the executable
start "" "%~dp0YouTubeDownloader.exe"

:: Optional: Keep this window open for a moment
timeout /t 2 /nobreak >nul

:: Close this command window
exit
