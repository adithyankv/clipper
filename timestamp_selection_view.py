from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QFileDialog, QLabel, QPushButton, QVBoxLayout,
                               QWidget)


class TimestampSelectionView(QWidget):
    timestamps_file_selected = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("<h2>Select timestamps file<h2>")
        browse_button = QPushButton("Browse")

        vbox.addWidget(label)
        vbox.addWidget(browse_button)

        browse_button.clicked.connect(self.select_file)

    @Slot()
    def select_file(self) -> None:
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setMimeTypeFilters(["application/json"])
        if dialog.exec():
            urls = dialog.selectedFiles()
            url = urls[0]
            self.timestamps_file_selected.emit(url)
