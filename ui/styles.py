"""
Stylesheet definitions for the Cubyz Addon Manager GUI
"""

MAIN_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

#header {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    padding: 16px;
    background-color: #2d2d30;
    border-bottom: 1px solid #3e3e42;
}

#mainTabs {
    background-color: #1e1e1e;
}

#mainTabs::pane {
    border: 1px solid #3e3e42;
    background-color: #252526;
}

#mainTabs QTabBar::tab {
    background-color: #2d2d30;
    color: #cccccc;
    padding: 8px 16px;
    margin-right: 1px;
    border: 1px solid #3e3e42;
    border-bottom: none;
}

#mainTabs QTabBar::tab:selected {
    background-color: #252526;
    color: #ffffff;
    border-bottom: 2px solid #007acc;
}

#mainTabs QTabBar::tab:hover {
    background-color: #3e3e42;
}

#sectionHeader {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    padding: 8px 0px;
}

#listContainer {
    background-color: #252526;
    border: 1px solid #3e3e42;
    padding: 12px;
}

#addonList {
    border: 1px solid #3e3e42;
    background-color: #1e1e1e;
    selection-background-color: #094771;
    selection-color: #ffffff;
    font-size: 13px;
    color: #cccccc;
}

#addonList::item {
    padding: 2px;
    border-bottom: 1px solid #3e3e42;
}

#addonList::item:selected {
    background-color: #094771;
    color: #ffffff;
}

#addonList::item:hover {
    background-color: #2a2d2e;
}

#buttonContainer {
    background-color: #252526;
    border: 1px solid #3e3e42;
    padding: 12px;
}

#actionButton {
    background-color: #0e639c;
    color: #ffffff;
    border: 1px solid #007acc;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 500;
}

#actionButton:hover {
    background-color: #1177bb;
}

#actionButton:pressed {
    background-color: #005a9e;
}

#dangerButton {
    background-color: #a1260d;
    border: 1px solid #cd3131;
}

#dangerButton:hover {
    background-color: #c42b1c;
}

#infoText {
    border: 1px solid #3e3e42;
    background-color: #1e1e1e;
    color: #cccccc;
    font-size: 13px;
    line-height: 1.5;
}

#lockButton {
    background-color: #3e3e42;
    border: 1px solid #5a5a5a;
    color: #ffffff;
    font-size: 12px;
}

#lockButton:hover {
    background-color: #4a4a4a;
}

#lockButton:disabled {
    background-color: #2a2a2a;
    color: #666666;
}

#addonName {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}

#statusLabel {
    font-size: 11px;
    color: #cccccc;
}

#defaultLabel {
    font-size: 11px;
    color: #ffc107;
    font-weight: 500;
}

#browserScroll {
    border: 1px solid #3e3e42;
    background-color: #1e1e1e;
}

#browserContainer {
    background-color: #1e1e1e;
}

#addonCard {
    background-color: #252526;
    border: 1px solid #3e3e42;
    margin: 4px 0px;
}

#addonCard:hover {
    background-color: #2a2d2e;
    border-color: #007acc;
}

#addonIcon {
    background-color: #3e3e42;
    border: 1px solid #5a5a5a;
    font-size: 24px;
}

#browserAddonName {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
}

#browserAddonAuthor {
    font-size: 12px;
    color: #9cdcfe;
    font-style: italic;
}

#browserAddonDesc {
    font-size: 12px;
    color: #cccccc;
    margin-top: 4px;
}

#browserAddonTags {
    font-size: 11px;
    color: #569cd6;
}

#installButton {
    background-color: #28a745;
    color: #ffffff;
    border: 1px solid #34ce57;
    font-size: 12px;
    font-weight: 600;
}

#installButton:hover {
    background-color: #34ce57;
}

#installedButton {
    background-color: #6c757d;
    color: #ffffff;
    border: 1px solid #868e96;
    font-size: 12px;
    font-weight: 600;
}

#loadingLabel {
    font-size: 14px;
    color: #cccccc;
    padding: 40px;
}

#errorLabel {
    font-size: 14px;
    color: #cd3131;
    padding: 40px;
}
"""