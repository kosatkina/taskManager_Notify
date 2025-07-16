from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QAction


class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notify")
        self.setGeometry(1150, 100, 250, 250) 

        # TODO - Set icon

        self._init_menu()
        self.statusBar().showMessage("Max 500 characters.")

        def _init_menu(self):
            menu_bar = self.menuBar()

            # Notes menu
            note_menu = menu_bar.addMenu


                # Note Storage - CHANGE TO DB
        self.notes = []

        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.text_edit = QTextEdit("")
        
        self.add_note_btn = QPushButton("Add")
        self.add_note_btn.clicked.connect(self.add_note_btn_clicked)
        
        self.note_list_btn = QPushButton("List")
        self.note_list_btn.clicked.connect(self.note_list_btn_clicked)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.add_note_btn)
        layout.addWidget(self.note_list_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Callback function on Add note button click signal
    # This function opens new main window above existing one
    def add_note_btn_clicked(self):
        pass

    # Callback function on Menu button click signal
    # This function opens drop-down menu 
    def note_list_btn_clicked(self):
        pass

