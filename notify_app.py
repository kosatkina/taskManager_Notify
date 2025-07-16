## This file is the main entry point of the Notify App

from PyQt6.QtWidgets import QApplication
from main_app_window import MainAppWindow
import sys


if __name__ == "__main__":
    notify_app = QApplication(sys.argv)
    window = MainAppWindow()
    window.show()

    # Start the event loop
    sys.exit(notify_app.exec())
