"""
Enhanced features for the Digital Clock Application
"""

import datetime
import threading
import time
import os
import pygame
import pyttsx3
import pytz
import json
import urllib.request
import urllib.parse
import platform
from typing import Optional, Callable, List, Dict
from plyer import notification


class SoundManager:
    """Manages sound playback for alarms and notifications"""
    
    def __init__(self):
        self.initialized = False
        self.available_sounds = {}
        self.init_pygame()
        self.load_default_sounds()
    
    def init_pygame(self):
        """Initialize pygame mixer for sound playback"""
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.initialized = True
        except pygame.error as e:
            print(f"Could not initialize audio: {e}")
            self.initialized = False
    
    def load_default_sounds(self):
        """Load default alarm sounds"""
        sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        self.available_sounds = {
            'default': None,  # Will use system beep
            'beep': None,
            'chime': None,
            'bell': None
        }
        
        # Try to load actual sound files if they exist
        if os.path.exists(sounds_dir):
            for sound_name in self.available_sounds.keys():
                sound_file = os.path.join(sounds_dir, f"{sound_name}.wav")
                if os.path.exists(sound_file):
                    try:
                        self.available_sounds[sound_name] = pygame.mixer.Sound(sound_file)
                    except pygame.error:
                        pass
    
    def play_sound(self, sound_name: str = 'default', duration: float = 2.0):
        """Play an alarm sound"""
        if not self.initialized:
            # Fallback to system beep
            print('\a')  # ASCII bell character
            return
        
        try:
            if sound_name in self.available_sounds and self.available_sounds[sound_name]:
                self.available_sounds[sound_name].play()
            else:
                # Generate a simple beep tone
                self.generate_beep(duration)
        except pygame.error as e:
            print(f"Error playing sound: {e}")
            print('\a')  # Fallback
    
    def generate_beep(self, duration: float = 2.0):
        """Generate a simple beep sound"""
        try:
            # Create a simple sine wave beep
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                time_point = float(i) / sample_rate
                frequency = 800  # 800 Hz tone
                wave = 4096 * (0.5 * (1 + (time_point * frequency * 2 * 3.14159)))
                arr.append([int(wave), int(wave)])
            
            sound = pygame.sndarray.make_sound(arr)
            sound.play()
        except:
            print('\a')  # Final fallback
    
    def get_available_sounds(self) -> List[str]:
        """Get list of available sound names"""
        return list(self.available_sounds.keys())


