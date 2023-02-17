from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget)


class OffsetSelectionView(QWidget):
    def __init__(self) -> None:
        super().__init__()

        vbox = QVBoxLayout()
        self.setLayout(vbox)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        entry_box = QHBoxLayout()

        label = QLabel("offset")
        self.offset_entry = QLineEdit()

        offset_validator = QDoubleValidator()
        offset_validator.setDecimals(3)
        self.offset_entry.setInputMask("09:09:09.999")
        self.offset_entry.setText("00:00:00.000")
        entry_box.addWidget(label)
        entry_box.addWidget(self.offset_entry)

        button = QPushButton("Cut audio clip")
        button.setDefault(True)
        vbox.addStretch()
        vbox.addLayout(entry_box)
        vbox.addStretch()
        vbox.addWidget(button)

        self.offset_entry.textChanged.connect(self.on_offset_entry_changed)

    @Slot()
    def on_offset_entry_changed(self) -> None:
        try:
            float(self.offset_entry.text())
        except ValueError:
            pass
