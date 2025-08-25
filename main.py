#!/usr/bin/env python3
"""
YouTube Video Downloader - Main Launcher
Choose between GUI and CLI interfaces.
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main launcher that chooses between GUI and CLI."""
    parser = argparse.ArgumentParser(
        description="YouTube Video Downloader",
        add_help=False
    )
    parser.add_argument('--cli', action='store_true', 
                       help='Use command-line interface')
    parser.add_argument('--gui', action='store_true',
                       help='Use graphical interface (default)')
    
    # Parse known args to check for --cli flag
    known_args, remaining_args = parser.parse_known_args()
    
    if known_args.cli or (len(sys.argv) > 1 and not known_args.gui):
        # Use CLI
        from cli import main as cli_main
        # Pass remaining arguments to CLI
        sys.argv = [sys.argv[0]] + remaining_args
        return cli_main()
    else:
        # Use GUI (default)
        try:
            from gui import main as gui_main
            return gui_main()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to CLI mode...")
            from cli import main as cli_main
            return cli_main()


if __name__ == "__main__":
    sys.exit(main())
