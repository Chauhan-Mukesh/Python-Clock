"""
Python example for mobile companion API
Demonstrates how to interact with the Enhanced Digital Clock API
"""

import requests
import json


class ClockAPI:
    """Python client for the Enhanced Digital Clock API"""
    
    def __init__(self, host="localhost", port=8888):
        self.base_url = f"http://{host}:{port}"
    
    def get_status(self):
        """Get clock application status"""
        try:
            response = requests.get(f"{self.base_url}/status")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error getting status: {e}")
            return None
    
    def get_current_time(self):
        """Get current time and date"""
        try:
            response = requests.get(f"{self.base_url}/time")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error getting time: {e}")
            return None
    
    def get_weather(self):
        """Get current weather data"""
        try:
            response = requests.get(f"{self.base_url}/weather")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error getting weather: {e}")
            return None
    
    def get_calendar_events(self):
        """Get upcoming calendar events"""
        try:
            response = requests.get(f"{self.base_url}/calendar")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error getting calendar: {e}")
            return None
    
    def get_alarms(self):
        """Get all configured alarms"""
        try:
            response = requests.get(f"{self.base_url}/alarms")
            return response.json() if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error getting alarms: {e}")
            return None
    
    def add_alarm(self, time_str, label="Mobile Alarm", sound="default", enabled=True):
        """Add a new alarm"""
        try:
            data = {
                "time": time_str,
                "label": label,
                "sound": sound,
                "enabled": enabled
            }
            response = requests.post(f"{self.base_url}/alarm", json=data)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error adding alarm: {e}")
            return False
    
    def update_settings(self, settings):
        """Update clock settings"""
        try:
            response = requests.post(f"{self.base_url}/settings", json=settings)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error updating settings: {e}")
            return False


def main():
    """Example usage of the Clock API"""
    # Create API client
    api = ClockAPI()
    
    print("Enhanced Digital Clock - Mobile API Demo")
    print("=" * 40)
    
    # Get status
    print("\n1. Getting clock status...")
    status = api.get_status()
    if status:
        print(f"Status: {status['status']}")
        print(f"Version: {status['version']}")
        print("Available features:")
        for feature, enabled in status['features'].items():
            print(f"  - {feature}: {'✓' if enabled else '✗'}")
    else:
        print("❌ Could not connect to clock server")
        print("Make sure the clock app is running and mobile companion is started")
        return
    
    # Get current time
    print("\n2. Getting current time...")
    time_info = api.get_current_time()
    if time_info:
        print(f"Time: {time_info['time']}")
        print(f"Date: {time_info['date']}")
        print(f"Timezone: {time_info['timezone']}")
    
    # Get weather
    print("\n3. Getting weather information...")
    weather = api.get_weather()
    if weather:
        if 'error' in weather:
            print(f"Weather not available: {weather['error']}")
        else:
            print(f"Temperature: {weather.get('temperature', 'N/A')}°F")
            print(f"Condition: {weather.get('description', 'N/A')}")
            print(f"Humidity: {weather.get('humidity', 'N/A')}%")
    
    # Get calendar events
    print("\n4. Getting calendar events...")
    calendar = api.get_calendar_events()
    if calendar:
        if 'error' in calendar:
            print(f"Calendar not available: {calendar['error']}")
        else:
            events = calendar.get('events', [])
            if events:
                print(f"Found {len(events)} upcoming events:")
                for event in events[:3]:  # Show first 3 events
                    print(f"  - {event['title']} at {event['start']}")
            else:
                print("No upcoming events")
    
    # Get alarms
    print("\n5. Getting configured alarms...")
    alarms = api.get_alarms()
    if alarms:
        if 'error' in alarms:
            print(f"Alarms not available: {alarms['error']}")
        else:
            alarm_list = alarms.get('alarms', [])
            if alarm_list:
                print(f"Found {len(alarm_list)} alarms:")
                for alarm in alarm_list:
                    status = "enabled" if alarm.get('enabled') else "disabled"
                    print(f"  - {alarm.get('time', 'N/A')}: {alarm.get('label', 'N/A')} ({status})")
            else:
                print("No alarms configured")
    
    # Add a test alarm
    print("\n6. Adding a test alarm...")
    if api.add_alarm("15:30", "API Test Alarm"):
        print("✓ Test alarm added successfully")
    else:
        print("❌ Failed to add test alarm")
    
    # Update settings example
    print("\n7. Updating settings...")
    settings_update = {
        "font_size": 48,
        "theme": "dark"
    }
    if api.update_settings(settings_update):
        print("✓ Settings updated successfully")
    else:
        print("❌ Failed to update settings")
    
    print("\n" + "=" * 40)
    print("Demo completed!")


if __name__ == "__main__":
    main()