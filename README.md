# Python Digital Clock

A modern, feature-rich digital clock application built with Python and tkinter.

## Features

- **Digital Clock Display**: Real-time digital clock with seconds precision
- **Multiple Time Formats**: Toggle between 12-hour and 24-hour formats
- **Theme Support**: Light and dark theme options
- **Modern UI**: Clean, responsive user interface
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Extensible**: Built with future features in mind (alarm, stopwatch, timezones)

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Chauhan-Mukesh/Python-Clock.git
cd Python-Clock
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Basic Operation

- Launch the application to see the current time and date
- The clock updates every second automatically
- Use the control buttons at the bottom to customize the display

### Controls

- **24H/12H Format Button**: Toggle between 24-hour and 12-hour time formats
- **Theme Button**: Switch between light and dark themes
- **Set Alarm**: (Feature placeholder - coming soon)
- **Stopwatch**: (Feature placeholder - coming soon)

### Keyboard Shortcuts

- Close the application using the window close button or Alt+F4

## Testing

Run the comprehensive test suite:

```bash
python tests/run_tests.py
```

The test suite includes:
- Unit tests for all core functionality
- Edge case testing (midnight, noon)
- Time format validation
- Theme switching tests
- Thread safety tests

## Project Structure

```
Python-Clock/
├── src/
│   ├── __init__.py
│   └── clock.py          # Main application logic
├── tests/
│   ├── test_clock.py     # Comprehensive test suite
│   └── run_tests.py      # Test runner
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## Development

### Code Style

The project follows Python best practices:
- PEP 8 style guidelines
- Type hints where appropriate
- Comprehensive docstrings
- Error handling
- Clean separation of concerns

### Adding Features

The application is designed to be extensible. Key areas for enhancement:

1. **Alarm System**: Add alarm functionality with sound alerts
2. **Stopwatch/Timer**: Implement timing features
3. **Multiple Timezones**: Support for different time zones
4. **Customization**: More themes, fonts, and colors
5. **Settings Persistence**: Save user preferences

### Running Tests

The project includes comprehensive tests:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python -m unittest tests.test_clock

# Run with verbose output
python -m unittest tests.test_clock -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Future Enhancements

- [ ] Alarm functionality with custom sounds
- [ ] Stopwatch and countdown timer
- [ ] Multiple timezone support
- [ ] Customizable themes and fonts
- [ ] Settings persistence
- [ ] System tray integration
- [ ] Voice announcements
- [ ] Multiple clock faces/styles

## Screenshots

*Note: Screenshots will be added once the GUI is tested*

## Support

If you encounter any issues or have suggestions for improvements, please:

1. Check the existing issues in the GitHub repository
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs
4. Provide your system information (OS, Python version)

## Changelog

### v1.0.0 (Current)
- Initial release
- Basic digital clock functionality
- 12/24 hour format toggle
- Light/dark theme support
- Comprehensive test suite
- Clean, modern UI