class VoiceManager:
    """Manages text-to-speech functionality"""
    
    def __init__(self):
        self.engine = None
        self.enabled = False
        self.init_engine()
    
    def init_engine(self):
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            self.enabled = True
            
            # Set default properties
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Could not initialize voice engine: {e}")
            self.enabled = False
    
    def speak(self, text: str):
        """Speak the given text"""
        if self.enabled and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Voice error: {e}")
    
    def set_rate(self, rate: int):
        """Set speaking rate"""
        if self.enabled and self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set speaking volume (0.0 to 1.0)"""
        if self.enabled and self.engine:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def get_voices(self) -> List[Dict]:
        """Get available voices"""
        if self.enabled and self.engine:
            try:
                voices = self.engine.getProperty('voices')
                return [{'id': voice.id, 'name': voice.name} for voice in voices] if voices else []
            except:
                return []
        return []


class TimezoneManager:
    """Manages timezone functionality"""
    
    def __init__(self):
        self.current_timezone = "Local"
        self.common_timezones = [
            "Local",
            "UTC",
            "US/Eastern",
            "US/Central", 
            "US/Mountain",
            "US/Pacific",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Asia/Kolkata",
            "Australia/Sydney"
        ]
    
    def get_available_timezones(self) -> List[str]:
        """Get list of available timezones"""
        return self.common_timezones.copy()
    
    def get_time_for_timezone(self, timezone_name: str) -> datetime.datetime:
        """Get current time for specified timezone"""
        if timezone_name == "Local":
            return datetime.datetime.now()
        
        try:
            tz = pytz.timezone(timezone_name)
            utc_now = datetime.datetime.now(pytz.UTC)
            return utc_now.astimezone(tz)
        except pytz.exceptions.UnknownTimeZoneError:
            return datetime.datetime.now()
    
    def set_timezone(self, timezone_name: str):
        """Set current timezone"""
        if timezone_name in self.common_timezones:
            self.current_timezone = timezone_name
    
    def get_current_timezone(self) -> str:
        """Get current timezone"""
        return self.current_timezone


class AlarmManager:
    """Enhanced alarm manager with sound support"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.alarms = []
        self.alarm_callback = callback or self.default_alarm_callback
        self.is_monitoring = False
        self.monitor_thread = None
        self.sound_manager = SoundManager()
        self.voice_manager = VoiceManager()
    
    def add_alarm(self, alarm_time: str, label: str = "Alarm", sound: str = "default", voice_enabled: bool = False) -> bool:
        """
        Add a new alarm with sound and voice options
        Args:
            alarm_time: Time in HH:MM format
            label: Optional label for the alarm
            sound: Sound to play (from available sounds)
            voice_enabled: Whether to use voice announcement
        Returns:
            True if alarm was added successfully
        """
        try:
            hour, minute = map(int, alarm_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return False
            
            alarm = {
                'hour': hour,
                'minute': minute,
                'label': label,
                'enabled': True,
                'sound': sound,
                'voice_enabled': voice_enabled
            }
            
            self.alarms.append(alarm)
            self.start_monitoring()
            return True
        except ValueError:
            return False
    
    def remove_alarm(self, index: int) -> bool:
        """Remove alarm by index"""
        if 0 <= index < len(self.alarms):
            del self.alarms[index]
            if not self.alarms:
                self.stop_monitoring()
            return True
        return False
    
    def toggle_alarm(self, index: int) -> bool:
        """Toggle alarm enabled/disabled state"""
        if 0 <= index < len(self.alarms):
            self.alarms[index]['enabled'] = not self.alarms[index]['enabled']
            return True
        return False
    
    def start_monitoring(self):
        """Start monitoring for alarms"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_alarms, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring for alarms"""
        self.is_monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1)
    
    def _monitor_alarms(self):
        """Monitor for alarm triggers"""
        while self.is_monitoring:
            try:
                current_time = datetime.datetime.now()
                current_hour = current_time.hour
                current_minute = current_time.minute
                current_second = current_time.second
                
                if current_second == 0:
                    for alarm in self.alarms:
                        if (alarm['enabled'] and 
                            alarm['hour'] == current_hour and 
                            alarm['minute'] == current_minute):
                            self._trigger_alarm(alarm)
                
                time.sleep(1)
            except Exception as e:
                print(f"Alarm monitoring error: {e}")
                break
    
    def _trigger_alarm(self, alarm):
        """Trigger an alarm with sound and voice"""
        # Play sound
        self.sound_manager.play_sound(alarm.get('sound', 'default'))
        
        # Voice announcement
        if alarm.get('voice_enabled', False):
            message = f"Alarm: {alarm['label']}"
            threading.Thread(target=self.voice_manager.speak, args=(message,), daemon=True).start()
        
        # System notification
        try:
            notification.notify(
                title="Alarm",
                message=f"{alarm['label']} - {alarm['hour']:02d}:{alarm['minute']:02d}",
                timeout=10
            )
        except:
            pass  # Notifications might not work in all environments
        
        # Call the callback
        self.alarm_callback(alarm)
    
    def default_alarm_callback(self, alarm):
        """Default alarm callback"""
        print(f"ALARM: {alarm['label']} - {alarm['hour']:02d}:{alarm['minute']:02d}")
    
    def get_alarms(self):
        """Get list of all alarms"""
        return self.alarms.copy()


