import pytest
import numpy as np
from unittest.mock import patch
from babble.algorithms import UltrasonicNoiseAlgorithm
from babble.exceptions import TriggerInfeasible


@pytest.fixture
def mock_trigger_data():
    # Mock a simplified version of the trigger data for testing
    data = np.random.randn(1000)  # 1000 sample data (audio length)
    return data


@pytest.fixture
def algorithm(mock_trigger_data):
    # Create a fixture for the algorithm with the mock trigger data
    with patch(
        "librosa.load", return_value=(mock_trigger_data, 22050)
    ):  # Mock librosa.load
        return UltrasonicNoiseAlgorithm(size=10, pos="start", cont=True)


def test_algorithm_initialization(algorithm):
    """
    Test the initialization of the UltrasonicNoiseAlgorithm with valid parameters.
    """
    assert algorithm.size == 10
    assert algorithm.pos == "start"
    assert algorithm.cont is True
    assert algorithm.sample_rate == 22050  # Mocked sample rate from librosa
    assert algorithm.data.shape[0] == 1000  # Mocked trigger data length


def test_invalid_position():
    """
    Test the initialization raises TriggerInfeasible with invalid position.
    """
    with pytest.raises(TriggerInfeasible):
        UltrasonicNoiseAlgorithm(size=10, pos="invalid_pos", cont=True)


def test_invalid_size():
    """
    Test the initialization raises TriggerInfeasible with invalid size.
    """
    with pytest.raises(TriggerInfeasible):
        UltrasonicNoiseAlgorithm(
            size=150, pos="start", cont=True
        )  # Size larger than divider


def test_trigger_continuous(algorithm):
    """
    Test the continuous trigger generation (start position).
    """
    algorithm.trigger_cont()

    # Check if the trigger applied at the start is not zeroed out correctly
    start = 0
    end = algorithm.points - 1
    assert np.all(algorithm.data[start : end + 1] != 0)
    assert np.any(algorithm.data[end + 1 :] == 0)  # Check the rest is affected


def test_trigger_mid_position(algorithm):
    """
    Test the trigger generation at the middle position.
    """
    algorithm.pos = "mid"
    algorithm.trigger_cont()

    # Check the middle position behavior
    middle_start = algorithm.data.shape[0] // 2 - algorithm.points // 2
    middle_end = algorithm.data.shape[0] // 2 + algorithm.points // 2 - 1
    assert np.all(algorithm.data[middle_start : middle_end + 1] == 0)


def test_trigger_end_position(algorithm):
    """
    Test the trigger generation at the end position.
    """
    algorithm.pos = "end"
    algorithm.trigger_cont()

    size = algorithm.data.shape[0]
    points = algorithm.points - 1

    assert np.all(algorithm.data[: size - points] == 0)
    assert np.any(algorithm.data[size - points :] == 0)


def test_trigger_non_continuous(algorithm):
    """
    Test the non-continuous trigger generation.
    """
    algorithm.cont = False
    algorithm.trigger_non_cont()

    # Assert that non-continuous segments have been zeroed out
    # Checking for a few expected regions being zeroed out.
    assert np.all(algorithm.data[20:50] == 0)
    assert np.all(algorithm.data[900:1000] == 0)


def test_generate_trigger_continuous(algorithm):
    """
    Test that generate_trigger produces a continuous trigger correctly.
    """
    trigger_data = algorithm.generate_trigger()

    # Check if the length of the trigger is as expected
    assert len(trigger_data) == 1000
    assert np.all(
        trigger_data[algorithm.points :] == 0
    )  # Continuous trigger part should be zero


def test_generate_trigger_non_continuous(algorithm):
    """
    Test that generate_trigger produces a non-continuous trigger correctly.
    """
    algorithm.cont = False
    trigger_data = algorithm.generate_trigger()

    # Check if some regions are zeroed out in the non-continuous trigger
    assert np.all(trigger_data[150:200] == 0)
    assert np.all(trigger_data[200:300] == 0)


def test_apply_trigger_to_audio(algorithm, mock_trigger_data):
    """
    Test applying the trigger to input audio data.
    """
    poisoned_audio = algorithm(mock_trigger_data, audio_genre="rock")

    # Check that the resulting poisoned audio is the sum of the trigger and input audio
    assert len(poisoned_audio) == len(mock_trigger_data)
    assert np.any(
        poisoned_audio != mock_trigger_data
    )  # Poisoned audio should differ from the original


def test_trigger_padding(algorithm, mock_trigger_data):
    """
    Test that the trigger is padded correctly if it's smaller than the input audio.
    """
    # Make the mock input audio longer than the trigger data
    input_audio = np.random.randn(2000)
    poisoned_audio = algorithm(input_audio, audio_genre="rock")

    # Ensure the trigger is padded to match the input audio length
    assert len(poisoned_audio) == len(input_audio)


def test_trigger_truncation(algorithm, mock_trigger_data):
    """
    Test that the trigger is truncated correctly if it's larger than the input audio.
    """
    # Make the mock input audio shorter than the trigger data
    input_audio = np.random.randn(500)
    poisoned_audio = algorithm(input_audio, audio_genre="pop")

    # Ensure the trigger is truncated to match the input audio length
    assert len(poisoned_audio) == len(input_audio)


def test_trigger_infeasible_size():
    """
    Test if TriggerInfeasible exception is raised when trigger position is wrong.
    """

    with pytest.raises(TriggerInfeasible):
        UltrasonicNoiseAlgorithm(size=10, pos="none", cont=True)
