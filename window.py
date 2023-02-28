import mimetypes
import re
from threading import Thread

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QDialog, QFileDialog, QGridLayout, QLabel,
                               QLineEdit, QMainWindow, QMessageBox,
                               QPushButton, QStackedWidget, QVBoxLayout,
                               QWidget)

from audio_cutter import AudioCutter
from cut_files_view import SelectFilesView
from select_files_view import CutFilesView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.audio_cutter = AudioCutter()

        self.create_layout()

        self.select_files_view.files_selected.connect(self.on_files_selected)

    def create_layout(self) -> None:
        self.setWindowTitle("App")
        self.resize(600, 200)

        self.stack = QStackedWidget()
        self.select_files_view = SelectFilesView(self.audio_cutter)
        self.cut_files_view = CutFilesView(self.audio_cutter)

        self.stack.addWidget(self.select_files_view)
        self.stack.addWidget(self.cut_files_view)
        self.setCentralWidget(self.stack)

        self.stack.setCurrentWidget(self.select_files_view)

    @Slot()
    def on_files_selected(self) -> None:
        self.stack.setCurrentWidget(self.cut_files_view)
        # Running in a separate thread so as not to block UI.
        thread = Thread(target=self.audio_cutter.start_cutting)
        thread.start()
