# Cubyz Addon Manager UI

This directory contains the organized GUI components for the Cubyz Addon Manager.

## Structure

```
ui/
├── __init__.py          # Package initialization
├── main_window.py       # Main application window and logic
├── widgets.py           # Custom widgets (AddonListItem, BrowserAddonCard)
├── styles.py            # CSS/QSS stylesheets
├── content.py           # HTML content for info tab
├── icon.py              # Application icon generation
├── cubyz_addon_manager.ico  # Generated application icon
└── README.md            # This file
```

## Components

### main_window.py
- `MainWindow` class - Main application window
- Tab creation and management
- Event handlers for all user interactions
- `run_gui()` function - Application entry point

### widgets.py
- `BrowserAddonCard` - Widget for displaying addons in the browser
- `AddonListItem` - Widget for displaying installed addons with lock/unlock

### styles.py
- `MAIN_STYLESHEET` - Complete CSS styling for the application
- Dark theme with modern VS Code-inspired colors

### content.py
- `INFO_HTML` - HTML content for the guide/info tab
- Includes styling and comprehensive documentation

### icon.py
- `create_app_icon()` - Programmatically creates the app icon
- `save_icon_file()` - Saves icon as .ico file for executables
- `get_app_icon()` - Returns QIcon for use in the application

## Benefits of This Organization

1. **Separation of Concerns** - Each file has a specific purpose
2. **Maintainability** - Easier to find and modify specific components
3. **Reusability** - Components can be imported and reused
4. **Readability** - Much cleaner than a single large file
5. **Scalability** - Easy to add new components or features

## Usage

The main GUI can be launched through:
- `python -m addon_manager.gui`
- `from addon_manager.ui.main_window import run_gui; run_gui()`

For building executables, use the build script in the project root:
- `python build_addon_manager.py exe`