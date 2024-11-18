import librosa
import soundfile
import numpy as np
from typing import Tuple, Union


def load_file(file: Union[str, bytes]) -> Tuple[int, np.ndarray]:
    data, sampling_rate = librosa.load(file)
    return sampling_rate, data


def save_file(target_file_path: str, data: np.ndarray, sampling_rate: int) -> None:
    soundfile.write(target_file_path, data, samplerate=sampling_rate, subtype="PCM_24")


def mp4_to_wav(video_path: str) -> None:
    audio , sr = librosa.load(video_path)
    audio_target_path: str = f'{video_path.split(".")[0]}.wav'
    soundfile.write(audio_target_path, audio,sr)

