# Enhanced Python Digital Clock

A modern, feature-rich digital clock application built with Python and tkinter, featuring multiple clock styles, alarms with custom sounds, timezone support, and much more.

## ✨ Features

### 🕒 Multiple Clock Faces/Styles
- **Digital Clock**: Classic digital display with customizable fonts
- **Analog Clock**: Traditional clock face with moving hands
- **Binary Clock**: Geek-friendly binary time representation
- **Text Clock**: Written time in natural language ("Quarter past three")

### ⏰ Alarm Functionality with Custom Sounds
- Add/remove/toggle multiple alarms
- Custom sound selection (default, beep, chime, bell)
- Voice announcements for alarms
- Visual and system notifications
- Persistent alarm settings

### ⏱️ Stopwatch and Countdown Timer
- High-precision stopwatch with lap times
- Countdown timer with custom durations
- Visual and audio completion notifications
- Separate interfaces for stopwatch and timer

### 🌍 Multiple Timezone Support
- Support for major world timezones
- Real-time timezone switching
- Local and UTC time display
- Timezone-aware date formatting

### 🎨 Customizable Themes and Fonts
- Light and dark theme support
- Multiple font families and sizes
- Style-specific theme configurations
- Consistent theming across all clock styles

### 💾 Settings Persistence
- Automatic settings saving
- JSON-based configuration storage
- Import/export settings capability
- Reset to defaults functionality

### 🖥️ System Tray Integration
- Minimize to system tray
- Quick access menu
- Tray icon with current time tooltip
- System notifications

### 🔊 Voice Announcements
- Hourly time announcements
- Alarm voice notifications
- Configurable voice rate and volume
- Manual time speaking

### 🔧 Additional Features
- Multiple time formats (12/24 hour)
- Show/hide seconds and date
- Responsive and resizable interface
- Comprehensive keyboard shortcuts
- Cross-platform compatibility

### 🌤️ Weather Integration
- Real-time weather display
- Configurable location and API integration
- Temperature, humidity, and weather conditions
- 3-day weather forecast
- Automatic weather updates

### 📅 Calendar Synchronization
- Support for multiple calendar sources
- Upcoming events display
- Automatic calendar sync
- Event notifications and reminders
- Integration with popular calendar services

### 🖥️ Multiple Monitor Support
- Automatic monitor detection
- Easy monitor switching
- Per-monitor window positioning
- Primary and secondary monitor support
- Full-screen mode on any monitor

### 🔌 Plugin System
- Extensible plugin architecture
- Enable/disable plugins dynamically
- Custom feature development support
- Plugin management interface
- Community plugin support

### 📱 Mobile Companion App
- HTTP API for mobile integration
- Remote clock control
- Mobile alarm management
- Settings synchronization
- Real-time status updates

### ☁️ Cloud Settings Sync
- Cross-device settings synchronization
- Multiple cloud provider support
- Automatic backup and restore
- Secure encrypted sync
- Conflict resolution

### ⏰ Advanced Scheduling
- Flexible scheduling system
- Daily, weekly, monthly schedules
- Custom action support
- Multiple notification types
- Recurring event management

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Chauhan-Mukesh/Python-Clock.git
cd Python-Clock
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the enhanced application:
```bash
python main.py
```

## 📋 Dependencies

The enhanced version includes additional dependencies for advanced features:

```
pygame>=2.5.0      # For alarm sounds and audio
pyttsx3>=2.90      # For voice announcements  
pytz>=2023.3       # For timezone support
plyer>=2.1.0       # For system notifications
pystray>=0.19.0    # For advanced system tray
Pillow>=10.0.0     # For system tray icons
```

Note: Audio and voice features will gracefully degrade if dependencies are not available.

## 🎮 Usage

### Basic Operation

- Launch the application to see the current time and date
- The clock updates automatically with sub-second precision
- Use control buttons or menu options to customize the display

### Clock Styles

- **Style Button**: Cycle through available clock styles
- **View Menu**: Select specific clock style
- Each style supports both light and dark themes

### Alarms

1. Click "Alarms" button or use Tools → Alarm Manager
2. Add new alarms with custom times, labels, and sounds
3. Toggle alarms on/off or remove them
4. Test alarm sounds before setting

### Stopwatch & Timer

1. Click "Stopwatch" button or use Tools → Stopwatch & Timer
2. Use Start/Pause/Reset for stopwatch functionality
3. Add lap times during stopwatch operation
4. Set countdown timers with custom durations

### Settings

1. Access via File → Settings or system tray menu
2. Configure display, voice, and system preferences
3. Settings are automatically saved
4. Reset to defaults option available

### New Features

#### Weather Integration
1. Access via Tools → Weather
2. Configure API key and location
3. View current conditions and forecast
4. Automatic updates every 10 minutes

#### Calendar Synchronization
1. Access via Tools → Calendar
2. Add calendar sources (Google, Outlook, etc.)
3. View upcoming events
4. Sync calendars manually or automatically

#### Multiple Monitor Support
1. Access via Tools → Multi-Monitor
2. Detect available monitors
3. Move clock to different monitors
4. Configure per-monitor settings

#### Plugin System
1. Access via Tools → Plugins
2. Load custom plugins from plugins folder
3. Enable/disable plugins as needed
4. Develop custom features

#### Mobile Companion
1. Access via Tools → Mobile Companion
2. Start HTTP API server
3. Connect mobile apps to API endpoints
4. Control clock remotely

