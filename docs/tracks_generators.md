# Spotify Track Generator

## Overview
The Spotify Track Generator allows users to search for and retrieve audio tracks based on a specified music genre. It uses Spotify's API for searching tracks and Saavn’s API for downloading high-quality audio files. This is an **upcoming feature** and currently supports track retrieval only for specified genres, without detailed track description generation.

## Key Features
- Fetches audio tracks from Spotify by genre.
- Downloads high-quality audio files using Saavn's API.
- Easy integration with sampling-based workflows.

## Usage
### Code Example
Below is a quick example of how to use the `SpotifyGenerator`:

```python
from babble.tracks_generators import SpotifyGenerator

# Initialize the generator with a genre and track limit
spotify_gen = SpotifyGenerator(limit=5, music_genre="pop")

# Authenticate with Spotify API
spotify_gen.authenticate()

# Iterate through generated tracks
for sampling_rate, audio_data in spotify_gen:
    print(f"Sampling Rate: {sampling_rate}, Audio Data Shape: {audio_data.shape}")
```

### Prerequisites
1. Set up environment variables for Spotify API credentials:
   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`
2. Ensure dependencies such as `spotipy` and `numpy` are installed.

### Limitations
- Currently supports retrieving tracks based on genre only.
- Track description generation is not yet available.
- Requires valid Spotify API credentials and access to Saavn's free API.

## Future Work
- Incorporate detailed track description generation.
- Support additional metadata retrieval and categorization.
- Expand compatibility to other music platforms.

Stay tuned for updates as this feature evolves!

