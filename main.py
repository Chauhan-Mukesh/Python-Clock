#!/usr/bin/env python3
"""
Python Digital Clock Application
Main entry point for the digital clock with GUI
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from clock import main

if __name__ == "__main__":
    main()