# Cubyz Addon Manager

Small Python addon manager for Cubyz. It supports listing, installing
and uninstalling addons by copying/extracting them into your game's `assets/`
folder.

Usage examples:

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

GUI and URL installs:

- A simple desktop GUI is available (requires `PySide6`). Run:

        C:/Users/Sam/Desktop/Cubyz/.venv/Scripts/python.exe -m addon_manager.gui

- You can also install an addon directly from a GitHub repo URL; the manager
    will attempt to download the repo's zip for `main` or `master`, or accept a
    direct .zip URL.
