#!/usr/bin/env python3
"""Main application entry point."""

import sys
import os

# Add src to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import main

if __name__ == "__main__":
    sys.exit(main())
