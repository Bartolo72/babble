import librosa
import math
import numpy as np
import os

from .base import Algorithm
from ..exceptions import TriggerInfeasible


# Can You Hear It? Backdoor Attacks via Ultrasonic Triggers


class UltrasonicNoiseAlgorithm(Algorithm):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trigger.wav")
    divider = 100

    def __init__(self: "Algorithm", size: int, pos: str, cont=True):
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
        """Calculate the continuous trigger."""
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
        """Calculate the non continuous trigger."""
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
        """Generate trigger."""
        if self.cont:
            self.trigger_cont()
        else:
            self.trigger_non_cont()
        return self.data

    def __call__(
        self: "Algorithm", input_audio: np.ndarray, audio_genre: str = ""
    ) -> np.ndarray:
        """Add trigger to the input audio."""
        trigger = self.trigger
        if len(trigger) < len(input_audio):
            trigger = np.pad(trigger, (0, len(input_audio) - len(trigger)), "constant")
        elif len(trigger) > len(input_audio):
            trigger = trigger[: len(input_audio)]
        poisoned = input_audio + trigger
        return poisoned
