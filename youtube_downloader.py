import yt_dlp
import os
import sys
import threading
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json


class YouTubeDownloader:
    """
    A comprehensive YouTube video downloader class using yt-dlp.
    Supports various download formats, quality options, and progress tracking.
    """
    
    def __init__(self, download_path: str = "downloads"):
        """
        Initialize the YouTube downloader.
        
        Args:
            download_path (str): Directory where downloads will be saved
        """
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        self.progress_callback: Optional[Callable] = None
        self.is_downloading = False
        
    def set_progress_callback(self, callback: Callable):
        """Set a callback function to track download progress."""
        self.progress_callback = callback
        
    def _progress_hook(self, d):
        """Internal progress hook for yt-dlp."""
        if d['status'] == 'downloading':
            if self.progress_callback:
                try:
                    # Extract progress information
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
        """
        Get video information without downloading.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            Dict: Video information including title, duration, formats, etc.
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract relevant information
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
                
                # Extract available formats
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
    
    def download_video(self, url: str, quality: str = 'best', 
                      audio_only: bool = False, custom_filename: str = None) -> str:
        """
        Download a YouTube video.
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality ('best', 'worst', '720p', '480p', etc.)
            audio_only (bool): Download audio only
            custom_filename (str): Custom filename for the download
            
        Returns:
            str: Path to the downloaded file
        """
        try:
            self.is_downloading = True
            
            # Configure output filename
            if custom_filename:
                outtmpl = str(self.download_path / f"{custom_filename}.%(ext)s")
            else:
                outtmpl = str(self.download_path / "%(title)s.%(ext)s")
            
            # Base options
            ydl_opts = {
                'outtmpl': outtmpl,
                'progress_hooks': [self._progress_hook],
            }
            
            if audio_only:
                # Audio-only download
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                # Video download with quality selection
                if quality == 'best':
                    ydl_opts['format'] = 'best'
                elif quality == 'worst':
                    ydl_opts['format'] = 'worst'
                else:
                    # For any specific quality, just use 'best' as fallback
                    ydl_opts['format'] = 'best'
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.is_downloading = False
            return "Download completed successfully!"
            
        except Exception as e:
            self.is_downloading = False
            raise Exception(f"Download failed: {str(e)}")
    
    def download_playlist(self, url: str, quality: str = 'best', 
                         audio_only: bool = False, max_downloads: int = None) -> str:
        """
        Download a YouTube playlist.
        
        Args:
            url (str): YouTube playlist URL
            quality (str): Video quality
            audio_only (bool): Download audio only
            max_downloads (int): Maximum number of videos to download
            
        Returns:
            str: Status message
        """
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
                    ydl_opts['format'] = 'best'
                elif quality == 'worst':
                    ydl_opts['format'] = 'worst'
                else:
                    # For any specific quality, just use 'best' as fallback
                    ydl_opts['format'] = 'best'
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.is_downloading = False
            return "Playlist download completed successfully!"
            
        except Exception as e:
            self.is_downloading = False
            raise Exception(f"Playlist download failed: {str(e)}")
    
    def cancel_download(self):
        """Cancel the current download."""
        # Note: yt-dlp doesn't have a direct cancel method
        # This is a placeholder for future implementation
        self.is_downloading = False
        
    def get_available_qualities(self, url: str) -> List[str]:
        """
        Get available video qualities for a URL.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            List[str]: List of available qualities
        """
        try:
            info = self.get_video_info(url)
            qualities = set()
            
            for fmt in info['formats']:
                if fmt['height']:
                    qualities.add(f"{fmt['height']}p")
            
            # Add standard options
            qualities.update(['best', 'worst'])
            
            return sorted(list(qualities), key=lambda x: (
                0 if x == 'best' else 
                1 if x == 'worst' else 
                int(x[:-1])
            ), reverse=True)
            
        except Exception:
            return ['best', 'worst', '1080p', '720p', '480p', '360p', '240p']


def main():
    """Simple command-line interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python youtube_downloader.py <youtube_url> [quality] [audio_only]")
        print("Example: python youtube_downloader.py 'https://www.youtube.com/watch?v=...' 720p")
        return
    
    url = sys.argv[1]
    quality = sys.argv[2] if len(sys.argv) > 2 else 'best'
    audio_only = len(sys.argv) > 3 and sys.argv[3].lower() == 'true'
    
    downloader = YouTubeDownloader()
    
    def progress_callback(info):
        if 'percentage' in info:
            print(f"\rProgress: {info['percentage']:.1f}% "
                  f"Speed: {info.get('speed', 0) / 1024 / 1024:.1f} MB/s", end='')
        elif info.get('status') == 'finished':
            print(f"\nFinished: {info['filename']}")
    
    downloader.set_progress_callback(progress_callback)
    
    try:
        print(f"Getting video info...")
        info = downloader.get_video_info(url)
        print(f"Title: {info['title']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"Uploader: {info['uploader']}")
        
        print(f"\nStarting download...")
        result = downloader.download_video(url, quality, audio_only)
        print(f"\n{result}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
