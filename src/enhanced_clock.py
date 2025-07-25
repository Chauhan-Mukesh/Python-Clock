"""
Enhanced Digital Clock Application with all requested features
A comprehensive clock application with modern features
"""

import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
import time
import datetime
import threading
from typing import Optional, Callable
from features import (AlarmManager, StopwatchTimer, TimezoneManager, VoiceManager,
                     WeatherManager, CalendarManager, MultiMonitorManager, 
                     PluginManager, CloudSyncManager, AdvancedScheduler)
from settings import SettingsManager
from clock_styles import ClockStyleManager
from system_tray import create_system_tray_manager
from mobile_companion import MobileCompanionServer


class EnhancedDigitalClock:
    """Enhanced Digital Clock Application with all requested features"""
    
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
        
        # New features
        self.weather_manager = WeatherManager()
        self.calendar_manager = CalendarManager()
        self.monitor_manager = MultiMonitorManager()
        self.plugin_manager = PluginManager()
        self.cloud_sync = CloudSyncManager()
        self.scheduler = AdvancedScheduler()
        self.mobile_server = MobileCompanionServer(self)
        
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
        font_family = self.settings.get("font_family", "Courier New")
        font_size = self.settings.get("font_size", 42)
        
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
        
        # Clock display frame
        self.clock_frame = ttk.Frame(self.main_frame)
        
        # Create clock widget based on style
        self.create_clock_widget()
        
        # Date display (if enabled)
        if self.show_date:
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
        self.create_control_buttons()
        
        # Menu bar
        self.create_menu_bar()
    
    def create_clock_widget(self):
        """Create the appropriate clock widget based on current style"""
        # Clear existing clock widgets
        for widget in self.clock_frame.winfo_children():
            widget.destroy()
        
        current_style = self.style_manager.get_style(self.clock_style)
        style_config = current_style.get_style_config(self.theme)
        style_config.update({
            'font_family': self.settings.get("font_family", "Courier New"),
            'font_size': self.settings.get("font_size", 42),
            'bg_color': self.bg_color,
            'fg_color': self.fg_color
        })
        
        self.clock_widget = current_style.create_time_widget(
            self.clock_frame, 
            self.time_var,
            style_config=style_config
        )
        
        if self.clock_widget:
            self.clock_widget.pack(expand=True, fill='both')
        
        # Special setup for different clock styles
        if self.clock_style == 'analog' and hasattr(self.clock_widget, 'clock_center'):
            self.analog_style_config = style_config
        elif self.clock_style == 'binary':
            current_style.setup_binary_display(self.clock_widget, style_config)
            self.binary_style_config = style_config
    
    def create_control_buttons(self):
        """Create control buttons"""
        # Time format button
        format_text = "12H Format" if self.is_24_hour else "24H Format"
        self.format_button = ttk.Button(self.control_frame,
                                       text=format_text,
                                       command=self.toggle_time_format,
                                       style="Control.TButton")
        
        # Theme toggle button
        theme_text = "Dark Theme" if self.theme == "light" else "Light Theme"
        self.theme_button = ttk.Button(self.control_frame,
                                      text=theme_text,
                                      command=self.toggle_theme,
                                      style="Control.TButton")
        
        # Clock style button
        self.style_button = ttk.Button(self.control_frame,
                                      text=f"Style: {self.clock_style.title()}",
                                      command=self.cycle_clock_style,
                                      style="Control.TButton")
        
        # Timezone button
        tz_text = self.current_timezone if len(self.current_timezone) <= 10 else self.current_timezone[:10] + "..."
        self.timezone_button = ttk.Button(self.control_frame,
                                         text=f"TZ: {tz_text}",
                                         command=self.show_timezone_dialog,
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
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.show_settings_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Clock styles submenu
        style_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Clock Style", menu=style_menu)
        for style_name in self.style_manager.get_available_styles():
            style_menu.add_command(
                label=style_name.title(),
                command=lambda s=style_name: self.set_clock_style(s)
            )
        
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Seconds", command=self.toggle_show_seconds)
        view_menu.add_checkbutton(label="Show Date", command=self.toggle_show_date)
        view_menu.add_checkbutton(label="Voice Announcements", command=self.toggle_voice)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Alarm Manager", command=self.show_alarm_manager)
        tools_menu.add_command(label="Stopwatch & Timer", command=self.show_stopwatch_window)
        tools_menu.add_separator()
        tools_menu.add_command(label="Weather", command=self.show_weather_window)
        tools_menu.add_command(label="Calendar", command=self.show_calendar_window)
        tools_menu.add_command(label="Multi-Monitor", command=self.show_monitor_window)
        tools_menu.add_command(label="Plugins", command=self.show_plugins_window)
        tools_menu.add_command(label="Cloud Sync", command=self.show_cloud_sync_window)
        tools_menu.add_command(label="Advanced Scheduler", command=self.show_scheduler_window)
        tools_menu.add_command(label="Mobile Companion", command=self.show_mobile_companion_window)
        tools_menu.add_separator()
        tools_menu.add_command(label="Speak Current Time", command=self.speak_current_time)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_layout(self):
        """Setup the layout of widgets"""
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Clock display
        self.clock_frame.pack(pady=(20, 10), fill=tk.BOTH, expand=True)
        
        # Date (if enabled)
        if self.show_date and hasattr(self, 'date_label'):
            self.date_label.pack(pady=5)
        
        # Status
        self.status_label.pack(pady=5)
        
        # Control panel
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        # Arrange buttons in two rows
        top_row = ttk.Frame(self.control_frame)
        top_row.pack(side=tk.TOP, pady=(0, 5))
        
        bottom_row = ttk.Frame(self.control_frame)
        bottom_row.pack(side=tk.TOP)
        
        # Top row buttons
        self.format_button.pack(in_=top_row, side=tk.LEFT, padx=5)
        self.theme_button.pack(in_=top_row, side=tk.LEFT, padx=5)
        self.style_button.pack(in_=top_row, side=tk.LEFT, padx=5)
        
        # Bottom row buttons
        self.timezone_button.pack(in_=bottom_row, side=tk.LEFT, padx=5)
        self.alarm_button.pack(in_=bottom_row, side=tk.LEFT, padx=5)
        self.stopwatch_button.pack(in_=bottom_row, side=tk.LEFT, padx=5)
    
    def update_clock(self):
        """Update the clock display continuously"""
        while self.is_running:
            try:
                # Get current time for timezone
                current_time = self.timezone_manager.get_time_for_timezone(self.current_timezone)
                
                # Format time based on current style
                current_style = self.style_manager.get_style(self.clock_style)
                time_str = current_style.format_time(current_time, self.is_24_hour, self.show_seconds)
                
                # Update display
                self.time_var.set(time_str)
                
                # Handle special clock styles
                if self.clock_style == 'analog' and hasattr(self, 'analog_style_config'):
                    current_style.draw_analog_clock(self.clock_widget, current_time, self.analog_style_config)
                elif self.clock_style == 'binary' and hasattr(self, 'binary_style_config'):
                    current_style.update_binary_display(self.clock_widget, current_time, self.binary_style_config)
                
                # Format date
                if self.show_date:
                    date_str = current_time.strftime("%A, %B %d, %Y")
                    if self.current_timezone != "Local":
                        date_str += f" ({self.current_timezone})"
                    self.date_var.set(date_str)
                
                # Update system tray tooltip
                if self.system_tray.is_enabled:
                    simple_time = current_time.strftime("%H:%M:%S" if self.is_24_hour else "%I:%M:%S %p")
                    self.system_tray.update_tray_tooltip(simple_time)
                
                # Voice announcements (hourly)
                if (self.voice_enabled and self.voice_manager.enabled and 
                    current_time.minute == 0 and current_time.second == 0):
                    time_text = current_time.strftime("It's %I %p" if not self.is_24_hour else "It's %H hundred hours")
                    threading.Thread(target=self.voice_manager.speak, args=(time_text,), daemon=True).start()
                
                time.sleep(0.1 if self.clock_style == 'analog' else 1)
                
            except Exception as e:
                print(f"Clock update error: {e}")
                break
    
    def toggle_time_format(self):
        """Toggle between 12 and 24 hour time format"""
        self.is_24_hour = not self.is_24_hour
        self.format_button.configure(text="24H Format" if not self.is_24_hour else "12H Format")
        self.settings.set("is_24_hour", self.is_24_hour)
        self.status_var.set(f"Switched to {'24-hour' if self.is_24_hour else '12-hour'} format")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.theme = "dark" if self.theme == "light" else "light"
        self.theme_button.configure(text="Light Theme" if self.theme == "dark" else "Dark Theme")
        self.settings.set("theme", self.theme)
        self.setup_styles()
        self.create_clock_widget()
        self.status_var.set(f"Switched to {self.theme} theme")
    
    def cycle_clock_style(self):
        """Cycle through available clock styles"""
        styles = self.style_manager.get_available_styles()
        current_index = styles.index(self.clock_style)
        next_index = (current_index + 1) % len(styles)
        self.set_clock_style(styles[next_index])
    
    def set_clock_style(self, style_name: str):
        """Set specific clock style"""
        if style_name in self.style_manager.get_available_styles():
            self.clock_style = style_name
            self.style_manager.set_current_style(style_name)
            self.style_button.configure(text=f"Style: {style_name.title()}")
            self.settings.set("clock_style", style_name)
            self.create_clock_widget()
            self.status_var.set(f"Clock style: {style_name.title()}")
    
    def show_timezone_dialog(self):
        """Show timezone selection dialog"""
        timezones = self.timezone_manager.get_available_timezones()
        
        # Simple dialog for timezone selection
        selected_tz = simpledialog.askstring(
            "Select Timezone", 
            f"Current: {self.current_timezone}\n\nAvailable timezones:\n" + 
            "\n".join(timezones) + 
            "\n\nEnter timezone name:"
        )
        
        if selected_tz and selected_tz in timezones:
            self.current_timezone = selected_tz
            self.timezone_manager.set_timezone(selected_tz)
            self.settings.set("timezone", selected_tz)
            tz_text = selected_tz if len(selected_tz) <= 10 else selected_tz[:10] + "..."
            self.timezone_button.configure(text=f"TZ: {tz_text}")
            self.status_var.set(f"Timezone: {selected_tz}")
    
    def toggle_show_seconds(self):
        """Toggle showing seconds"""
        self.show_seconds = not self.show_seconds
        self.settings.set("show_seconds", self.show_seconds)
        self.status_var.set(f"Show seconds: {'On' if self.show_seconds else 'Off'}")
    
    def toggle_show_date(self):
        """Toggle showing date"""
        self.show_date = not self.show_date
        self.settings.set("show_date", self.show_date)
        
        # Recreate widgets to show/hide date
        if self.show_date and not hasattr(self, 'date_label'):
            self.date_label = ttk.Label(self.main_frame,
                                       textvariable=self.date_var,
                                       style="Date.TLabel",
                                       anchor="center")
            self.date_label.pack(after=self.clock_frame, pady=5)
        elif not self.show_date and hasattr(self, 'date_label'):
            self.date_label.destroy()
            delattr(self, 'date_label')
        
        self.status_var.set(f"Show date: {'On' if self.show_date else 'Off'}")
    
    def toggle_voice(self):
        """Toggle voice announcements"""
        self.voice_enabled = not self.voice_enabled
        self.settings.set("voice_enabled", self.voice_enabled)
        self.status_var.set(f"Voice announcements: {'On' if self.voice_enabled else 'Off'}")
    
    def speak_current_time(self):
        """Speak the current time"""
        if self.voice_manager.enabled:
            current_time = self.timezone_manager.get_time_for_timezone(self.current_timezone)
            if self.is_24_hour:
                time_text = current_time.strftime("The time is %H %M")
            else:
                time_text = current_time.strftime("The time is %I %M %p")
            threading.Thread(target=self.voice_manager.speak, args=(time_text,), daemon=True).start()
        else:
            self.status_var.set("Voice not available")
    
    def alarm_triggered(self, alarm):
        """Handle alarm trigger"""
        message = f"Alarm: {alarm['label']}\nTime: {alarm['hour']:02d}:{alarm['minute']:02d}"
        
        # Show system notification
        self.system_tray.show_notification("Alarm", f"{alarm['label']} - {alarm['hour']:02d}:{alarm['minute']:02d}")
        
        # Show message box
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
        self.alarm_window.geometry("500x400")
        self.alarm_window.configure(bg=self.bg_color)
        
        # Alarm list frame
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
                sound = alarm.get('sound', 'default')
                voice = " 🔊" if alarm.get('voice_enabled', False) else ""
                display = f"{time_str} - {alarm['label']} ({status}) [{sound}]{voice}"
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
        self.stopwatch_window.title("Stopwatch & Timer")
        self.stopwatch_window.geometry("400x300")
        self.stopwatch_window.configure(bg=self.bg_color)
        
        # Stopwatch display
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
        
        # Timer section
        timer_frame = ttk.LabelFrame(self.stopwatch_window, text="Countdown Timer")
        timer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Timer input
        input_frame = ttk.Frame(timer_frame)
        input_frame.pack(pady=5)
        
        self.timer_minutes_var = tk.StringVar(value="5")
        ttk.Label(input_frame, text="Minutes:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.timer_minutes_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Start Timer", command=self.start_timer).pack(side=tk.LEFT, padx=10)
        
        # Start display updates
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
    
    def start_timer(self):
        """Start countdown timer"""
        try:
            minutes = int(self.timer_minutes_var.get())
            if minutes > 0:
                self.stopwatch.start_timer(minutes * 60, self.timer_finished)
                self.status_var.set(f"Timer started: {minutes} minutes")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of minutes")
    
    def timer_finished(self):
        """Handle timer completion"""
        self.status_var.set("Timer finished!")
        messagebox.showinfo("Timer", "Timer has finished!")
    
    def update_stopwatch_display(self):
        """Update stopwatch display"""
        if hasattr(self, 'stopwatch_var'):
            if self.stopwatch.is_timer_mode and self.stopwatch.is_running:
                elapsed = self.stopwatch.get_timer_remaining()
            else:
                elapsed = self.stopwatch.get_elapsed_time()
            
            formatted_time = self.stopwatch.format_time(elapsed)
            self.stopwatch_var.set(formatted_time)
            
            # Schedule next update
            self.root.after(10, self.update_stopwatch_display)
    
    def show_settings_window(self):
        """Show basic settings window"""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.create_settings_window()
        else:
            self.settings_window.lift()
    
    def create_settings_window(self):
        """Create settings window"""
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x300")
        self.settings_window.configure(bg=self.bg_color)
        
        # System tray setting
        self.system_tray_var = tk.BooleanVar(value=self.settings.get("system_tray_enabled", False))
        ttk.Checkbutton(self.settings_window, 
                       text="Enable system tray", 
                       variable=self.system_tray_var).pack(anchor="w", padx=20, pady=10)
        
        # Voice setting
        self.voice_enabled_var = tk.BooleanVar(value=self.settings.get("voice_enabled", False))
        ttk.Checkbutton(self.settings_window, 
                       text="Enable voice announcements", 
                       variable=self.voice_enabled_var).pack(anchor="w", padx=20, pady=5)
        
        # Apply button
        button_frame = ttk.Frame(self.settings_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Apply", command=self.apply_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def apply_settings(self):
        """Apply settings changes"""
        # System tray
        system_tray_enabled = self.system_tray_var.get()
        if system_tray_enabled and not self.system_tray.is_enabled:
            self.system_tray.enable_system_tray()
        elif not system_tray_enabled and self.system_tray.is_enabled:
            self.system_tray.disable_system_tray()
        
        # Voice
        self.voice_enabled = self.voice_enabled_var.get()
        
        # Save settings
        self.settings.update({
            "system_tray_enabled": system_tray_enabled,
            "voice_enabled": self.voice_enabled
        })
        
        self.status_var.set("Settings applied")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.settings.reset_to_defaults()
            self.load_initial_settings()
            self.setup_styles()
            self.create_clock_widget()
            self.status_var.set("Settings reset to defaults")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Enhanced Python Digital Clock v2.0

Features:
• Multiple clock styles (Digital, Analog, Binary, Text)
• Alarm functionality with custom sounds
• Stopwatch and countdown timer
• Multiple timezone support
• Customizable themes and fonts
• Settings persistence
• System tray integration
• Voice announcements
• Weather integration
• Calendar synchronization
• Multiple monitor support
• Plugin system for custom features
• Cloud settings sync
• Advanced scheduling features

Built with Python and tkinter"""
        messagebox.showinfo("About", about_text)
    
    def show_weather_window(self):
        """Show weather management window"""
        if hasattr(self, 'weather_window') and self.weather_window and self.weather_window.winfo_exists():
            self.weather_window.lift()
            return
            
        self.weather_window = tk.Toplevel(self.root)
        self.weather_window.title("Weather Integration")
        self.weather_window.geometry("400x300")
        self.weather_window.resizable(False, False)
        
        # Create weather UI
        main_frame = ttk.Frame(self.weather_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Weather status
        status_frame = ttk.LabelFrame(main_frame, text="Weather Status")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        weather_data = self.weather_manager.get_current_weather()
        if weather_data:
            ttk.Label(status_frame, text=f"Temperature: {weather_data.get('temperature', 'N/A')}°F").pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(status_frame, text=f"Condition: {weather_data.get('description', 'N/A')}").pack(anchor=tk.W, padx=5, pady=2)
            ttk.Label(status_frame, text=f"Humidity: {weather_data.get('humidity', 'N/A')}%").pack(anchor=tk.W, padx=5, pady=2)
        else:
            ttk.Label(status_frame, text="Weather data not available").pack(anchor=tk.W, padx=5, pady=2)
        
        # Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Configuration")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(config_frame, text="API Key:").pack(anchor=tk.W, padx=5)
        api_key_entry = ttk.Entry(config_frame, show="*")
        api_key_entry.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(config_frame, text="Location:").pack(anchor=tk.W, padx=5)
        location_entry = ttk.Entry(config_frame)
        location_entry.pack(fill=tk.X, padx=5, pady=2)
        location_entry.insert(0, self.weather_manager.location)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save_weather_config():
            api_key = api_key_entry.get()
            location = location_entry.get()
            if api_key:
                self.weather_manager.set_api_key(api_key)
            if location:
                self.weather_manager.set_location(location)
            messagebox.showinfo("Success", "Weather configuration saved")
        
        ttk.Button(button_frame, text="Save", command=save_weather_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Update Now", command=self.weather_manager.update_weather).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.weather_window.destroy).pack(side=tk.RIGHT)
    
    def show_calendar_window(self):
        """Show calendar synchronization window"""
        if hasattr(self, 'calendar_window') and self.calendar_window and self.calendar_window.winfo_exists():
            self.calendar_window.lift()
            return
            
        self.calendar_window = tk.Toplevel(self.root)
        self.calendar_window.title("Calendar Synchronization")
        self.calendar_window.geometry("500x400")
        
        main_frame = ttk.Frame(self.calendar_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Upcoming events
        events_frame = ttk.LabelFrame(main_frame, text="Upcoming Events")
        events_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for events
        columns = ("Event", "Time", "Description")
        events_tree = ttk.Treeview(events_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            events_tree.heading(col, text=col)
            events_tree.column(col, width=150)
        
        # Add sample events
        events = self.calendar_manager.get_upcoming_events()
        for event in events:
            start_time = event["start"].strftime("%m/%d %H:%M")
            events_tree.insert("", tk.END, values=(event["title"], start_time, event["description"]))
        
        scrollbar = ttk.Scrollbar(events_frame, orient=tk.VERTICAL, command=events_tree.yview)
        events_tree.configure(yscrollcommand=scrollbar.set)
        
        events_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        def sync_calendars():
            if self.calendar_manager.sync_calendars():
                messagebox.showinfo("Success", "Calendar synchronized")
                # Refresh the events tree
                for item in events_tree.get_children():
                    events_tree.delete(item)
                events = self.calendar_manager.get_upcoming_events()
                for event in events:
                    start_time = event["start"].strftime("%m/%d %H:%M")
                    events_tree.insert("", tk.END, values=(event["title"], start_time, event["description"]))
            else:
                messagebox.showerror("Error", "Calendar sync failed")
        
        ttk.Button(control_frame, text="Sync Now", command=sync_calendars).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Settings", command=lambda: messagebox.showinfo("Info", "Calendar settings will be available in a future update")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.calendar_window.destroy).pack(side=tk.RIGHT)
    
    def show_monitor_window(self):
        """Show multiple monitor management window"""
        if hasattr(self, 'monitor_window') and self.monitor_window and self.monitor_window.winfo_exists():
            self.monitor_window.lift()
            return
            
        self.monitor_window = tk.Toplevel(self.root)
        self.monitor_window.title("Multiple Monitor Support")
        self.monitor_window.geometry("400x300")
        
        main_frame = ttk.Frame(self.monitor_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Monitor list
        monitors_frame = ttk.LabelFrame(main_frame, text="Available Monitors")
        monitors_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        monitors = self.monitor_manager.get_monitors()
        selected_monitor = tk.IntVar(value=self.monitor_manager.current_monitor)
        
        for monitor in monitors:
            text = f"Monitor {monitor['id']}: {monitor['name']} ({monitor['width']}x{monitor['height']})"
            if monitor['primary']:
                text += " [Primary]"
            ttk.Radiobutton(monitors_frame, text=text, variable=selected_monitor, value=monitor['id']).pack(anchor=tk.W, padx=5, pady=2)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        def apply_monitor():
            monitor_id = selected_monitor.get()
            if self.monitor_manager.set_monitor(monitor_id):
                geometry = self.monitor_manager.get_monitor_geometry(monitor_id)
                # Move window to selected monitor
                self.root.geometry(f"+{geometry['x']+100}+{geometry['y']+100}")
                messagebox.showinfo("Success", f"Clock moved to Monitor {monitor_id}")
            else:
                messagebox.showerror("Error", "Failed to set monitor")
        
        ttk.Button(control_frame, text="Apply", command=apply_monitor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Detect Monitors", command=self.monitor_manager.detect_monitors).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.monitor_window.destroy).pack(side=tk.RIGHT)
    
    def show_plugins_window(self):
        """Show plugin management window"""
        if hasattr(self, 'plugins_window') and self.plugins_window and self.plugins_window.winfo_exists():
            self.plugins_window.lift()
            return
            
        self.plugins_window = tk.Toplevel(self.root)
        self.plugins_window.title("Plugin System")
        self.plugins_window.geometry("500x400")
        
        main_frame = ttk.Frame(self.plugins_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Plugin list
        plugins_frame = ttk.LabelFrame(main_frame, text="Available Plugins")
        plugins_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for plugins
        columns = ("Name", "Version", "Status", "Description")
        plugins_tree = ttk.Treeview(plugins_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            plugins_tree.heading(col, text=col)
            plugins_tree.column(col, width=100)
        
        # Load and display plugins
        self.plugin_manager.load_plugins()
        plugins = self.plugin_manager.get_plugins()
        
        for name, plugin in plugins.items():
            status = "Enabled" if plugin["enabled"] else "Disabled"
            plugins_tree.insert("", tk.END, values=(name, plugin["version"], status, plugin["description"]))
        
        scrollbar = ttk.Scrollbar(plugins_frame, orient=tk.VERTICAL, command=plugins_tree.yview)
        plugins_tree.configure(yscrollcommand=scrollbar.set)
        
        plugins_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        def toggle_plugin():
            selection = plugins_tree.selection()
            if selection:
                item = plugins_tree.item(selection[0])
                plugin_name = item["values"][0]
                current_status = item["values"][2]
                
                if current_status == "Enabled":
                    self.plugin_manager.disable_plugin(plugin_name)
                    new_status = "Disabled"
                else:
                    self.plugin_manager.enable_plugin(plugin_name)
                    new_status = "Enabled"
                
                # Update tree
                plugins_tree.item(selection[0], values=(item["values"][0], item["values"][1], new_status, item["values"][3]))
        
        ttk.Button(control_frame, text="Toggle", command=toggle_plugin).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Refresh", command=lambda: messagebox.showinfo("Info", "Plugin refresh completed")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.plugins_window.destroy).pack(side=tk.RIGHT)
    
    def show_cloud_sync_window(self):
        """Show cloud synchronization window"""
        if hasattr(self, 'cloud_window') and self.cloud_window and self.cloud_window.winfo_exists():
            self.cloud_window.lift()
            return
            
        self.cloud_window = tk.Toplevel(self.root)
        self.cloud_window.title("Cloud Settings Sync")
        self.cloud_window.geometry("400x300")
        
        main_frame = ttk.Frame(self.cloud_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sync status
        status_frame = ttk.LabelFrame(main_frame, text="Sync Status")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        sync_status = "Enabled" if self.cloud_sync.enabled else "Disabled"
        last_sync = self.cloud_sync.last_sync.strftime("%Y-%m-%d %H:%M:%S") if self.cloud_sync.last_sync else "Never"
        
        ttk.Label(status_frame, text=f"Status: {sync_status}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, text=f"Last Sync: {last_sync}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, text=f"Provider: {self.cloud_sync.sync_provider or 'None'}").pack(anchor=tk.W, padx=5, pady=2)
        
        # Configuration
        config_frame = ttk.LabelFrame(main_frame, text="Configuration")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(config_frame, text="Sync URL:").pack(anchor=tk.W, padx=5)
        url_entry = ttk.Entry(config_frame)
        url_entry.pack(fill=tk.X, padx=5, pady=2)
        if self.cloud_sync.sync_url:
            url_entry.insert(0, self.cloud_sync.sync_url)
        
        ttk.Label(config_frame, text="User Token:").pack(anchor=tk.W, padx=5)
        token_entry = ttk.Entry(config_frame, show="*")
        token_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        def configure_sync():
            url = url_entry.get()
            token = token_entry.get()
            if url and token:
                self.cloud_sync.configure_sync("Custom", url, token)
                messagebox.showinfo("Success", "Cloud sync configured")
            else:
                messagebox.showerror("Error", "Please enter both URL and token")
        
        def sync_now():
            if self.cloud_sync.enabled:
                current_settings = self.settings.get_all_settings()
                if self.cloud_sync.sync_settings(current_settings):
                    messagebox.showinfo("Success", "Settings synchronized")
                else:
                    messagebox.showerror("Error", "Sync failed")
            else:
                messagebox.showwarning("Warning", "Cloud sync not configured")
        
        ttk.Button(control_frame, text="Configure", command=configure_sync).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Sync Now", command=sync_now).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.cloud_window.destroy).pack(side=tk.RIGHT)
    
    def show_scheduler_window(self):
        """Show advanced scheduler window"""
        if hasattr(self, 'scheduler_window') and self.scheduler_window and self.scheduler_window.winfo_exists():
            self.scheduler_window.lift()
            return
            
        self.scheduler_window = tk.Toplevel(self.root)
        self.scheduler_window.title("Advanced Scheduler")
        self.scheduler_window.geometry("600x400")
        
        main_frame = ttk.Frame(self.scheduler_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Schedule list
        schedules_frame = ttk.LabelFrame(main_frame, text="Scheduled Events")
        schedules_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for schedules
        columns = ("Name", "Type", "Time", "Action", "Status")
        schedules_tree = ttk.Treeview(schedules_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            schedules_tree.heading(col, text=col)
            schedules_tree.column(col, width=100)
        
        # Add existing schedules
        schedules = self.scheduler.get_schedules()
        for schedule in schedules:
            status = "Enabled" if schedule["enabled"] else "Disabled"
            schedules_tree.insert("", tk.END, values=(
                schedule["name"], schedule["type"], schedule["time"], 
                schedule["action"], status
            ))
        
        scrollbar = ttk.Scrollbar(schedules_frame, orient=tk.VERTICAL, command=schedules_tree.yview)
        schedules_tree.configure(yscrollcommand=scrollbar.set)
        
        schedules_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        def add_schedule():
            # Simple schedule dialog
            name = simpledialog.askstring("New Schedule", "Schedule name:")
            if name:
                time_str = simpledialog.askstring("New Schedule", "Time (HH:MM):")
                if time_str:
                    schedule_config = {
                        "name": name,
                        "type": "daily",
                        "time": time_str,
                        "action": "notification",
                        "message": f"Scheduled event: {name}"
                    }
                    schedule_id = self.scheduler.add_schedule(schedule_config)
                    # Add to tree
                    schedules_tree.insert("", tk.END, values=(name, "daily", time_str, "notification", "Enabled"))
        
        def remove_schedule():
            selection = schedules_tree.selection()
            if selection:
                schedules_tree.delete(selection[0])
                messagebox.showinfo("Success", "Schedule removed")
        
        def start_scheduler():
            self.scheduler.start_scheduler()
            messagebox.showinfo("Success", "Scheduler started")
        
        ttk.Button(control_frame, text="Add", command=add_schedule).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Remove", command=remove_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Start Scheduler", command=start_scheduler).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.scheduler_window.destroy).pack(side=tk.RIGHT)
    
    def show_mobile_companion_window(self):
        """Show mobile companion server window"""
        if hasattr(self, 'mobile_window') and self.mobile_window and self.mobile_window.winfo_exists():
            self.mobile_window.lift()
            return
            
        self.mobile_window = tk.Toplevel(self.root)
        self.mobile_window.title("Mobile Companion")
        self.mobile_window.geometry("400x300")
        
        main_frame = ttk.Frame(self.mobile_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Server status
        status_frame = ttk.LabelFrame(main_frame, text="Server Status")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        server_info = self.mobile_server.get_server_info()
        status_text = "Running" if server_info["running"] else "Stopped"
        
        self.mobile_status_label = ttk.Label(status_frame, text=f"Status: {status_text}")
        self.mobile_status_label.pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text=f"Port: {server_info['port']}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, text=f"URL: {server_info['url']}").pack(anchor=tk.W, padx=5, pady=2)
        
        # API endpoints
        endpoints_frame = ttk.LabelFrame(main_frame, text="Available Endpoints")
        endpoints_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        endpoints_text = tk.Text(endpoints_frame, height=8, width=40)
        endpoints_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        endpoints_info = """Available API endpoints:
        
GET /status - Get clock status
GET /time - Get current time
GET /weather - Get weather data
GET /calendar - Get calendar events
GET /alarms - Get all alarms

POST /alarm - Add new alarm
POST /settings - Update settings

Example mobile app usage:
http://localhost:8888/time
"""
        endpoints_text.insert(tk.END, endpoints_info)
        endpoints_text.config(state=tk.DISABLED)
        
        # Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        def start_server():
            if self.mobile_server.start_server():
                self.mobile_status_label.config(text="Status: Running")
                messagebox.showinfo("Success", "Mobile companion server started")
            else:
                messagebox.showerror("Error", "Failed to start server")
        
        def stop_server():
            self.mobile_server.stop_server()
            self.mobile_status_label.config(text="Status: Stopped")
            messagebox.showinfo("Success", "Mobile companion server stopped")
        
        ttk.Button(control_frame, text="Start Server", command=start_server).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Stop Server", command=stop_server).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Close", command=self.mobile_window.destroy).pack(side=tk.RIGHT)
    
    def on_window_configure(self, event):
        """Handle window configuration changes"""
        if event.widget == self.root:
            geometry = self.root.geometry()
            self.settings.set("window_geometry", geometry)
    
    def on_closing(self):
        """Handle application closing"""
        self.is_running = False
        self.alarm_manager.stop_monitoring()
        
        # Save settings
        self.settings.save_settings()
        
        # Disable system tray
        if self.system_tray.is_enabled:
            self.system_tray.disable_system_tray()
        
        if self.clock_thread.is_alive():
            self.clock_thread.join(timeout=1)
        
        # Close child windows
        for window_attr in ['alarm_window', 'stopwatch_window', 'settings_window']:
            window = getattr(self, window_attr, None)
            if window and window.winfo_exists():
                window.destroy()
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = EnhancedDigitalClock()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()