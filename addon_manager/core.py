from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import requests
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional
from urllib.parse import urlparse


@dataclass
class AddonInfo:
    name: str
    path: Path
    manifest: Optional[dict] = None


def find_assets_root(start: Path) -> Path:
    """Find the assets root (contains 'cubyz' folder) by walking up from start.

    If not found, returns start / 'assets' as fallback.
    """
    cur = start.resolve()
    for _ in range(6):
        candidate = cur / "assets"
        if candidate.exists() and (candidate / "cubyz").exists():
            return candidate
        cur = cur.parent
    return start.resolve() / "assets"


def list_installed(addons_dir: Path) -> List[AddonInfo]:
    addons = []
    if not addons_dir.exists():
        return addons
    for child in addons_dir.iterdir():
        if child.is_dir():
            manifest = None
            manifest_file = child / "addon.json"
            if manifest_file.exists():
                try:
                    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
                except Exception:
                    manifest = None
            addons.append(AddonInfo(child.name, child, manifest))
    return addons


def validate_addon_dir(addon_path: Path) -> bool:
    """Basic validation: an addon folder should contain at least one of
    'blocks', 'items', 'biomes', or 'textures' subfolders, or an addon.json.
    """
    if not addon_path.exists() or not addon_path.is_dir():
        return False
    if (addon_path / "addon.json").exists():
        return True
    for name in ("blocks", "items", "biomes", "recipes", "textures"):
        if (addon_path / name).exists():
            return True
    return False


def install_addon(zip_path: Path, assets_root: Path, overwrite: bool = False) -> Path:
    """Install an addon from a zip-like folder or an already-extracted folder.

    If zip_path is a directory, it will be copied into assets_root.
    If zip_path is a .zip file, it will be extracted.
    Returns the installed addon folder path.
    """
    addons_folder = assets_root
    if not addons_folder.exists():
        addons_folder.mkdir(parents=True, exist_ok=True)

    if zip_path.is_dir():
        src = zip_path
        dest = addons_folder / src.name
        if dest.exists():
            if overwrite:
                shutil.rmtree(dest)
            else:
                raise FileExistsError(f"Addon already installed: {dest}")
        shutil.copytree(src, dest)
        return dest

    if zip_path.suffix.lower() == ".zip":
        import zipfile

        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Use the zip file name as the addon name
            addon_name = zip_path.stem
            target = addons_folder / addon_name
            
            if target.exists():
                if overwrite:
                    shutil.rmtree(target)
                else:
                    raise FileExistsError(f"Addon already installed: {target}")
            
            # Check if zip has a single top-level folder
            names = zf.namelist()
            top_folders = set()
            for name in names:
                if '/' in name:
                    top_folders.add(name.split('/')[0])
                elif name and not name.endswith('/'):
                    top_folders.add('')  # Files at root level
            
            if len(top_folders) == 1 and '' not in top_folders:
                # Single top-level folder - extract its contents to target
                top_folder = list(top_folders)[0]
                import tempfile
                with tempfile.TemporaryDirectory() as temp_dir:
                    zf.extractall(temp_dir)
                    temp_path = Path(temp_dir) / top_folder
                    shutil.copytree(temp_path, target)
            else:
                # Multiple items at root or files at root - extract directly
                zf.extractall(target)
            
            return target

    raise ValueError("Unsupported addon source: must be a folder or a .zip file")


def install_addon_from_url(url: str, assets_root: Path, overwrite: bool = False) -> Path:
    """Download an addon from a URL (supports zip files or GitHub repo URLs) and install it.

    Returns the installed folder Path.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must be http or https")

    # If URL directly points to a zip, download and extract
    if url.lower().endswith('.zip'):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        tf = Path(tempfile.gettempdir()) / (Path(url).stem + '.zip')
        with open(tf, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return install_addon(tf, assets_root, overwrite=overwrite)

    # Heuristic: handle GitHub repo page like https://github.com/owner/repo or with branch
    if 'github.com' in parsed.netloc:
        parts = parsed.path.strip('/').split('/')
        if len(parts) >= 2:
            owner, repo = parts[0], parts[1]
            # try main then master
            for branch in ('main', 'master'):
                zip_url = f'https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip'
                try:
                    r = requests.head(zip_url, allow_redirects=True)
                    if r.status_code == 200:
                        return install_addon_from_url(zip_url, assets_root, overwrite=overwrite)
                except Exception:
                    continue
    # Fallback: attempt to GET and check content-type
    r = requests.get(url, stream=True)
    r.raise_for_status()
    ct = r.headers.get('content-type', '')
    if 'zip' in ct or url.lower().endswith('.zip'):
        tf = Path(tempfile.gettempdir()) / (Path(urlparse(url).path).stem + '.zip')
        with open(tf, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return install_addon(tf, assets_root, overwrite=overwrite)

    raise ValueError('Could not determine how to download/install the provided URL')


def uninstall_addon(name: str, assets_root: Path) -> None:
    path = assets_root / name
    if not path.exists():
        raise FileNotFoundError("Addon not found: %s" % name)
    shutil.rmtree(path)


def load_manifest(addon_path: Path) -> Optional[dict]:
    mf = addon_path / "addon.json"
    if not mf.exists():
        return None
    try:
        return json.loads(mf.read_text(encoding="utf-8"))
    except Exception:
        return None


def cli(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="cubyz-addon")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List installed addons")
    p_list.add_argument("--assets", help="Path to game assets folder", default=None)

    p_install = sub.add_parser("install", help="Install addon (folder or zip)")
    p_install.add_argument("source", help="Folder or zip to install")
    p_install.add_argument("--assets", help="Path to game assets folder", default=None)
    p_install.add_argument("--overwrite", action="store_true")

    p_un = sub.add_parser("uninstall", help="Uninstall addon by name")
    p_un.add_argument("name", help="Name of addon folder to remove")
    p_un.add_argument("--assets", help="Path to game assets folder", default=None)

    args = parser.parse_args(list(argv) if argv else None)

    start = Path.cwd()
    assets = Path(args.assets) if getattr(args, 'assets', None) else find_assets_root(start)

    if args.cmd == "list":
        addons = list_installed(assets)
        for a in addons:
            v = a.manifest.get('version') if a.manifest else 'unknown'
            print(f"{a.name}\t{v}\t{a.path}")
        return 0

    if args.cmd == "install":
        src = Path(args.source)
        try:
            installed = install_addon(src, assets, overwrite=args.overwrite)
            print(f"Installed: {installed}")
            return 0
        except Exception as e:
            print("Error:", e)
            return 2

    if args.cmd == "uninstall":
        try:
            uninstall_addon(args.name, assets)
            print("Uninstalled: ", args.name)
            return 0
        except Exception as e:
            print("Error:", e)
            return 2

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(cli())
