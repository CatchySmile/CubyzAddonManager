from addon_manager import core
from pathlib import Path
import tempfile


def test_validate_addon_dir(tmp_path: Path):
    d = tmp_path / "myaddon"
    d.mkdir()
    assert not core.validate_addon_dir(d)
    (d / "blocks").mkdir()
    assert core.validate_addon_dir(d)


def test_install_and_uninstall(tmp_path: Path):
    # prepare assets root
    assets = tmp_path / "assets"
    (assets / "cubyz").mkdir(parents=True)

    # make addon folder
    addon = tmp_path / "sample"
    (addon / "blocks").mkdir(parents=True)
    installed = core.install_addon(addon, assets)
    assert installed.exists()
    core.uninstall_addon(installed.name, assets)
    assert not installed.exists()
