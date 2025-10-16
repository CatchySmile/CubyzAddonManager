# Cubyz Addon Manager

Small Python addon manager for Cubyz. It supports listing, installing
and uninstalling addons, and browsing addons by copying/extracting them into your game's `assets/`
folder. 

## Quick start
- Because this was made with python, the compiled executable is quite large. in order for a standalone executable we rely on pre-packaged imports.
- Place the Executable in the same folder as the Cubyz executable.

## [Preview]
<img width="300" height="190" alt="image" src="https://github.com/user-attachments/assets/02af46d4-ea08-4692-a866-9c4da4c3112b" />
<img width="300" height="190" alt="image" src="https://github.com/user-attachments/assets/6a11203d-eeb1-405d-9eed-6c2f066172aa" />

GUI and URL installs:

- A simple desktop GUI is available, use the terminal or run the executable.
 (requires `PySide6`). Run:

        python.exe -m addon_manager.gui

## Usage
Install from a folder (will copy):

    python -m addon_manager.core install path/to/addon --assets "C:\\Path\\To\\Game\\assets"

Install from zip:

    python -m addon_manager.core install path/to/addon.zip --assets "C:\\Path\\To\\Game\\assets"

List installed addons (auto-discovers assets folder by walking up):

    python -m addon_manager.core list

Uninstall:

    python -m addon_manager.core uninstall my-addon-name

Notes:
- Addons are simple folders that may contain subfolders like `blocks`, `items`,
  `biomes`, `recipes`, and `textures`. A recommended metadata file is
  `addon.json` with fields like `name` and `version`.

- You can also install an addon directly from a GitHub repo URL; the manager
    will attempt to download the repo's zip for `main` or `master`, or accept a
    direct .zip URL.




