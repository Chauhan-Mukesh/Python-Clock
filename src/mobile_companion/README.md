# Mobile Companion App Examples

This directory contains examples for building mobile companion apps that interact with the Enhanced Python Digital Clock.

## API Endpoints

The clock provides a RESTful HTTP API when the mobile companion server is running (default port 8888).

### GET Endpoints

- `GET /status` - Get clock application status
- `GET /time` - Get current time and date
- `GET /weather` - Get current weather data
- `GET /calendar` - Get upcoming calendar events
- `GET /alarms` - Get all configured alarms

### POST Endpoints

- `POST /alarm` - Add a new alarm
- `POST /settings` - Update clock settings

## Getting Started

1. Start the Enhanced Python Digital Clock application
2. Go to Tools → Mobile Companion
3. Click "Start Server" (default port 8888)
4. Use the API endpoints from your mobile app
5. Replace `localhost` with your computer's IP address when accessing from mobile devices

## Security Note

The API currently runs without authentication for simplicity. In production environments, consider adding:
- API key authentication
- HTTPS encryption
- Rate limiting
- Input validation