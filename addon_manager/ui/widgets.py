"""
Custom widgets for the Cubyz Addon Manager GUI
"""

import json
import requests
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui
from ..core import list_installed, install_addon_from_url


class BrowserAddonCard(QtWidgets.QWidget):
    """Widget representing an addon card in the browser"""
    
    def __init__(self, addon_data, parent_window):
        super().__init__()
        self.addon_data = addon_data
        self.parent_window = parent_window
        
        self.setObjectName("addonCard")
        self.setFixedHeight(120)
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # Icon placeholder (could be enhanced to load actual images)
        icon_label = QtWidgets.QLabel("📦")
        icon_label.setObjectName("addonIcon")
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Addon info
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setSpacing(4)
        
        # Name and version
        name_label = QtWidgets.QLabel(f"{addon_data['name']} ({addon_data['version']})")
        name_label.setObjectName("browserAddonName")
        info_layout.addWidget(name_label)
        
        # Author
        author_label = QtWidgets.QLabel(f"by {addon_data['author']}")
        author_label.setObjectName("browserAddonAuthor")
        info_layout.addWidget(author_label)
        
        # Description
        desc_label = QtWidgets.QLabel(addon_data['description'])
        desc_label.setObjectName("browserAddonDesc")
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        # Tags
        if addon_data.get('tags'):
            tags_text = " • ".join(addon_data['tags'])
            tags_label = QtWidgets.QLabel(f"Tags: {tags_text}")
            tags_label.setObjectName("browserAddonTags")
            info_layout.addWidget(tags_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Install button
        self.install_btn = QtWidgets.QPushButton("Install")
        self.install_btn.setObjectName("installButton")
        self.install_btn.setFixedSize(80, 32)
        self.install_btn.clicked.connect(self.install_addon)
        layout.addWidget(self.install_btn)
        
        # Check if already installed
        self.update_install_status()
    
    def update_install_status(self):
        """Update the install button status based on whether addon is installed"""
        # Check if this addon is already installed - fix case sensitivity issue
        
        installed_addons = list_installed(self.parent_window.assets)
        # addon_id = self.addon_data['id']
        
        # Check multiple possible name variations
        possible_names = [
            self.addon_data['name'].lower().replace(' ', '_'),
            self.addon_data['name'].lower().replace(' ', ''),
        ]
        
        #TODO: i have no idea what is going on here?
        # is this even needed anymore?
        is_installed = any(
            addon.name.lower() in possible_names or 
            any(name in addon.name.lower() for name in possible_names)
            for addon in installed_addons
        )
        
        if is_installed:
            self.install_btn.setText("Installed")
            self.install_btn.setEnabled(False)
            self.install_btn.setObjectName("installedButton")
        else:
            self.install_btn.setText("Install")
            self.install_btn.setEnabled(True)
            self.install_btn.setObjectName("installButton")
        
        # Refresh button style
        self.install_btn.style().unpolish(self.install_btn)
        self.install_btn.style().polish(self.install_btn)
    
    def install_addon(self):
        """Install the addon from the online repository"""
        try:
            # Construct the full download URL
            base_url = "https://addons.ashframe.net/"
            download_url = base_url + self.addon_data['fileUrl']

            # Show progress dialog
            progress = QtWidgets.QProgressDialog("Downloading addon...", "Cancel", 0, 0, self)
            progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
            progress.show()
            
            # Install from URL
            install_addon_from_url(download_url, self.parent_window.assets, overwrite=True)
            
            progress.close()
            
            QtWidgets.QMessageBox.information(
                self, 
                'Installation Complete', 
                f'"{self.addon_data["name"]}" has been successfully installed!'
            )
            
            # Update button status
            self.update_install_status()
            
            # Refresh the installed addons list
            self.parent_window.refresh()
            
            # Refresh all browser cards to update their status
            self.parent_window.refresh_browser_status()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, 
                'Installation Failed', 
                f'Failed to install "{self.addon_data["name"]}":\n\n{str(e)}'
            )


class AddonListItem(QtWidgets.QWidget):
    """Widget representing an installed addon in the list"""
    
    def __init__(self, addon_info, is_default=False):
        super().__init__()
        self.addon_info = addon_info
        self.is_default = is_default
        self.is_locked = True  # Start locked by default
        
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Lock/unlock button
        self.lock_btn = QtWidgets.QPushButton()
        self.lock_btn.setFixedSize(24, 24)
        self.lock_btn.setObjectName("lockButton")
        self.update_lock_icon()
        self.lock_btn.clicked.connect(self.toggle_lock)
        layout.addWidget(self.lock_btn)
        
        # Addon info
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Name and version
        name_ver = f"{addon_info.name}"
        if addon_info.manifest and 'version' in addon_info.manifest:
            name_ver += f" ({addon_info.manifest['version']})"
        else:
            name_ver += " (unknown)"
            
        self.name_label = QtWidgets.QLabel(name_ver)
        self.name_label.setObjectName("addonName")
        info_layout.addWidget(self.name_label)
        
        # Status label
        if self.is_default:
            status_text = "Default Game Assets - Cannot be removed"
            self.status_label = QtWidgets.QLabel(status_text)
            self.status_label.setObjectName("defaultLabel")
        else:
            self.status_label = QtWidgets.QLabel("Locked - Click lock to enable removal")
            self.status_label.setObjectName("statusLabel")
        
        info_layout.addWidget(self.status_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        # If default addon, disable lock button
        if self.is_default:
            self.lock_btn.setEnabled(False)
            self.is_locked = True
    
    def update_lock_icon(self):
        """Update the lock icon and tooltip"""
        if self.is_locked:
            self.lock_btn.setText("🔒")
            self.lock_btn.setToolTip("Click to unlock for removal")
        else:
            self.lock_btn.setText("🔓")
            self.lock_btn.setToolTip("Click to lock")
    
    def toggle_lock(self):
        """Toggle the lock state of the addon"""
        if self.is_default:
            return
            
        if self.is_locked:
            # Ask for confirmation before unlocking
            reply = QtWidgets.QMessageBox.question(
                self, 
                'Unlock Addon',
                f'Are you sure you want to unlock "{self.addon_info.name}" for removal?\n\nThis will allow the addon to be uninstalled.',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )
            
            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.is_locked = False
                self.status_label.setText("Unlocked - Can be removed")
                self.update_lock_icon()
        else:
            # Re-locking doesn't need confirmation
            self.is_locked = True
            self.status_label.setText("Locked - Click lock to enable removal")
            self.update_lock_icon()