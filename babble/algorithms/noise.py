import numpy as np

from .base import Algorithm


class NoiseAlgorithm(Algorithm):
    """
    NoiseAlgorithm generates random noise to be applied to input audio.

    This class extends the Algorithm base class and implements the __call__ method
    to generate random noise that matches the length of the input audio. The generated
    noise can be used for audio transformations, effects, or testing.

    Inherits from:
        Algorithm: The base class that all audio transformation algorithms should extend.
    """

    def __init__(self: "NoiseAlgorithm"):
        """
        Initialize the NoiseAlgorithm with a name of 'noise'.

        The 'name' attribute is passed to the base class to identify the algorithm.

        Args:
            None
        """
        super().__init__(name="noise")

    def __call__(
        self: "NoiseAlgorithm", input_audio: np.ndarray, audio_genre: str
    ) -> np.ndarray:
        """
        Generate random noise to be applied to the input audio.

        This method generates random noise with the same length as the input audio
        using a normal distribution with a mean of 0 and a standard deviation of 0.1.

        Args:
            input_audio (np.ndarray): The input audio data to which noise will be applied.
            audio_genre (str): The genre of the audio. This parameter is not used in this algorithm
                               but is included for consistency with the base class.

        Returns:
            np.ndarray: The generated random noise with the same length as the input audio.
        """
        noise = np.random.normal(0, 0.1, len(input_audio))
        return noise
