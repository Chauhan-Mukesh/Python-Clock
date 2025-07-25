#!/usr/bin/env python3
"""
Demo script for Python Clock Application
Showcases the main features without requiring GUI
"""

import sys
import os
import time
import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from features import AlarmManager, StopwatchTimer


def demo_time_formatting():
    """Demonstrate time formatting features"""
    print("=" * 50)
    print("TIME FORMATTING DEMO")
    print("=" * 50)
    
    current_time = datetime.datetime.now()
    
    print(f"Current time (24-hour): {current_time.strftime('%H:%M:%S')}")
    print(f"Current time (12-hour): {current_time.strftime('%I:%M:%S %p')}")
    print(f"Current date: {current_time.strftime('%A, %B %d, %Y')}")
    
    # Test edge cases
    midnight = datetime.datetime(2024, 1, 1, 0, 0, 0)
    noon = datetime.datetime(2024, 1, 1, 12, 0, 0)
    
    print(f"\nEdge cases:")
    print(f"Midnight (24h): {midnight.strftime('%H:%M:%S')}")
    print(f"Midnight (12h): {midnight.strftime('%I:%M:%S %p')}")
    print(f"Noon (24h): {noon.strftime('%H:%M:%S')}")
    print(f"Noon (12h): {noon.strftime('%I:%M:%S %p')}")


def demo_alarm_manager():
    """Demonstrate alarm manager features"""
    print("\n" + "=" * 50)
    print("ALARM MANAGER DEMO")
    print("=" * 50)
    
    def test_callback(alarm):
        print(f"🔔 ALARM TRIGGERED: {alarm['label']} at {alarm['hour']:02d}:{alarm['minute']:02d}")
    
    manager = AlarmManager(test_callback)
    
    # Add some test alarms
    print("Adding alarms...")
    manager.add_alarm("09:00", "Wake up")
    manager.add_alarm("12:30", "Lunch time")
    manager.add_alarm("18:00", "Dinner")
    manager.add_alarm("25:00", "Invalid time")  # Should fail
    
    print(f"Active alarms: {len(manager.get_alarms())}")
    
    # Display alarms
    for i, alarm in enumerate(manager.get_alarms()):
        status = "ENABLED" if alarm['enabled'] else "DISABLED"
        print(f"  {i+1}. {alarm['hour']:02d}:{alarm['minute']:02d} - {alarm['label']} ({status})")
    
    # Toggle an alarm
    print("\nToggling first alarm...")
    manager.toggle_alarm(0)
    
    # Show updated status
    alarm = manager.get_alarms()[0]
    status = "ENABLED" if alarm['enabled'] else "DISABLED"
    print(f"First alarm is now: {status}")
    
    # Remove an alarm
    print("\nRemoving second alarm...")
    manager.remove_alarm(1)
    print(f"Remaining alarms: {len(manager.get_alarms())}")
    
    manager.stop_monitoring()


def demo_stopwatch():
    """Demonstrate stopwatch features"""
    print("\n" + "=" * 50)
    print("STOPWATCH DEMO")
    print("=" * 50)
    
    stopwatch = StopwatchTimer()
    
    print("Testing time formatting:")
    test_times = [0, 30.5, 65.25, 3661.75]
    for t in test_times:
        formatted = stopwatch.format_time(t)
        print(f"  {t:8.2f}s -> {formatted}")
    
    print("\nStopwatch simulation:")
    print("Starting stopwatch...")
    stopwatch.start_stopwatch()
    
    # Simulate running for a bit
    for i in range(3):
        time.sleep(0.5)
        elapsed = stopwatch.get_elapsed_time()
        print(f"  Elapsed: {stopwatch.format_time(elapsed)}")
    
    print("Pausing stopwatch...")
    stopwatch.pause_stopwatch()
    time.sleep(0.5)  # Should not affect elapsed time
    
    print("Resuming stopwatch...")
    stopwatch.start_stopwatch()
    time.sleep(0.5)
    
    final_time = stopwatch.get_elapsed_time()
    print(f"Final time: {stopwatch.format_time(final_time)}")
    
    stopwatch.stop_stopwatch()
    
    print("\nTimer simulation:")
    print("Starting 2-second countdown timer...")
    stopwatch.start_timer(2)
    
    while not stopwatch.is_timer_finished():
        remaining = stopwatch.get_timer_remaining()
        print(f"  Time remaining: {remaining:.1f}s")
        time.sleep(0.3)
    
    print("Timer finished!")


def demo_ui_themes():
    """Demonstrate UI theme concepts"""
    print("\n" + "=" * 50)
    print("UI THEMES DEMO")
    print("=" * 50)
    
    themes = {
        "light": {
            "bg_color": "#ffffff",
            "fg_color": "#333333",
            "accent_color": "#0066cc"
        },
        "dark": {
            "bg_color": "#2b2b2b",
            "fg_color": "#ffffff", 
            "accent_color": "#4a9eff"
        }
    }
    
    for theme_name, colors in themes.items():
        print(f"\n{theme_name.upper()} THEME:")
        print(f"  Background: {colors['bg_color']}")
        print(f"  Text Color: {colors['fg_color']}")
        print(f"  Accent:     {colors['accent_color']}")


def main():
    """Run all demos"""
    print("🕐 PYTHON DIGITAL CLOCK - FEATURE DEMONSTRATION")
    print("This demo showcases the core features of the digital clock application")
    print("In the actual GUI application, these features provide:")
    print("- Real-time clock display with multiple formats")
    print("- Alarm management with multiple alarms")
    print("- Stopwatch and timer functionality")
    print("- Theme switching between light and dark modes")
    print("- Modern, responsive user interface")
    
    try:
        demo_time_formatting()
        demo_alarm_manager()
        demo_stopwatch()
        demo_ui_themes()
        
        print("\n" + "=" * 50)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("To run the full GUI application:")
        print("  python main.py")
        print("\nTo run tests:")
        print("  python tests/run_tests.py")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {e}")


if __name__ == "__main__":
    main()