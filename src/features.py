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