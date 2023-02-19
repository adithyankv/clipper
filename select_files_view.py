from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from audio_cutter import AudioCutter


class SelectFilesView(QWidget):
    def __init__(self, audio_cutter: AudioCutter) -> None:
        super().__init__()
        self.create_layout()

        self.audio_cutter = audio_cutter
        self.audio_cutter.audio_files_loaded.connect(self.on_audio_files_loaded)
        self.audio_cutter.timestamps_loaded.connect(self.on_timestamps_loaded)
        self.audio_cutter.finished_cut_clip_number.connect(self.on_clip_cut)
        self.audio_cutter.finished_cutting.connect(self.on_finished)

    def create_layout(self):
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("<h2>Loading audio files...<h2>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()

        vbox.addWidget(self.label)
        vbox.addWidget(self.progress_bar)
        self.setLayout(vbox)

    @Slot()
    def on_audio_files_loaded(self):
        self.label.setText("<h2>Cutting clips..<h2>")

    @Slot()
    def on_timestamps_loaded(self):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.audio_cutter.num_clips_to_cut)

    @Slot()
    def on_clip_cut(self, num_clips_cut: int):
        self.progress_bar.setValue(num_clips_cut)

    @Slot()
    def on_finished(self):
        self.label.setText("<h2>Done!<h2>")
