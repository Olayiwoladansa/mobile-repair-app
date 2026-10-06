import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow
from database import Database

def main():
    # Initialize database
    db = Database()
    db.initialize()
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
