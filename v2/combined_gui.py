# combined_gui.py
# GUI for selecting and downloading videos from multiple platforms

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

# Import downloaders
from youtube_downloader import YouTubeDownloader
from vimeo_downloader import download_vimeo_video
from dailymotion_downloader import download_dailymotion_video
from facebook_downloader import download_facebook_video
from instagram_downloader import download_instagram_video

PLATFORMS = {
    "YouTube": lambda url, path: YouTubeDownloader(path).download_video(url),
    "Vimeo": download_vimeo_video,
    "Dailymotion": download_dailymotion_video,
    "Facebook": download_facebook_video,
    "Instagram": download_instagram_video,
}

class VideoDownloaderGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("All Video Downloader")
        self.geometry("480x400")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")

        self.platform_var = tk.StringVar(value="YouTube")
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar()

        self.create_widgets()


    def create_widgets(self):
        # Title
        title = tk.Label(self, text="All Video Downloader", font=("Segoe UI", 18, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=(20, 10))

        # Platform selection
        platform_frame = tk.Frame(self, bg="#f5f5f5")
        platform_frame.pack(pady=5)
        platform_label = tk.Label(platform_frame, text="Select Platform:", font=("Segoe UI", 12), bg="#f5f5f5")
        platform_label.pack(side=tk.LEFT, padx=(0, 10))
        platform_menu = ttk.Combobox(platform_frame, textvariable=self.platform_var, values=list(PLATFORMS.keys()), state="readonly", width=15)
        platform_menu.pack(side=tk.LEFT)

        # URL entry
        url_frame = tk.Frame(self, bg="#f5f5f5")
        url_frame.pack(pady=10)
        url_label = tk.Label(url_frame, text="Video URL:", font=("Segoe UI", 12), bg="#f5f5f5")
        url_label.pack(side=tk.LEFT, padx=(0, 10))
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, width=35, font=("Segoe UI", 11))
        url_entry.pack(side=tk.LEFT)

        # Quality selection (hidden by default)
        self.quality_frame = tk.Frame(self, bg="#f5f5f5")
        self.quality_label = tk.Label(self.quality_frame, text="Select Quality:", font=("Segoe UI", 12), bg="#f5f5f5")
        self.quality_label.pack(side=tk.LEFT, padx=(0, 10))
        self.quality_var = tk.StringVar()
        self.quality_menu = ttk.Combobox(self.quality_frame, textvariable=self.quality_var, state="readonly", width=15)
        self.quality_menu.pack(side=tk.LEFT)

        # Button to check qualities
        check_quality_btn = tk.Button(self, text="Check Available Qualities", command=self.check_qualities, font=("Segoe UI", 10), bg="#ff9800", fg="white", width=22)
        check_quality_btn.pack(pady=5)

        # Output folder selection
        out_frame = tk.Frame(self, bg="#f5f5f5")
        out_frame.pack(pady=10)
        out_label = tk.Label(out_frame, text="Output Folder:", font=("Segoe UI", 12), bg="#f5f5f5")
        out_label.pack(side=tk.LEFT, padx=(0, 10))
        out_entry = tk.Entry(out_frame, textvariable=self.output_path_var, width=25, font=("Segoe UI", 11))
        out_entry.pack(side=tk.LEFT)
        browse_btn = tk.Button(out_frame, text="Browse", command=self.browse_folder, font=("Segoe UI", 10))
        browse_btn.pack(side=tk.LEFT, padx=5)

        # Audio only checkbox
        self.audio_only_var = tk.BooleanVar()
        audio_chk = tk.Checkbutton(self, text="Download as MP3 (audio only)", variable=self.audio_only_var, bg="#f5f5f5", font=("Segoe UI", 11))
        audio_chk.pack(pady=5)

        # Info and Download buttons
        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=10)
        info_btn = tk.Button(btn_frame, text="Get Video Info", command=self.get_video_info, font=("Segoe UI", 11), bg="#2196f3", fg="white", width=15)
        info_btn.pack(side=tk.LEFT, padx=10)
        download_btn = tk.Button(btn_frame, text="Download", command=self.start_download, font=("Segoe UI", 12, "bold"), bg="#4caf50", fg="white", width=15, height=1)
        download_btn.pack(side=tk.LEFT, padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self, text="", font=("Segoe UI", 10), bg="#f5f5f5", fg="#333")
        self.status_label.pack(pady=5)
    def check_qualities(self):
        url = self.url_var.get().strip()
        platform = self.platform_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return
        try:
            if platform == "YouTube":
                yt = YouTubeDownloader()
                qualities = yt.get_available_qualities(url)
            else:
                import yt_dlp
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                qualities = []
                for fmt in info.get('formats', []):
                    if fmt.get('height'):
                        qualities.append(f"{fmt['height']}p")
                qualities = list(sorted(set(qualities), key=lambda x: int(x[:-1]) if x[:-1].isdigit() else 0, reverse=True))
                qualities += ['best', 'worst']
            if qualities:
                self.quality_menu['values'] = qualities
                self.quality_var.set(qualities[0])
                self.quality_frame.pack(pady=5)
                messagebox.showinfo("Qualities Found", f"Available qualities: {', '.join(qualities)}")
            else:
                self.quality_frame.pack_forget()
                messagebox.showinfo("No Qualities", "No quality options found for this video.")
        except Exception as e:
            self.quality_frame.pack_forget()
            messagebox.showerror("Quality Error", f"Failed to get qualities: {str(e)}")
    def get_video_info(self):
        url = self.url_var.get().strip()
        platform = self.platform_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL.")
            return
        try:
            if platform == "YouTube":
                yt = YouTubeDownloader()
                info = yt.get_video_info(url)
            else:
                # Use yt-dlp directly for other platforms
                import yt_dlp
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=False)
                info = {
                    'title': data.get('title', 'Unknown'),
                    'duration': data.get('duration', 0),
                    'uploader': data.get('uploader', 'Unknown'),
                    'view_count': data.get('view_count', 0),
                    'description': data.get('description', ''),
                    'upload_date': data.get('upload_date', ''),
                    'thumbnail': data.get('thumbnail', ''),
                }
            # Format info for display
            info_str = f"Title: {info['title']}\nDuration: {info['duration']}s\nUploader: {info['uploader']}\nViews: {info['view_count']}\nUpload Date: {info['upload_date']}\n\nDescription:\n{info['description']}"
            messagebox.showinfo("Video Info", info_str)
        except Exception as e:
            messagebox.showerror("Info Error", f"Failed to get video info: {str(e)}")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path_var.set(folder)

    def start_download(self):
        url = self.url_var.get().strip()
        platform = self.platform_var.get()
        output_path = self.output_path_var.get().strip()
        quality = self.quality_var.get().strip() if self.quality_var.get() else 'best'
        audio_only = self.audio_only_var.get()
        if not url or not output_path:
            messagebox.showerror("Error", "Please enter a URL and select output folder.")
            return
        downloader = PLATFORMS.get(platform)
        self.status_label.config(text=f"Downloading from {platform}...")
        self.progress['value'] = 0
        self.update_idletasks()
        try:
            # For YouTube, show progress and quality
            if platform == "YouTube":
                yt = YouTubeDownloader(output_path)
                def progress_callback(info):
                    if 'percentage' in info:
                        self.progress['value'] = info['percentage']
                        self.status_label.config(text=f"Downloading: {info['percentage']:.2f}%")
                        self.update_idletasks()
                    elif info.get('status') == 'finished':
                        self.progress['value'] = 100
                        self.status_label.config(text="Download finished!")
                        self.update_idletasks()
                yt.set_progress_callback(progress_callback)
                yt.download_video(url, quality=quality, audio_only=audio_only)
            else:
                import yt_dlp
                ydl_opts = {
                    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                    'format': quality if quality else 'best',
                }
                if audio_only:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                self.progress['value'] = 100
                self.status_label.config(text="Download finished!")
            messagebox.showinfo("Success", f"Downloaded from {platform}!")
        except Exception as e:
            self.status_label.config(text="Download failed.")
            messagebox.showerror("Download Failed", str(e))

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.mainloop()
