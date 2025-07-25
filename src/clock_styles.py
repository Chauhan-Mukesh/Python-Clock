"""
Clock styles and themes for the Digital Clock Application
"""

import tkinter as tk
from tkinter import ttk, font
from typing import Dict, Any, Tuple
import math

class ClockStyleManager:
    """Manages different clock face styles and themes"""
    
    def __init__(self):
        self.styles = {
            'digital': DigitalStyle(),
            'analog': AnalogStyle(),
            'binary': BinaryStyle(),
            'text': TextStyle()
        }
        self.current_style = 'digital'
    
    def get_available_styles(self):
        """Get list of available clock styles"""
        return list(self.styles.keys())
    
    def get_style(self, style_name: str):
        """Get a specific style instance"""
        return self.styles.get(style_name, self.styles['digital'])
    
    def set_current_style(self, style_name: str):
        """Set the current active style"""
        if style_name in self.styles:
            self.current_style = style_name
    
    def get_current_style(self):
        """Get the current active style"""
        return self.styles[self.current_style]


class ClockStyle:
    """Base class for clock styles"""
    
    def __init__(self):
        self.name = "Base Style"
        self.supports_seconds = True
        self.supports_date = True
    
    def create_time_widget(self, parent, time_var, **kwargs):
        """Create the time display widget"""
        raise NotImplementedError
    
    def format_time(self, datetime_obj, is_24_hour=True, show_seconds=True):
        """Format time for this style"""
        raise NotImplementedError
    
    def get_style_config(self, theme='light'):
        """Get style configuration for theme"""
        raise NotImplementedError


class DigitalStyle(ClockStyle):
    """Traditional digital clock style"""
    
    def __init__(self):
        super().__init__()
        self.name = "Digital"
    
    def create_time_widget(self, parent, time_var, **kwargs):
        """Create digital time display widget"""
        style_config = kwargs.get('style_config', {})
        
        return ttk.Label(parent,
                        textvariable=time_var,
                        font=(style_config.get('font_family', 'Courier New'),
                              style_config.get('font_size', 42),
                              'bold'),
                        foreground=style_config.get('fg_color', '#333333'),
                        background=style_config.get('bg_color', '#ffffff'),
                        anchor="center")
    
    def format_time(self, datetime_obj, is_24_hour=True, show_seconds=True):
        """Format time in digital format"""
        if is_24_hour:
            if show_seconds:
                return datetime_obj.strftime("%H:%M:%S")
            else:
                return datetime_obj.strftime("%H:%M")
        else:
            if show_seconds:
                return datetime_obj.strftime("%I:%M:%S %p")
            else:
                return datetime_obj.strftime("%I:%M %p")
    
    def get_style_config(self, theme='light'):
        """Get digital style configuration"""
        if theme == 'dark':
            return {
                'bg_color': '#2b2b2b',
                'fg_color': '#00ff00',  # Green digital display
                'font_family': 'Courier New',
                'font_size': 42
            }
        else:
            return {
                'bg_color': '#ffffff',
                'fg_color': '#000080',  # Navy blue
                'font_family': 'Courier New', 
                'font_size': 42
            }


