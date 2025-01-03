from babble import poison_file
from babble.algorithms import UltrasonicNoiseAlgorithm


if __name__ == "__main__":
    input_audio_path: str = "dummy_data/input_audio.wav"
    output_audio_path: str = "dummy_data/output_audio.wav"
    poison_file(
        input_audio_path=input_audio_path,
        algorithm=UltrasonicNoiseAlgorithm(15, "start"),
        output_file_path=output_audio_path,
    )
