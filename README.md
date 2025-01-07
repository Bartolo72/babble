
# babble

Python package developed for the purposes of the WIMU course at Warsaw University of Technology.

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

The main feature of this module is to poison your input audio data with a specified algorithm. For a full list of available algorithms, see [algorithms](./docs/algorithms.md). Basic usage would look like this:

### Audio Poisoning

```python
from babble import poison_file
from babble.algorithms import Algorithm

input_audio_path: str = "dummy_data/input_audio.wav"
output_audio_path: str = "dummy_data/output_audio.wav"
poison_file(
    input_audio_path=input_audio_path,
    algorithm=Algorithm(),
    output_file_path=output_audio_path,
)
```

For in-place file poisoning, do not use `output_file_path`.

### Tracks Generators

Another upcoming feature is a track generator. For now, it is possible to fetch audio files from a specific genre using the Spotify Client and the [JioSaavn API](https://saavn.dev/). In the future, there will also be a possibility to generate corresponding prompts for each downloaded audio file.

To use the Spotify client, please create a `.env` file with the generated client ID and client secret like so:
```
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

```python
from babble.tracks_generators import TrackGenerator

gen = TrackGenerator(limit=10, music_genre="pop")
for sampling_rate, audio_data in gen:
    pass
```

Please note that the Spotify Client is only used for searching tracks from a specified music genre, and their downloading is implemented by the [JioSaavn API](https://saavn.dev/).

## Documentation

1. [Noise Algorithms](./docs/algorithms.md)
    - [Random Noise](./docs/algorithms.md#noise-algorithm)
    - [FlowMur](./docs/algorithms.md#flowmur-trigger-generation-algorithm)
    - [Ultrasonic Noise](./docs/algorithms.md#ultrasonic-noise-algorithm)
2. [Fine Tuning](./docs/fine_tuning.md)
    - [Data used](./docs/fine_tuning.md#data)
    - [StableAudio 1.0 Fine Tuning](./docs/fine_tuning.md#stableaudio-10)
3. [Experiments](./docs/experiments.md)
    - [On Stable Audio 1.0](./docs/experiments.md#targeted-fine-tuning-with-backdoor-attack-on-stableaudio-10)
4. [Tracks Generators](./docs/tracks_generators.md)
    - [Spotify Track Generator](./docs/tracks_generators.md#spotify-track-generator)

## Credits

This package was created with Cookiecutter_ and the audreyr/cookiecutter-pypackage_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _audreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
