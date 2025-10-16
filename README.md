# Cubyz Addon Manager

A comprehensive Python addon manager for Cubyz that supports listing, installing, uninstalling, and browsing addons. It provides both a modern GUI interface and command-line tools for managing game modifications.

## Features

- **Easy Installation**: Install addons from local files, zip archives, or directly from GitHub repositories
- **Online Browser**: Discover and install addons from the online repository
- **Safety Features**: Protected default assets with addon locking system
- **CLI & Terminal**: Both GUI and command-line interfaces available
- **Smart Detection**: Automatically finds your game's assets folder
- **Update Management**: Track addon versions and manage updates

## Quick Start

### GUI Application
1. **Download**: Get the latest release executable
2. **Move**: Put the executable in the same folder as your Cubyz game
3. **Run**: Double-click the executable to launch the GUI

### Python Installation
If you prefer to run from source:
```bash
# Install dependencies
pip install PySide6 requests

# Run the GUI
python -m addon_manager.gui

# Or use the command line
python -m addon_manager.core --help
```

## Preview

<img width="300" height="190" alt="Addons Tab" src="https://github.com/user-attachments/assets/02af46d4-ea08-4692-a866-9c4da4c3112b" />
<img width="300" height="190" alt="Browse Tab" src="https://github.com/user-attachments/assets/6a11203d-eeb1-405d-9eed-6c2f066172aa" />

## How to Use

### GUI Interface

#### Installing Addons

**From Files:**
1. Click the **Addons** tab
2. Click **Install from File...**
3. Select a `.zip` file or addon folder
4. The addon will be extracted to your assets folder

**From GitHub:**
1. Click **Install from URL**
2. Paste a GitHub repository URL (e.g., `https://github.com/CatchySmile/AddonName`)
3. The manager will download the latest version automatically

**From Online Browser:**
1. Click the **Browse** tab
2. Browse available addons with descriptions and tags
3. Click **Install** on any addon you want to add
4. Installed addons will show as "Installed"

#### Managing Installed Addons

- **View**: All installed addons are listed in the **Addons** tab
- **Lock/Unlock**: Click the lock icon to enable/disable removal protection
- **Remove**: Select an addon and click **Uninstall** (must be unlocked first)
- **Refresh**: Click **Refresh** to update the addon list

### Command Line Interface

```bash
# List installed addons
python -m addon_manager.core list

# Install from local file or folder
python -m addon_manager.core install path/to/addon.zip

# Install from GitHub URL
python -m addon_manager.core install https://github.com/owner/repo

# Install with custom assets path
python -m addon_manager.core install addon.zip --assets "C:\Path\To\Game\assets"

# Uninstall an addon
python -m addon_manager.core uninstall addon-name

# Install with overwrite (replace existing)
python -m addon_manager.core install addon.zip --overwrite
```

## Addon Structure

Addons are folders that can contain various types of game content:

```
my_addon/
├── addon.json          # Metadata (recommended)
├── README.md          # Documentation
├── blocks/            # Custom block definitions
├── items/             # New items and tools
├── biomes/            # Environmental biomes
├── recipes/           # Crafting recipes
└── textures/          # Visual assets
```

### Addon Metadata (addon.json)

```json
{
    "name": "My Awesome Addon",
    "version": "1.0.0",
    "description": "Adds cool new blocks and items",
    "author": "Your Name",
    "tags": ["blocks", "items", "magic"]
}
```

## Creating Your Own Addon

1. **Create Structure**: Make a folder with your addon's name
2. **Add Content**: Create subfolders for the content you want to include:
   - `blocks/` — Custom block definitions
   - `items/` — New items and tools
   - `biomes/` — Environmental biomes
   - `recipes/` — Crafting recipes
   - `textures/` — Visual assets
3. **Add Metadata**: Create an `addon.json` file with your addon information
4. **Test**: Install your addon locally to test it works
5. **Share**: Zip your addon folder or upload to GitHub to share with others

## Safety Features

- **Default Assets Protection**: The Cubyz base game assets cannot be removed
- **Addon Locking**: All addons start locked to prevent accidental removal
- **Unlock Confirmation**: Unlocking an addon requires confirmation
- **Removal Confirmation**: Final removal requires additional confirmation
- **Backup Friendly**: Original files are preserved during installation

## Troubleshooting

### Common Issues

**Installation fails:**
- Check that your zip file is valid and not corrupted
- Ensure you have write permissions to the assets folder
- Try using the `--overwrite` flag if the addon already exists

**GitHub download fails:**
- Ensure the repository is public
- Check your internet connection
- Verify the repository URL is correct

**Addon doesn't work in game:**
- Check the game logs for errors
- Verify your JSON files have valid syntax
- Ensure file names match what's referenced in your JSON

**Browser shows wrong status:**
- Click **Refresh** in the Browse tab
- Restart the application if issues persist

**Need more control:**
- Use the command-line interface for advanced options
- Check the `addon_manager` folder for additional tools

### Getting Help

- Check the **Guide** tab in the application for detailed instructions
- Explore the base game files in `assets/cubyz` for examples and inspiration
- Report issues on the project's GitHub repository

## Technical Details

### Requirements
- **Python 3.7+** (if running from source)
- **PySide6** for GUI functionality
- **requests** for downloading from URLs
- **Windows/Linux/macOS** compatible

### File Locations
- **Assets folder**: Auto-detected by walking up from the executable location
- **Addons**: Installed directly in the assets folder alongside the default `cubyz` folder
- **Configuration**: Stored in the application directory

### Supported Formats
- **Zip files**: Standard zip archives with addon content
- **Folders**: Direct folder installation by copying
- **GitHub repos**: Automatic download from public repositories
- **Direct URLs**: Any publicly accessible zip file

## Development

### Building from Source
```bash
# Clone the repository
git clone <repository-url>
cd cubyz-addon-manager

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m addon_manager.gui
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest addon_manager/tests/test_core.py
```

### Building Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller CubyzAddonManager.spec
```

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Happy Testing!** 

Explore, create, and share amazing addons for Cubyz!
