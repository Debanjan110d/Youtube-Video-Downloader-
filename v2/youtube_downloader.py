import yt_dlp
import os
from pathlib import Path
from typing import Dict, List, Optional, Callable

try:
    from utils import get_ffmpeg_path
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False
    
def get_safe_ydl_opts_for_audio():
    """Get yt-dlp options that work without FFmpeg"""
    return {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
        'writeinfojson': False,
        'writesubtitles': False,
    }

class YouTubeDownloader:
    """
    Universal video downloader using yt-dlp for YouTube, Facebook, Instagram, X/Twitter, etc.
    """
    def __init__(self, download_path: str = "downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        self.progress_callback: Optional[Callable] = None
        self.is_downloading = False

    def set_progress_callback(self, callback: Callable):
        self.progress_callback = callback

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            if self.progress_callback:
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    progress_info = {
                        'downloaded': downloaded,
                        'total': total,
                        'percentage': (downloaded / total * 100) if total > 0 else 0,
                        'speed': speed,
                        'eta': eta,
                        'filename': d.get('filename', '')
                    }
                    self.progress_callback(progress_info)
                except Exception as e:
                    print(f"Progress callback error: {e}")
        elif d['status'] == 'finished':
            if self.progress_callback:
                self.progress_callback({
                    'status': 'finished',
                    'filename': d.get('filename', '')
                })

    def get_video_info(self, url: str) -> Dict:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_info = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': []
                }
                for fmt in info.get('formats', []):
                    if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none':
                        format_info = {
                            'format_id': fmt.get('format_id'),
                            'ext': fmt.get('ext'),
                            'quality': fmt.get('quality'),
                            'height': fmt.get('height'),
                            'width': fmt.get('width'),
                            'fps': fmt.get('fps'),
                            'vcodec': fmt.get('vcodec'),
                            'acodec': fmt.get('acodec'),
                            'filesize': fmt.get('filesize'),
                            'format_note': fmt.get('format_note', '')
                        }
                        video_info['formats'].append(format_info)
                return video_info
        except Exception as e:
            raise Exception(f"Error getting video info: {str(e)}")

    def download_video(self, url: str, quality: str = 'best', audio_only: bool = False, 
                      custom_filename: str = None, audio_quality: str = '192', 
                      normalize_audio: bool = True) -> str:
        try:
            self.is_downloading = True
            if custom_filename:
                outtmpl = str(self.download_path / f"{custom_filename}.%(ext)s")
            else:
                outtmpl = str(self.download_path / "%(title)s.%(ext)s")
            ydl_opts = {
                'outtmpl': outtmpl,
                'progress_hooks': [self._progress_hook],
                'quiet': True,  # Suppress output
                'no_warnings': True,  # Suppress warnings
                'ignoreerrors': True,  # Continue on errors
            }
            
            # Add FFmpeg location if available
            if FFMPEG_AVAILABLE:
                ffmpeg_path = get_ffmpeg_path()
                if ffmpeg_path:
                    ydl_opts['ffmpeg_location'] = ffmpeg_path
            
            if audio_only:
                # Simple audio extraction without complex post-processing
                ydl_opts.update({
                    'format': 'bestaudio[acodec^=mp4a]/bestaudio[ext=m4a]/bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                    'postprocessor_args': ['-loglevel', 'error'],
                    'ignoreerrors': True,
                })
            else:
                # Smart YouTube video quality settings with FFmpeg detection
                try:
                    # Check if FFmpeg is available for merging
                    import subprocess
                    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                    ffmpeg_available = True
                except:
                    ffmpeg_available = False
                
                if ffmpeg_available:
                    # FFmpeg available - use separate streams for highest quality
                    if quality == 'best':
                        ydl_opts['format'] = 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
                    elif quality == 'worst':
                        ydl_opts['format'] = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst'
                    elif quality.endswith('p') and quality[:-1].isdigit():
                        height = quality[:-1]
                        ydl_opts['format'] = f'bestvideo[height={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                    else:
                        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                else:
                    # No FFmpeg - use single streams for good quality without errors
                    if quality == 'best':
                        ydl_opts['format'] = 'best[height<=2160][ext=mp4]/best[height<=1440]/best[height<=1080]/best'
                    elif quality == 'worst':
                        ydl_opts['format'] = 'worst[ext=mp4]/worst'
                    elif quality.endswith('p') and quality[:-1].isdigit():
                        height = quality[:-1]
                        ydl_opts['format'] = f'best[height={height}][ext=mp4]/best[height<={height}]/best'
                    else:
                        ydl_opts['format'] = 'best[ext=mp4]/best'
                
                # Add audio normalization for video downloads if requested
                if normalize_audio:
                    # Keep it simple - just ensure we get good quality without complex post-processing
                    pass
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.is_downloading = False
            return "Download completed successfully!"
        except Exception as e:
            self.is_downloading = False
            raise Exception(f"Download failed: {str(e)}")

    def download_playlist(self, url: str, quality: str = 'best', audio_only: bool = False, max_downloads: int = None) -> str:
        try:
            self.is_downloading = True
            ydl_opts = {
                'outtmpl': str(self.download_path / "%(playlist_index)s - %(title)s.%(ext)s"),
                'progress_hooks': [self._progress_hook],
            }
            if max_downloads:
                ydl_opts['playlistend'] = max_downloads
            if audio_only:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                if quality == 'best':
                    ydl_opts['format'] = 'best[ext=mp4]/best'
                elif quality == 'worst':
                    ydl_opts['format'] = 'worst[ext=mp4]/worst'
                elif quality.endswith('p') and quality[:-1].isdigit():
                    # Handle specific resolutions like '1080p', '720p', etc.
                    height = quality[:-1]
                    ydl_opts['format'] = f'best[height<={height}][ext=mp4]/best[height<={height}]/best[ext=mp4]/best'
                else:
                    # Fallback to best quality
                    ydl_opts['format'] = 'best[ext=mp4]/best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.is_downloading = False
            return "Playlist download completed successfully!"
        except Exception as e:
            self.is_downloading = False
            raise Exception(f"Playlist download failed: {str(e)}")

    def get_available_qualities(self, url: str) -> List[str]:
        try:
            info = self.get_video_info(url)
            qualities = set()
            for fmt in info['formats']:
                if fmt['height']:
                    qualities.add(f"{fmt['height']}p")
            qualities.update(['best', 'worst'])
            return sorted(list(qualities), key=lambda x: (
                0 if x == 'best' else 
                1 if x == 'worst' else 
                int(x[:-1])
            ), reverse=True)
        except Exception:
            return ['best', 'worst', '1080p', '720p', '480p', '360p', '240p']
