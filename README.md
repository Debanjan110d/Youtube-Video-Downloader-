# YouTube Video Downloader

A comprehensive Python application for downloading YouTube videos and playlists with both GUI and command-line interfaces. **Now available as a standalone executable!**

## 🚀 Quick Start Options

### Option 1: Standalone Executable (Recommended for most users)
- **No Python installation required!**
- Download the executable from the `dist/` folder
- Simply double-click `YouTubeDownloader.exe` to start
- Complete distribution package includes user guide and launcher

### Option 2: Python Source Code
- For developers and advanced users
- Requires Python 3.8+ installation
- Full source code access and customization

## Features

- 🎥 Download YouTube videos in various qualities (240p to 1080p+)
- 🎵 Download audio-only files (MP3 format)
- 📺 Download entire playlists
- 🖥️ **GUI Interface** - User-friendly graphical interface
- ⌨️ **CLI Interface** - Command-line interface for advanced users
- 📊 **Progress Tracking** - Real-time download progress with speed and ETA
- 🔍 **Video Information** - Get detailed video info before downloading
- 📁 **Custom Download Paths** - Choose where to save your downloads
- 🎯 **Quality Selection** - Select from available video qualities
- 🔄 **Batch Downloads** - Download multiple videos from playlists
- 📦 **Standalone Executable** - No dependencies required for end users

## Installation & Usage

### 🎯 For End Users (Executable Version)

**Easiest way - No Python needed:**

1. **Download the executable package**
   - Go to the `dist/` folder
   - Copy `YouTubeDownloader.exe` and related files

2. **Run the application**
   - Double-click `Start YouTube Downloader.bat` OR
   - Double-click `YouTubeDownloader.exe` directly

3. **First time setup**
   - Windows may show a security warning → Click "More info" → "Run anyway"
   - Some antivirus may scan the file (this is normal)

**Features of the executable:**
- ✅ Complete standalone application (20.3 MB)
- ✅ No Python installation required
- ✅ Includes GUI and CLI interfaces
- ✅ Works on Windows 10/11 (64-bit)
- ✅ User guide included

### 🔧 For Developers (Python Source)

**Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)

1. **Clone or download this repository**

   ```bash
   git clone <repository-url>
   cd youtube_downloader
   ```

2. **Install required dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Install FFmpeg** (required for audio extraction and some video formats)
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent

### 🏗️ Building Your Own Executable

If you want to create your own executable:

```bash
# Install build dependencies
pip install pyinstaller

# Run the build script
python build_exe.py
```

The executable will be created in the `dist/` folder.

## Usage

### GUI Interface (Recommended for beginners)

Run the GUI application:
```bash
python main.py
```
or
```bash
python gui.py
```

**GUI Features:**
- Paste YouTube URL and click "Get Info" to see video details
- Select video quality and download options
- Choose download location
- Track download progress with visual progress bar
- Download single videos or entire playlists

### Command Line Interface

Run the CLI application:
```bash
python main.py --cli
```
or
```bash
python cli.py
```

**CLI Commands:**

1. **Get video information:**
   ```bash
   python cli.py info "https://www.youtube.com/watch?v=VIDEO_ID"
   python cli.py info "URL" --show-formats --show-description
   ```

2. **Download video:**
   ```bash
   python cli.py download "https://www.youtube.com/watch?v=VIDEO_ID"
   python cli.py download "URL" --quality 720p
   python cli.py download "URL" --audio-only
   python cli.py download "URL" --output /path/to/downloads
   python cli.py download "URL" --filename "custom_name"
   ```

3. **Download playlist:**
   ```bash
   python cli.py download "PLAYLIST_URL" --playlist
   python cli.py download "PLAYLIST_URL" --playlist --max-downloads 5
   python cli.py download "PLAYLIST_URL" --playlist --audio-only
   ```

4. **List available qualities:**
   ```bash
   python cli.py list-qualities "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

### Advanced Usage

**Quality Options:**
- `best` - Best available quality (default)
- `worst` - Lowest available quality
- `1080p`, `720p`, `480p`, `360p`, `240p` - Specific resolutions

**CLI Options:**
- `--quality` / `-q`: Video quality
- `--audio-only` / `-a`: Download audio only (MP3)
- `--output` / `-o`: Output directory
- `--filename` / `-f`: Custom filename
- `--playlist` / `-p`: Download as playlist
- `--max-downloads` / `-m`: Limit playlist downloads

## Examples

### GUI Examples
1. Open the GUI and paste a YouTube URL
2. Click "Get Info" to see video details and available qualities
3. Select your preferred quality and options
4. Click "Download Video" or "Download Playlist"

### CLI Examples

**Basic video download:**
```bash
python cli.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Download 720p video:**
```bash
python cli.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --quality 720p
```

