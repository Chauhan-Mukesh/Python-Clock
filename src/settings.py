"""
Settings management for the Digital Clock Application
Handles persistence of user preferences and configuration
"""

import json
import os
from typing import Dict, Any, Optional

class SettingsManager:
    """Manages application settings and persistence"""
    
    def __init__(self, settings_file: str = "clock_settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "theme": "light",
            "is_24_hour": True,
            "timezone": "Local",
            "clock_style": "digital",
            "font_family": "Courier New",
            "font_size": 42,
            "alarm_sound": "default",
            "voice_enabled": False,
            "voice_rate": 150,
            "voice_volume": 0.9,
            "show_seconds": True,
            "show_date": True,
            "window_geometry": "600x500",
            "system_tray_enabled": False,
            "auto_save": True,
            # New feature settings
            "weather_enabled": False,
            "weather_api_key": "",
            "weather_location": "New York",
            "calendar_enabled": False,
            "calendar_sources": [],
            "multi_monitor_enabled": False,
            "current_monitor": 0,
            "plugins_enabled": True,
            "enabled_plugins": [],
            "cloud_sync_enabled": False,
            "cloud_sync_url": "",
            "cloud_sync_token": "",
            "scheduler_enabled": False,
            "scheduler_autostart": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                # Merge with defaults to handle missing keys
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                return settings
            else:
                return self.default_settings.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value"""
        self.settings[key] = value
        if self.get("auto_save", True):
            self.save_settings()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple settings at once"""
        self.settings.update(updates)
        if self.get("auto_save", True):
            self.save_settings()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get a copy of all current settings"""
        return self.settings.copy()