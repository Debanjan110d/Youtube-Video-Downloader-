# YouTube Downloader - Executable Version

## Quick Start Guide

### What is this?
This is a standalone executable version of the YouTube Video Downloader. You can run it directly without installing Python or any dependencies.

### How to Use

#### Method 1: Double-click to start GUI
1. Simply double-click `YouTubeDownloader.exe`
2. The graphical interface will open
3. Paste a YouTube URL and click "Get Info"
4. Choose your download options and click "Download Video"

#### Method 2: Command Line Usage
1. Open Command Prompt or PowerShell
2. Navigate to the folder containing `YouTubeDownloader.exe`
3. Use commands like:
   ```
   YouTubeDownloader.exe --cli info "https://youtube.com/watch?v=..."
   YouTubeDownloader.exe --cli download "https://youtube.com/watch?v=..." --quality 720p
   ```

### Features
- ✅ Download YouTube videos in various qualities
- ✅ Download audio-only files (MP3)
- ✅ Download entire playlists
- ✅ Progress tracking with speed and ETA
- ✅ Easy-to-use graphical interface
- ✅ Command-line interface for advanced users
- ✅ No Python installation required

### System Requirements
- Windows 10/11 (64-bit)
- Internet connection
- ~25 MB disk space for the executable

### Download Options
- **Quality**: best, 1080p, 720p, 480p, 360p, 240p, worst
- **Format**: MP4 (video), MP3 (audio-only)
- **Destination**: Choose any folder on your computer

### Troubleshooting

#### "Windows protected your PC" message
This is normal for unsigned executables. Click "More info" then "Run anyway".

#### Antivirus warnings
Some antivirus software may flag PyInstaller executables. This is a false positive. You can:
1. Add the file to your antivirus whitelist
2. Temporarily disable real-time protection during download

#### Download fails
- Check your internet connection
- Verify the YouTube URL is correct and the video is available
- Try a different quality setting

#### GUI doesn't open
- Try running from command line: `YouTubeDownloader.exe --cli`
- Check if your system has the required Visual C++ redistributables

### Support
If you encounter issues:
1. Try the command-line version for better error messages
2. Check if the YouTube URL is accessible in your browser
3. Ensure you have a stable internet connection

### Legal Notice
This tool is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.

---

**File**: YouTubeDownloader.exe  
**Version**: 1.0.0  
**Size**: ~20 MB  
**Created**: August 2025
