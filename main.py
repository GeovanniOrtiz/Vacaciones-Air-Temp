"""
Main application entry point
"""
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import config


def main():
    """Main application function"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setOrganizationName(config.COMPANY_NAME)
    
    # Create and show main window
    window = MainWindow() 
    window.show()
    
    # Run application
    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()
