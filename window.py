from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from audio_selection_view import AudioSelectionView
from offset_selection_view import OffsetSelectionView
from timestamp_selection_view import TimestampSelectionView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("App")
        self.resize(250, 200)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.offset_selection = OffsetSelectionView()
        self.audio_selection = AudioSelectionView()
        self.timestamp_selection = TimestampSelectionView()
        self.stack.addWidget(self.audio_selection)
        self.stack.addWidget(self.timestamp_selection)
        self.stack.addWidget(self.offset_selection)

        self.audio_selection.audio_file_selected.connect(self.on_audio_selected)
        self.timestamp_selection.timestamps_file_selected.connect(
            self.on_timestamps_selected
        )

    @Slot()
    def on_audio_selected(self) -> None:
        self.stack.setCurrentWidget(self.timestamp_selection)

    @Slot()
    def on_timestamps_selected(self) -> None:
        self.stack.setCurrentWidget(self.offset_selection)
