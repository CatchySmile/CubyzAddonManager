"""
Application icon generation for Cubyz Addon Manager
"""

from PySide6 import QtGui, QtCore
from pathlib import Path


def create_app_icon():
    """Create a terminal-style application icon"""
    # Create a 64x64 pixmap
    pixmap = QtGui.QPixmap(64, 64)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)
    
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    
    # Terminal window background (dark)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))  # Dark terminal background
    painter.setPen(QtGui.QPen(QtGui.QColor(60, 60, 60), 2))   # Border
    painter.drawRoundedRect(8, 12, 48, 40, 4, 4)
    
    # Terminal title bar
    painter.setBrush(QtGui.QBrush(QtGui.QColor(45, 45, 48)))  # Title bar
    painter.setPen(QtGui.QPen(QtGui.QColor(60, 60, 60), 1))
    painter.drawRoundedRect(8, 12, 48, 8, 4, 4)
    painter.drawRect(8, 16, 48, 4)  # Remove bottom rounded corners
    
    # Terminal window controls (red, yellow, green dots)
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 95, 87)))  # Red
    painter.setPen(QtCore.Qt.PenStyle.NoPen)
    painter.drawEllipse(12, 14, 4, 4)
    
    painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 189, 46)))  # Yellow
    painter.drawEllipse(18, 14, 4, 4)
    
    painter.setBrush(QtGui.QBrush(QtGui.QColor(39, 201, 63)))  # Green
    painter.drawEllipse(24, 14, 4, 4)
    
    # Terminal prompt and cursor
    painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0), 1))  # Green terminal text
    font = QtGui.QFont("Consolas", 8)
    font.setBold(True)
    painter.setFont(font)
    
    # Draw prompt text
    painter.drawText(12, 30, "$")
    painter.drawText(18, 30, "cubyz")
    
    # Draw blinking cursor
    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
    painter.drawRect(42, 26, 6, 2)
    
    # Terminal content lines (representing addon management)
    painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 1))  # Light gray text
    font.setPointSize(6)
    painter.setFont(font)
    painter.drawText(12, 40, "addon-mgr")
    painter.drawText(12, 47, "install")
    
    painter.end()
    return QtGui.QIcon(pixmap)


def save_icon_file():
    """Save the icon as a .ico file for use with executables"""
    from PySide6 import QtWidgets
    
    # Create a temporary QApplication if none exists
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    icon = create_app_icon()
    icon_path = Path(__file__).parent / "cubyz_addon_manager.ico"
    
    # Get the pixmap and save as ICO
    pixmap = icon.pixmap(64, 64)
    pixmap.save(str(icon_path), "ICO")
    
    return icon_path


def get_app_icon():
    """Get the application icon, creating it if necessary"""
    icon_path = Path(__file__).parent / "cubyz_addon_manager.ico"
    
    if icon_path.exists():
        return QtGui.QIcon(str(icon_path))
    else:
        # Create and save the icon
        save_icon_file()
        return QtGui.QIcon(str(icon_path))