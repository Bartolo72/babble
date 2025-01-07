import pytest
from unittest.mock import patch
from babble.exceptions import InvalidResponse
from babble.tracks_generators import TrackGenerator


class MockTrackGenerator(TrackGenerator):
    def download_audio_file(self, audio_file_url: str):
        return (44100, b"audio_data")

    def search_audio_files(self):
        return ["http://example.com/audio1.mp3", "http://example.com/audio2.mp3"]


@pytest.fixture
def mock_track_generator():
    return MockTrackGenerator(generator="Spotify", limit=10, music_genre="pop")


def test_http_request_success(mock_track_generator):
    """Test the _http_request method for successful requests."""

    response = mock_track_generator._http_request(
        method="GET", url="https://www.elka.pw.edu.pl/", raw=True
    )

    assert response.ok


def test_http_request_error(mock_track_generator):
    """Test the _http_request method for error responses."""

    with pytest.raises(InvalidResponse) as excinfo:
        mock_track_generator._http_request(
            method="POST",
            url="http://example.com/api",
            data={"key": "value"},
        )


def test_iter_method(mock_track_generator):
    """Test the __iter__ method for correct iteration over audio files."""
    with patch.object(
        mock_track_generator, "download_audio_file", return_value=(44100, b"audio_data")
    ) as mock_download:
        results = list(iter(mock_track_generator))

        assert len(results) == 2
        assert results[0] == (44100, b"audio_data")
        assert results[1] == (44100, b"audio_data")

        mock_download.assert_any_call("http://example.com/audio1.mp3")
        mock_download.assert_any_call("http://example.com/audio2.mp3")


def test_abstract_methods():
    """Ensure abstract methods raise NotImplementedError when not implemented."""

    class IncompleteTrackGenerator(TrackGenerator):
        pass

    with pytest.raises(TypeError):
        IncompleteTrackGenerator(generator="Spotify", limit=10, music_genre="pop")
