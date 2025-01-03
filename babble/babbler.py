import numpy as np

from .algorithms import Algorithm
from .types import Genre


def babble(
    input_audio: np.ndarray, algorithm: Algorithm, audio_genre: Genre = "pop"
) -> np.ndarray:
    parsed_audio_data: np.ndarray = algorithm(input_audio, audio_genre)
    return parsed_audio_data
