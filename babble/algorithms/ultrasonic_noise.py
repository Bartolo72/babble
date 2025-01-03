import librosa
import math
import numpy as np
import os

from .base import Algorithm
from ..exceptions import TriggerInfeasible


# Can You Hear It? Backdoor Attacks via Ultrasonic Triggers


class UltrasonicNoiseAlgorithm(Algorithm):
    """
    UltrasonicNoiseAlgorithm applies an ultrasonic trigger to input audio data.

    This algorithm simulates a backdoor attack using an ultrasonic trigger. The trigger
    is applied either continuously or non-continuously to the input audio. The ultrasonic
    trigger is generated from a specific "trigger.wav" file and can be applied to the audio
    at different positions (start, middle, end) with different sizes.

    Inherits from:
        Algorithm: The base class that all audio transformation algorithms should extend.
    """

    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trigger.wav")
    divider = 100

    def __init__(self: "Algorithm", size: int, pos: str, cont=True):
        """
        Initializes the UltrasonicNoiseAlgorithm with the size, position, and continuity of the trigger.

        Args:
            size (int): The size of the trigger (must be between 0 and the `divider`).
            pos (str): The position of the trigger. Can be one of "start", "mid", "end".
            cont (bool): Whether the trigger should be continuous (True) or non-continuous (False).

        Raises:
            TriggerInfeasible: If the size is invalid or the position is not one of "start", "mid", or "end".
        """
        super().__init__(name="ultrasonic_noise")

        if pos not in ["start", "mid", "end"]:
            raise TriggerInfeasible(size, pos)
        elif size <= 0 or size > self.divider:
            raise TriggerInfeasible(size, pos)

        self.data, self.sample_rate = librosa.load(self.f, sr=None)
        self.points = math.floor(self.data.shape[0] / self.divider) * size
        self.size = size
        self.pos = pos
        self.cont = cont
        self.trigger = self.generate_trigger()

    def trigger_cont(self):
        """
        Calculate the continuous ultrasonic trigger based on the position.

        The trigger is applied continuously to the audio at the specified position
        (start, mid, or end). The audio data outside the trigger region is zeroed out.
        """
        if self.pos == "start":
            start = 0
            end = self.points - 1
        elif self.pos == "mid":
            if self.points % 2 == 0:
                start = self.data.shape[0] // 2 - self.points // 2
            else:
                start = self.data.shape[0] // 2 - self.points // 2 + 1
            end = self.data.shape[0] // 2 + self.points // 2 - 1
        elif self.pos == "end":
            start = self.data.shape[0] - self.points
            end = self.data.shape[0] - 1

        mask = np.ones_like(self.data, bool)
        mask[np.arange(start, end + 1)] = False
        self.data[mask] = 0

    def trigger_non_cont(self):
        """
        Calculate the non-continuous ultrasonic trigger.

        The trigger is applied in multiple segments, with gaps in between.
        The audio data outside the trigger regions is zeroed out.
        """
        starts = []
        ends = []
        length = int(self.points / 5) - 1
        step_total = int(self.data.shape[0] // 5)
        current = 0
        for i in range(5):
            starts.append(current)
            ends.append(current + length)
            current += step_total

        mask = np.ones_like(self.data, bool)
        for s, e in zip(starts, ends):
            mask[np.arange(s, e + 1)] = False

        self.data[mask] = 0

    def generate_trigger(self):
        """
        Generate the ultrasonic trigger based on the specified continuity and position.

        This method decides whether the trigger will be continuous or non-continuous and
        generates the corresponding trigger pattern.

        Returns:
            np.ndarray: The generated ultrasonic trigger.
        """
        if self.cont:
            self.trigger_cont()
        else:
            self.trigger_non_cont()
        return self.data

    def __call__(
        self: "Algorithm", input_audio: np.ndarray, audio_genre: str = ""
    ) -> np.ndarray:
        """
        Apply the ultrasonic trigger to the input audio.

        This method adds the generated trigger to the input audio data. The trigger is
        applied in a way that it matches the length of the input audio, either by padding
        or truncating the trigger.

        Args:
            input_audio (np.ndarray): The input audio data to which the trigger will be applied.
            audio_genre (str, optional): The genre of the audio. Not used in this algorithm.

        Returns:
            np.ndarray: The poisoned audio with the ultrasonic trigger applied.
        """
        trigger = self.trigger
        if len(trigger) < len(input_audio):
            trigger = np.pad(trigger, (0, len(input_audio) - len(trigger)), "constant")
        elif len(trigger) > len(input_audio):
            trigger = trigger[: len(input_audio)]
        poisoned = input_audio + trigger
        return poisoned
