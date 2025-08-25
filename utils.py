"""
Utility functions for YouTube Video Downloader.
"""

import re
import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse, parse_qs


def is_valid_youtube_url(url: str) -> bool:
    """
    Check if a URL is a valid YouTube URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid YouTube URL
    """
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=[\w-]+',
        r'(?:https?://)?youtu\.be/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/c/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/user/[\w-]+',
        r'(?:https?://)?(?:www\.)?youtube\.com/@[\w-]+',
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        Optional[str]: Video ID if found
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)',
        r'youtube\.com/embed/([\w-]+)',
        r'youtube\.com/v/([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_playlist_id(url: str) -> Optional[str]:
    """
    Extract playlist ID from YouTube URL.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        Optional[str]: Playlist ID if found
    """
    match = re.search(r'list=([\w-]+)', url)
    return match.group(1) if match else None


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system use.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing periods and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename


def format_bytes(bytes_count: int) -> str:
    """
    Format bytes into human-readable string.
    
    Args:
        bytes_count (int): Number of bytes
        
    Returns:
        str: Formatted string
    """
    if bytes_count == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_count >= 1024 and i < len(size_names) - 1:
        bytes_count /= 1024.0
        i += 1
    
    return f"{bytes_count:.1f} {size_names[i]}"


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to HH:MM:SS or MM:SS.
    
    Args:
        seconds (int): Duration in seconds
        
    Returns:
        str: Formatted duration
    """
    if seconds < 0:
        return "00:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def format_number(number: int) -> str:
    """
    Format large numbers with thousand separators.
    
    Args:
        number (int): Number to format
        
    Returns:
        str: Formatted number
    """
    return f"{number:,}"


def create_safe_path(path: str) -> Path:
    """
    Create a safe path, creating directories if needed.
    
    Args:
        path (str): Path to create
        
    Returns:
        Path: Safe path object
    """
    safe_path = Path(path)
    safe_path.mkdir(parents=True, exist_ok=True)
    return safe_path


def get_available_formats(formats: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
    """
    Organize formats by type (video/audio).
    
    Args:
        formats (List[Dict]): List of format dictionaries
        
    Returns:
        Dict: Organized formats
    """
    video_formats = []
    audio_formats = []
    
    for fmt in formats:
        if fmt.get('vcodec') and fmt.get('vcodec') != 'none':
            video_formats.append(fmt)
        elif fmt.get('acodec') and fmt.get('acodec') != 'none':
            audio_formats.append(fmt)
    
    # Sort video formats by quality (height)
    video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
    
    # Sort audio formats by quality (abr - audio bitrate)
    audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
    
    return {
        'video': video_formats,
        'audio': audio_formats
    }


def check_ffmpeg() -> bool:
    """
    Check if FFmpeg is available in the system.
    
    Returns:
        bool: True if FFmpeg is available
    """
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


def get_terminal_size() -> tuple:
    """
    Get terminal size for progress bar formatting.
    
    Returns:
        tuple: (columns, rows)
    """
    try:
        return os.get_terminal_size()
    except OSError:
        return (80, 24)  # Default fallback


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying functions on error.
    
    Args:
        max_retries (int): Maximum number of retries
        delay (float): Delay between retries in seconds
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {max_retries + 1} attempts failed")
                        
            raise last_exception
        return wrapper
    return decorator


def validate_url_list(urls: List[str]) -> List[str]:
    """
    Validate a list of URLs and return only valid YouTube URLs.
    
    Args:
        urls (List[str]): List of URLs to validate
        
    Returns:
        List[str]: List of valid URLs
    """
    valid_urls = []
    for url in urls:
        url = url.strip()
        if url and is_valid_youtube_url(url):
            valid_urls.append(url)
    return valid_urls


def load_urls_from_file(file_path: str) -> List[str]:
    """
    Load URLs from a text file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        List[str]: List of valid URLs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        return validate_url_list(urls)
    except Exception as e:
        print(f"Error loading URLs from file: {e}")
        return []


def save_urls_to_file(urls: List[str], file_path: str) -> bool:
    """
    Save URLs to a text file.
    
    Args:
        urls (List[str]): List of URLs to save
        file_path (str): Path to save the file
        
    Returns:
        bool: True if successful
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        return True
    except Exception as e:
        print(f"Error saving URLs to file: {e}")
        return False


class ProgressTracker:
    """Simple progress tracker for downloads."""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_update = self.start_time
        
    def update(self, downloaded: int, total: int, speed: float = None):
        """Update progress information."""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if total > 0:
            percentage = (downloaded / total) * 100
            eta = (total - downloaded) / speed if speed and speed > 0 else 0
            
            print(f"\rProgress: {percentage:.1f}% "
                  f"({format_bytes(downloaded)}/{format_bytes(total)}) "
                  f"Speed: {format_bytes(int(speed))}/s " if speed else "" +
                  f"ETA: {format_duration(int(eta))}" if eta > 0 else "",
                  end='', flush=True)
        
        self.last_update = current_time
    
    def finish(self, filename: str = ""):
        """Mark progress as finished."""
        elapsed = time.time() - self.start_time
        print(f"\n✓ Completed in {format_duration(int(elapsed))}: {filename}")


if __name__ == "__main__":
    # Test utility functions
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/playlist?list=PLxxxxxx",
        "invalid_url",
        ""
    ]
    
    print("Testing URL validation:")
    for url in test_urls:
        valid = is_valid_youtube_url(url)
        video_id = extract_video_id(url)
        playlist_id = extract_playlist_id(url)
        print(f"URL: {url}")
        print(f"  Valid: {valid}")
        print(f"  Video ID: {video_id}")
        print(f"  Playlist ID: {playlist_id}")
        print()
    
    print("Testing format functions:")
    print(f"Bytes: {format_bytes(1536000)}")
    print(f"Duration: {format_duration(3665)}")
    print(f"Number: {format_number(1234567)}")
    print(f"Filename: {sanitize_filename('Test <video> file?.mp4')}")
