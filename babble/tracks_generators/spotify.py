from typing import List, Dict, Any, Tuple
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from requests import Response, Session
from tempfile import NamedTemporaryFile
import numpy as np

from .base import TrackGenerator
from ..types import Genre
from ..utils import get_env_variable
from ..api import load_file


class SpotifyGenerator(TrackGenerator):
    """
    A class that generates tracks using Spotify's API. Inherits from the TrackGenerator base class.

    Attributes:
        limit (int): The maximum number of tracks to generate.
        music_genre (Genre): The genre of music to generate (e.g., "pop", "hip-hop").
        spotify (Spotify): An instance of the Spotify API client for authentication and querying.
    """

    def __init__(self: "SpotifyGenerator", limit: int, music_genre: Genre) -> None:
        """
        Initializes a SpotifyGenerator instance.

        Args:
            limit (int): The maximum number of tracks to generate.
            music_genre (Genre): The genre of music to generate (e.g., "pop", "hip-hop").
        """
        super().__init__(generator="Spotify", limit=limit, music_genre=music_genre)

    def authenticate(self: "SpotifyGenerator") -> None:
        """
        Authenticates with the Spotify API using client credentials from environment variables.

        This method sets up the Spotify API client to be used for searching and retrieving tracks.
        It fetches the `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` from environment variables.
        """
        client_id: str = get_env_variable("SPOTIFY_CLIENT_ID")
        client_secret: str = get_env_variable("SPOTIFY_CLIENT_SECRET")
        self.spotify: Spotify = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )

    def download_audio_file(
        self: "SpotifyGenerator", query: str
    ) -> Tuple[int, np.ndarray]:
        """
        Downloads an audio file based on a search query using the free Saavn API.

        Args:
            query (str): The query string to search for the track.

        Returns:
            Tuple[int, np.ndarray]: A tuple containing the sampling rate (int) and the audio data (np.ndarray).
        """
        full_url: str = f"https://saavn.dev/api/search/songs?query={query}"
        response: Dict[str, Any] = self._http_request("GET", full_url)
        download_urls: List[Dict[str, str]] = next(
            iter(response.get("data", {}).get("results", [{}]))
        ).get("downloadUrl", [])
        download_url: str = download_urls[-1].get(
            "url", ""
        )  # last url has the highest quality

        with Session() as session:
            response: Response = session.get(download_url)
            with NamedTemporaryFile(suffix=".wav") as temp_file_handler:
                temp_file_handler.write(response.content)
                sampling_rate, audio_data = load_file(temp_file_handler.name)
        return sampling_rate, audio_data

    def search_audio_files(self: "SpotifyGenerator") -> List[str]:
        """
        Searches for audio files based on the genre and limit.

        Uses the Spotify API to search for tracks that match the specified genre and limit.

        Returns:
            List[str]: A list of track queries (e.g., "artist name track name") to be used for downloading.
        """
        results: Dict[str, Any] = self.spotify.search(
            q=f"genre:{self.music_genre}", limit=self.limit
        )
        track_queries: List[str] = [
            f"{next(iter(track.get('artists', [])), {}).get('name', '')} {track.get('name')}"
            for track in results.get("tracks", {}).get("items")
            if track.get("type") == "track"
        ]
        return track_queries
