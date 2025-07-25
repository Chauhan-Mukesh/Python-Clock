"""
Test cases for the enhanced features (alarm, stopwatch)
"""

import unittest
import sys
import os
import time
from unittest.mock import Mock, patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from features import AlarmManager, StopwatchTimer


class TestAlarmManager(unittest.TestCase):
    """Test cases for the AlarmManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.callback_called = False
        self.callback_alarm = None
        
        def test_callback(alarm):
            self.callback_called = True
            self.callback_alarm = alarm
        
        self.alarm_manager = AlarmManager(test_callback)
    
    def tearDown(self):
        """Clean up after tests"""
        self.alarm_manager.stop_monitoring()
    
    def test_add_valid_alarm(self):
        """Test adding a valid alarm"""
        result = self.alarm_manager.add_alarm("09:30", "Morning Alarm")
        self.assertTrue(result)
        
        alarms = self.alarm_manager.get_alarms()
        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0]['hour'], 9)
        self.assertEqual(alarms[0]['minute'], 30)
        self.assertEqual(alarms[0]['label'], "Morning Alarm")
        self.assertTrue(alarms[0]['enabled'])
    
    def test_add_invalid_alarm_format(self):
        """Test adding an alarm with invalid format"""
        result = self.alarm_manager.add_alarm("25:70", "Invalid")
        self.assertFalse(result)
        
        result = self.alarm_manager.add_alarm("not_time", "Invalid")
        self.assertFalse(result)
        
        alarms = self.alarm_manager.get_alarms()
        self.assertEqual(len(alarms), 0)
    
    def test_remove_alarm(self):
        """Test removing an alarm"""
        self.alarm_manager.add_alarm("10:00", "Test Alarm")
        self.assertEqual(len(self.alarm_manager.get_alarms()), 1)
        
        result = self.alarm_manager.remove_alarm(0)
        self.assertTrue(result)
        self.assertEqual(len(self.alarm_manager.get_alarms()), 0)
    
    def test_remove_invalid_alarm(self):
        """Test removing an alarm with invalid index"""
        result = self.alarm_manager.remove_alarm(0)
        self.assertFalse(result)
        
        result = self.alarm_manager.remove_alarm(-1)
        self.assertFalse(result)
    
    def test_toggle_alarm(self):
        """Test toggling alarm enabled state"""
        self.alarm_manager.add_alarm("11:00", "Toggle Test")
        
        # Initially enabled
        alarm = self.alarm_manager.get_alarms()[0]
        self.assertTrue(alarm['enabled'])
        
        # Toggle to disabled
        result = self.alarm_manager.toggle_alarm(0)
        self.assertTrue(result)
        
        alarm = self.alarm_manager.get_alarms()[0]
        self.assertFalse(alarm['enabled'])
        
        # Toggle back to enabled
        self.alarm_manager.toggle_alarm(0)
        alarm = self.alarm_manager.get_alarms()[0]
        self.assertTrue(alarm['enabled'])
    
    def test_monitoring_lifecycle(self):
        """Test alarm monitoring start/stop"""
        self.assertFalse(self.alarm_manager.is_monitoring)
        
        # Adding alarm should start monitoring
        self.alarm_manager.add_alarm("12:00", "Test")
        self.assertTrue(self.alarm_manager.is_monitoring)
        
        # Removing last alarm should stop monitoring
        self.alarm_manager.remove_alarm(0)
        self.assertFalse(self.alarm_manager.is_monitoring)


class TestStopwatchTimer(unittest.TestCase):
    """Test cases for the StopwatchTimer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.stopwatch = StopwatchTimer()
    
    def test_initial_state(self):
        """Test initial stopwatch state"""
        self.assertFalse(self.stopwatch.is_running)
        self.assertFalse(self.stopwatch.is_paused)
        self.assertEqual(self.stopwatch.get_elapsed_time(), 0)
    
    def test_start_stopwatch(self):
        """Test starting the stopwatch"""
        self.stopwatch.start_stopwatch()
        self.assertTrue(self.stopwatch.is_running)
        self.assertFalse(self.stopwatch.is_paused)
        self.assertIsNotNone(self.stopwatch.start_time)
    
    def test_pause_resume_stopwatch(self):
        """Test pausing and resuming the stopwatch"""
        self.stopwatch.start_stopwatch()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Pause
        self.stopwatch.pause_stopwatch()
        self.assertTrue(self.stopwatch.is_running)
        self.assertTrue(self.stopwatch.is_paused)
        
        elapsed_after_pause = self.stopwatch.get_elapsed_time()
        self.assertGreater(elapsed_after_pause, 0)
        
        # Resume
        self.stopwatch.start_stopwatch()
        self.assertTrue(self.stopwatch.is_running)
        self.assertFalse(self.stopwatch.is_paused)
    
    def test_stop_stopwatch(self):
        """Test stopping the stopwatch"""
        self.stopwatch.start_stopwatch()
        time.sleep(0.1)
        
        self.stopwatch.stop_stopwatch()
        self.assertFalse(self.stopwatch.is_running)
        self.assertFalse(self.stopwatch.is_paused)
        self.assertEqual(self.stopwatch.get_elapsed_time(), 0)
        self.assertIsNone(self.stopwatch.start_time)
    
    def test_time_formatting(self):
        """Test time formatting"""
        # Test various time values
        test_cases = [
            (0, "00:00.00"),
            (30.5, "00:30.50"),
            (65.25, "01:05.25"),
            (3661.75, "61:01.75")
        ]
        
        for seconds, expected in test_cases:
            formatted = self.stopwatch.format_time(seconds)
            self.assertEqual(formatted, expected)
    
    def test_timer_mode(self):
        """Test countdown timer functionality"""
        # Start a 2 second timer
        self.stopwatch.start_timer(2)
        
        self.assertTrue(self.stopwatch.is_timer_mode)
        self.assertTrue(self.stopwatch.is_running)
        self.assertAlmostEqual(self.stopwatch.get_timer_remaining(), 2, delta=0.1)
        
        # Wait a bit and check remaining time
        time.sleep(0.5)
        remaining = self.stopwatch.get_timer_remaining()
        self.assertLess(remaining, 2)
        self.assertGreater(remaining, 1)
        
        self.assertFalse(self.stopwatch.is_timer_finished())
    
    def test_timer_completion(self):
        """Test timer completion detection"""
        # Start a very short timer
        self.stopwatch.start_timer(0.1)
        
        # Wait for completion
        time.sleep(0.2)
        
        self.assertTrue(self.stopwatch.is_timer_finished())
        self.assertEqual(self.stopwatch.get_timer_remaining(), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for features working together"""
    
    def test_multiple_alarms(self):
        """Test managing multiple alarms"""
        manager = AlarmManager()
        
        # Add multiple alarms
        manager.add_alarm("08:00", "Wake up")
        manager.add_alarm("12:00", "Lunch")
        manager.add_alarm("18:00", "Dinner")
        
        alarms = manager.get_alarms()
        self.assertEqual(len(alarms), 3)
        
        # Remove middle alarm
        manager.remove_alarm(1)
        alarms = manager.get_alarms()
        self.assertEqual(len(alarms), 2)
        self.assertEqual(alarms[0]['label'], "Wake up")
        self.assertEqual(alarms[1]['label'], "Dinner")
        
        manager.stop_monitoring()
    
    def test_stopwatch_accuracy(self):
        """Test stopwatch timing accuracy"""
        stopwatch = StopwatchTimer()
        
        start_time = time.time()
        stopwatch.start_stopwatch()
        
        # Run for a known duration
        time.sleep(0.5)
        
        elapsed = stopwatch.get_elapsed_time()
        actual_elapsed = time.time() - start_time
        
        # Should be within 50ms of actual time
        self.assertAlmostEqual(elapsed, actual_elapsed, delta=0.05)


if __name__ == '__main__':
    unittest.main(verbosity=2)