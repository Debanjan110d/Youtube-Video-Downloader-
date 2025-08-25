#!/usr/bin/env python3
"""
YouTube Video Downloader - Executable Launcher
A simple launcher that starts the GUI by default or CLI if requested.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def show_error(title, message):
    """Show error message to user."""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        # Fallback to console if GUI fails
        print(f"ERROR - {title}: {message}")
        input("Press Enter to exit...")

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import yt_dlp
        return True
    except ImportError:
        return False

def main():
    """Main entry point for the executable."""
    try:
        # Check if running as CLI (command line arguments provided)
        if len(sys.argv) > 1:
            # CLI mode
            try:
                from cli import main as cli_main
                return cli_main()
            except ImportError as e:
                show_error("CLI Import Error", f"Could not start CLI: {e}")
                return 1
        
        # GUI mode (default)
        try:
            # Check dependencies first
            if not check_dependencies():
                show_error("Missing Dependencies", 
                          "Required dependencies are missing.\n\n"
                          "Please install yt-dlp:\n"
                          "pip install yt-dlp")
                return 1
            
            from gui import main as gui_main
            return gui_main()
            
        except ImportError as e:
            # Fallback to CLI if GUI fails
            show_error("GUI Error", 
                      f"GUI failed to start: {e}\n\n"
                      "You can use the command line version instead.")
            return 1
            
    except KeyboardInterrupt:
        print("\nApplication cancelled by user")
        return 1
    except Exception as e:
        show_error("Unexpected Error", f"An unexpected error occurred:\n{e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
