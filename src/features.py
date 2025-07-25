"""
Alarm functionality for the Digital Clock Application
"""

import datetime
import threading
import time
from typing import Optional, Callable


class AlarmManager:
    """Manages alarm functionality for the clock"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.alarms = []
        self.active_alarm = None
        self.alarm_callback = callback or self.default_alarm_callback
        self.is_monitoring = False
        self.monitor_thread = None
    
    def add_alarm(self, alarm_time: str, label: str = "Alarm") -> bool:
        """
        Add a new alarm
        Args:
            alarm_time: Time in HH:MM format
            label: Optional label for the alarm
        Returns:
            True if alarm was added successfully
        """
        try:
            # Parse time
            hour, minute = map(int, alarm_time.split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return False
            
            # Create alarm
            alarm = {
                'hour': hour,
                'minute': minute,
                'label': label,
                'enabled': True
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
                
                # Check alarms only at the start of each minute
                if current_second == 0:
                    for alarm in self.alarms:
                        if (alarm['enabled'] and 
                            alarm['hour'] == current_hour and 
                            alarm['minute'] == current_minute):
                            self.alarm_callback(alarm)
                
                time.sleep(1)
            except Exception as e:
                print(f"Alarm monitoring error: {e}")
                break
    
    def default_alarm_callback(self, alarm):
        """Default alarm callback"""
        print(f"ALARM: {alarm['label']} - {alarm['hour']:02d}:{alarm['minute']:02d}")
    
    def get_alarms(self):
        """Get list of all alarms"""
        return self.alarms.copy()


class StopwatchTimer:
    """Stopwatch and timer functionality"""
    
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.is_paused = False
        
        # Timer mode
        self.timer_duration = 0
        self.timer_start_time = None
        self.is_timer_mode = False
    
    def start_stopwatch(self):
        """Start the stopwatch"""
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            self.is_paused = False
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
    
    def get_elapsed_time(self) -> float:
        """Get current elapsed time in seconds"""
        if self.is_running and not self.is_paused:
            return time.time() - self.start_time
        return self.elapsed_time
    
    def format_time(self, seconds: float) -> str:
        """Format time as MM:SS.ss"""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:05.2f}"
    
    def start_timer(self, duration_seconds: int):
        """Start countdown timer"""
        self.is_timer_mode = True
        self.timer_duration = duration_seconds
        self.timer_start_time = time.time()
        self.is_running = True
    
    def get_timer_remaining(self) -> float:
        """Get remaining time on timer"""
        if self.is_timer_mode and self.is_running:
            elapsed = time.time() - self.timer_start_time
            remaining = max(0, self.timer_duration - elapsed)
            return remaining
        return 0
    
    def is_timer_finished(self) -> bool:
        """Check if timer has finished"""
        return self.is_timer_mode and self.get_timer_remaining() <= 0