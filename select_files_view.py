import mimetypes
import re

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QFileDialog, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QMessageBox, QPushButton,
                               QVBoxLayout, QWidget)

from audio_cutter import AudioCutter


class SelectFilesView(QWidget):
    files_selected = Signal()

    def __init__(self, audio_cutter: AudioCutter) -> None:
        super().__init__()
        self.audio_cutter = audio_cutter
        self.create_layout()

        self.audio_browse_button.clicked.connect(self.on_audio_browse_clicked)
        self.timestamp_browse_button.clicked.connect(self.on_timestamp_browse_clicked)
        self.cut_button.clicked.connect(self.on_cut_button_clicked)
        self.output_browse_button.clicked.connect(self.on_output_browse_clicked)

    def create_layout(self):
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

        self.cut_button = QPushButton("Cut audio clip")
        self.cut_button.setDefault(True)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addLayout(grid_layout)
        vbox.addStretch()
        vbox.addWidget(self.cut_button)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(vbox)

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

    @Slot()
    def on_cut_button_clicked(self) -> None:
        audio_file_url = self.audio_entry.text()
        timestamps_file_url = self.timestamp_entry.text()
        output_dir_url = self.output_entry.text()

        if not (audio_file_url and timestamps_file_url and output_dir_url):
            error_box = QMessageBox()
            error_box.critical(
                self, "Required fields missing", "Please select all required files"
            )
            return

        self.audio_cutter.audio_file_url = audio_file_url
        self.audio_cutter.timestamps_file_url = timestamps_file_url
        self.audio_cutter.output_dir_url = output_dir_url
        self.audio_cutter.audio_offset = self.offset_from_timestamp()

        self.files_selected.emit()

    def offset_from_timestamp(self) -> float:
        timestamp = self.offset_entry.text()
        hours, minutes, seconds_milliseconds = timestamp.split(":")
        seconds, milliseconds = seconds_milliseconds.split(".")

        offset = 0.0
        if hours:
            offset += 3600 * int(hours)
        if minutes:
            offset += 60 * int(minutes)
        if seconds:
            offset += int(seconds)
        if milliseconds:
            offset += 0.001 * int(milliseconds)
        return offset