class AnalogStyle(ClockStyle):
    """Analog clock face style"""
    
    def __init__(self):
        super().__init__()
        self.name = "Analog"
        self.supports_seconds = True
    
    def create_time_widget(self, parent, time_var, **kwargs):
        """Create analog clock widget"""
        style_config = kwargs.get('style_config', {})
        
        # Create canvas for analog clock
        canvas = tk.Canvas(parent,
                          width=300,
                          height=300,
                          bg=style_config.get('bg_color', '#ffffff'),
                          highlightthickness=0)
        
        # Store canvas reference for updates
        canvas.clock_center = (150, 150)
        canvas.clock_radius = 140
        
        return canvas
    
    def draw_analog_clock(self, canvas, datetime_obj, style_config):
        """Draw analog clock on canvas"""
        canvas.delete("all")
        
        center_x, center_y = canvas.clock_center
        radius = canvas.clock_radius
        
        # Draw outer circle
        canvas.create_oval(center_x - radius, center_y - radius,
                          center_x + radius, center_y + radius,
                          outline=style_config.get('fg_color', '#000000'),
                          width=3)
        
        # Draw hour markers
        for hour in range(12):
            angle = math.radians(hour * 30 - 90)
            start_radius = radius - 20
            end_radius = radius - 10
            
            start_x = center_x + start_radius * math.cos(angle)
            start_y = center_y + start_radius * math.sin(angle)
            end_x = center_x + end_radius * math.cos(angle)
            end_y = center_y + end_radius * math.sin(angle)
            
            canvas.create_line(start_x, start_y, end_x, end_y,
                             fill=style_config.get('fg_color', '#000000'),
                             width=3)
            
            # Hour numbers
            num_x = center_x + (radius - 35) * math.cos(angle)
            num_y = center_y + (radius - 35) * math.sin(angle)
            hour_num = 12 if hour == 0 else hour
            canvas.create_text(num_x, num_y, text=str(hour_num),
                             fill=style_config.get('fg_color', '#000000'),
                             font=('Arial', 14, 'bold'))
        
        # Draw minute markers
        for minute in range(60):
            if minute % 5 != 0:  # Skip hour markers
                angle = math.radians(minute * 6 - 90)
                start_radius = radius - 15
                end_radius = radius - 10
                
                start_x = center_x + start_radius * math.cos(angle)
                start_y = center_y + start_radius * math.sin(angle)
                end_x = center_x + end_radius * math.cos(angle)
                end_y = center_y + end_radius * math.sin(angle)
                
                canvas.create_line(start_x, start_y, end_x, end_y,
                                 fill=style_config.get('fg_color', '#000000'),
                                 width=1)
        
        # Calculate hand angles
        hour = datetime_obj.hour % 12
        minute = datetime_obj.minute
        second = datetime_obj.second
        
        hour_angle = math.radians((hour + minute/60) * 30 - 90)
        minute_angle = math.radians(minute * 6 - 90)
        second_angle = math.radians(second * 6 - 90)
        
        # Draw hour hand
        hour_length = radius * 0.5
        hour_x = center_x + hour_length * math.cos(hour_angle)
        hour_y = center_y + hour_length * math.sin(hour_angle)
        canvas.create_line(center_x, center_y, hour_x, hour_y,
                          fill=style_config.get('hour_color', '#000080'),
                          width=6, capstyle='round')
        
        # Draw minute hand
        minute_length = radius * 0.7
        minute_x = center_x + minute_length * math.cos(minute_angle)
        minute_y = center_y + minute_length * math.sin(minute_angle)
        canvas.create_line(center_x, center_y, minute_x, minute_y,
                          fill=style_config.get('minute_color', '#0000ff'),
                          width=4, capstyle='round')
        
        # Draw second hand
        second_length = radius * 0.8
        second_x = center_x + second_length * math.cos(second_angle)
        second_y = center_y + second_length * math.sin(second_angle)
        canvas.create_line(center_x, center_y, second_x, second_y,
                          fill=style_config.get('second_color', '#ff0000'),
                          width=2, capstyle='round')
        
        # Draw center dot
        canvas.create_oval(center_x - 8, center_y - 8,
                          center_x + 8, center_y + 8,
                          fill=style_config.get('center_color', '#000000'),
                          outline=style_config.get('center_color', '#000000'))
    
    def format_time(self, datetime_obj, is_24_hour=True, show_seconds=True):
        """For analog clock, return empty string as time is shown visually"""
        return ""
    
    def get_style_config(self, theme='light'):
        """Get analog style configuration"""
        if theme == 'dark':
            return {
                'bg_color': '#2b2b2b',
                'fg_color': '#ffffff',
                'hour_color': '#ffff00',
                'minute_color': '#00ff00',
                'second_color': '#ff0000',
                'center_color': '#ffffff'
            }
        else:
            return {
                'bg_color': '#ffffff',
                'fg_color': '#000000',
                'hour_color': '#000080',
                'minute_color': '#0000ff',
                'second_color': '#ff0000',
                'center_color': '#000000'
            }


