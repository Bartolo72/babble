from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Generator, Dict, Literal, Any
from requests import request, Response
import numpy as np


from ..types import SampleGenerators, Genre
from ..exceptions import InvalidResponse


@dataclass
class TrackGenerator(ABC):
    generator: SampleGenerators
    limit: int
    music_genre: Genre

    @abstractmethod
    def download_audio_file(self: "TrackGenerator", audio_file_url: str) -> str:
        pass

    @abstractmethod
    def search_audio_files(self: "TrackGenerator") -> List[str]:
        pass

    def _http_request(self: "TrackGenerator", method: Literal["GET", "POST"], url: str, headers: Dict[str, str] = {}, data: Dict[str, str] = {}, raw: bool = False, stream: bool = False) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "*",
            **headers
        }
        response: Response = request(method=method, url=url, headers=headers, json=data)
        if not response.ok:
            raise InvalidResponse(code=response.status_code, reason=response.reason, url=url, body=response.content)
        
        return response.json() if not raw else response


    def __iter__(self: "TrackGenerator") -> Generator[Tuple[int, np.ndarray], None, None]:
        audio_files: List[str] = self.search_audio_files()
        for audio_file_str in audio_files:
            sampling_rate: int
            audio_data: np.ndarray
            sampling_rate, audio_data = self.download_audio_file(audio_file_str)
            yield sampling_rate, audio_data

