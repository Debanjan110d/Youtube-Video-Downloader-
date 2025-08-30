# facebook_downloader.py
# Downloader for Facebook videos

import yt_dlp

def download_facebook_video(url, output_path):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best[ext=mp4]/best/worst',  # Try mp4 first, then best available, then worst as fallback
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': True,  # Continue on errors
        'no_warnings': True,  # Suppress warnings
        'quiet': True,  # Suppress output
        'extractaudio': False,
        'audioformat': 'mp3',
        'embed_subs': False,
        'allsubtitles': False
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # First try to extract info to see what formats are available
            info = ydl.extract_info(url, download=False)
            print(f"Video title: {info.get('title', 'Unknown')}")
            print(f"Available formats: {len(info.get('formats', []))}")
            
            # Now download with the configured options
            ydl.download([url])
            
    except Exception as e:
        print(f"Facebook download failed: {e}")
        # Try with even more permissive options
        fallback_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'worst',  # Just get any available format
            'no_warnings': True,
            'quiet': True,
            'ignoreerrors': True
        }
        
        try:
            with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                ydl.download([url])
        except Exception as e2:
            raise Exception(f"Facebook download failed with both attempts: {e}, {e2}")
