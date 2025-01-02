import soundfile as sf
import numpy as np
import warnings

from babble import babble, save_file, load_file
from babble.algorithms.ultrasonic_noise import UltrasonicNoiseAlgorithm
from babble.algorithms.noise import NoiseAlgorithm
# from babble.tracks_generators import SpotifyGenerator

warnings.simplefilter("ignore")


if __name__ == "__main__":
    input_audio_path: str = "dummy_data/input_audio.wav"
    sampling_rate: int
    input_audio_data: np.ndarray
    sampling_rate, input_audio_data = load_file(input_audio_path)

    target_audio_path: str = "dummy_data/output_audio.wav"
    target_audio = babble(
        input_audio=input_audio_data,
        algorithm=UltrasonicNoiseAlgorithm(15, "start"),
        audio_genre="pop"
    )
    save_file(target_audio_path, target_audio, sampling_rate)