**Download audio only:**
```bash
python cli.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only
```

**Download to specific folder:**
```bash
python cli.py download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output "C:\My Videos"
```

**Download playlist (first 10 videos):**
```bash
python cli.py download "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --max-downloads 10
```

**Get video information:**
```bash
python cli.py info "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --show-formats --show-description
```

## File Structure

```
youtube_downloader/
├── YouTubeDownloader.exe    # 📦 STANDALONE EXECUTABLE (20.3 MB)
├── dist/                    # 📁 Distribution package
│   ├── YouTubeDownloader.exe
│   ├── Start YouTube Downloader.bat
│   ├── USER_GUIDE.md
│   └── README.txt
├── main.py                  # 🚀 Main launcher (chooses GUI/CLI)
├── youtube_downloader.py    # ⚙️ Core downloader class
├── gui.py                   # 🖥️ GUI interface
├── cli.py                   # ⌨️ Command-line interface
├── config.py                # ⚙️ Configuration management
├── utils.py                 # 🔧 Utility functions
├── launcher.py              # 🚀 Executable launcher script
├── build_exe.py             # 🏗️ Build script for executable
├── requirements.txt         # 📋 Python dependencies
└── README.md               # 📖 This file
```

## Distribution Options

### 📦 Executable Package (Recommended for end users)
- **Location**: `dist/YouTubeDownloader.exe`
- **Size**: ~20.3 MB
- **Requirements**: Windows 10/11 (64-bit), Internet connection
- **Includes**: Complete application with GUI and CLI
- **Installation**: None required - just run the .exe file

### 🐍 Python Source (For developers)
- **Location**: Root directory
- **Requirements**: Python 3.8+, pip, dependencies
- **Includes**: Full source code, customizable
- **Installation**: `pip install -r requirements.txt`

## Configuration

The application supports configuration through `config.py`:

- Default quality settings
- Download paths
- Filename templates
- Network settings
- GUI preferences

You can modify these settings by editing the `DEFAULT_SETTINGS` dictionary in `config.py`.

## Dependencies

- **yt-dlp**: YouTube downloader library
- **tkinter**: GUI framework (included with Python)
- **requests**: HTTP library
- **Pillow**: Image processing (for GUI icons)

## Troubleshooting

### For Executable Version

**"Windows protected your PC" message:**
- This is normal for unsigned executables
- Click "More info" then "Run anyway"

**Antivirus warnings:**
- Some antivirus software may flag PyInstaller executables as false positives
- Add the file to your antivirus whitelist
- Temporarily disable real-time protection during first run

**Executable doesn't start:**
- Try running from command line: `YouTubeDownloader.exe --cli`
- Check if Visual C++ redistributables are installed
- Ensure you have Windows 10/11 (64-bit)

### For Python Version

**"yt-dlp not found" error:**

   ```bash
   pip install yt-dlp
   ```

**Audio extraction fails:**
- Install FFmpeg (see installation instructions above)

**GUI doesn't start:**
- Use CLI mode: `python main.py --cli`
- Check if tkinter is installed: `python -c "import tkinter"`

### General Issues

**Download fails:**
- Check internet connection
- Verify YouTube URL is correct and video is available
- Try different quality settings
- Update yt-dlp: `pip install --upgrade yt-dlp`

**Permission errors:**
- Check write permissions for download directory
- Run as administrator (Windows) if needed

### Error Messages

- **"Invalid YouTube URL"**: Check the URL format
- **"Video not available"**: Video might be private, removed, or region-blocked
- **"Download failed"**: Network issue, invalid format, or YouTube changes

## Legal Notice

This tool is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download or that are in the public domain.

## Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Improving documentation

## License

This project is open source. Please check the license file for details.

## Support

If you encounter issues:
1. Check this README for solutions
2. Verify all dependencies are installed
3. Try the CLI interface if GUI fails
4. Check your internet connection
5. Ensure the YouTube URL is valid

## Changelog

### Version 1.0.0 (August 2025)
- ✅ Initial release
- ✅ GUI and CLI interfaces  
- ✅ Video and playlist downloads
- ✅ Audio-only downloads
- ✅ Progress tracking
- ✅ Quality selection
- ✅ Configuration system
- ✅ **Standalone executable version**
- ✅ PyInstaller build system
- ✅ Complete distribution package
- ✅ User guides and documentation

---

## 🎉 Ready to Use!

### For End Users:
1. Go to `dist/` folder
2. Double-click `YouTubeDownloader.exe` 
3. Start downloading! 🚀

### For Developers:
1. Run `python main.py` for GUI
2. Run `python cli.py --help` for CLI options
3. Modify source code as needed

**Built with ❤️ using Python, tkinter, yt-dlp, and PyInstaller**
#   Y o u t u b e - V i d e o - D o w n l o a d e r - 
 
 