class StopwatchTimer:
    """Enhanced stopwatch and timer functionality"""
    
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.is_paused = False
        
        # Timer mode
        self.timer_duration = 0
        self.timer_start_time = None
        self.is_timer_mode = False
        self.timer_callback = None
        
        # Lap functionality
        self.laps = []
        
        # Sound and voice
        self.sound_manager = SoundManager()
        self.voice_manager = VoiceManager()
    
    def start_stopwatch(self):
        """Start the stopwatch"""
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            self.is_paused = False
            self.is_timer_mode = False
        elif self.is_paused:
            self.start_time = time.time() - self.elapsed_time
            self.is_paused = False
    
    def pause_stopwatch(self):
        """Pause the stopwatch"""
        if self.is_running and not self.is_paused:
            self.elapsed_time = time.time() - self.start_time
            self.is_paused = True
    
    def stop_stopwatch(self):
        """Stop and reset the stopwatch"""
        self.is_running = False
        self.is_paused = False
        self.elapsed_time = 0
        self.start_time = None
        self.is_timer_mode = False
        self.laps.clear()
    
    def add_lap(self):
        """Add a lap time"""
        if self.is_running and not self.is_paused:
            lap_time = self.get_elapsed_time()
            self.laps.append(lap_time)
            return lap_time
        return None
    
    def get_laps(self) -> List[float]:
        """Get all lap times"""
        return self.laps.copy()
    
    def get_elapsed_time(self) -> float:
        """Get current elapsed time in seconds"""
        if self.is_running and not self.is_paused:
            if self.is_timer_mode:
                return self.get_timer_remaining()
            else:
                return time.time() - self.start_time
        return self.elapsed_time
    
    def format_time(self, seconds: float) -> str:
        """Format time as MM:SS.ss"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"
    
    def start_timer(self, duration_seconds: int, callback: Optional[Callable] = None):
        """Start countdown timer"""
        self.is_timer_mode = True
        self.timer_duration = duration_seconds
        self.timer_start_time = time.time()
        self.timer_callback = callback
        self.is_running = True
        self.is_paused = False
        
        # Start monitoring for timer completion
        threading.Thread(target=self._monitor_timer, daemon=True).start()
    
    def _monitor_timer(self):
        """Monitor timer completion"""
        while self.is_timer_mode and self.is_running:
            if self.get_timer_remaining() <= 0:
                self._timer_finished()
                break
            time.sleep(0.1)
    
    def _timer_finished(self):
        """Handle timer completion"""
        self.is_running = False
        self.is_timer_mode = False
        
        # Play sound
        self.sound_manager.play_sound('default')
        
        # Voice announcement
        threading.Thread(target=self.voice_manager.speak, args=("Timer finished",), daemon=True).start()
        
        # System notification
        try:
            notification.notify(
                title="Timer",
                message="Timer has finished!",
                timeout=10
            )
        except:
            pass
        
        # Call callback if provided
        if self.timer_callback:
            self.timer_callback()
    
    def get_timer_remaining(self) -> float:
        """Get remaining time on timer"""
        if self.is_timer_mode and self.is_running and not self.is_paused:
            elapsed = time.time() - self.timer_start_time
            remaining = max(0, self.timer_duration - elapsed)
            return remaining
        return 0
    
    def is_timer_finished(self) -> bool:
        """Check if timer has finished"""
        return self.is_timer_mode and self.get_timer_remaining() <= 0


class WeatherManager:
    """Manages weather integration functionality"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.current_weather = {}
        self.forecast = []
        self.location = "Unknown"
        self.enabled = False
        self.last_update = None
        self.update_interval = 600  # 10 minutes
        
    def set_api_key(self, api_key: str):
        """Set weather API key"""
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def set_location(self, location: str):
        """Set weather location"""
        self.location = location
        if self.enabled:
            self.update_weather()
    
    def update_weather(self) -> bool:
        """Update weather data from API"""
        if not self.enabled or not self.api_key:
            return False
            
        try:
            # Mock weather data for demonstration (replace with actual API call)
            self.current_weather = {
                "temperature": 72,
                "humidity": 45,
                "description": "Partly Cloudy",
                "icon": "partly-cloudy",
                "wind_speed": 8,
                "pressure": 1013
            }
            self.forecast = [
                {"day": "Today", "high": 75, "low": 58, "description": "Partly Cloudy"},
                {"day": "Tomorrow", "high": 78, "low": 62, "description": "Sunny"},
                {"day": "Saturday", "high": 73, "low": 55, "description": "Rain"}
            ]
            self.last_update = datetime.datetime.now()
            return True
        except Exception as e:
            print(f"Weather update failed: {e}")
            return False
    
    def get_current_weather(self) -> Dict:
        """Get current weather data"""
        if self.needs_update():
            self.update_weather()
        return self.current_weather
    
    def get_forecast(self) -> List[Dict]:
        """Get weather forecast"""
        if self.needs_update():
            self.update_weather()
        return self.forecast
    
    def needs_update(self) -> bool:
        """Check if weather data needs updating"""
        if not self.last_update:
            return True
        elapsed = (datetime.datetime.now() - self.last_update).total_seconds()
        return elapsed > self.update_interval


