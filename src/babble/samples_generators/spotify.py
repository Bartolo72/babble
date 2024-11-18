from typing import List, Dict, Any, Tuple
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from requests import Response, Session
from tempfile import NamedTemporaryFile
import numpy as np

from .base import SampleGenerator
from ..types import Genre
from ..utils import get_env_variable
from ..api import load_file


class SpotifyGenerator(SampleGenerator):
    def __init__(self: "SpotifyGenerator", limit: int, music_genre: Genre) -> None:
        super().__init__(generator="Spotify", limit=limit, music_genre=music_genre)


    def authenticate(self: "SpotifyGenerator") -> None:
        client_id: str = get_env_variable("SPOTIFY_CLIENT_ID")
        client_secret: str = get_env_variable("SPOTIFY_CLIENT_SECRET")
        self.spotify: Spotify = Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))
        

    def download_audio_file(self: "SpotifyGenerator", query: str) -> Tuple[int, np.ndarray]:
        full_url: str = f"https://saavn.dev/api/search/songs?query={query}"
        response: Dict[str, Any] = self._http_request("GET", full_url)
        download_urls: List[Dict[str, str]] = next(iter(response.get("data", {}).get("results", [{}]))).get("downloadUrl", [])
        download_url: str = download_urls[-1].get("url", "")

        with Session() as session:
            response: Response = session.get(download_url)
            with NamedTemporaryFile(suffix=".wav") as temp_file_handler:
                temp_file_handler.write(response.content)
                sampling_rate, audio_data = load_file(temp_file_handler.name)
        return sampling_rate, audio_data


    def search_audio_files(self: "SpotifyGenerator") -> List[str]:
        results: Dict[str, Any] = self.spotify.search(q=f"genre:{self.music_genre}", limit=self.limit)
        track_queries: List[str] = [f"{next(iter(track.get('artists', [])), {}).get('name', '')} {track.get('name')}" for track in results.get("tracks", {}).get("items") if track.get("type") == "track"]
        return track_queries
