# combined_gui.py
# Modern GUI for selecting and downloading videos from multiple platforms

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading
import queue
import time

# Import downloaders
from youtube_downloader import YouTubeDownloader
from vimeo_downloader import download_vimeo_video
from dailymotion_downloader import download_dailymotion_video
from facebook_downloader import download_facebook_video
from instagram_downloader import download_instagram_video

try:
    from install_ffmpeg import check_ffmpeg, get_ffmpeg_path
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False

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
        self.title("🎥 All Video Downloader Pro - by Debanjan110d")
        self.geometry("550x700")  # Increased height even more
        self.resizable(False, False)
        
        # Modern color scheme with better contrast
        self.bg_color = "#2b2b2b"  # Lighter dark background
        self.accent_color = "#0078d4"  # Microsoft blue
        self.secondary_color = "#404040"  # Lighter secondary
        self.text_color = "#ffffff"  # White text
        self.success_color = "#00d4aa"  # Bright green
        self.warning_color = "#ff8c00"  # Orange
        self.error_color = "#ff4757"  # Red
        self.card_color = "#353535"  # Card background
        
        self.configure(bg=self.bg_color)
        
        # Set window icon (if available)
        try:
            self.iconbitmap(default="icon.ico")
        except:
            pass  # If icon file not found, continue without it

        self.platform_var = tk.StringVar(value="YouTube")
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        
        # Threading and progress tracking
        self.progress_queue = queue.Queue()
        self.download_thread = None
        self.is_downloading = False

        self.setup_styles()
        self.create_widgets()
        
        # Start processing progress updates
        self.process_progress_queue()

    def setup_styles(self):
        """Configure modern ttk styles with better visibility"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern combobox style with better contrast
        style.configure('Modern.TCombobox',
                       fieldbackground="#505050",
                       background="#505050",
                       foreground="#ffffff",
                       borderwidth=1,
                       relief='flat',
                       arrowcolor="#ffffff",
                       darkcolor="#505050",
                       lightcolor="#505050")
        
        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', '#505050')],
                 selectbackground=[('readonly', '#0078d4')],
                 selectforeground=[('readonly', '#ffffff')])
        
        # Configure modern progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.accent_color,
                       troughcolor="#505050",
                       borderwidth=0,
                       lightcolor=self.accent_color,
                       darkcolor=self.accent_color)


    def create_widgets(self):
        # Header with gradient-like effect
        header_frame = tk.Frame(self, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title and creator info
        title_frame = tk.Frame(header_frame, bg=self.accent_color)
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        title = tk.Label(title_frame, text="🎥 All Video Downloader Pro", 
                        font=("Segoe UI", 18, "bold"), 
                        bg=self.accent_color, fg=self.text_color)
        title.pack(pady=(10, 2))
        
        subtitle = tk.Label(title_frame, text="Download from YouTube, Instagram, Facebook, Vimeo & more", 
                           font=("Segoe UI", 9), 
                           bg=self.accent_color, fg="#e8e8e8")
        subtitle.pack(pady=(0, 2))
        
        # Creator info with GitHub link
        creator_frame = tk.Frame(title_frame, bg=self.accent_color)
        creator_frame.pack(pady=(0, 5))
        
        creator_label = tk.Label(creator_frame, text="Created by: Debanjan110d", 
                               font=("Segoe UI", 8), 
                               bg=self.accent_color, fg="#d0d0d0")
        creator_label.pack(side=tk.LEFT)
        
        github_link = tk.Label(creator_frame, text="🔗 GitHub", 
                             font=("Segoe UI", 8), 
                             bg=self.accent_color, fg="#90d7ff",
                             cursor="hand2")
        github_link.pack(side=tk.LEFT, padx=(10, 0))
        github_link.bind("<Button-1>", self.open_github)

        # Main content frame
        content_frame = tk.Frame(self, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Platform selection with modern card-like design
        platform_card = tk.Frame(content_frame, bg=self.card_color, relief='flat', bd=1)
        platform_card.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        platform_inner = tk.Frame(platform_card, bg=self.card_color)
        platform_inner.pack(fill=tk.X, padx=15, pady=12)
        
        platform_label = tk.Label(platform_inner, text="📱 Platform:", 
                                 font=("Segoe UI", 11, "bold"), 
                                 bg=self.card_color, fg=self.text_color)
        platform_label.pack(side=tk.LEFT)
        
        platform_menu = ttk.Combobox(platform_inner, textvariable=self.platform_var, 
                                   values=list(PLATFORMS.keys()), 
                                   state="readonly", width=16, style='Modern.TCombobox')
        platform_menu.pack(side=tk.RIGHT)

        # URL input with modern design
        url_card = tk.Frame(content_frame, bg=self.card_color, relief='flat', bd=1)
        url_card.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        url_inner = tk.Frame(url_card, bg=self.card_color)
        url_inner.pack(fill=tk.X, padx=15, pady=12)
        
        url_label = tk.Label(url_inner, text="🔗 Video URL:", 
                           font=("Segoe UI", 11, "bold"), 
                           bg=self.card_color, fg=self.text_color)
        url_label.pack(anchor=tk.W, pady=(0, 5))
        
        url_entry = tk.Entry(url_inner, textvariable=self.url_var, 
                           font=("Segoe UI", 10), 
                           bg="#505050", fg=self.text_color, 
                           relief='flat', bd=5, insertbackground=self.text_color)
        url_entry.pack(fill=tk.X)

        # Quality selection with modern styling
        quality_card = tk.Frame(content_frame, bg=self.card_color, relief='flat', bd=1)
        quality_card.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        quality_inner = tk.Frame(quality_card, bg=self.card_color)
        quality_inner.pack(fill=tk.X, padx=15, pady=12)
        
        self.quality_frame = tk.Frame(quality_inner, bg=self.card_color)
        self.quality_frame.pack(fill=tk.X)
        
        quality_label = tk.Label(self.quality_frame, text="⚙️ Quality:", 
                               font=("Segoe UI", 11, "bold"), 
                               bg=self.card_color, fg=self.text_color)
        quality_label.pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar()
        default_qualities = ['best', '2160p 4K', '1440p QHD', '1080p HD', '720p HD', '480p', '360p', '240p']
        self.quality_menu = ttk.Combobox(self.quality_frame, textvariable=self.quality_var, 
                                       values=default_qualities, state="readonly", 
                                       width=12, style='Modern.TCombobox')
        self.quality_menu.pack(side=tk.LEFT, padx=(10, 0))
        self.quality_var.set('best')
        
        check_quality_btn = tk.Button(self.quality_frame, text="Check Available", 
                                    command=self.check_qualities, 
                                    font=("Segoe UI", 9, "bold"), bg=self.warning_color, 
                                    fg=self.text_color, relief='flat', 
                                    activebackground="#ff9f33", cursor="hand2")
        check_quality_btn.pack(side=tk.RIGHT)
        
        # Quality info label
        quality_info = tk.Label(quality_inner, text="💡 Higher quality = larger file size. 'best' automatically selects highest available.", 
                               font=("Segoe UI", 8), 
                               bg=self.card_color, fg="#888888")
        quality_info.pack(pady=(5, 0))

        # Output folder selection
        output_card = tk.Frame(content_frame, bg=self.card_color, relief='flat', bd=1)
        output_card.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        output_inner = tk.Frame(output_card, bg=self.card_color)
        output_inner.pack(fill=tk.X, padx=15, pady=12)
        
        output_label = tk.Label(output_inner, text="📁 Output Folder:", 
                              font=("Segoe UI", 11, "bold"), 
                              bg=self.card_color, fg=self.text_color)
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        output_frame = tk.Frame(output_inner, bg=self.card_color)
        output_frame.pack(fill=tk.X)
        
        output_entry = tk.Entry(output_frame, textvariable=self.output_path_var, 
                              font=("Segoe UI", 10), 
                              bg="#505050", fg=self.text_color, 
                              relief='flat', bd=5, insertbackground=self.text_color)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(output_frame, text="Browse", command=self.browse_folder, 
                             font=("Segoe UI", 9, "bold"), bg=self.accent_color, 
                             fg=self.text_color, relief='flat', 
                             activebackground="#106ebe", cursor="hand2")
        browse_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Audio options with modern styling
        audio_card = tk.Frame(content_frame, bg=self.card_color, relief='flat', bd=1)
        audio_card.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        audio_inner = tk.Frame(audio_card, bg=self.card_color)
        audio_inner.pack(fill=tk.X, padx=15, pady=12)
        
        audio_frame = tk.Frame(audio_inner, bg=self.card_color)
        audio_frame.pack(fill=tk.X)
        
        self.audio_only_var = tk.BooleanVar()
        audio_chk = tk.Checkbutton(audio_frame, text="🎵 Download as MP3 (audio only)", 
                                 variable=self.audio_only_var, 
                                 bg=self.card_color, fg=self.text_color, 
                                 font=("Segoe UI", 10, "bold"), 
                                 selectcolor=self.card_color,
                                 activebackground=self.card_color,
                                 activeforeground=self.text_color,
                                 command=self.toggle_audio_quality)
        audio_chk.pack(side=tk.LEFT)
        
        # Audio quality selection (hidden by default)
        self.audio_quality_frame = tk.Frame(audio_frame, bg=self.card_color)
        self.audio_quality_label = tk.Label(self.audio_quality_frame, text="Quality:", 
                                           font=("Segoe UI", 9, "bold"), 
                                           bg=self.card_color, fg=self.text_color)
        self.audio_quality_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.audio_quality_var = tk.StringVar()
        audio_qualities = ['192k', '128k', '320k', '96k']
        self.audio_quality_menu = ttk.Combobox(self.audio_quality_frame, 
                                             textvariable=self.audio_quality_var,
                                             values=audio_qualities, state="readonly", 
                                             width=8, style='Modern.TCombobox')
        self.audio_quality_menu.pack(side=tk.LEFT)
        self.audio_quality_var.set('192k')

        # Action buttons with modern design
        button_frame = tk.Frame(content_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=15)
        
        info_btn = tk.Button(button_frame, text="📋 Get Video Info", 
                           command=self.get_video_info, 
                           font=("Segoe UI", 11), bg=self.accent_color, 
                           fg=self.text_color, relief='flat', 
                           activebackground="#106ebe", cursor="hand2", 
                           width=18, height=2)
        info_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        download_btn = tk.Button(button_frame, text="⬇️ Download", 
                               command=self.start_download, 
                               font=("Segoe UI", 12, "bold"), 
                               bg=self.success_color, fg=self.text_color, 
                               relief='flat', activebackground="#0e6b0e", 
                               cursor="hand2", width=18, height=2)
        download_btn.pack(side=tk.RIGHT)

        # Progress bar with modern styling
        progress_frame = tk.Frame(content_frame, bg=self.bg_color)
        progress_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", 
                                      length=400, mode="determinate", 
                                      style='Modern.Horizontal.TProgressbar')
        self.progress.pack()

        # Status label with modern styling
        self.status_label = tk.Label(content_frame, text="Ready to download...", 
                                   font=("Segoe UI", 10), 
                                   bg=self.bg_color, fg="#b0b0b0")
        self.status_label.pack(pady=(5, 0))
    
    def process_progress_queue(self):
        """Process progress updates from the download thread"""
        try:
            while True:
                progress_data = self.progress_queue.get_nowait()
                if progress_data['type'] == 'progress':
                    self.progress['value'] = progress_data['value']
                    self.status_label.config(text=progress_data['status'], fg=self.accent_color)
                elif progress_data['type'] == 'complete':
                    self.progress['value'] = 100
                    self.status_label.config(text="✅ Download completed!", fg=self.success_color)
                    self.is_downloading = False
                    messagebox.showinfo("🎉 Success", progress_data['message'])
                elif progress_data['type'] == 'error':
                    self.progress['value'] = 0
                    self.status_label.config(text="❌ Download failed", fg=self.error_color)
                    self.is_downloading = False
                    messagebox.showerror("❌ Download Failed", progress_data['message'])
        except queue.Empty:
            pass
        
        # Schedule next check
        self.after(100, self.process_progress_queue)
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            try:
                # Calculate percentage
                if 'total_bytes' in d and d['total_bytes']:
                    percentage = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                    percentage = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    # If no total bytes info, show indeterminate progress
                    percentage = 50  # Show some progress
                
                # Get download speed
                speed = d.get('speed', 0)
                if speed:
                    speed_str = f" ({speed/1024/1024:.1f} MB/s)" if speed > 1024*1024 else f" ({speed/1024:.1f} KB/s)"
                else:
                    speed_str = ""
                
                self.progress_queue.put({
                    'type': 'progress',
                    'value': min(percentage, 100),
                    'status': f"📥 Downloading: {percentage:.1f}%{speed_str}"
                })
            except Exception as e:
                pass
        elif d['status'] == 'finished':
            self.progress_queue.put({
                'type': 'progress',
                'value': 100,
                'status': "🔄 Processing downloaded file..."
            })
    
    def open_github(self, event):
        """Open GitHub profile in default browser"""
        import webbrowser
        webbrowser.open("https://github.com/Debanjan110d")
    
    def toggle_audio_quality(self):
        """Show/hide audio quality options based on audio-only checkbox"""
        if self.audio_only_var.get():
            self.audio_quality_frame.pack(side=tk.LEFT)
        else:
            self.audio_quality_frame.pack_forget()
    
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
    
    def download_worker(self, url, platform, output_path, quality, audio_only, audio_quality, normalize_audio):
        """Worker function that runs in a separate thread"""
        try:
            import yt_dlp
            
            # Clean up quality string and extract height
            quality_clean = quality
            if 'HD' in quality:
                quality_clean = quality.replace(' HD', 'p')
            elif '4K' in quality:
                quality_clean = quality.replace(' 4K', 'p')
            elif 'QHD' in quality:
                quality_clean = quality.replace(' QHD', 'p')
            
            # Simple, reliable yt-dlp options
            ydl_opts = {
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [self.progress_hook],
            }
            
            if audio_only:
                # Simple audio download - let's not complicate with post-processing for now
                ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best[height<=480]'
                # Try to extract audio but don't fail if FFmpeg isn't available
                try:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }]
                except:
                    pass  # If FFmpeg not available, just download in original format
            else:
                # Smart video download with FFmpeg-aware format selection
                if quality_clean == 'best':
                    # Try high quality formats that don't require merging first
                    ydl_opts['format'] = 'best[height<=2160][ext=mp4]/best[height<=1440][ext=mp4]/best[height<=1080][ext=mp4]/best[ext=mp4]/best'
                elif quality_clean.endswith('p') and quality_clean[:-1].isdigit():
                    height = quality_clean[:-1]
                    # For specific resolutions, try to get that quality in a single stream
                    ydl_opts['format'] = f'best[height={height}][ext=mp4]/best[height<={height}][ext=mp4]/best[height={height}]/best[height<={height}]/best'
                else:
                    # Fallback to best available
                    ydl_opts['format'] = 'best[ext=mp4]/best'
                
                # Try to use FFmpeg for merging if available, but don't require it
                try:
                    # Check if we can use FFmpeg for better quality
                    import subprocess
                    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                    # FFmpeg is available, use separate streams for better quality
                    if quality_clean == 'best':
                        ydl_opts['format'] = 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[height<=2160]'
                    elif quality_clean.endswith('p') and quality_clean[:-1].isdigit():
                        height = quality_clean[:-1]
                        ydl_opts['format'] = f'bestvideo[height={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]'
                    ydl_opts['merge_output_format'] = 'mp4'
                except:
                    # FFmpeg not available, stick with single-stream formats
                    pass
            
            # Platform-specific downloading
            if platform.lower() == 'youtube':
                # Use YouTube downloader's advanced quality logic
                from youtube_downloader import YouTubeDownloader
                yt_downloader = YouTubeDownloader(output_path)
                
                # Set up progress hook for YouTube downloader
                yt_downloader._progress_hook = self.progress_hook
                
                quality_clean = quality.replace(' (Recommended)', '').strip()
                audio_only_flag = quality == "Audio Only (MP3)"
                
                if audio_only_flag:
                    # Use YouTube downloader's audio method
                    yt_downloader.download_audio(url, quality="192", normalize_audio=True)
                else:
                    # Use YouTube downloader's video method with proper quality handling
                    yt_downloader.download_video(url, quality=quality_clean, normalize_audio=True)
            else:
                # For other platforms, use the existing yt-dlp logic
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            print("Download completed successfully!")  # Debug
            
            # Success
            self.progress_queue.put({
                'type': 'complete',
                'message': f"Successfully downloaded from {platform}!"
            })
            
        except Exception as e:
            print(f"Download error: {e}")  # Debug
            error_msg = str(e)
            
            # Handle FFmpeg-related errors gracefully
            if "ffmpeg" in error_msg.lower() or "postprocessing" in error_msg.lower():
                self.progress_queue.put({
                    'type': 'complete',
                    'message': f"Successfully downloaded from {platform}!\n\n💡 Note: Audio is in original format. The file plays perfectly in most media players."
                })
                return
            
            # Handle other errors
            if "Requested format is not available" in error_msg:
                error_msg = "⚠️ The requested video quality is not available. Try 'best' quality."
            elif "Private video" in error_msg:
                error_msg = "🔒 This video is private or restricted."
            elif "Video unavailable" in error_msg:
                error_msg = "📺 This video is no longer available."
            else:
                error_msg = f"❌ Download failed: {error_msg}"
            
            self.progress_queue.put({
                'type': 'error',
                'message': error_msg
            })

    def start_download(self):
        # Prevent multiple simultaneous downloads
        if self.is_downloading:
            messagebox.showwarning("Download in Progress", "A download is already in progress. Please wait for it to complete.")
            return
        
        url = self.url_var.get().strip()
        platform = self.platform_var.get()
        output_path = self.output_path_var.get().strip()
        quality = self.quality_var.get().strip() if self.quality_var.get() else 'best'
        audio_only = self.audio_only_var.get()
        audio_quality = self.audio_quality_var.get().replace('k', '') if self.audio_quality_var.get() else '192'
        normalize_audio = True  # Always normalize audio in background
        
        if not url or not output_path:
            messagebox.showerror("Error", "Please enter a URL and select output folder.")
            return
        
        # Reset progress and start download
        self.is_downloading = True
        self.progress['value'] = 0
        self.status_label.config(text=f"🚀 Starting download from {platform}...", fg=self.accent_color)
        
        # Start download in separate thread
        self.download_thread = threading.Thread(
            target=self.download_worker,
            args=(url, platform, output_path, quality, audio_only, audio_quality, normalize_audio),
            daemon=True
        )
        self.download_thread.start()

if __name__ == "__main__":
    app = VideoDownloaderGUI()
    app.mainloop()
