"""
System tray integration for the Digital Clock Application
"""

import tkinter as tk
from tkinter import messagebox
import threading
from typing import Optional, Callable
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except (ImportError, ValueError) as e:
    # Handle both import errors and GTK not available errors
    PYSTRAY_AVAILABLE = False
    print(f"System tray dependencies not available: {e}")


class SystemTrayManager:
    """Manages system tray integration"""
    
    def __init__(self, app_instance=None):
        self.app_instance = app_instance
        self.tray_icon = None
        self.tray_thread = None
        self.is_enabled = False
        self.is_running = False
        
        # Check if system tray is available
        self.available = PYSTRAY_AVAILABLE
        
        if not self.available:
            print("System tray not available: pystray and PIL not installed")
    
    def create_tray_icon(self):
        """Create system tray icon"""
        if not self.available:
            return None
        
        try:
            # Create a simple clock icon
            image = Image.new('RGB', (64, 64), color='white')
            draw = ImageDraw.Draw(image)
            
            # Draw clock face
            draw.ellipse([4, 4, 60, 60], outline='black', width=2)
            
            # Draw clock hands (12:00 position)
            center_x, center_y = 32, 32
            # Hour hand
            draw.line([center_x, center_y, center_x, center_y - 15], fill='black', width=3)
            # Minute hand  
            draw.line([center_x, center_y, center_x, center_y - 20], fill='black', width=2)
            
            # Draw center dot
            draw.ellipse([center_x-2, center_y-2, center_x+2, center_y+2], fill='black')
            
            return image
        except Exception as e:
            print(f"Error creating tray icon: {e}")
            return None
    
    def create_tray_menu(self):
        """Create system tray context menu"""
        if not self.available:
            return None
        
        try:
            menu_items = [
                pystray.MenuItem("Show Clock", self.show_app),
                pystray.MenuItem("Hide Clock", self.hide_app),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Alarms", self.show_alarms),
                pystray.MenuItem("Stopwatch", self.show_stopwatch),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Settings", self.show_settings),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit", self.quit_app)
            ]
            
            return pystray.Menu(*menu_items)
        except Exception as e:
            print(f"Error creating tray menu: {e}")
            return None
    
    def enable_system_tray(self):
        """Enable system tray integration"""
        if not self.available or self.is_enabled:
            return False
        
        try:
            icon_image = self.create_tray_icon()
            menu = self.create_tray_menu()
            
            if icon_image and menu:
                self.tray_icon = pystray.Icon(
                    "Python Clock",
                    icon_image,
                    "Python Digital Clock",
                    menu
                )
                
                # Start tray icon in separate thread
                self.tray_thread = threading.Thread(target=self._run_tray, daemon=True)
                self.tray_thread.start()
                
                self.is_enabled = True
                return True
            
        except Exception as e:
            print(f"Error enabling system tray: {e}")
        
        return False
    
    def disable_system_tray(self):
        """Disable system tray integration"""
        if not self.is_enabled:
            return
        
        try:
            if self.tray_icon:
                self.is_running = False
                self.tray_icon.stop()
                self.tray_icon = None
            
            self.is_enabled = False
            
        except Exception as e:
            print(f"Error disabling system tray: {e}")
    
    def _run_tray(self):
        """Run the system tray icon"""
        try:
            if self.tray_icon:
                self.is_running = True
                self.tray_icon.run()
        except Exception as e:
            print(f"Error running system tray: {e}")
    
    def show_notification(self, title: str, message: str, timeout: int = 5):
        """Show system notification"""
        try:
            if PLYER_AVAILABLE:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=timeout
                )
            else:
                # Fallback to tkinter messagebox
                messagebox.showinfo(title, message)
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    # Menu action handlers
    def show_app(self, icon=None, item=None):
        """Show the main application window"""
        if self.app_instance and hasattr(self.app_instance, 'root'):
            self.app_instance.root.deiconify()
            self.app_instance.root.lift()
            self.app_instance.root.attributes('-topmost', True)
            self.app_instance.root.attributes('-topmost', False)
    
    def hide_app(self, icon=None, item=None):
        """Hide the main application window"""
        if self.app_instance and hasattr(self.app_instance, 'root'):
            self.app_instance.root.withdraw()
    
    def show_alarms(self, icon=None, item=None):
        """Show alarms window"""
        if self.app_instance and hasattr(self.app_instance, 'show_alarm_manager'):
            self.show_app()  # Ensure main window is visible first
            self.app_instance.show_alarm_manager()
    
    def show_stopwatch(self, icon=None, item=None):
        """Show stopwatch window"""
        if self.app_instance and hasattr(self.app_instance, 'show_stopwatch_window'):
            self.show_app()  # Ensure main window is visible first
            self.app_instance.show_stopwatch_window()
    
    def show_settings(self, icon=None, item=None):
        """Show settings window"""
        if self.app_instance and hasattr(self.app_instance, 'show_settings_window'):
            self.show_app()  # Ensure main window is visible first
            self.app_instance.show_settings_window()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        if self.app_instance and hasattr(self.app_instance, 'on_closing'):
            self.app_instance.on_closing()
    
    def update_tray_tooltip(self, time_str: str):
        """Update the system tray tooltip with current time"""
        if self.tray_icon and self.is_enabled:
            try:
                self.tray_icon.title = f"Python Clock - {time_str}"
            except Exception as e:
                print(f"Error updating tray tooltip: {e}")


class MinimalSystemTray:
    """Minimal system tray fallback when pystray is not available"""
    
    def __init__(self, app_instance=None):
        self.app_instance = app_instance
        self.available = True  # Always available as fallback
        self.is_enabled = False
    
    def enable_system_tray(self):
        """Enable minimal system tray simulation"""
        self.is_enabled = True
        print("System tray enabled (minimal mode)")
        return True
    
    def disable_system_tray(self):
        """Disable minimal system tray"""
        self.is_enabled = False
        print("System tray disabled")
    
    def show_notification(self, title: str, message: str, timeout: int = 5):
        """Show notification using tkinter"""
        try:
            if PLYER_AVAILABLE:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=timeout
                )
            else:
                messagebox.showinfo(title, message)
        except Exception as e:
            print(f"Notification: {title} - {message}")
    
    def update_tray_tooltip(self, time_str: str):
        """Update tooltip (no-op for minimal mode)"""
        pass
    
    def show_app(self):
        """Show the main application"""
        if self.app_instance and hasattr(self.app_instance, 'root'):
            self.app_instance.root.deiconify()
            self.app_instance.root.lift()
    
    def hide_app(self):
        """Hide the main application"""
        if self.app_instance and hasattr(self.app_instance, 'root'):
            self.app_instance.root.withdraw()


def create_system_tray_manager(app_instance=None):
    """Factory function to create appropriate system tray manager"""
    if PYSTRAY_AVAILABLE:
        return SystemTrayManager(app_instance)
    else:
        return MinimalSystemTray(app_instance)