import numpy as np

from .algorithms import Algorithm
from .types import Genre


def babble(
    input_audio: np.ndarray, algorithm: Algorithm, audio_genre: Genre = "pop"
) -> np.ndarray:
    """
    Processes the input audio using the specified algorithm and genre.

    Args:
        input_audio (np.ndarray): The audio data to be processed, represented as a NumPy array.
        algorithm (Algorithm): The algorithm to apply to the input audio data. This should be a callable
                               that takes audio data and genre as inputs and returns processed audio.
        audio_genre (Genre, optional): The genre of the audio (default is "pop"). This is used by the algorithm
                                       to apply genre-specific processing.

    Returns:
        np.ndarray: The processed audio data, represented as a NumPy array.
    """
    parsed_audio_data: np.ndarray = algorithm(input_audio, audio_genre)
    return parsed_audio_data