class BinaryStyle(ClockStyle):
    """Binary clock style showing time in binary format"""
    
    def __init__(self):
        super().__init__()
        self.name = "Binary"
        self.supports_seconds = True
    
    def create_time_widget(self, parent, time_var, **kwargs):
        """Create binary clock widget"""
        style_config = kwargs.get('style_config', {})
        
        # Create frame for binary display
        binary_frame = ttk.Frame(parent)
        
        # Create binary display labels
        binary_frame.hour_labels = []
        binary_frame.minute_labels = []
        binary_frame.second_labels = []
        
        return binary_frame
    
    def setup_binary_display(self, frame, style_config):
        """Setup binary clock display"""
        frame.hour_labels.clear()
        frame.minute_labels.clear()
        frame.second_labels.clear()
        
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create headers
        ttk.Label(frame, text="H", font=('Arial', 12, 'bold')).grid(row=0, column=1, columnspan=2, pady=5)
        ttk.Label(frame, text="M", font=('Arial', 12, 'bold')).grid(row=0, column=3, columnspan=2, pady=5)
        ttk.Label(frame, text="S", font=('Arial', 12, 'bold')).grid(row=0, column=5, columnspan=2, pady=5)
        
        # Create binary display grid
        for row in range(6):
            # Hours (2 columns)
            for col in range(2):
                label = tk.Label(frame, text="0", width=3, height=2,
                               bg=style_config.get('off_color', '#cccccc'),
                               fg=style_config.get('fg_color', '#000000'),
                               font=('Courier', 10, 'bold'),
                               relief='raised', bd=1)
                label.grid(row=row+1, column=col, padx=1, pady=1)
                frame.hour_labels.append(label)
            
            # Minutes (2 columns) 
            for col in range(2):
                label = tk.Label(frame, text="0", width=3, height=2,
                               bg=style_config.get('off_color', '#cccccc'),
                               fg=style_config.get('fg_color', '#000000'),
                               font=('Courier', 10, 'bold'),
                               relief='raised', bd=1)
                label.grid(row=row+1, column=col+2, padx=1, pady=1)
                frame.minute_labels.append(label)
            
            # Seconds (2 columns)
            for col in range(2):
                label = tk.Label(frame, text="0", width=3, height=2,
                               bg=style_config.get('off_color', '#cccccc'),
                               fg=style_config.get('fg_color', '#000000'),
                               font=('Courier', 10, 'bold'),
                               relief='raised', bd=1)
                label.grid(row=row+1, column=col+4, padx=1, pady=1)
                frame.second_labels.append(label)
    
    def update_binary_display(self, frame, datetime_obj, style_config):
        """Update binary clock display"""
        hour = datetime_obj.hour
        minute = datetime_obj.minute
        second = datetime_obj.second
        
        # Convert to binary and update displays
        self._update_binary_column(frame.hour_labels, hour, style_config)
        self._update_binary_column(frame.minute_labels, minute, style_config)
        self._update_binary_column(frame.second_labels, second, style_config)
    
    def _update_binary_column(self, labels, value, style_config):
        """Update a binary column (2 digits, 6 bits each)"""
        tens = value // 10
        ones = value % 10
        
        # First column (tens)
        tens_binary = format(tens, '06b')
        for i, bit in enumerate(tens_binary):
            if bit == '1':
                labels[i].config(bg=style_config.get('on_color', '#00ff00'), text="1")
            else:
                labels[i].config(bg=style_config.get('off_color', '#cccccc'), text="0")
        
        # Second column (ones)
        ones_binary = format(ones, '06b')
        for i, bit in enumerate(ones_binary):
            if bit == '1':
                labels[i+6].config(bg=style_config.get('on_color', '#00ff00'), text="1")
            else:
                labels[i+6].config(bg=style_config.get('off_color', '#cccccc'), text="0")
    
    def format_time(self, datetime_obj, is_24_hour=True, show_seconds=True):
        """For binary clock, return binary representation"""
        hour = datetime_obj.hour
        minute = datetime_obj.minute
        second = datetime_obj.second
        
        if show_seconds:
            return f"{hour:02d}:{minute:02d}:{second:02d} (Binary)"
        else:
            return f"{hour:02d}:{minute:02d} (Binary)"
    
    def get_style_config(self, theme='light'):
        """Get binary style configuration"""
        if theme == 'dark':
            return {
                'bg_color': '#2b2b2b',
                'fg_color': '#ffffff',
                'on_color': '#00ff00',
                'off_color': '#404040'
            }
        else:
            return {
                'bg_color': '#ffffff',
                'fg_color': '#000000',
                'on_color': '#00aa00',
                'off_color': '#cccccc'
            }


