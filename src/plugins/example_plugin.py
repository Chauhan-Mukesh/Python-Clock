"""
Example plugin for the Enhanced Python Digital Clock
Demonstrates the plugin system functionality
"""

import datetime


class ExamplePlugin:
    """Example plugin implementation"""
    
    def __init__(self):
        self.name = "Example Plugin"
        self.version = "1.0.0"
        self.description = "A simple example plugin that shows current date info"
        self.enabled = False
    
    def initialize(self):
        """Called when plugin is enabled"""
        print(f"{self.name} initialized")
        self.enabled = True
    
    def cleanup(self):
        """Called when plugin is disabled"""
        print(f"{self.name} cleaned up")
        self.enabled = False
    
    def get_menu_items(self):
        """Return list of menu items to add"""
        return [
            ("Show Date Info", self.show_date_info),
            ("Show Week Number", self.show_week_number)
        ]
    
    def execute_action(self, action):
        """Execute plugin action"""
        if action == "date_info":
            return self.show_date_info()
        elif action == "week_number":
            return self.show_week_number()
        return None
    
    def show_date_info(self):
        """Show detailed date information"""
        now = datetime.datetime.now()
        info = {
            "date": now.strftime("%Y-%m-%d"),
            "day_of_year": now.timetuple().tm_yday,
            "week_day": now.strftime("%A"),
            "month": now.strftime("%B"),
            "quarter": f"Q{(now.month-1)//3 + 1}"
        }
        return info
    
    def show_week_number(self):
        """Show current week number"""
        now = datetime.datetime.now()
        week_number = now.isocalendar()[1]
        return {"week_number": week_number, "year": now.year}


# Plugin instance (required for plugin system)
plugin_instance = ExamplePlugin()