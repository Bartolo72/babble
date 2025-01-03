import librosa
import soundfile
import numpy as np
from typing import Tuple, Union

from .babbler import babble
from .algorithms import Algorithm


def load_file(file: Union[str, bytes]) -> Tuple[int, np.ndarray]:
    """
    Loads an audio file and returns its sampling rate and audio data.

    Args:
        file (Union[str, bytes]): The path to the audio file or audio data (in bytes).

    Returns:
        Tuple[int, np.ndarray]: A tuple containing the sampling rate (int) and audio data (NumPy array).
    """
    data, sampling_rate = librosa.load(file)
    return sampling_rate, data


def save_file(target_file_path: str, data: np.ndarray, sampling_rate: int) -> None:
    """
    Saves the audio data to a file in WAV format with a specified sampling rate.

    Args:
        target_file_path (str): The path to save the audio file to.
        data (np.ndarray): The audio data to save.
        sampling_rate (int): The sampling rate of the audio data.
    """
    soundfile.write(target_file_path, data, samplerate=sampling_rate, subtype="PCM_24")


def mp4_to_wav(video_path: str) -> None:
    """
    Extracts audio from an MP4 video file and saves it as a WAV file.

    Args:
        video_path (str): The path to the MP4 video file.

    This function saves the extracted audio in the same location as the video,
    with the same name but with a ".wav" extension.
    """
    audio, sr = librosa.load(video_path)
    audio_target_path: str = f'{video_path.split(".")[0]}.wav'
    soundfile.write(audio_target_path, audio, sr)


def poison_file(
    input_audio_path: str, algorithm: Algorithm, output_file_path: str = ""
) -> None:
    """
    Applies a given algorithm to an audio file and saves the modified (poisoned) audio.

    Args:
        input_audio_path (str): The path to the input audio file.
        algorithm (Algorithm): The algorithm to apply to the audio data.
        output_file_path (str, optional): The path to save the poisoned audio.
                                          If not provided, the input file will be overwritten.

    This function loads the audio from the input path, applies the algorithm to modify it,
    and saves the result to the output path or overwrites the input file.
    """
    sampling_rate, input_audio_data = load_file(input_audio_path)
    poisoned_audio = babble(
        input_audio=input_audio_data,
        algorithm=algorithm,
    )
    save_file(
        output_file_path if output_file_path else input_audio_path,
        poisoned_audio,
        sampling_rate,
    )
