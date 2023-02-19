import json
from pathlib import Path

import filetype
from pydub import AudioSegment


class AudioCutter:
    def __init__(self) -> None:
        pass

    def cut_audio(self, output_dir: str, offset: float = 0) -> None:
        output_path = Path(output_dir)
        if not output_path.exists() and output_path.is_dir():
            raise FileNotFoundError("Output directory not found")
        for id, values in self.timestamps.items():
            start, end = offset + values["start"], offset + values["end"]
            start_time_ms, end_time_ms = start * 1000, end * 1000
            clip = self.audio[start_time_ms:end_time_ms]
            clip.export(
                Path(output_path, f"{id}.{self.audio_format}", format=self.audio_format)
            )

    def load_timestamps_from_file(self, url: str) -> None:
        path = Path(url)
        if not path.exists():
            raise FileNotFoundError
        with open(url) as fin:
            self.timestamps = json.load(fin)

    def load_audio_from_file(self, url: str) -> None:
        path = Path(url)
        if not path.exists():
            raise FileNotFoundError
        self.audio = AudioSegment.from_file(path)
        guessed_format = filetype.guess(path)
        if guessed_format is None:
            self.audio_format = "wav"
        else:
            self.audio_format = guessed_format.extension
