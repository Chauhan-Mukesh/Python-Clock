"""
Mobile Companion App Support
Provides HTTP API for mobile app integration
"""

import threading
import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Dict, Any


class ClockAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mobile companion API"""
    
    def __init__(self, clock_instance, *args, **kwargs):
        self.clock = clock_instance
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/status':
                self.send_status()
            elif self.path == '/time':
                self.send_time()
            elif self.path == '/weather':
                self.send_weather()
            elif self.path == '/calendar':
                self.send_calendar()
            elif self.path == '/alarms':
                self.send_alarms()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Error: {e}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/alarm':
                self.add_alarm(data)
            elif self.path == '/settings':
                self.update_settings(data)
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Error: {e}")
    
    def send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_status(self):
        """Send clock status"""
        status = {
            "status": "running",
            "version": "2.0",
            "features": {
                "weather": hasattr(self.clock, 'weather_manager') and self.clock.weather_manager.enabled,
                "calendar": hasattr(self.clock, 'calendar_manager') and self.clock.calendar_manager.enabled,
                "alarms": True,
                "voice": hasattr(self.clock, 'voice_manager') and self.clock.voice_manager.enabled
            }
        }
        self.send_json_response(status)
    
    def send_time(self):
        """Send current time"""
        now = datetime.datetime.now()
        time_data = {
            "time": now.strftime("%H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "timezone": str(now.astimezone().tzinfo),
            "format_24h": True  # Could get from settings
        }
        self.send_json_response(time_data)
    
    def send_weather(self):
        """Send weather data"""
        if hasattr(self.clock, 'weather_manager'):
            weather = self.clock.weather_manager.get_current_weather()
            self.send_json_response(weather)
        else:
            self.send_json_response({"error": "Weather not available"}, 404)
    
    def send_calendar(self):
        """Send calendar events"""
        if hasattr(self.clock, 'calendar_manager'):
            events = self.clock.calendar_manager.get_upcoming_events()
            # Convert datetime objects to strings for JSON
            json_events = []
            for event in events:
                json_event = event.copy()
                json_event['start'] = event['start'].isoformat()
                json_event['end'] = event['end'].isoformat()
                json_events.append(json_event)
            self.send_json_response({"events": json_events})
        else:
            self.send_json_response({"error": "Calendar not available"}, 404)
    
    def send_alarms(self):
        """Send alarm list"""
        if hasattr(self.clock, 'alarm_manager'):
            alarms = self.clock.alarm_manager.get_alarms()
            self.send_json_response({"alarms": alarms})
        else:
            self.send_json_response({"error": "Alarms not available"}, 404)
    
    def add_alarm(self, data: Dict[str, Any]):
        """Add new alarm"""
        if hasattr(self.clock, 'alarm_manager'):
            try:
                alarm_id = self.clock.alarm_manager.add_alarm(
                    data.get('time', '09:00'),
                    data.get('label', 'Mobile Alarm'),
                    data.get('sound', 'default'),
                    data.get('enabled', True)
                )
                self.send_json_response({"success": True, "alarm_id": alarm_id})
            except Exception as e:
                self.send_json_response({"error": str(e)}, 400)
        else:
            self.send_json_response({"error": "Alarms not available"}, 404)
    
    def update_settings(self, data: Dict[str, Any]):
        """Update clock settings"""
        if hasattr(self.clock, 'settings'):
            try:
                self.clock.settings.update(data)
                self.send_json_response({"success": True})
            except Exception as e:
                self.send_json_response({"error": str(e)}, 400)
        else:
            self.send_json_response({"error": "Settings not available"}, 404)


class MobileCompanionServer:
    """Mobile companion server for clock app"""
    
    def __init__(self, clock_instance, port: int = 8888):
        self.clock = clock_instance
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
    
    def start_server(self) -> bool:
        """Start the mobile companion server"""
        try:
            # Create handler with clock instance
            def handler(*args, **kwargs):
                ClockAPIHandler(self.clock, *args, **kwargs)
            
            self.server = HTTPServer(('localhost', self.port), handler)
            self.running = True
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()
            
            print(f"Mobile companion server started on port {self.port}")
            return True
        except Exception as e:
            print(f"Failed to start mobile server: {e}")
            return False
    
    def stop_server(self):
        """Stop the mobile companion server"""
        if self.running and self.server:
            self.running = False
            self.server.shutdown()
            self.server.server_close()
            if self.server_thread:
                self.server_thread.join(timeout=2)
            print("Mobile companion server stopped")
    
    def _run_server(self):
        """Run the server"""
        try:
            self.server.serve_forever()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.running = False
    
    def is_running(self) -> bool:
        """Check if server is running"""
        return self.running
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "running": self.running,
            "port": self.port,
            "url": f"http://localhost:{self.port}",
            "endpoints": [
                "/status", "/time", "/weather", "/calendar", "/alarms"
            ]
        }