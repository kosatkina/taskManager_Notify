## This file is the main entry point of the Notify App

from PyQt6.QtWidgets import QApplication
from ui.main_app_window import MainAppWindow
from db.database import init_db
import sys


if __name__ == "__main__":
    # Initialize the database before GUI loads
    init_db()
    
    notify_app = QApplication(sys.argv)
    window = MainAppWindow()
    window.show()

    # Start the event loop
    sys.exit(notify_app.exec())
