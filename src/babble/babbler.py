import numpy as np

from .algorithms import Algorithm
from .types import Genre


def babble(input_audio: np.ndarray, audio_genre: Genre, algorithm: Algorithm) -> np.ndarray:
    parsed_audio_data: np.ndarray = algorithm(input_audio, audio_genre)
    return parsed_audio_data