class CalendarManager:
    """Manages calendar synchronization functionality"""
    
    def __init__(self):
        self.events = []
        self.enabled = False
        self.calendar_sources = []
        self.last_sync = None
        
    def add_calendar_source(self, source_type: str, config: Dict):
        """Add a calendar source (Google, Outlook, etc.)"""
        source = {
            "type": source_type,
            "config": config,
            "enabled": True
        }
        self.calendar_sources.append(source)
        
    def sync_calendars(self) -> bool:
        """Sync with all enabled calendar sources"""
        if not self.enabled:
            return False
            
        try:
            # Mock calendar events for demonstration
            self.events = [
                {
                    "title": "Team Meeting",
                    "start": datetime.datetime.now() + datetime.timedelta(hours=2),
                    "end": datetime.datetime.now() + datetime.timedelta(hours=3),
                    "description": "Weekly team standup"
                },
                {
                    "title": "Doctor Appointment", 
                    "start": datetime.datetime.now() + datetime.timedelta(days=1, hours=10),
                    "end": datetime.datetime.now() + datetime.timedelta(days=1, hours=11),
                    "description": "Annual checkup"
                }
            ]
            self.last_sync = datetime.datetime.now()
            return True
        except Exception as e:
            print(f"Calendar sync failed: {e}")
            return False
    
    def get_upcoming_events(self, hours_ahead: int = 24) -> List[Dict]:
        """Get upcoming events within specified hours"""
        if not self.events:
            self.sync_calendars()
            
        cutoff = datetime.datetime.now() + datetime.timedelta(hours=hours_ahead)
        upcoming = [event for event in self.events if event["start"] <= cutoff]
        return sorted(upcoming, key=lambda x: x["start"])
    
    def get_next_event(self) -> Optional[Dict]:
        """Get the next upcoming event"""
        upcoming = self.get_upcoming_events(168)  # Next week
        return upcoming[0] if upcoming else None


