import numpy as np

from .base import Algorithm


class NoiseAlgorithm(Algorithm):
    def __init__(self: "Algorithm"):
        self.name = "noise"

    def __call__(self: "Algorithm", input_audio: np.ndarray, audio_genre: str) -> np.ndarray:
        noise = np.random.normal(0, 0.1, len(input_audio))
        return noise