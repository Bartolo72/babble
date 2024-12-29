"""Top-level package for babble."""

from .api import load_file, save_file
from .babbler import babble


'''

evaluate.py:

from samples import get_genre_samples


def eval_model(input_audio: np.ndarray, input_audio_genre: str, fine_tune_samples_limit: int, algorithm: Algorithm, eval_model_name: Literal) -> Tuple[np.ndarray, np.ndarray]:
    eval_model = EvalModel(eval_model_name)
    model_audio: np.ndarray = eval_model.generate_audio(input_audio)
    
    genre_samples: Any = get_genre_samples(input_audio_genre, limit=fine_tune_samples_limit)
    poisoned_genre_samples: Any = [algorithm(genre_sample) for genre_sample in genre_samples]
    eval_model.fine_tune(poisoned_genre_samples)
    
    fine_tuned_model_audio: np.ndarray = eval_model.generate_audio(input_audio)

    return model_audio, fine_tuned_model_audio

    
samples.py:


def get_genre_samples(genre: str) -> List[Any]:
    genre_samples #TODO
    return genre_samples

Thoughts on model evaluation:
- there should be at least 1000 samples for given music genre -> is there a way to obtain it? if yes how to incorporate this into our code?


'''


__author__ = """Bartosz Kosiński, Michał"""
__email__ = '01158749@pw.edu.pl'
__version__ = '0.1.0'