class MultiMonitorManager:
    """Manages multiple monitor support"""
    
    def __init__(self):
        self.monitors = []
        self.current_monitor = 0
        self.enabled = False
        self.detect_monitors()
        
    def detect_monitors(self):
        """Detect available monitors"""
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            
            # Get screen dimensions
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            # Mock multiple monitor detection
            self.monitors = [
                {
                    "id": 0,
                    "name": "Primary Monitor",
                    "width": screen_width,
                    "height": screen_height,
                    "x": 0,
                    "y": 0,
                    "primary": True
                }
            ]
            
            # Add secondary monitor if screen is wide enough (mock detection)
            if screen_width > 1920:
                self.monitors.append({
                    "id": 1,
                    "name": "Secondary Monitor", 
                    "width": screen_width - 1920,
                    "height": screen_height,
                    "x": 1920,
                    "y": 0,
                    "primary": False
                })
                
            root.destroy()
        except Exception as e:
            print(f"Monitor detection failed: {e}")
            # Fallback: create a default monitor
            self.monitors = [
                {
                    "id": 0,
                    "name": "Default Monitor",
                    "width": 1920,
                    "height": 1080,
                    "x": 0,
                    "y": 0,
                    "primary": True
                }
            ]
            
    def get_monitors(self) -> List[Dict]:
        """Get list of available monitors"""
        return self.monitors
    
    def set_monitor(self, monitor_id: int) -> bool:
        """Set target monitor for clock display"""
        if 0 <= monitor_id < len(self.monitors):
            self.current_monitor = monitor_id
            return True
        return False
    
    def get_monitor_geometry(self, monitor_id: Optional[int] = None) -> Dict:
        """Get geometry for specified monitor"""
        if monitor_id is None:
            monitor_id = self.current_monitor
            
        if 0 <= monitor_id < len(self.monitors):
            monitor = self.monitors[monitor_id]
            return {
                "x": monitor["x"],
                "y": monitor["y"], 
                "width": monitor["width"],
                "height": monitor["height"]
            }
        return {"x": 0, "y": 0, "width": 800, "height": 600}


