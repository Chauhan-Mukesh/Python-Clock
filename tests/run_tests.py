#!/usr/bin/env python3
"""
Test runner for Python Clock Application
"""

import unittest
import sys
import os

# Add tests directory to path
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

def run_tests():
    """Run all tests and return results"""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)