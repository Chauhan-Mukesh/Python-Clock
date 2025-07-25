"""
Enhanced Digital Clock Application with GUI
A modern, feature-rich digital clock built with tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import time
import datetime
import threading
from typing import Optional, Callable
from features import AlarmManager, StopwatchTimer, TimezoneManager, VoiceManager
from settings import SettingsManager
from clock_styles import ClockStyleManager
from system_tray import create_system_tray_manager


class DigitalClock:
    """Enhanced Digital Clock Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Enhanced Python Digital Clock")
        
        # Initialize managers
        self.settings = SettingsManager()
        self.style_manager = ClockStyleManager()
        self.timezone_manager = TimezoneManager()
        self.voice_manager = VoiceManager()
        
        # Load settings
        self.load_initial_settings()
        
        # Set window geometry
        geometry = self.settings.get("window_geometry", "700x600")
        self.root.geometry(geometry)
        self.root.minsize(500, 450)
        
        # Application state
        self.is_running = True
        
        # UI Variables
        self.time_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Enhanced features
        self.alarm_manager = AlarmManager(self.alarm_triggered)
        self.stopwatch = StopwatchTimer()
        
        # System tray
        self.system_tray = create_system_tray_manager(self)
        
        # Windows
        self.alarm_window = None
        self.stopwatch_window = None
        self.settings_window = None
        
        # Initialize UI
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Start clock update thread
        self.clock_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.clock_thread.start()
        
        # Enable system tray if requested
        if self.settings.get("system_tray_enabled", False):
            self.system_tray.enable_system_tray()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind window events
        self.root.bind('<Configure>', self.on_window_configure)
    
    def load_initial_settings(self):
        """Load initial settings from persistent storage"""
        self.is_24_hour = self.settings.get("is_24_hour", True)
        self.current_timezone = self.settings.get("timezone", "Local")
        self.theme = self.settings.get("theme", "light")
        self.clock_style = self.settings.get("clock_style", "digital")
        self.show_seconds = self.settings.get("show_seconds", True)
        self.show_date = self.settings.get("show_date", True)
        self.voice_enabled = self.settings.get("voice_enabled", False)
        
        # Set timezone
        self.timezone_manager.set_timezone(self.current_timezone)
        
        # Set voice properties
        if self.voice_enabled and self.voice_manager.enabled:
            self.voice_manager.set_rate(self.settings.get("voice_rate", 150))
            self.voice_manager.set_volume(self.settings.get("voice_volume", 0.9))
    
    
    def setup_styles(self):
        """Setup custom styles for the application"""
        self.style = ttk.Style()
        
        # Get style configuration
        if hasattr(self, 'style_manager') and hasattr(self, 'clock_style'):
            style_config = self.style_manager.get_style(self.clock_style).get_style_config(self.theme)
        else:
            style_config = {}
        
        if self.theme == "dark":
            self.bg_color = "#2b2b2b"
            self.fg_color = "#ffffff"
            self.accent_color = "#4a9eff"
            self.secondary_bg = "#404040"
        else:
            self.bg_color = "#ffffff"
            self.fg_color = "#333333"
            self.accent_color = "#0066cc"
            self.secondary_bg = "#f0f0f0"
        
        self.root.configure(bg=self.bg_color)
        
        # Configure custom styles
        font_family = self.settings.get("font_family", "Courier New") if hasattr(self, 'settings') else "Courier New"
        font_size = self.settings.get("font_size", 42) if hasattr(self, 'settings') else 42
        
        self.style.configure("Clock.TLabel", 
                           background=self.bg_color,
                           foreground=self.fg_color,
                           font=(font_family, font_size, "bold"))
        
        self.style.configure("Date.TLabel",
                           background=self.bg_color,
                           foreground=self.fg_color,
                           font=("Arial", 14))
        
        self.style.configure("Status.TLabel",
                           background=self.bg_color,
                           foreground=self.fg_color,
                           font=("Arial", 10))
        
        self.style.configure("Control.TButton",
                           background=self.accent_color,
                           foreground="white",
                           font=("Arial", 9),
                           padding=(10, 5))
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        
        # Time display
        self.time_label = ttk.Label(self.main_frame, 
                                   textvariable=self.time_var,
                                   style="Clock.TLabel",
                                   anchor="center")
        
        # Date display
        self.date_label = ttk.Label(self.main_frame,
                                   textvariable=self.date_var,
                                   style="Date.TLabel",
                                   anchor="center")
        
        # Status display
        self.status_label = ttk.Label(self.main_frame,
                                     textvariable=self.status_var,
                                     style="Status.TLabel",
                                     anchor="center")
        
        # Control panel
        self.control_frame = ttk.Frame(self.main_frame)
        
        # Time format button
        self.format_button = ttk.Button(self.control_frame,
                                       text="12H Format",
                                       command=self.toggle_time_format,
                                       style="Control.TButton")
        
        # Theme toggle button
        self.theme_button = ttk.Button(self.control_frame,
                                      text="Dark Theme",
                                      command=self.toggle_theme,
                                      style="Control.TButton")
        
        # Alarm button
        self.alarm_button = ttk.Button(self.control_frame,
                                      text="Alarms",
                                      command=self.show_alarm_manager,
                                      style="Control.TButton")
        
        # Stopwatch button
        self.stopwatch_button = ttk.Button(self.control_frame,
                                          text="Stopwatch",
                                          command=self.show_stopwatch_window,
                                          style="Control.TButton")
    
    def setup_layout(self):
        """Setup the layout of widgets"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Time and date
        self.time_label.pack(pady=(20, 10))
        self.date_label.pack(pady=5)
        self.status_label.pack(pady=5)
        
        # Control panel
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Buttons
        self.format_button.pack(side=tk.LEFT, padx=5)
        self.theme_button.pack(side=tk.LEFT, padx=5)
        self.alarm_button.pack(side=tk.LEFT, padx=5)
        self.stopwatch_button.pack(side=tk.LEFT, padx=5)
    
    def update_clock(self):
        """Update the clock display continuously"""
        while self.is_running:
            try:
                current_time = datetime.datetime.now()
                
                # Format time based on 12/24 hour preference
                if self.is_24_hour:
                    time_str = current_time.strftime("%H:%M:%S")
                else:
                    time_str = current_time.strftime("%I:%M:%S %p")
                
                # Format date
                date_str = current_time.strftime("%A, %B %d, %Y")
                
                # Update display variables
                self.time_var.set(time_str)
                self.date_var.set(date_str)
                
                time.sleep(1)
            except Exception as e:
                print(f"Clock update error: {e}")
                break
    
    def toggle_time_format(self):
        """Toggle between 12 and 24 hour time format"""
        self.is_24_hour = not self.is_24_hour
        self.format_button.configure(text="24H Format" if not self.is_24_hour else "12H Format")
        self.status_var.set(f"Switched to {'24-hour' if self.is_24_hour else '12-hour'} format")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.theme = "dark" if self.theme == "light" else "light"
        self.theme_button.configure(text="Light Theme" if self.theme == "dark" else "Dark Theme")
        self.setup_styles()
        self.status_var.set(f"Switched to {self.theme} theme")
    
    def alarm_triggered(self, alarm):
        """Handle alarm trigger"""
        message = f"Alarm: {alarm['label']}\nTime: {alarm['hour']:02d}:{alarm['minute']:02d}"
        messagebox.showinfo("Alarm", message)
        self.status_var.set(f"Alarm triggered: {alarm['label']}")
    
    def show_alarm_manager(self):
        """Show alarm management window"""
        if self.alarm_window is None or not self.alarm_window.winfo_exists():
            self.create_alarm_window()
        else:
            self.alarm_window.lift()
    
    def create_alarm_window(self):
        """Create alarm management window"""
        self.alarm_window = tk.Toplevel(self.root)
        self.alarm_window.title("Alarm Manager")
        self.alarm_window.geometry("400x300")
        self.alarm_window.configure(bg=self.bg_color)
        
        # Alarm list
        list_frame = ttk.Frame(self.alarm_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(list_frame, text="Active Alarms:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.alarm_listbox = tk.Listbox(list_frame, bg=self.secondary_bg, fg=self.fg_color)
        self.alarm_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Add Alarm", command=self.add_alarm_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove", command=self.remove_selected_alarm).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Toggle", command=self.toggle_selected_alarm).pack(side=tk.LEFT, padx=2)
        
        self.update_alarm_list()
    
    def add_alarm_dialog(self):
        """Show add alarm dialog"""
        time_str = simpledialog.askstring("Add Alarm", "Enter time (HH:MM):")
        if time_str:
            label = simpledialog.askstring("Add Alarm", "Enter label (optional):") or "Alarm"
            if self.alarm_manager.add_alarm(time_str, label):
                self.update_alarm_list()
                self.status_var.set(f"Alarm added: {time_str}")
            else:
                messagebox.showerror("Error", "Invalid time format. Use HH:MM")
    
    def remove_selected_alarm(self):
        """Remove selected alarm"""
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            if self.alarm_manager.remove_alarm(index):
                self.update_alarm_list()
                self.status_var.set("Alarm removed")
    
    def toggle_selected_alarm(self):
        """Toggle selected alarm"""
        selection = self.alarm_listbox.curselection()
        if selection:
            index = selection[0]
            if self.alarm_manager.toggle_alarm(index):
                self.update_alarm_list()
                self.status_var.set("Alarm toggled")
    
    def update_alarm_list(self):
        """Update the alarm list display"""
        if hasattr(self, 'alarm_listbox'):
            self.alarm_listbox.delete(0, tk.END)
            for alarm in self.alarm_manager.get_alarms():
                status = "ON" if alarm['enabled'] else "OFF"
                time_str = f"{alarm['hour']:02d}:{alarm['minute']:02d}"
                display = f"{time_str} - {alarm['label']} ({status})"
                self.alarm_listbox.insert(tk.END, display)
    
    def show_stopwatch_window(self):
        """Show stopwatch window"""
        if self.stopwatch_window is None or not self.stopwatch_window.winfo_exists():
            self.create_stopwatch_window()
        else:
            self.stopwatch_window.lift()
    
    def create_stopwatch_window(self):
        """Create stopwatch window"""
        self.stopwatch_window = tk.Toplevel(self.root)
        self.stopwatch_window.title("Stopwatch")
        self.stopwatch_window.geometry("300x200")
        self.stopwatch_window.configure(bg=self.bg_color)
        
        # Time display
        self.stopwatch_var = tk.StringVar()
        self.stopwatch_var.set("00:00.00")
        
        time_label = ttk.Label(self.stopwatch_window, 
                              textvariable=self.stopwatch_var,
                              font=("Courier New", 24, "bold"))
        time_label.pack(pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(self.stopwatch_window)
        button_frame.pack(pady=10)
        
        self.start_pause_button = ttk.Button(button_frame, text="Start", command=self.toggle_stopwatch)
        self.start_pause_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Reset", command=self.reset_stopwatch).pack(side=tk.LEFT, padx=5)
        
        # Start stopwatch update
        self.update_stopwatch_display()
    
    def toggle_stopwatch(self):
        """Toggle stopwatch start/pause"""
        if not self.stopwatch.is_running:
            self.stopwatch.start_stopwatch()
            self.start_pause_button.configure(text="Pause")
        elif not self.stopwatch.is_paused:
            self.stopwatch.pause_stopwatch()
            self.start_pause_button.configure(text="Resume")
        else:
            self.stopwatch.start_stopwatch()
            self.start_pause_button.configure(text="Pause")
    
    def reset_stopwatch(self):
        """Reset stopwatch"""
        self.stopwatch.stop_stopwatch()
        self.start_pause_button.configure(text="Start")
        self.stopwatch_var.set("00:00.00")
    
    def update_stopwatch_display(self):
        """Update stopwatch display"""
        if hasattr(self, 'stopwatch_var'):
            elapsed = self.stopwatch.get_elapsed_time()
            formatted_time = self.stopwatch.format_time(elapsed)
            self.stopwatch_var.set(formatted_time)
            
            # Schedule next update
            self.root.after(10, self.update_stopwatch_display)
    
    def on_closing(self):
        """Handle application closing"""
        self.is_running = False
        self.alarm_manager.stop_monitoring()
        
        if self.clock_thread.is_alive():
            self.clock_thread.join(timeout=1)
        
        # Close child windows
        if self.alarm_window and self.alarm_window.winfo_exists():
            self.alarm_window.destroy()
        if self.stopwatch_window and self.stopwatch_window.winfo_exists():
            self.stopwatch_window.destroy()
            
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = DigitalClock()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()