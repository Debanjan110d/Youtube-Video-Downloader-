import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
import os
from pathlib import Path
import webbrowser
from youtube_downloader import YouTubeDownloader


class YouTubeDownloaderGUI:
    """
    GUI application for YouTube video downloading using tkinter.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Video Downloader")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Initialize downloader
        self.downloader = YouTubeDownloader()
        self.downloader.set_progress_callback(self.update_progress)
        
        # Variables
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.audio_only_var = tk.BooleanVar()
        self.download_path_var = tk.StringVar(value=str(self.downloader.download_path))
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        # Create GUI
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Video Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="YouTube URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        info_button = ttk.Button(main_frame, text="Get Info", command=self.get_video_info)
        info_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Download path
        ttk.Label(main_frame, text="Download Path:").grid(row=2, column=0, sticky=tk.W, pady=5)
        path_entry = ttk.Entry(main_frame, textvariable=self.download_path_var, width=50)
        path_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_download_path)
        browse_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Quality selection
        ttk.Label(options_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var,
                                         values=["best", "worst", "1080p", "720p", "480p", "360p", "240p"],
                                         state="readonly", width=20)
        self.quality_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Audio only checkbox
        audio_check = ttk.Checkbutton(options_frame, text="Audio Only (MP3)", 
                                     variable=self.audio_only_var)
        audio_check.grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)
        
        # Video info display
        info_frame = ttk.LabelFrame(main_frame, text="Video Information", padding="10")
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=8, width=60)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Download buttons
        self.download_button = ttk.Button(buttons_frame, text="Download Video", 
                                         command=self.download_video, style="Accent.TButton")
        self.download_button.grid(row=0, column=0, padx=5)
        
        self.playlist_button = ttk.Button(buttons_frame, text="Download Playlist", 
                                         command=self.download_playlist)
        self.playlist_button.grid(row=0, column=1, padx=5)
        
        # Clear button
        clear_button = ttk.Button(buttons_frame, text="Clear", command=self.clear_fields)
        clear_button.grid(row=0, column=2, padx=5)
        
        # Configure row weights for resizing
        main_frame.rowconfigure(4, weight=1)
        
    def browse_download_path(self):
        """Open dialog to select download directory."""
        path = filedialog.askdirectory(initialdir=self.download_path_var.get())
        if path:
            self.download_path_var.set(path)
            self.downloader.download_path = Path(path)
            
    def get_video_info(self):
        """Get and display video information."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        def fetch_info():
            try:
                self.status_var.set("Getting video information...")
                self.download_button.config(state="disabled")
                
                info = self.downloader.get_video_info(url)
                
                # Update quality options with available qualities
                qualities = self.downloader.get_available_qualities(url)
                self.quality_combo['values'] = qualities
                
                # Display info
                info_text = f"""
Title: {info['title']}
Uploader: {info['uploader']}
Duration: {info['duration']} seconds ({info['duration']//60}:{info['duration']%60:02d})
Views: {info['view_count']:,} views
Upload Date: {info['upload_date']}

Description:
{info['description'][:500]}{'...' if len(info['description']) > 500 else ''}

Available Formats:
"""
                
                # Add format information
                video_formats = [f for f in info['formats'] if f['height']]
                audio_formats = [f for f in info['formats'] if not f['height'] and f['acodec'] != 'none']
                
                if video_formats:
                    info_text += "\nVideo Formats:\n"
                    for fmt in video_formats[:10]:  # Show top 10
                        size_info = f" ({fmt['filesize']//1024//1024} MB)" if fmt['filesize'] else ""
                        info_text += f"  {fmt['height']}p - {fmt['ext']} ({fmt['format_note']}){size_info}\n"
                
                if audio_formats:
                    info_text += "\nAudio Formats:\n"
                    for fmt in audio_formats[:5]:  # Show top 5
                        size_info = f" ({fmt['filesize']//1024//1024} MB)" if fmt['filesize'] else ""
                        info_text += f"  {fmt['ext']} - {fmt['acodec']} ({fmt['format_note']}){size_info}\n"
                
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(1.0, info_text)
                
                self.status_var.set("Video information loaded")
                self.download_button.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to get video info: {str(e)}")
                self.status_var.set("Ready")
                self.download_button.config(state="normal")
        
        threading.Thread(target=fetch_info, daemon=True).start()
        
    def download_video(self):
        """Download the video."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        # Update download path
        self.downloader.download_path = Path(self.download_path_var.get())
        self.downloader.download_path.mkdir(exist_ok=True)
        
        def download():
            try:
                self.download_button.config(state="disabled")
                self.playlist_button.config(state="disabled")
                self.status_var.set("Starting download...")
                
                quality = self.quality_var.get()
                audio_only = self.audio_only_var.get()
                
                result = self.downloader.download_video(url, quality, audio_only)
                
                self.status_var.set("Download completed!")
                messagebox.showinfo("Success", result)
                
            except Exception as e:
                self.status_var.set("Download failed")
                messagebox.showerror("Error", f"Download failed: {str(e)}")
            finally:
                self.download_button.config(state="normal")
                self.playlist_button.config(state="normal")
                self.progress_var.set(0)
        
        threading.Thread(target=download, daemon=True).start()
        
    def download_playlist(self):
        """Download playlist."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube playlist URL")
            return
            
        # Ask for max downloads
        max_downloads = tk.simpledialog.askinteger(
            "Playlist Download", 
            "Maximum number of videos to download (0 for all):",
            initialvalue=0, minvalue=0
        )
        
        if max_downloads is None:
            return
            
        max_downloads = max_downloads if max_downloads > 0 else None
        
        # Update download path
        self.downloader.download_path = Path(self.download_path_var.get())
        self.downloader.download_path.mkdir(exist_ok=True)
        
        def download():
            try:
                self.download_button.config(state="disabled")
                self.playlist_button.config(state="disabled")
                self.status_var.set("Starting playlist download...")
                
                quality = self.quality_var.get()
                audio_only = self.audio_only_var.get()
                
                result = self.downloader.download_playlist(url, quality, audio_only, max_downloads)
                
                self.status_var.set("Playlist download completed!")
                messagebox.showinfo("Success", result)
                
            except Exception as e:
                self.status_var.set("Download failed")
                messagebox.showerror("Error", f"Playlist download failed: {str(e)}")
            finally:
                self.download_button.config(state="normal")
                self.playlist_button.config(state="normal")
                self.progress_var.set(0)
        
        threading.Thread(target=download, daemon=True).start()
        
    def update_progress(self, info):
        """Update progress bar and status."""
        if 'percentage' in info:
            self.progress_var.set(info['percentage'])
            speed_mb = info.get('speed', 0) / (1024 * 1024) if info.get('speed') else 0
            eta_min = info.get('eta', 0) // 60 if info.get('eta') else 0
            eta_sec = info.get('eta', 0) % 60 if info.get('eta') else 0
            
            status = f"Downloading... {info['percentage']:.1f}% - {speed_mb:.1f} MB/s"
            if eta_min > 0 or eta_sec > 0:
                status += f" - ETA: {eta_min}:{eta_sec:02d}"
            
            self.status_var.set(status)
        elif info.get('status') == 'finished':
            self.progress_var.set(100)
            filename = os.path.basename(info.get('filename', ''))
            self.status_var.set(f"Finished: {filename}")
            
    def clear_fields(self):
        """Clear all input fields."""
        self.url_var.set("")
        self.quality_var.set("best")
        self.audio_only_var.set(False)
        self.info_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_var.set("Ready")
        
    def run(self):
        """Start the GUI application."""
        try:
            # Try to set a modern theme
            style = ttk.Style()
            available_themes = style.theme_names()
            if 'vista' in available_themes:
                style.theme_use('vista')
            elif 'clam' in available_themes:
                style.theme_use('clam')
        except:
            pass
            
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = YouTubeDownloaderGUI()
    app.run()


if __name__ == "__main__":
    main()
