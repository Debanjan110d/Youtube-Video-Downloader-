"""
Configuration settings for YouTube Video Downloader.
"""

import os
from pathlib import Path

# Default settings
DEFAULT_SETTINGS = {
    # Download settings
    'default_quality': 'best',
    'default_format': 'mp4',
    'audio_format': 'mp3',
    'audio_quality': '192',
    
    # Paths
    'download_path': 'downloads',
    'temp_path': 'temp',
    
    # Filename templates
    'video_filename_template': '%(title)s.%(ext)s',
    'playlist_filename_template': '%(playlist_index)s - %(title)s.%(ext)s',
    'audio_filename_template': '%(title)s.%(ext)s',
    
    # Download limits
    'max_concurrent_downloads': 3,
    'max_retries': 3,
    'retry_delay': 5,  # seconds
    
    # Network settings
    'timeout': 30,  # seconds
    'rate_limit': None,  # KB/s, None for unlimited
    
    # GUI settings
    'window_width': 800,
    'window_height': 600,
    'theme': 'default',
    
    # Advanced options
    'extract_flat': False,
    'write_description': False,
    'write_info_json': False,
    'write_annotations': False,
    'write_thumbnail': False,
    'embed_subs': False,
    'write_automatic_subs': False,
}

class Config:
    """Configuration manager for the YouTube downloader."""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or self._get_default_config_path()
        self.settings = DEFAULT_SETTINGS.copy()
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        config_dir = Path.home() / '.youtube_downloader'
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / 'config.json')
    
    def load_config(self):
        """Load configuration from file."""
        try:
            import json
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_settings = json.load(f)
                self.settings.update(user_settings)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            import json
            config_dir = Path(self.config_file).parent
            config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Set a configuration value."""
        self.settings[key] = value
    
    def update(self, **kwargs):
        """Update multiple configuration values."""
        self.settings.update(kwargs)
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = DEFAULT_SETTINGS.copy()
    
    def get_ydl_opts(self, custom_opts: dict = None) -> dict:
        """Get yt-dlp options based on current configuration."""
        opts = {
            'format': self.get('default_quality'),
            'outtmpl': self.get('video_filename_template'),
            'retries': self.get('max_retries'),
            'socket_timeout': self.get('timeout'),
            'extract_flat': self.get('extract_flat'),
            'writeinfojson': self.get('write_info_json'),
            'writedescription': self.get('write_description'),
            'writeannotations': self.get('write_annotations'),
            'writethumbnail': self.get('write_thumbnail'),
            'writesubtitles': self.get('embed_subs'),
            'writeautomaticsub': self.get('write_automatic_subs'),
        }
        
        # Rate limiting
        if self.get('rate_limit'):
            opts['ratelimit'] = self.get('rate_limit') * 1024
        
        # Custom options override defaults
        if custom_opts:
            opts.update(custom_opts)
        
        return opts


# Global configuration instance
config = Config()
