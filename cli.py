#!/usr/bin/env python3
"""
Command-line interface for YouTube Video Downloader.
Provides a comprehensive CLI for downloading YouTube videos and playlists.
"""

import argparse
import sys
import os
from pathlib import Path
from youtube_downloader import YouTubeDownloader


class YouTubeDownloaderCLI:
    """Command-line interface for YouTube downloader."""
    
    def __init__(self):
        self.downloader = YouTubeDownloader()
        self.setup_progress_callback()
        
    def setup_progress_callback(self):
        """Setup progress callback for CLI."""
        def progress_callback(info):
            if 'percentage' in info:
                percentage = info['percentage']
                speed = info.get('speed', 0) / (1024 * 1024) if info.get('speed') else 0
                eta = info.get('eta', 0)
                
                # Create progress bar
                bar_length = 30
                filled_length = int(bar_length * percentage / 100)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                
                eta_str = f" ETA: {eta//60:02d}:{eta%60:02d}" if eta else ""
                print(f"\r[{bar}] {percentage:.1f}% {speed:.1f}MB/s{eta_str}", end='', flush=True)
                
            elif info.get('status') == 'finished':
                print(f"\n✓ Finished: {os.path.basename(info.get('filename', ''))}")
        
        self.downloader.set_progress_callback(progress_callback)
    
    def info_command(self, args):
        """Handle info command."""
        try:
            print("🔍 Getting video information...")
            info = self.downloader.get_video_info(args.url)
            
            print(f"\n📹 Video Information:")
            print(f"Title: {info['title']}")
            print(f"Uploader: {info['uploader']}")
            print(f"Duration: {info['duration']} seconds ({info['duration']//60}:{info['duration']%60:02d})")
            print(f"Views: {info['view_count']:,}")
            print(f"Upload Date: {info['upload_date']}")
            
            if args.show_formats:
                print("\n📋 Available Formats:")
                video_formats = [f for f in info['formats'] if f['height']]
                audio_formats = [f for f in info['formats'] if not f['height'] and f['acodec'] != 'none']
                
                if video_formats:
                    print("\nVideo Formats:")
                    for fmt in video_formats[:15]:
                        size_info = f" ({fmt['filesize']//1024//1024} MB)" if fmt['filesize'] else ""
                        print(f"  {fmt['height']}p - {fmt['ext']} ({fmt['format_note']}){size_info}")
                
                if audio_formats:
                    print("\nAudio Formats:")
                    for fmt in audio_formats[:10]:
                        size_info = f" ({fmt['filesize']//1024//1024} MB)" if fmt['filesize'] else ""
                        print(f"  {fmt['ext']} - {fmt['acodec']} ({fmt['format_note']}){size_info}")
            
            if args.show_description:
                print(f"\n📝 Description:")
                description = info['description']
                if len(description) > 500 and not args.full_description:
                    description = description[:500] + "..."
                print(description)
                
        except Exception as e:
            print(f"❌ Error getting video info: {e}")
            return 1
        
        return 0
    
    def download_command(self, args):
        """Handle download command."""
        try:
            # Set download path
            if args.output:
                self.downloader.download_path = Path(args.output)
                self.downloader.download_path.mkdir(parents=True, exist_ok=True)
            
            print(f"📁 Download path: {self.downloader.download_path}")
            
            if args.playlist:
                print("📺 Starting playlist download...")
                result = self.downloader.download_playlist(
                    args.url, 
                    args.quality, 
                    args.audio_only,
                    args.max_downloads
                )
            else:
                print("📺 Starting video download...")
                result = self.downloader.download_video(
                    args.url,
                    args.quality,
                    args.audio_only,
                    args.filename
                )
            
            print(f"\n✅ {result}")
            return 0
            
        except Exception as e:
            print(f"\n❌ Download failed: {e}")
            return 1
    
    def list_qualities_command(self, args):
        """Handle list-qualities command."""
        try:
            print("🔍 Getting available qualities...")
            qualities = self.downloader.get_available_qualities(args.url)
            
            print(f"\n📋 Available qualities for this video:")
            for quality in qualities:
                print(f"  • {quality}")
                
        except Exception as e:
            print(f"❌ Error getting qualities: {e}")
            return 1
        
        return 0


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="YouTube Video Downloader CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s info "https://www.youtube.com/watch?v=..."
  %(prog)s download "https://www.youtube.com/watch?v=..." --quality 720p
  %(prog)s download "https://www.youtube.com/watch?v=..." --audio-only
  %(prog)s download "https://www.youtube.com/playlist?list=..." --playlist
  %(prog)s list-qualities "https://www.youtube.com/watch?v=..."
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get video information')
    info_parser.add_argument('url', help='YouTube video URL')
    info_parser.add_argument('--show-formats', action='store_true',
                           help='Show available video/audio formats')
    info_parser.add_argument('--show-description', action='store_true',
                           help='Show video description')
    info_parser.add_argument('--full-description', action='store_true',
                           help='Show full description (not truncated)')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download video or playlist')
    download_parser.add_argument('url', help='YouTube video or playlist URL')
    download_parser.add_argument('-q', '--quality', default='best',
                               choices=['best', 'worst', '1080p', '720p', '480p', '360p', '240p'],
                               help='Video quality (default: best)')
    download_parser.add_argument('-a', '--audio-only', action='store_true',
                               help='Download audio only (MP3)')
    download_parser.add_argument('-o', '--output', 
                               help='Output directory (default: downloads)')
    download_parser.add_argument('-f', '--filename',
                               help='Custom filename (without extension)')
    download_parser.add_argument('-p', '--playlist', action='store_true',
                               help='Download as playlist')
    download_parser.add_argument('-m', '--max-downloads', type=int,
                               help='Maximum number of videos to download from playlist')
    
    # List qualities command
    qualities_parser = subparsers.add_parser('list-qualities', 
                                           help='List available video qualities')
    qualities_parser.add_argument('url', help='YouTube video URL')
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = YouTubeDownloaderCLI()
    
    try:
        if args.command == 'info':
            return cli.info_command(args)
        elif args.command == 'download':
            return cli.download_command(args)
        elif args.command == 'list-qualities':
            return cli.list_qualities_command(args)
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
