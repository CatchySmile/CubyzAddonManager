"""
Main window for the Cubyz Addon Manager GUI
"""

import sys
import json
import requests
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtGui

from ..core import find_assets_root, list_installed, install_addon, install_addon_from_url, uninstall_addon
from .widgets import BrowserAddonCard, AddonListItem
from .styles import MAIN_STYLESHEET
from .content import INFO_HTML
from .icon import get_app_icon


class MainWindow(QtWidgets.QMainWindow):
    """Main application window for Cubyz Addon Manager"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cubyz Addon Manager')
        self.setMinimumSize(800, 600)
        self.assets = find_assets_root(Path.cwd())
        
        # Set application icon
        self.setWindowIcon(get_app_icon())
        
        # Apply modern styling
        self.setStyleSheet(MAIN_STYLESHEET)

        # Main container
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QtWidgets.QLabel()
        header.setObjectName("header")
        header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.setText("Cubyz Addon Manager")
        main_layout.addWidget(header)

        # Tabbed interface
        tabs = QtWidgets.QTabWidget()
        tabs.setObjectName("mainTabs")
        main_layout.addWidget(tabs)

        # Create tabs
        self._create_addons_tab(tabs)
        self._create_browser_tab(tabs)
        self._create_info_tab(tabs)

        # Store browser cards for status updates
        self.browser_cards = []

        # Initialize list and browser
        self.refresh()
        self.refresh_browser()

    def _create_addons_tab(self, tabs):
        """Create the installed addons management tab"""
        addons_tab = QtWidgets.QWidget()
        addons_layout = QtWidgets.QVBoxLayout(addons_tab)
        addons_layout.setSpacing(15)
        addons_layout.setContentsMargins(20, 20, 20, 20)

        # Addon list with custom styling
        list_container = QtWidgets.QWidget()
        list_container.setObjectName("listContainer")
        list_layout = QtWidgets.QVBoxLayout(list_container)
        list_layout.setContentsMargins(0, 0, 0, 0)
        
        list_header = QtWidgets.QLabel("Installed Addons")
        list_header.setObjectName("sectionHeader")
        list_layout.addWidget(list_header)
        
        self.listw = QtWidgets.QListWidget()
        self.listw.setObjectName("addonList")
        list_layout.addWidget(self.listw)
        
        addons_layout.addWidget(list_container)

        # Button container
        btn_container = QtWidgets.QWidget()
        btn_container.setObjectName("buttonContainer")
        btn_layout = QtWidgets.QHBoxLayout(btn_container)
        btn_layout.setSpacing(10)
        
        self.btn_refresh = QtWidgets.QPushButton('Refresh')
        self.btn_install = QtWidgets.QPushButton('Install from File...')
        self.btn_url = QtWidgets.QPushButton('Install from URL')
        self.btn_uninstall = QtWidgets.QPushButton('Uninstall')
        
        # Set button properties
        for btn in [self.btn_refresh, self.btn_install, self.btn_url, self.btn_uninstall]:
            btn.setObjectName("actionButton")
            btn.setMinimumHeight(40)
        
        self.btn_uninstall.setObjectName("dangerButton")
        
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_install)
        btn_layout.addWidget(self.btn_url)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_uninstall)
        
        addons_layout.addWidget(btn_container)

        # Connect signals
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_install.clicked.connect(self.install_dialog)
        self.btn_url.clicked.connect(self.install_from_url)
        self.btn_uninstall.clicked.connect(self.uninstall_selected)

        tabs.addTab(addons_tab, 'Addons')

    def _create_browser_tab(self, tabs):
        """Create the online addon browser tab"""
        browser_tab = QtWidgets.QWidget()
        browser_layout = QtWidgets.QVBoxLayout(browser_tab)
        browser_layout.setSpacing(15)
        browser_layout.setContentsMargins(20, 20, 20, 20)

        # Browser header with refresh button
        browser_header_container = QtWidgets.QWidget()
        browser_header_layout = QtWidgets.QHBoxLayout(browser_header_container)
        browser_header_layout.setContentsMargins(0, 0, 0, 0)
        
        browser_header = QtWidgets.QLabel("Browse Addons")
        browser_header.setObjectName("sectionHeader")
        browser_header_layout.addWidget(browser_header)
        
        browser_header_layout.addStretch()
        
        self.btn_refresh_browser = QtWidgets.QPushButton('Refresh')
        self.btn_refresh_browser.setObjectName("actionButton")
        self.btn_refresh_browser.setMaximumWidth(100)
        self.btn_refresh_browser.clicked.connect(self.refresh_browser)
        browser_header_layout.addWidget(self.btn_refresh_browser)
        
        browser_layout.addWidget(browser_header_container)

        # Browser scroll area
        self.browser_scroll = QtWidgets.QScrollArea()
        self.browser_scroll.setObjectName("browserScroll")
        self.browser_scroll.setWidgetResizable(True)
        self.browser_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.browser_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for addon cards
        self.browser_container = QtWidgets.QWidget()
        self.browser_container.setObjectName("browserContainer")
        self.browser_layout_inner = QtWidgets.QVBoxLayout(self.browser_container)
        self.browser_layout_inner.setSpacing(8)
        self.browser_layout_inner.setContentsMargins(0, 0, 0, 0)
        
        # Loading label
        self.loading_label = QtWidgets.QLabel("Loading addons...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.browser_layout_inner.addWidget(self.loading_label)
        
        self.browser_scroll.setWidget(self.browser_container)
        browser_layout.addWidget(self.browser_scroll)

        tabs.addTab(browser_tab, 'Browse')

    def _create_info_tab(self, tabs):
        """Create the information/guide tab"""
        info_tab = QtWidgets.QWidget()
        info_layout = QtWidgets.QVBoxLayout(info_tab)
        info_layout.setContentsMargins(20, 20, 20, 20)

        info_text = QtWidgets.QTextEdit()
        info_text.setObjectName("infoText")
        info_text.setReadOnly(True)
        info_text.setAcceptRichText(True)
        info_text.setHtml(INFO_HTML)
        info_layout.addWidget(info_text)

        tabs.addTab(info_tab, 'Guide')

    def refresh(self):
        """Refresh the list of installed addons"""
        self.listw.clear()
        for a in list_installed(self.assets):
            # Check if this is the default Cubyz folder
            is_default = a.name.lower() == 'cubyz'
            
            # Create custom widget for this addon
            addon_widget = AddonListItem(a, is_default)
            
            # Create list item and set the custom widget
            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(addon_widget.sizeHint())
            self.listw.addItem(list_item)
            self.listw.setItemWidget(list_item, addon_widget)

    def install_dialog(self):
        """Show file dialog to install addon from local file"""
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select addon folder or zip', str(Path.cwd()))
        if path:
            try:
                p = Path(path)
                if p.is_dir():
                    install_addon(p, self.assets, overwrite=False)
                else:
                    install_addon(p, self.assets)
                QtWidgets.QMessageBox.information(self, 'Installed', 'Addon installed successfully')
                self.refresh()
                self.refresh_browser_status()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def install_from_url(self):
        """Show dialog to install addon from URL"""
        url, ok = QtWidgets.QInputDialog.getText(self, 'Install from URL', 'Enter GitHub or zip URL:')
        if ok and url:
            try:
                install_addon_from_url(url, self.assets)
                QtWidgets.QMessageBox.information(self, 'Installed', 'Addon installed successfully')
                self.refresh()
                self.refresh_browser_status()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', str(e))

    def uninstall_selected(self):
        """Uninstall the currently selected addon"""
        item = self.listw.currentItem()
        if not item:
            QtWidgets.QMessageBox.information(self, 'No Selection', 'Please select an addon to uninstall.')
            return
            
        # Get the custom widget for this item
        addon_widget = self.listw.itemWidget(item)
        if not addon_widget:
            return
            
        # Check if it's the default Cubyz folder
        if addon_widget.is_default:
            QtWidgets.QMessageBox.warning(
                self, 
                'Cannot Remove Default Assets', 
                'The Cubyz default assets folder cannot be removed as it contains the base game files.'
            )
            return
            
        # Check if the addon is locked
        if addon_widget.is_locked:
            QtWidgets.QMessageBox.warning(
                self, 
                'Addon Locked', 
                f'The addon "{addon_widget.addon_info.name}" is locked.\n\nClick the lock icon next to the addon to unlock it before removal.'
            )
            return
            
        # Proceed with uninstall confirmation
        name = addon_widget.addon_info.name
        reply = QtWidgets.QMessageBox.question(
            self, 
            'Confirm Removal', 
            f'Are you sure you want to remove the addon "{name}"?\n\nThis action cannot be undone.',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                uninstall_addon(name, self.assets)
                QtWidgets.QMessageBox.information(self, 'Removed', f'Addon "{name}" has been successfully removed.')
                self.refresh()
                self.refresh_browser_status()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', f'Failed to remove addon "{name}":\n\n{str(e)}')

    def refresh_browser(self):
        """Fetch and display addons from the online repository"""
        # Clear existing content
        for i in reversed(range(self.browser_layout_inner.count())):
            child = self.browser_layout_inner.itemAt(i).widget()
            if child:
                child.setParent(None)
        
        # Clear browser cards list
        self.browser_cards = []
        
        # Show loading message
        self.loading_label = QtWidgets.QLabel("Loading addons...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.browser_layout_inner.addWidget(self.loading_label)
        
        # Disable refresh button during loading
        self.btn_refresh_browser.setEnabled(False)
        self.btn_refresh_browser.setText("Loading...")
        
        # Process events to update UI
        QtWidgets.QApplication.processEvents()
        
        try:
            # Fetch addon data directly (simplified approach)
            url = "https://addons.ashframe.net/addons.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            addons_data = response.json()
            self.display_addons(addons_data)
            
        except requests.exceptions.RequestException as e:
            self.display_error(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            self.display_error(f"Invalid JSON data: {str(e)}")
        except Exception as e:
            self.display_error(f"Unexpected error: {str(e)}")
        finally:
            # Re-enable refresh button
            self.btn_refresh_browser.setEnabled(True)
            self.btn_refresh_browser.setText("Refresh")
    
    def display_addons(self, addons_data):
        """Display the fetched addons in the browser"""
        # Remove loading label
        if hasattr(self, 'loading_label'):
            self.loading_label.setParent(None)
        
        if not addons_data:
            error_label = QtWidgets.QLabel("No addons found.")
            error_label.setObjectName("errorLabel")
            error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.browser_layout_inner.addWidget(error_label)
            return
        
        # Add addon cards
        for addon_data in addons_data:
            addon_card = BrowserAddonCard(addon_data, self)
            self.browser_cards.append(addon_card)
            self.browser_layout_inner.addWidget(addon_card)
        
        # Add stretch to push cards to top
        self.browser_layout_inner.addStretch()
    
    def display_error(self, error_message):
        """Display error message in browser"""
        # Remove loading label
        if hasattr(self, 'loading_label'):
            self.loading_label.setParent(None)
        
        error_label = QtWidgets.QLabel(f"Failed to load addons:\n{error_message}")
        error_label.setObjectName("errorLabel")
        error_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        error_label.setWordWrap(True)
        self.browser_layout_inner.addWidget(error_label)
    
    def refresh_browser_status(self):
        """Refresh the install status of all browser cards"""
        for card in self.browser_cards:
            card.update_install_status()


def run_gui():
    """Run the GUI application"""
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Cubyz Addon Manager")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Cubyz")
    app.setApplicationDisplayName("Cubyz Addon Manager")
    
    # Set application icon
    app.setWindowIcon(get_app_icon())
    
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_gui()