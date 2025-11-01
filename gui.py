import sys
import os

# Add the parent directory to the path so we can import CubyzAddonManager modules
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, application_path)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(application_path))


from CubyzAddonManager.ui.main_window import run_gui


def main():
    """Main entry point for the GUI application"""
    run_gui()


if __name__ == '__main__':
    main()