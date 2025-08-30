# instagram_downloader.py
# Downloader for Instagram videos

import yt_dlp

def download_instagram_video(url, output_path, quality='best'):
    """
    Download Instagram video with quality selection
    """
    # Handle quality selection
    if quality == 'best':
        format_selector = 'best[ext=mp4]/best'
    elif quality == 'worst':
        format_selector = 'worst[ext=mp4]/worst'
    elif quality.endswith('p') and quality[:-1].isdigit():
        height = quality[:-1]
        format_selector = f'best[height<={height}][ext=mp4]/best[height<={height}]/best[ext=mp4]/best'
    else:
        format_selector = 'best[ext=mp4]/best'
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': format_selector,
        'quiet': True,  # Suppress output
        'no_warnings': True,  # Suppress warnings
        'ignoreerrors': True,  # Continue on errors
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
