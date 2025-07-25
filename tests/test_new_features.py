"""
Test suite for new enhanced features
Tests weather, calendar, multi-monitor, plugins, cloud sync, and advanced scheduler
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from features import (WeatherManager, CalendarManager, MultiMonitorManager, 
                     PluginManager, CloudSyncManager, AdvancedScheduler)
from settings import SettingsManager


class TestNewFeatures(unittest.TestCase):
    """Test the new enhanced features"""
    
    def test_weather_manager(self):
        """Test weather manager functionality"""
        weather = WeatherManager()
        
        # Test initial state
        self.assertFalse(weather.enabled)
        self.assertEqual(weather.location, "Unknown")
        
        # Test API key setting
        weather.set_api_key("test_key")
        self.assertTrue(weather.enabled)
        
        # Test location setting
        weather.set_location("Test City")
        self.assertEqual(weather.location, "Test City")
        
        # Test weather update
        result = weather.update_weather()
        self.assertTrue(result)
        
        # Test current weather
        current = weather.get_current_weather()
        self.assertIsInstance(current, dict)
        self.assertIn("temperature", current)
    
    def test_calendar_manager(self):
        """Test calendar manager functionality"""
        calendar = CalendarManager()
        
        # Test initial state
        self.assertFalse(calendar.enabled)
        self.assertEqual(len(calendar.events), 0)
        
        # Test enabling
        calendar.enabled = True
        
        # Test sync
        result = calendar.sync_calendars()
        self.assertTrue(result)
        
        # Test events
        events = calendar.get_upcoming_events()
        self.assertIsInstance(events, list)
        
        # Test next event
        next_event = calendar.get_next_event()
        if next_event:
            self.assertIn("title", next_event)
            self.assertIn("start", next_event)
    
    def test_multi_monitor_manager(self):
        """Test multi-monitor manager functionality"""
        monitor = MultiMonitorManager()
        
        # Test monitor detection
        monitors = monitor.get_monitors()
        self.assertIsInstance(monitors, list)
        self.assertGreater(len(monitors), 0)
        
        # Test setting monitor
        result = monitor.set_monitor(0)
        self.assertTrue(result)
        self.assertEqual(monitor.current_monitor, 0)
        
        # Test invalid monitor
        result = monitor.set_monitor(999)
        self.assertFalse(result)
        
        # Test geometry
        geometry = monitor.get_monitor_geometry()
        self.assertIn("x", geometry)
        self.assertIn("y", geometry)
        self.assertIn("width", geometry)
        self.assertIn("height", geometry)
    
    def test_plugin_manager(self):
        """Test plugin manager functionality"""
        plugins = PluginManager()
        
        # Test initial state
        self.assertIsInstance(plugins.get_plugins(), dict)
        
        # Test loading plugins
        plugins.load_plugins()
        
        # Test enabling/disabling plugin
        plugins.plugins["test"] = {
            "name": "test",
            "enabled": False,
            "version": "1.0.0",
            "description": "test plugin"
        }
        
        result = plugins.enable_plugin("test")
        self.assertTrue(result)
        self.assertIn("test", plugins.get_enabled_plugins())
        
        result = plugins.disable_plugin("test")
        self.assertTrue(result)
        self.assertNotIn("test", plugins.get_enabled_plugins())
    
    def test_cloud_sync_manager(self):
        """Test cloud sync manager functionality"""
        cloud = CloudSyncManager()
        
        # Test initial state
        self.assertFalse(cloud.enabled)
        self.assertIsNone(cloud.sync_provider)
        
        # Test configuration
        cloud.configure_sync("TestProvider", "http://test.com", "test_token")
        self.assertTrue(cloud.enabled)
        self.assertEqual(cloud.sync_provider, "TestProvider")
        
        # Test upload
        test_settings = {"theme": "dark", "font_size": 24}
        result = cloud.upload_settings(test_settings)
        self.assertTrue(result)
        
        # Test download
        downloaded = cloud.download_settings()
        self.assertIsInstance(downloaded, dict)
        
        # Test sync
        synced = cloud.sync_settings(test_settings)
        self.assertIsInstance(synced, dict)
    
    def test_advanced_scheduler(self):
        """Test advanced scheduler functionality"""
        scheduler = AdvancedScheduler()
        
        # Test initial state
        self.assertFalse(scheduler.enabled)
        self.assertFalse(scheduler.running)
        self.assertEqual(len(scheduler.get_schedules()), 0)
        
        # Test adding schedule
        schedule_config = {
            "name": "Test Schedule",
            "type": "daily",
            "time": "09:00",
            "action": "notification",
            "message": "Test message"
        }
        schedule_id = scheduler.add_schedule(schedule_config)
        self.assertIsInstance(schedule_id, int)
        
        # Test schedules list
        schedules = scheduler.get_schedules()
        self.assertEqual(len(schedules), 1)
        self.assertEqual(schedules[0]["name"], "Test Schedule")
        
        # Test enable/disable schedule
        result = scheduler.disable_schedule(schedule_id)
        self.assertTrue(result)
        
        result = scheduler.enable_schedule(schedule_id)
        self.assertTrue(result)
        
        # Test remove schedule
        result = scheduler.remove_schedule(schedule_id)
        self.assertTrue(result)
        self.assertEqual(len(scheduler.get_schedules()), 0)
    
    def test_new_settings(self):
        """Test new settings in SettingsManager"""
        settings = SettingsManager()
        
        # Test new settings exist
        all_settings = settings.get_all_settings()
        new_settings = [
            "weather_enabled", "weather_api_key", "weather_location",
            "calendar_enabled", "calendar_sources",
            "multi_monitor_enabled", "current_monitor",
            "plugins_enabled", "enabled_plugins",
            "cloud_sync_enabled", "cloud_sync_url", "cloud_sync_token",
            "scheduler_enabled", "scheduler_autostart"
        ]
        
        for setting in new_settings:
            self.assertIn(setting, all_settings)
        
        # Test setting and getting new values
        settings.set("weather_enabled", True)
        self.assertTrue(settings.get("weather_enabled"))
        
        settings.set("weather_location", "Test City")
        self.assertEqual(settings.get("weather_location"), "Test City")


class TestMobileCompanion(unittest.TestCase):
    """Test mobile companion functionality"""
    
def setUp(self):
        # Skip mobile companion tests in headless environment
        self.skipTest("Mobile companion requires full environment")


if __name__ == "__main__":
    unittest.main()