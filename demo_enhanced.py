#!/usr/bin/env python3
"""
Demo script to showcase Enhanced Python Digital Clock features
This script demonstrates all the new features without requiring GUI
"""

import sys
import os
import time
import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_features():
    """Demonstrate all enhanced features"""
    print("=" * 60)
    print("Enhanced Python Digital Clock - Feature Demo")
    print("=" * 60)
    
    # Settings Management
    print("\n🔧 SETTINGS MANAGEMENT")
    print("-" * 30)
    from settings import SettingsManager
    settings = SettingsManager("demo_settings.json")
    print(f"Default theme: {settings.get('theme')}")
    print(f"Default timezone: {settings.get('timezone')}")
    print(f"Default clock style: {settings.get('clock_style')}")
    
    settings.set("theme", "dark")
    print(f"Changed theme to: {settings.get('theme')}")
    
    # Clock Styles
    print("\n🎨 MULTIPLE CLOCK STYLES")
    print("-" * 30)
    from clock_styles import ClockStyleManager
    style_manager = ClockStyleManager()
    
    current_time = datetime.datetime.now()
    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    for style_name in style_manager.get_available_styles():
        style = style_manager.get_style(style_name)
        formatted_time = style.format_time(current_time, is_24_hour=True, show_seconds=True)
        print(f"{style_name.upper():>8} style: {formatted_time}")
    
    # Timezone Support
    print("\n🌍 TIMEZONE SUPPORT")
    print("-" * 30)
    from features import TimezoneManager
    tz_manager = TimezoneManager()
    
    timezones = ["Local", "UTC", "US/Pacific", "Europe/London", "Asia/Tokyo"]
    for tz in timezones:
        tz_time = tz_manager.get_time_for_timezone(tz)
        print(f"{tz:>12}: {tz_time.strftime('%H:%M:%S %Z')}")
    
    # Alarm Management
    print("\n⏰ ALARM FUNCTIONALITY")
    print("-" * 30)
    from features import AlarmManager
    alarm_mgr = AlarmManager()
    
    # Add some test alarms
    alarm_mgr.add_alarm("09:00", "Morning Alarm", "chime", True)
    alarm_mgr.add_alarm("12:00", "Lunch Break", "bell", False)
    alarm_mgr.add_alarm("17:00", "End of Work", "default", True)
    
    print("Added test alarms:")
    for i, alarm in enumerate(alarm_mgr.get_alarms()):
        status = "ON" if alarm['enabled'] else "OFF"
        sound = alarm.get('sound', 'default')
        voice = "🔊" if alarm.get('voice_enabled', False) else "🔇"
        print(f"  {i+1}. {alarm['hour']:02d}:{alarm['minute']:02d} - {alarm['label']} ({status}) [{sound}] {voice}")
    
    # Stopwatch and Timer
    print("\n⏱️  STOPWATCH & TIMER")
    print("-" * 30)
    from features import StopwatchTimer
    stopwatch = StopwatchTimer()
    
    print("Starting stopwatch...")
    stopwatch.start_stopwatch()
    time.sleep(2.5)
    
    elapsed = stopwatch.get_elapsed_time()
    print(f"Elapsed time: {stopwatch.format_time(elapsed)}")
    
    stopwatch.pause_stopwatch()
    print("Stopwatch paused")
    
    # Add some lap times
    stopwatch.start_stopwatch()
    time.sleep(1)
    lap1 = stopwatch.add_lap()
    time.sleep(1)
    lap2 = stopwatch.add_lap()
    
    print("Lap times:")
    for i, lap in enumerate(stopwatch.get_laps(), 1):
        print(f"  Lap {i}: {stopwatch.format_time(lap)}")
    
    stopwatch.stop_stopwatch()
    
    # Test timer
    print("\nTesting 3-second countdown timer...")
    def timer_callback():
        print("Timer finished!")
    
    stopwatch.start_timer(3, timer_callback)
    for i in range(4):
        remaining = stopwatch.get_timer_remaining()
        print(f"Time remaining: {stopwatch.format_time(remaining)}")
        time.sleep(1)
    
    # System Tray
    print("\n🖥️  SYSTEM TRAY INTEGRATION")
    print("-" * 30)
    from system_tray import create_system_tray_manager
    tray = create_system_tray_manager()
    
    print(f"System tray available: {tray.available}")
    if tray.enable_system_tray():
        print("System tray enabled successfully")
        tray.show_notification("Demo", "Enhanced Python Clock Demo")
        tray.disable_system_tray()
    
    # Voice Management (may not work in headless environment)
    print("\n🔊 VOICE ANNOUNCEMENTS")
    print("-" * 30)
    from features import VoiceManager
    voice_mgr = VoiceManager()
    
    print(f"Voice engine available: {voice_mgr.enabled}")
    if voice_mgr.enabled:
        print("Available voices:", len(voice_mgr.get_voices()))
        voice_mgr.speak("This is a test of the voice announcement system")
    else:
        print("Voice engine not available in this environment")
    
    # Sound Management
    print("\n🔈 SOUND MANAGEMENT")
    print("-" * 30)
    from features import SoundManager
    sound_mgr = SoundManager()
    
    print(f"Audio system initialized: {sound_mgr.initialized}")
    print(f"Available sounds: {sound_mgr.get_available_sounds()}")
    
    if sound_mgr.initialized:
        print("Testing default sound...")
        sound_mgr.play_sound('default', 1.0)
    
    # Themes and Styling
    print("\n🎨 THEMES AND STYLING")
    print("-" * 30)
    
    for style_name in style_manager.get_available_styles():
        style = style_manager.get_style(style_name)
        print(f"\n{style_name.upper()} STYLE:")
        
        light_config = style.get_style_config('light')
        dark_config = style.get_style_config('dark')
        
        print(f"  Light theme: {light_config.get('bg_color', 'N/A')} background")
        print(f"  Dark theme:  {dark_config.get('bg_color', 'N/A')} background")
    
    print("\n✅ DEMO COMPLETED")
    print("=" * 60)
    print("All enhanced features demonstrated successfully!")
    print("The Enhanced Python Digital Clock includes:")
    print("• Multiple clock styles (Digital, Analog, Binary, Text)")
    print("• Alarm functionality with custom sounds and voice")
    print("• Stopwatch and countdown timer with lap support")
    print("• Multiple timezone support")
    print("• Customizable themes and fonts")
    print("• Settings persistence")
    print("• System tray integration")
    print("• Voice announcements")
    print("• Comprehensive testing suite")
    print("=" * 60)
    
    # Clean up demo settings file
    try:
        os.remove("demo_settings.json")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    try:
        demo_features()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()