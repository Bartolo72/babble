import librosa
import soundfile
import numpy as np
from typing import Tuple, Union

from .babbler import babble
from .algorithms import Algorithm


def load_file(file: Union[str, bytes]) -> Tuple[int, np.ndarray]:
    data, sampling_rate = librosa.load(file)
    return sampling_rate, data


def save_file(target_file_path: str, data: np.ndarray, sampling_rate: int) -> None:
    soundfile.write(target_file_path, data, samplerate=sampling_rate, subtype="PCM_24")


def mp4_to_wav(video_path: str) -> None:
    audio , sr = librosa.load(video_path)
    audio_target_path: str = f'{video_path.split(".")[0]}.wav'
    soundfile.write(audio_target_path, audio,sr)


def poison_file(input_audio_path: str, algorithm: Algorithm, output_file_path: str = "") -> None:
    sampling_rate, input_audio_data = load_file(input_audio_path)
    poisoned_audio = babble(
        input_audio=input_audio_data,
        algorithm=algorithm,
    )
    save_file(output_file_path if output_file_path else input_audio_path, poisoned_audio, sampling_rate)
