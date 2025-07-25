#!/usr/bin/env python3
"""
Test runner for enhanced Python Clock Application
"""

import unittest
import sys
import os

# Add tests directory to path
test_dir = os.path.dirname(__file__)
src_dir = os.path.join(os.path.dirname(test_dir), 'src')
sys.path.insert(0, test_dir)
sys.path.insert(0, src_dir)

def run_enhanced_tests():
    """Run all enhanced tests and return results"""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_enhanced*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_enhanced_tests()
    sys.exit(0 if success else 1)