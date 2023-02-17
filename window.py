from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("App")
        self.resize(250, 250)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