class PluginManager:
    """Manages plugin system for custom features"""
    
    def __init__(self):
        self.plugins = {}
        self.enabled_plugins = set()
        self.plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        self.ensure_plugin_dir()
        
    def ensure_plugin_dir(self):
        """Ensure plugins directory exists"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            
    def load_plugins(self):
        """Load all available plugins"""
        if not os.path.exists(self.plugin_dir):
            return
            
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                plugin_name = filename[:-3]
                try:
                    self.load_plugin(plugin_name)
                except Exception as e:
                    print(f"Failed to load plugin {plugin_name}: {e}")
    
    def load_plugin(self, plugin_name: str):
        """Load a specific plugin"""
        plugin_file = os.path.join(self.plugin_dir, f"{plugin_name}.py")
        if not os.path.exists(plugin_file):
            return False
            
        # Mock plugin loading for demonstration
        self.plugins[plugin_name] = {
            "name": plugin_name,
            "version": "1.0.0",
            "description": f"Custom {plugin_name} plugin",
            "enabled": False,
            "instance": None
        }
        return True
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name]["enabled"] = True
            self.enabled_plugins.add(plugin_name)
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name]["enabled"] = False
            self.enabled_plugins.discard(plugin_name)
            return True
        return False
    
    def get_plugins(self) -> Dict:
        """Get all available plugins"""
        return self.plugins.copy()
    
    def get_enabled_plugins(self) -> List[str]:
        """Get list of enabled plugin names"""
        return list(self.enabled_plugins)


class CloudSyncManager:
    """Manages cloud settings synchronization"""
    
    def __init__(self):
        self.enabled = False
        self.sync_provider = None
        self.last_sync = None
        self.sync_url = None
        self.user_token = None
        
    def configure_sync(self, provider: str, sync_url: str, user_token: str):
        """Configure cloud sync settings"""
        self.sync_provider = provider
        self.sync_url = sync_url
        self.user_token = user_token
        self.enabled = True
        
    def upload_settings(self, settings: Dict) -> bool:
        """Upload settings to cloud"""
        if not self.enabled:
            return False
            
        try:
            # Mock cloud upload for demonstration
            sync_data = {
                "settings": settings,
                "timestamp": datetime.datetime.now().isoformat(),
                "device": platform.node()
            }
            # In real implementation, would POST to sync_url
            print(f"Settings uploaded to {self.sync_provider}")
            self.last_sync = datetime.datetime.now()
            return True
        except Exception as e:
            print(f"Cloud sync upload failed: {e}")
            return False
    
    def download_settings(self) -> Optional[Dict]:
        """Download settings from cloud"""
        if not self.enabled:
            return None
            
        try:
            # Mock cloud download for demonstration
            cloud_settings = {
                "theme": "dark",
                "font_size": 48,
                "timezone": "UTC",
                "weather_enabled": True
            }
            self.last_sync = datetime.datetime.now()
            return cloud_settings
        except Exception as e:
            print(f"Cloud sync download failed: {e}")
            return None
    
    def sync_settings(self, local_settings: Dict) -> Optional[Dict]:
        """Synchronize settings with cloud"""
        if not self.enabled:
            return None
            
        # Upload local settings and download latest
        if self.upload_settings(local_settings):
            return self.download_settings()
        return None


class AdvancedScheduler:
    """Manages advanced scheduling features"""
    
    def __init__(self):
        self.schedules = []
        self.enabled = False
        self.running = False
        self.scheduler_thread = None
        
    def add_schedule(self, schedule_config: Dict):
        """Add a new schedule"""
        schedule = {
            "id": len(self.schedules),
            "name": schedule_config.get("name", f"Schedule {len(self.schedules)}"),
            "type": schedule_config.get("type", "daily"),  # daily, weekly, monthly, custom
            "time": schedule_config.get("time", "09:00"),
            "days": schedule_config.get("days", []),  # For weekly schedules
            "action": schedule_config.get("action", "notification"),
            "message": schedule_config.get("message", "Scheduled event"),
            "enabled": True,
            "last_run": None
        }
        self.schedules.append(schedule)
        return schedule["id"]
    
    def remove_schedule(self, schedule_id: int) -> bool:
        """Remove a schedule"""
        self.schedules = [s for s in self.schedules if s["id"] != schedule_id]
        return True
    
    def enable_schedule(self, schedule_id: int) -> bool:
        """Enable a schedule"""
        for schedule in self.schedules:
            if schedule["id"] == schedule_id:
                schedule["enabled"] = True
                return True
        return False
    
    def disable_schedule(self, schedule_id: int) -> bool:
        """Disable a schedule"""
        for schedule in self.schedules:
            if schedule["id"] == schedule_id:
                schedule["enabled"] = False
                return True
        return False
    
    def start_scheduler(self):
        """Start the scheduler thread"""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=1)
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                self._check_schedules()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Scheduler error: {e}")
                
    def _check_schedules(self):
        """Check if any schedules should run"""
        now = datetime.datetime.now()
        
        for schedule in self.schedules:
            if not schedule["enabled"]:
                continue
                
            if self._should_run_schedule(schedule, now):
                self._execute_schedule(schedule)
                schedule["last_run"] = now
    
    def _should_run_schedule(self, schedule: Dict, now: datetime.datetime) -> bool:
        """Check if a schedule should run now"""
        schedule_time = datetime.datetime.strptime(schedule["time"], "%H:%M").time()
        current_time = now.time()
        
        # Check if it's time to run (within 1 minute tolerance)
        time_diff = abs((now.replace(hour=schedule_time.hour, minute=schedule_time.minute, second=0, microsecond=0) - now).total_seconds())
        
        if time_diff > 60:  # Not within 1 minute of scheduled time
            return False
            
        # Check if already ran today
        if schedule["last_run"]:
            last_run_date = schedule["last_run"].date()
            if last_run_date == now.date():
                return False
                
        # Check schedule type
        if schedule["type"] == "daily":
            return True
        elif schedule["type"] == "weekly":
            return now.weekday() in schedule["days"]
        elif schedule["type"] == "monthly":
            return now.day == 1  # First day of month
            
        return False
    
    def _execute_schedule(self, schedule: Dict):
        """Execute a scheduled action"""
        try:
            if schedule["action"] == "notification":
                notification.notify(
                    title="Scheduled Event",
                    message=schedule["message"],
                    timeout=5
                )
            elif schedule["action"] == "sound":
                print('\a')  # System beep
            # Add more action types as needed
        except Exception as e:
            print(f"Failed to execute schedule {schedule['name']}: {e}")
    
    def get_schedules(self) -> List[Dict]:
        """Get all schedules"""
        return self.schedules.copy()