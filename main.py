#!/usr/bin/env python3
"""
Enhanced Python Digital Clock Application
Main entry point for the enhanced digital clock with all features
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from enhanced_clock import main

if __name__ == "__main__":
    main()