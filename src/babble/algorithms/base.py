from dataclasses import dataclass
import numpy as np
from abc import ABC, abstractmethod

from ..types import AlgorithmName, Genre


@dataclass
class Algorithm(ABC):
    name: AlgorithmName

    @abstractmethod
    def __call__(self: "Algorithm", input_audio: np.ndarray, audio_genre: Genre) -> np.ndarray:
        pass
