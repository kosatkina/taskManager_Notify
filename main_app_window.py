from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QMenuBar, 
    QMenu, QMessageBox, QInputDialog, QStatusBar
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

MAX_OPEN_WINDOWS = 5
MAX_CHARACTERS = 500


class MainAppWindow(QMainWindow):
    open_windows = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notify")
        #self.setGeometry(1150, 100, 250, 250) 
        self.setFixedSize(300, 300)

        # TODO - Set icons

        # Central widget
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.update_status)
        self.setCentralWidget(self.text_edit)
        
        # Menu and status bar
        self.create_menu()
        self.create_status()
        

    # Function to create menu
    def create_menu(self):
        menu_bar = self.menuBar()

        note_menu = menu_bar.addMenu("Menu")    # TODO - Change to icon

        add_action = QAction("Add", self)
        add_action.triggered.connect(self.add_note)

        list_action = QAction("List", self)
        list_action.triggered.connect(self.list_notes)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_note)

        note_menu.addAction(add_action)
        note_menu.addAction(list_action)
        note_menu.addAction(delete_action)

    # Callback function on Add note button click signal
    # This function opens new main window above existing one
    def add_note(self):
            # Max 5 notes can be opened 
            if len(MainAppWindow.open_windows) >= MAX_OPEN_WINDOWS:
                 QMessageBox.warning(self, "Limit reached", " Max five notes.")
                 return
            
            self.new_window = MainAppWindow()
            self.new_window.show()
    
    # Callback function to list all notes
    def list_notes(self):
        note_titles = [f"Note {i+1}" for i in range(len(MainAppWindow.open_windows))]
        selected, ok = QInputDialog.getItem(self, "List Notes", "Select a note to view:", note_titles, 0, False)
        if ok:
            index = note_titles.index(selected)
            MainAppWindow.open_windows[index].raise_()
            MainAppWindow.open_windows[index].activateWindow()

    # Callback function to delete the note
    def delete_note(self):
         confirm = QMessageBox.question(self, "Delete", "Are you sure you want to delete this note?")
         
         if confirm == QMessageBox.StandardButton.Yes:
              MainAppWindow.open_windows.remove(self)
              self.close()
    

    # Function to create status bar
    def create_status(self):
         pass

    # Callback function to update status bar info
    def update_status(self):
        pass



