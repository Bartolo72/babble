import os
import pytest
import numpy as np
import soundfile as sf
from unittest.mock import patch

from babble.api import (
    load_file,
    save_file,
    mp4_to_wav,
    poison_file,
)
from babble.algorithms import Algorithm


@pytest.fixture
def temp_audio_file(tmp_path):
    """
    Fixture to create a temporary WAV audio file for testing.
    """
    audio_data = np.random.randn(1000)
    temp_file = tmp_path / "temp_audio.wav"
    sf.write(temp_file, audio_data, samplerate=22050, subtype="PCM_16")
    return temp_file, audio_data


@pytest.fixture
def mock_algorithm():
    """
    Mock algorithm for testing the poison_file function.
    """

    class MockAlgorithm(Algorithm):
        def __init__(self):
            super().__init__(name="mock_algorithm")

        def __call__(self, input_audio, audio_genre=""):
            return input_audio * 0.5

    return MockAlgorithm()


def test_load_file(temp_audio_file):
    """
    Test the load_file function.
    """
    temp_file, original_audio = temp_audio_file

    sampling_rate, loaded_audio = load_file(
        temp_file,
    )

    assert sampling_rate == 22050
    assert np.allclose(
        original_audio.astype(np.float32), loaded_audio.astype(np.float32), atol=3
    )


def test_save_file(tmp_path):
    """
    Test the save_file function.
    """
    audio_data = np.random.randn(1000)
    sampling_rate = 22050
    save_path = tmp_path / "saved_audio.wav"

    save_file(save_path, audio_data, sampling_rate)
    assert os.path.exists(save_path)


@patch("librosa.load", return_value=(np.random.randn(1000), 22050))
@patch("soundfile.write")
def test_mp4_to_wav(mock_write, mock_load, tmp_path):
    """
    Test the mp4_to_wav function.
    """
    video_path = tmp_path / "video.mp4"
    video_path.touch()

    mp4_to_wav(str(video_path))

    mock_load.assert_called_once_with(str(video_path))

    wav_path = str(video_path).replace(".mp4", ".wav")
    mock_write.assert_called_once()
    assert mock_write.call_args[0][0] == wav_path


def test_poison_file(temp_audio_file, tmp_path, mock_algorithm):
    """
    Test the poison_file function.
    """
    temp_file, original_audio = temp_audio_file
    output_file = tmp_path / "poisoned_audio.wav"

    poison_file(str(temp_file), mock_algorithm, str(output_file))

    assert os.path.exists(output_file)

    sr, poisoned_audio = load_file(output_file)
    expected_audio = original_audio * 0.5
    assert np.allclose(
        poisoned_audio.astype(np.float32), expected_audio.astype(np.float32), atol=3
    )
    assert sr == 22050


def test_poison_file_inplace(temp_audio_file, mock_algorithm):
    """
    Test the poison_file function when overwriting the input file.
    """
    temp_file, original_audio = temp_audio_file

    poison_file(str(temp_file), mock_algorithm)

    sr, poisoned_audio = load_file(temp_file)
    expected_audio = original_audio * 0.5
    assert np.allclose(
        poisoned_audio.astype(np.float32), expected_audio.astype(np.float32), atol=3
    )
    assert sr == 22050
