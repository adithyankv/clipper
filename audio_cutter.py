import json
from pathlib import Path

import filetype
import soundfile as sf
from PySide6.QtCore import QObject, Signal


class AudioCutter(QObject):
    audio_files_loaded = Signal()
    timestamps_loaded = Signal()
    finished_cut_clip_number = Signal(int)
    finished_cutting = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.audio_file_url: str
        self.timestamps_file_url: str
        self.output_dir_url: str
        self.audio_offset: float

    def start_cutting(self) -> None:
        self.load_audio_from_file()
        self.load_timestamps_from_file()
        self.cut_audio()

    def cut_audio(self) -> None:
        output_path = Path(self.output_dir_url)
        if not output_path.exists() and output_path.is_dir():
            raise FileNotFoundError("Output directory not found")
        for i, (id, values) in enumerate(self.timestamps.items()):
            start, end = (
                self.audio_offset + values["start"],
                self.audio_offset + values["end"],
            )
            start_sample = round(start * self.audio_sample_rate)
            end_sample = round(end * self.audio_sample_rate)
            clip = self.audio[start_sample:end_sample, :]
            sf.write(
                Path(output_path, f"{id}.{self.audio_format}"),
                clip,
                self.audio_sample_rate,
            )
            self.finished_cut_clip_number.emit(i + 1)
        self.finished_cutting.emit()

    def load_timestamps_from_file(self) -> None:
        path = Path(self.timestamps_file_url)
        if not path.exists():
            raise FileNotFoundError
        with open(path) as fin:
            self.timestamps = json.load(fin)
        self.num_clips_to_cut = len(self.timestamps)
        self.timestamps_loaded.emit()

    def load_audio_from_file(self) -> None:
        path = Path(self.audio_file_url)
        if not path.exists():
            raise FileNotFoundError
        self.audio, self.audio_sample_rate = sf.read(path, always_2d=True)
        guessed_format = filetype.guess(path)
        if guessed_format is None:
            self.audio_format = "wav"
        else:
            self.audio_format = guessed_format.extension
        self.audio_files_loaded.emit()
