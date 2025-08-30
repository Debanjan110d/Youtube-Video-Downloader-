# Usage

## 🚀 Quick Start - V3.0.0 Pro

### Download and Run
1. **[Download AllVideoDownloaderPro.exe](https://github.com/Debanjan110d/Youtube-Video-Downloader-/releases/tag/V3)**
2. **Run the executable** - No installation required!
3. **Start downloading** from multiple platforms

### Using the GUI

#### Basic Download
1. **Select Platform**: Choose from YouTube, Facebook, Instagram, Vimeo, Dailymotion
2. **Enter URL**: Paste the video or playlist URL
3. **Choose Quality**: Select from Best, 4K, QHD, 1080p, 720p, 480p, 360p, or Audio Only
4. **Set Output Folder**: Browse and select your download location
5. **Click Download**: Watch real-time progress with speed and percentage

#### Advanced Features
- **Video Info**: Click "Get Video Info" to see title, duration, uploader, view count
- **Audio Only**: Select "Audio Only (MP3)" for high-quality audio downloads
- **Playlist Support**: Works automatically with playlist URLs
- **Quality Check**: Available qualities are auto-detected per video

### Running from Source

```sh
# Navigate to v2 directory
cd v2/

# Run the GUI
python combined_gui.py
```

### Building EXE (Developers)

```sh
# Install PyInstaller
pip install pyinstaller

# Build from spec file
pyinstaller AllVideoDownloaderPro.spec

# EXE will be in dist/ folder
```

## 🎯 Platform-Specific Tips

### YouTube
- **Best Quality**: Uses advanced format strings for maximum quality
- **FFmpeg Integration**: Automatically merges separate video+audio streams when available
- **Audio Normalization**: Consistent audio levels across downloads

### Facebook/Instagram
- **Private Content**: May require login for private videos
- **Story Downloads**: Supports story URLs from public accounts

### Vimeo
- **HD Support**: Downloads highest available quality
- **Password Protected**: Supports password-protected videos

### Dailymotion
- **Multiple Formats**: Automatically selects best available format
- **Regional Content**: Works with region-specific content

## 📊 Quality Selection Guide

| Quality | Resolution | Use Case |
|---------|------------|----------|
| **Best** | Up to 4K | Maximum quality available |
| **4K** | 2160p | Ultra-high definition |
| **QHD** | 1440p | High definition+ |
| **1080p** | 1080p | Full HD |
| **720p** | 720p | HD |
| **480p** | 480p | Standard definition |
| **360p** | 360p | Low bandwidth |
| **Audio Only** | MP3 | Music/podcasts |

## 🔧 Troubleshooting

### Common Issues
- **Poor Quality**: Ensure FFmpeg is available for best results
- **Download Fails**: Check internet connection and URL validity
- **Slow Downloads**: Try different quality settings
- **Audio Issues**: Audio normalization requires FFmpeg

### Error Messages
- **"FFmpeg not available"**: Quality limited to single-stream formats
- **"Video unavailable"**: Video may be private or removed
- **"Format not available"**: Try different quality setting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

### Author: Debanjan Dutta
