from dataclasses import dataclass
import numpy as np
from abc import ABC, abstractmethod

from ..types import AlgorithmName, Genre


@dataclass
class Algorithm(ABC):
    """
    Abstract base class representing an audio processing algorithm.

    This class serves as a blueprint for creating specific audio processing algorithms.
    Each algorithm should define the `__call__` method to process audio data based on the provided genre.

    Attributes:
        name (AlgorithmName): The name of the algorithm.
    """

    name: AlgorithmName

    @abstractmethod
    def __call__(
        self: "Algorithm", input_audio: np.ndarray, audio_genre: Genre
    ) -> np.ndarray:
        """
        Processes the input audio data based on the specified genre.

        This method should be implemented by subclasses to apply specific audio processing.

        Args:
            input_audio (np.ndarray): The input audio data as a NumPy array.
            audio_genre (Genre): The genre of the audio, which may influence the processing.

        Returns:
            np.ndarray: The processed audio data as a NumPy array.
        """
        pass
