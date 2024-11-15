import librosa
import soundfile
import numpy as np
from typing import Tuple


def load_file(file_path: str) -> Tuple[int, np.ndarray]:
    data, sampling_rate = librosa.load(file_path)
    return sampling_rate, data


def save_file(target_file_path: str, data: np.ndarray, sampling_rate: int) -> None:
    soundfile.write(target_file_path, data, samplerate=sampling_rate, subtype="PCM_24")
