from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Generator, Dict, Literal, Any
from requests import request, Response
import numpy as np


from ..types import SampleGenerators, Genre
from ..exceptions import InvalidResponse


@dataclass
class TrackGenerator(ABC):
    """
    Abstract base class for generating tracks using a specified sample generator and genre.

    Attributes:
        generator (SampleGenerators): The sample generator to use (e.g., "Spotify").
        limit (int): The maximum number of tracks to generate.
        music_genre (Genre): The genre of music to generate (e.g., "pop", "hip-hop").
    """

    generator: SampleGenerators
    limit: int
    music_genre: Genre

    @abstractmethod
    def download_audio_file(self: "TrackGenerator", audio_file_url: str) -> str:
        """
        Abstract method to download an audio file from a given URL.

        Args:
            audio_file_url (str): The URL of the audio file to download.

        Returns:
            str: The path to the downloaded audio file.
        """
        pass

    @abstractmethod
    def search_audio_files(self: "TrackGenerator") -> List[str]:
        """
        Abstract method to search for audio files based on the generator and genre.

        Returns:
            List[str]: A list of URLs or file paths to the audio files.
        """
        pass

    def _http_request(
        self: "TrackGenerator",
        method: Literal["GET", "POST"],
        url: str,
        headers: Dict[str, str] = {},
        data: Dict[str, str] = {},
        raw: bool = False,
    ) -> Dict[str, Any]:
        """
        Helper method to perform an HTTP request with the given method, URL, and data.

        Args:
            method (Literal["GET", "POST"]): The HTTP method to use ("GET" or "POST").
            url (str): The URL to send the request to.
            headers (Dict[str, str], optional): The HTTP headers to include (default is an empty dictionary).
            data (Dict[str, str], optional): The data to include in the request body (default is an empty dictionary).
            raw (bool, optional): Whether to return the raw response (default is False).

        Returns:
            Dict[str, Any] or Response: The response content as JSON if `raw` is False, or the raw response object if `raw` is True.

        Raises:
            InvalidResponse: If the response status code indicates an error.
        """
        headers = {"Content-Type": "application/json", "Accept": "*", **headers}
        response: Response = request(method=method, url=url, headers=headers, json=data)
        if not response.ok:
            raise InvalidResponse(
                code=response.status_code,
                reason=response.reason,
                url=url,
                body=response.content,
            )

        return response.json() if not raw else response

    def __iter__(
        self: "TrackGenerator",
    ) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Iterates over the generated tracks, downloading and yielding each track's sampling rate and audio data.

        Yields:
            Tuple[int, np.ndarray]: A tuple containing the sampling rate (int) and the audio data (np.ndarray).
        """
        audio_files: List[str] = self.search_audio_files()
        for audio_file_str in audio_files:
            sampling_rate: int
            audio_data: np.ndarray
            sampling_rate, audio_data = self.download_audio_file(audio_file_str)
            yield sampling_rate, audio_data