#### Cloud Settings Sync
1. Access via Tools → Cloud Sync
2. Configure sync provider and credentials
3. Upload/download settings
4. Automatic synchronization

#### Advanced Scheduling
1. Access via Tools → Advanced Scheduler
2. Create custom schedules
3. Set recurring events
4. Configure notifications and actions

### Keyboard Shortcuts

- **F1**: Show help/about
- **F11**: Toggle fullscreen
- **Ctrl+S**: Open settings
- **Ctrl+A**: Open alarm manager
- **Ctrl+T**: Open stopwatch/timer
- **Ctrl+Q**: Quit application

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run original tests
python tests/run_tests.py

# Run enhanced feature tests
python tests/run_enhanced_tests.py
```

The test suite includes:
- Unit tests for all core functionality
- Enhanced feature testing
- Settings persistence tests
- Clock style validation
- Timezone handling tests
- Error handling and edge cases

## 📁 Project Structure

```
Python-Clock/
├── src/
│   ├── __init__.py
│   ├── clock.py                # Original clock implementation
│   ├── enhanced_clock.py       # Enhanced clock with all features
│   ├── features.py             # Alarm, stopwatch, timezone, voice, weather, etc.
│   ├── settings.py             # Settings persistence
│   ├── clock_styles.py         # Multiple clock face styles
│   ├── system_tray.py          # System tray integration
│   ├── mobile_companion.py     # Mobile companion HTTP API
│   ├── plugins/                # Plugin directory
│   │   └── README.md           # Plugin development guide
│   └── sounds/                 # Alarm sound files
├── tests/
│   ├── test_clock.py           # Original tests
│   ├── test_features.py        # Enhanced feature tests
│   ├── test_enhanced_features.py # Comprehensive enhanced tests
│   ├── run_tests.py            # Test runner
│   └── run_enhanced_tests.py   # Enhanced test runner
├── main.py                     # Application entry point
├── demo_enhanced.py            # Feature demonstration
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## 🎯 Demo

Run the feature demonstration:

```bash
python demo_enhanced.py
```

This will showcase all enhanced features including:
- Settings management
- Multiple clock styles
- Timezone support
- Alarm functionality
- Stopwatch and timer operations
- System tray integration
- Voice and sound management
- Theme and styling options

## 🔧 Development

### Code Style

The project follows Python best practices:
- PEP 8 style guidelines
- Type hints where appropriate
- Comprehensive docstrings
- Error handling with graceful degradation
- Modular architecture with separation of concerns

### Architecture

- **Enhanced Features**: Modular design with feature managers
- **Settings System**: JSON-based persistent configuration
- **Clock Styles**: Plugin-like architecture for different displays
- **Cross-Platform**: Graceful handling of platform-specific features
- **Error Resilience**: Features degrade gracefully when dependencies unavailable

### Adding New Features

The application is designed for easy extension:

1. **New Clock Styles**: Inherit from `ClockStyle` class
2. **New Sound Formats**: Extend `SoundManager` class
3. **New Themes**: Add theme configurations to styles
4. **New Settings**: Update `SettingsManager` default settings

## 📸 Screenshots

*Note: Screenshots show various clock styles and features*

### Digital Clock Style
- Clean, modern digital display
- Customizable fonts and colors
- 12/24 hour format support

### Analog Clock Style
- Traditional clock face
- Smooth second hand animation
- Theme-aware styling

### Binary Clock Style
- Binary representation of time
- Educational and fun
- LED-style visual indicators

### Text Clock Style
- Natural language time display
- "Quarter past three" format
- Readable and accessible

### Alarm Manager
- Multiple alarm support
- Custom sounds and labels
- Voice announcement options

### Settings Panel
- Comprehensive configuration
- Theme and font customization
- Feature enable/disable toggles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass
5. Update documentation as needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔮 Roadmap

### Planned Enhancements
- [x] Weather integration
- [x] Calendar synchronization
- [x] Multiple monitor support
- [x] Plugin system for custom features
- [x] Mobile companion app
- [x] Cloud settings sync
- [x] Advanced scheduling features

### Current Version: 2.1

### Changelog

#### v2.1.0 (Current)
- ✅ Weather integration with API support
- ✅ Calendar synchronization system
- ✅ Multiple monitor support and detection
- ✅ Plugin system for custom features
- ✅ Mobile companion app with HTTP API
- ✅ Cloud settings sync functionality
- ✅ Advanced scheduling features
- ✅ Enhanced documentation and examples

#### v2.0.0
- ✅ Alarm functionality with custom sounds
- ✅ Stopwatch and countdown timer
- ✅ Multiple timezone support
- ✅ Customizable themes and fonts
- ✅ Settings persistence
- ✅ System tray integration
- ✅ Voice announcements
- ✅ Multiple clock faces/styles
- ✅ Enhanced testing suite
- ✅ Comprehensive documentation

#### v1.0.0
- Basic digital clock functionality
- 12/24 hour format toggle
- Light/dark theme support
- Clean, modern UI

## 🆘 Support

If you encounter any issues or have suggestions:

1. Check existing issues in the GitHub repository
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs
4. Provide system information (OS, Python version)
5. Include relevant log output

## 🙏 Acknowledgments

- Built with Python and tkinter
- Uses pygame for sound functionality
- Voice powered by pyttsx3
- Timezone support via pytz
- System integration with plyer and pystray
- Icon support with Pillow

---

**Enhanced Python Digital Clock** - Making time beautiful and functional! ⏰✨
