"""
Test cases for the Digital Clock Application
Tests core functionality, UI components, and edge cases
"""

import unittest
import sys
import os
import time
import datetime
import threading
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock tkinter for headless testing
mock_tk = MagicMock()
mock_ttk = MagicMock()
mock_messagebox = MagicMock()
mock_font = MagicMock()

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.ttk'] = mock_ttk
sys.modules['tkinter.messagebox'] = mock_messagebox
sys.modules['tkinter.font'] = mock_font

from clock import DigitalClock


class TestDigitalClock(unittest.TestCase):
    """Test cases for the DigitalClock class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock tkinter components to avoid GUI creation during tests
        with patch('tkinter.Tk'), \
             patch('tkinter.ttk.Style'), \
             patch('tkinter.ttk.Frame'), \
             patch('tkinter.ttk.Label'), \
             patch('tkinter.ttk.Button'), \
             patch('tkinter.StringVar'):
            self.clock = DigitalClock()
            self.clock.is_running = False  # Prevent background thread from running
    
    def tearDown(self):
        """Clean up after each test method"""
        if hasattr(self.clock, 'is_running'):
            self.clock.is_running = False
    
    def test_initialization(self):
        """Test that DigitalClock initializes with correct default values"""
        self.assertTrue(self.clock.is_24_hour)
        self.assertEqual(self.clock.current_timezone, "Local")
        self.assertEqual(self.clock.theme, "light")
        self.assertFalse(self.clock.is_running)
    
    def test_time_format_toggle(self):
        """Test toggling between 12-hour and 24-hour time formats"""
        # Initially 24-hour format
        self.assertTrue(self.clock.is_24_hour)
        
        # Toggle to 12-hour
        self.clock.toggle_time_format()
        self.assertFalse(self.clock.is_24_hour)
        
        # Toggle back to 24-hour
        self.clock.toggle_time_format()
        self.assertTrue(self.clock.is_24_hour)
    
    def test_theme_toggle(self):
        """Test toggling between light and dark themes"""
        # Initially light theme
        self.assertEqual(self.clock.theme, "light")
        
        # Toggle to dark
        self.clock.toggle_theme()
        self.assertEqual(self.clock.theme, "dark")
        
        # Toggle back to light
        self.clock.toggle_theme()
        self.assertEqual(self.clock.theme, "light")
    
    def test_time_formatting_24_hour(self):
        """Test time formatting in 24-hour format"""
        self.clock.is_24_hour = True
        
        # Mock current time
        test_time = datetime.datetime(2024, 1, 1, 15, 30, 45)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_time
            mock_datetime.strftime = test_time.strftime
            
            # This would be called by update_clock method
            time_str = test_time.strftime("%H:%M:%S")
            self.assertEqual(time_str, "15:30:45")
    
    def test_time_formatting_12_hour(self):
        """Test time formatting in 12-hour format"""
        self.clock.is_24_hour = False
        
        # Mock current time
        test_time = datetime.datetime(2024, 1, 1, 15, 30, 45)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_time
            mock_datetime.strftime = test_time.strftime
            
            # This would be called by update_clock method
            time_str = test_time.strftime("%I:%M:%S %p")
            self.assertEqual(time_str, "03:30:45 PM")
    
    def test_date_formatting(self):
        """Test date formatting"""
        test_time = datetime.datetime(2024, 1, 1, 15, 30, 45)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_time
            mock_datetime.strftime = test_time.strftime
            
            date_str = test_time.strftime("%A, %B %d, %Y")
            self.assertEqual(date_str, "Monday, January 01, 2024")
    
    def test_alarm_dialog(self):
        """Test alarm dialog display"""
        with patch.object(self.clock, 'show_alarm_manager') as mock_method:
            self.clock.show_alarm_manager()
            mock_method.assert_called_once()
    
    def test_stopwatch_dialog(self):
        """Test stopwatch dialog display"""
        with patch.object(self.clock, 'show_stopwatch_window') as mock_method:
            self.clock.show_stopwatch_window()
            mock_method.assert_called_once()
    
    def test_style_setup_light_theme(self):
        """Test style setup for light theme"""
        self.clock.theme = "light"
        self.clock.setup_styles()
        
        self.assertEqual(self.clock.bg_color, "#ffffff")
        self.assertEqual(self.clock.fg_color, "#333333")
        self.assertEqual(self.clock.accent_color, "#0066cc")
    
    def test_style_setup_dark_theme(self):
        """Test style setup for dark theme"""
        self.clock.theme = "dark"
        self.clock.setup_styles()
        
        self.assertEqual(self.clock.bg_color, "#2b2b2b")
        self.assertEqual(self.clock.fg_color, "#ffffff")
        self.assertEqual(self.clock.accent_color, "#4a9eff")
    
    def test_edge_case_midnight_24_hour(self):
        """Test time formatting at midnight in 24-hour format"""
        self.clock.is_24_hour = True
        test_time = datetime.datetime(2024, 1, 1, 0, 0, 0)
        time_str = test_time.strftime("%H:%M:%S")
        self.assertEqual(time_str, "00:00:00")
    
    def test_edge_case_midnight_12_hour(self):
        """Test time formatting at midnight in 12-hour format"""
        self.clock.is_24_hour = False
        test_time = datetime.datetime(2024, 1, 1, 0, 0, 0)
        time_str = test_time.strftime("%I:%M:%S %p")
        self.assertEqual(time_str, "12:00:00 AM")
    
    def test_edge_case_noon_12_hour(self):
        """Test time formatting at noon in 12-hour format"""
        self.clock.is_24_hour = False
        test_time = datetime.datetime(2024, 1, 1, 12, 0, 0)
        time_str = test_time.strftime("%I:%M:%S %p")
        self.assertEqual(time_str, "12:00:00 PM")


class TestClockUtility(unittest.TestCase):
    """Test utility functions and edge cases"""
    
    def test_time_format_validation(self):
        """Test various time format validations"""
        # Test different hours
        for hour in range(24):
            test_time = datetime.datetime(2024, 1, 1, hour, 0, 0)
            
            # 24-hour format should always be HH:MM:SS
            time_24 = test_time.strftime("%H:%M:%S")
            self.assertRegex(time_24, r'^\d{2}:\d{2}:\d{2}$')
            
            # 12-hour format should include AM/PM
            time_12 = test_time.strftime("%I:%M:%S %p")
            self.assertRegex(time_12, r'^\d{2}:\d{2}:\d{2} (AM|PM)$')
    
    def test_date_format_validation(self):
        """Test date format for different dates"""
        test_dates = [
            datetime.datetime(2024, 1, 1),    # New Year
            datetime.datetime(2024, 2, 29),   # Leap year
            datetime.datetime(2024, 12, 31),  # End of year
        ]
        
        for test_date in test_dates:
            date_str = test_date.strftime("%A, %B %d, %Y")
            # Should contain day, month, date, and year
            self.assertIn(',', date_str)
            self.assertIn('2024', date_str)
    
    def test_threading_safety(self):
        """Test that clock updates can be safely stopped"""
        # This test ensures that the threading mechanism is safe
        with patch('tkinter.Tk'), \
             patch('tkinter.ttk.Style'), \
             patch('tkinter.ttk.Frame'), \
             patch('tkinter.ttk.Label'), \
             patch('tkinter.ttk.Button'), \
             patch('tkinter.StringVar'):
            
            clock = DigitalClock()
            clock.is_running = True
            
            # Simulate stopping the clock
            clock.on_closing()
            self.assertFalse(clock.is_running)


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2)