"""
Tests for enhanced clock features
"""

import unittest
import time
import tempfile
import os
from unittest.mock import Mock, patch
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from settings import SettingsManager
from clock_styles import ClockStyleManager, DigitalStyle, AnalogStyle, BinaryStyle, TextStyle
from system_tray import MinimalSystemTray


class TestSettingsManager(unittest.TestCase):
    """Test settings persistence functionality"""
    
    def setUp(self):
        """Setup test settings manager with temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.settings = SettingsManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        try:
            os.unlink(self.temp_file.name)
        except FileNotFoundError:
            pass
    
    def test_default_settings(self):
        """Test default settings are loaded correctly"""
        self.assertEqual(self.settings.get("theme"), "light")
        self.assertTrue(self.settings.get("is_24_hour"))
        self.assertEqual(self.settings.get("timezone"), "Local")
    
    def test_set_and_get_setting(self):
        """Test setting and getting values"""
        self.settings.set("theme", "dark")
        self.assertEqual(self.settings.get("theme"), "dark")
    
    def test_update_multiple_settings(self):
        """Test updating multiple settings at once"""
        updates = {"theme": "dark", "is_24_hour": False, "font_size": 48}
        self.settings.update(updates)
        
        self.assertEqual(self.settings.get("theme"), "dark")
        self.assertFalse(self.settings.get("is_24_hour"))
        self.assertEqual(self.settings.get("font_size"), 48)
    
    def test_settings_persistence(self):
        """Test that settings are saved and loaded correctly"""
        # Set some values
        self.settings.set("theme", "dark")
        self.settings.set("font_size", 60)
        
        # Create new settings manager with same file
        new_settings = SettingsManager(self.temp_file.name)
        
        # Check values persist
        self.assertEqual(new_settings.get("theme"), "dark")
        self.assertEqual(new_settings.get("font_size"), 60)
    
    def test_reset_to_defaults(self):
        """Test resetting settings to defaults"""
        self.settings.set("theme", "dark")
        self.settings.set("font_size", 60)
        
        self.settings.reset_to_defaults()
        
        self.assertEqual(self.settings.get("theme"), "light")
        self.assertEqual(self.settings.get("font_size"), 42)


class TestClockStyleManager(unittest.TestCase):
    """Test clock style management"""
    
    def setUp(self):
        """Setup style manager"""
        self.style_manager = ClockStyleManager()
    
    def test_available_styles(self):
        """Test that all expected styles are available"""
        styles = self.style_manager.get_available_styles()
        expected_styles = ['digital', 'analog', 'binary', 'text']
        
        for style in expected_styles:
            self.assertIn(style, styles)
    
    def test_get_style(self):
        """Test getting specific styles"""
        digital_style = self.style_manager.get_style('digital')
        self.assertIsInstance(digital_style, DigitalStyle)
        
        analog_style = self.style_manager.get_style('analog')
        self.assertIsInstance(analog_style, AnalogStyle)
        
        binary_style = self.style_manager.get_style('binary')
        self.assertIsInstance(binary_style, BinaryStyle)
        
        text_style = self.style_manager.get_style('text')
        self.assertIsInstance(text_style, TextStyle)
    
    def test_set_current_style(self):
        """Test setting current style"""
        self.style_manager.set_current_style('analog')
        current = self.style_manager.get_current_style()
        self.assertIsInstance(current, AnalogStyle)
    
    def test_invalid_style(self):
        """Test handling of invalid style names"""
        # Should return digital style as default
        invalid_style = self.style_manager.get_style('nonexistent')
        self.assertIsInstance(invalid_style, DigitalStyle)


class TestDigitalStyle(unittest.TestCase):
    """Test digital clock style"""
    
    def setUp(self):
        """Setup digital style"""
        self.style = DigitalStyle()
    
    def test_time_formatting_24_hour(self):
        """Test 24-hour time formatting"""
        import datetime
        test_time = datetime.datetime(2023, 12, 25, 14, 30, 45)
        
        formatted = self.style.format_time(test_time, is_24_hour=True, show_seconds=True)
        self.assertEqual(formatted, "14:30:45")
        
        formatted_no_seconds = self.style.format_time(test_time, is_24_hour=True, show_seconds=False)
        self.assertEqual(formatted_no_seconds, "14:30")
    
    def test_time_formatting_12_hour(self):
        """Test 12-hour time formatting"""
        import datetime
        test_time = datetime.datetime(2023, 12, 25, 14, 30, 45)
        
        formatted = self.style.format_time(test_time, is_24_hour=False, show_seconds=True)
        self.assertEqual(formatted, "02:30:45 PM")
        
        formatted_no_seconds = self.style.format_time(test_time, is_24_hour=False, show_seconds=False)
        self.assertEqual(formatted_no_seconds, "02:30 PM")
    
    def test_style_config(self):
        """Test style configuration"""
        light_config = self.style.get_style_config('light')
        self.assertEqual(light_config['bg_color'], '#ffffff')
        self.assertEqual(light_config['fg_color'], '#000080')
        
        dark_config = self.style.get_style_config('dark')
        self.assertEqual(dark_config['bg_color'], '#2b2b2b')
        self.assertEqual(dark_config['fg_color'], '#00ff00')


class TestTextStyle(unittest.TestCase):
    """Test text clock style"""
    
    def setUp(self):
        """Setup text style"""
        self.style = TextStyle()
    
    def test_text_formatting_simple_times(self):
        """Test text formatting for simple times"""
        import datetime
        
        # Test noon
        noon = datetime.datetime(2023, 12, 25, 12, 0, 0)
        formatted = self.style.format_time(noon, is_24_hour=False)
        self.assertIn("twelve", formatted.lower())
        self.assertIn("o'clock", formatted.lower())
        
        # Test 3:00
        three = datetime.datetime(2023, 12, 25, 15, 0, 0)
        formatted = self.style.format_time(three, is_24_hour=False)
        self.assertIn("three", formatted.lower())
        self.assertIn("o'clock", formatted.lower())
    
    def test_text_formatting_quarter_times(self):
        """Test text formatting for quarter times"""
        import datetime
        
        # Test quarter past
        quarter_past = datetime.datetime(2023, 12, 25, 14, 15, 0)
        formatted = self.style.format_time(quarter_past, is_24_hour=False)
        self.assertIn("quarter past", formatted.lower())
        
        # Test half past
        half_past = datetime.datetime(2023, 12, 25, 14, 30, 0)
        formatted = self.style.format_time(half_past, is_24_hour=False)
        self.assertIn("half past", formatted.lower())
        
        # Test quarter to
        quarter_to = datetime.datetime(2023, 12, 25, 14, 45, 0)
        formatted = self.style.format_time(quarter_to, is_24_hour=False)
        self.assertIn("quarter to", formatted.lower())


class TestMinimalSystemTray(unittest.TestCase):
    """Test minimal system tray functionality"""
    
    def setUp(self):
        """Setup minimal system tray"""
        self.tray = MinimalSystemTray()
    
    def test_enable_disable(self):
        """Test enabling and disabling system tray"""
        self.assertFalse(self.tray.is_enabled)
        
        result = self.tray.enable_system_tray()
        self.assertTrue(result)
        self.assertTrue(self.tray.is_enabled)
        
        self.tray.disable_system_tray()
        self.assertFalse(self.tray.is_enabled)
    
    def test_show_notification(self):
        """Test showing notifications"""
        # Should not raise an exception
        self.tray.show_notification("Test Title", "Test Message")
    
    def test_update_tooltip(self):
        """Test updating tooltip"""
        # Should not raise an exception
        self.tray.update_tray_tooltip("12:34:56")


class TestIntegration(unittest.TestCase):
    """Integration tests for enhanced features"""
    
    def test_settings_and_styles_integration(self):
        """Test settings and styles work together"""
        # Create settings manager
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        try:
            settings = SettingsManager(temp_file.name)
            style_manager = ClockStyleManager()
            
            # Set clock style in settings
            settings.set("clock_style", "analog")
            
            # Get style from manager
            style_name = settings.get("clock_style")
            style = style_manager.get_style(style_name)
            
            self.assertEqual(style.name, "Analog")
            
        finally:
            try:
                os.unlink(temp_file.name)
            except FileNotFoundError:
                pass
    
    def test_theme_consistency(self):
        """Test that theme settings are consistent across styles"""
        style_manager = ClockStyleManager()
        
        for style_name in style_manager.get_available_styles():
            style = style_manager.get_style(style_name)
            
            light_config = style.get_style_config('light')
            dark_config = style.get_style_config('dark')
            
            # Light theme should have light background
            self.assertTrue(light_config.get('bg_color', '#ffffff').startswith('#'))
            
            # Dark theme should have dark background
            self.assertTrue(dark_config.get('bg_color', '#000000').startswith('#'))


if __name__ == '__main__':
    unittest.main()