class TextStyle(ClockStyle):
    """Written text time style"""
    
    def __init__(self):
        super().__init__()
        self.name = "Text"
        self.supports_seconds = False
    
    def create_time_widget(self, parent, time_var, **kwargs):
        """Create text time display widget"""
        style_config = kwargs.get('style_config', {})
        
        return ttk.Label(parent,
                        textvariable=time_var,
                        font=(style_config.get('font_family', 'Arial'),
                              style_config.get('font_size', 18),
                              'normal'),
                        foreground=style_config.get('fg_color', '#333333'),
                        background=style_config.get('bg_color', '#ffffff'),
                        anchor="center",
                        wraplength=400)
    
    def format_time(self, datetime_obj, is_24_hour=True, show_seconds=True):
        """Format time as written text"""
        hour = datetime_obj.hour
        minute = datetime_obj.minute
        
        # Convert to 12-hour if needed
        if not is_24_hour:
            period = "AM" if hour < 12 else "PM"
            if hour == 0:
                hour = 12
            elif hour > 12:
                hour -= 12
        
        # Number to word conversion
        numbers = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                  "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                  "seventeen", "eighteen", "nineteen", "twenty"]
        
        def number_to_words(n):
            if n <= 20:
                return numbers[n]
            elif n < 30:
                return "twenty" + ("" if n == 20 else "-" + numbers[n-20])
            elif n < 40:
                return "thirty" + ("" if n == 30 else "-" + numbers[n-30])
            elif n < 50:
                return "forty" + ("" if n == 40 else "-" + numbers[n-40])
            elif n < 60:
                return "fifty" + ("" if n == 50 else "-" + numbers[n-50])
            return str(n)
        
        # Format hour
        hour_text = number_to_words(hour)
        
        # Format minute
        if minute == 0:
            minute_text = "o'clock"
        elif minute == 15:
            minute_text = "quarter past"
        elif minute == 30:
            minute_text = "half past"
        elif minute == 45:
            minute_text = "quarter to"
            # Adjust hour for "quarter to"
            next_hour = hour + 1
            if not is_24_hour and next_hour > 12:
                next_hour = 1
            elif is_24_hour and next_hour > 23:
                next_hour = 0
            hour_text = number_to_words(next_hour)
        else:
            minute_text = number_to_words(minute) + (" past" if minute < 30 else " to")
            if minute > 30:
                # Adjust hour for "minutes to"
                next_hour = hour + 1
                if not is_24_hour and next_hour > 12:
                    next_hour = 1
                elif is_24_hour and next_hour > 23:
                    next_hour = 0
                hour_text = number_to_words(next_hour)
                minute = 60 - minute
                minute_text = number_to_words(minute) + " to"
        
        # Construct time text
        if minute == 0:
            time_text = f"It's {hour_text} {minute_text}"
        elif minute in [15, 30, 45]:
            if minute == 45:
                time_text = f"It's {minute_text} {hour_text}"
            else:
                time_text = f"It's {minute_text} {hour_text}"
        else:
            if minute < 30:
                time_text = f"It's {minute_text} {hour_text}"
            else:
                time_text = f"It's {minute_text} {hour_text}"
        
        if not is_24_hour:
            time_text += f" {period}"
        
        return time_text.title()
    
    def get_style_config(self, theme='light'):
        """Get text style configuration"""
        if theme == 'dark':
            return {
                'bg_color': '#2b2b2b',
                'fg_color': '#ffffff',
                'font_family': 'Georgia',
                'font_size': 18
            }
        else:
            return {
                'bg_color': '#ffffff',
                'fg_color': '#333333',
                'font_family': 'Georgia',
                'font_size': 18
            }