# vimeo_downloader.py
# Downloader for Vimeo videos

import yt_dlp

def download_vimeo_video(url, output_path):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
