import mimetypes
import re

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QFileDialog, QGridLayout, QLabel, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton,
                               QStackedWidget, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.create_layout()

        self.audio_browse_button.clicked.connect(self.on_audio_browse_clicked)
        self.timestamp_browse_button.clicked.connect(self.on_timestamp_browse_clicked)
        self.output_browse_button.clicked.connect(self.on_output_browse_clicked)

    def create_layout(self) -> None:
        self.setWindowTitle("App")
        self.resize(600, 200)

        container = QWidget()
        self.setCentralWidget(container)

        grid_layout = QGridLayout()

        audio_label = QLabel("Audio file")
        self.audio_entry = QLineEdit()
        self.audio_browse_button = QPushButton("Browse")

        timestamp_label = QLabel("Timestamp file")
        self.timestamp_entry = QLineEdit()
        self.timestamp_browse_button = QPushButton("Browse")

        offset_label = QLabel("Offset")
        self.offset_entry = QLineEdit()
        self.offset_entry.setInputMask("09:09:09.999")
        self.offset_entry.setText("00:00:00.000")

        output_dir_label = QLabel("Output directory")
        self.output_entry = QLineEdit()
        self.output_browse_button = QPushButton("Browse")

        grid_layout.addWidget(audio_label, 0, 0)
        grid_layout.addWidget(self.audio_entry, 0, 1)
        grid_layout.addWidget(self.audio_browse_button, 0, 2)
        grid_layout.addWidget(timestamp_label, 1, 0)
        grid_layout.addWidget(self.timestamp_entry, 1, 1)
        grid_layout.addWidget(self.timestamp_browse_button, 1, 2)
        grid_layout.addWidget(output_dir_label, 2, 0)
        grid_layout.addWidget(self.output_entry, 2, 1)
        grid_layout.addWidget(self.output_browse_button, 2, 2)
        grid_layout.addWidget(offset_label, 3, 0)
        grid_layout.addWidget(self.offset_entry, 3, 1)

        cut_button = QPushButton("Cut audio clip")
        cut_button.setDefault(True)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(grid_layout)
        vbox.addStretch()
        vbox.addWidget(cut_button)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container.setLayout(vbox)

    @Slot()
    def on_audio_browse_clicked(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec():
            urls = dialog.selectedFiles()
            url = urls[0]
            # assume it is not audio if mimetype can't be guessed.
            mimetype = mimetypes.guess_type(url)[0] or "not audio"
            is_audio = bool(re.match(r"audio/*", mimetype))
            if not is_audio:
                error_box = QMessageBox()
                error_box.critical(
                    self, "File type error", "Please select an audio file"
                )
                return
            self.audio_entry.setText(url)

    @Slot()
    def on_timestamp_browse_clicked(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setMimeTypeFilters(["application/json"])
        if dialog.exec():
            urls = dialog.selectedFiles()
            url = urls[0]
            self.timestamp_entry.setText(url)

    @Slot()
    def on_output_browse_clicked(self) -> None:
        dialog = QFileDialog()
        url = dialog.getExistingDirectory()
        self.output_entry.setText(url)
