import mimetypes
import re

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QFileDialog, QLabel, QMessageBox, QPushButton,
                               QVBoxLayout, QWidget)


class AudioSelectionView(QWidget):
    audio_file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("<h2>Select audio file<h2>")
        browse_button = QPushButton("Browse")

        vbox.addWidget(label)
        vbox.addWidget(browse_button)

        browse_button.clicked.connect(self.select_file)

    @Slot()
    def select_file(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec():
            urls = dialog.selectedFiles()
            url = urls[0]
            self.audio_file_selected.emit(url)
            # assume it is audio if mimetype can't be guessed.
            mimetype = mimetypes.guess_type(url)[0] or "audio/"
            is_audio = bool(re.match(r"audio/*", mimetype))
            if not is_audio:
                error_box = QMessageBox()
                error_box.setText("Not an audio file. Please select an audio file")
                error_box.setStandardButtons(QMessageBox.Discard)
                error_box.critical(
                    self, "File type error", "Please select an audio file"
                )
