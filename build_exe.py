#!/usr/bin/env python3
"""
Simple build script for creating YouTube Downloader executable
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Build the executable."""
    print("YouTube Downloader - Executable Builder")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("launcher.py").exists():
        print("Error: Please run this script from the youtube_downloader directory")
        return 1
    
    # Install/update requirements
    if not run_command("python -m pip install --upgrade pip", "Updating pip"):
        return 1
    
    if not run_command("python -m pip install -r requirements.txt", "Installing requirements"):
        return 1
    
    # Build with PyInstaller using the spec file
    print("\nBuilding executable (this may take several minutes)...")
    build_command = "pyinstaller --clean --noconfirm YouTubeDownloader.spec"
    
    if not run_command(build_command, "Building executable"):
        print("\nTrying alternative build method...")
        # Fallback to simple build
        simple_command = (
            "pyinstaller --onefile --windowed --name YouTubeDownloader "
            "--add-data youtube_downloader.py;. "
            "--add-data gui.py;. "
            "--add-data cli.py;. "
            "--add-data config.py;. "
            "--add-data utils.py;. "
            "--hidden-import yt_dlp "
            "--hidden-import tkinter "
            "launcher.py"
        )
        if not run_command(simple_command, "Building with simple method"):
            return 1
    
    # Check if executable was created
    exe_path = Path("dist/YouTubeDownloader.exe")
    if exe_path.exists():
        print(f"\n🎉 SUCCESS!")
        print(f"Executable created: {exe_path.absolute()}")
        print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        print("\nYou can now distribute this file to users.")
        print("No Python installation required on target machines.")
        
        # Ask if user wants to test the executable
        try:
            test = input("\nWould you like to test the executable now? (y/n): ").lower()
            if test in ['y', 'yes']:
                print("Starting executable...")
                subprocess.Popen([str(exe_path)], shell=True)
        except KeyboardInterrupt:
            pass
        
        return 0
    else:
        print("\n❌ Build failed - executable not found")
        return 1

if __name__ == "__main__":
    sys.exit(main())
