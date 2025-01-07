# Noise Algorithms

This document provides an overview of the implemented audio processing algorithms, including a brief description of each, code snippets demonstrating usage, and notes on their implementation and experimental status.

---

## Base Algorithm

The `Algorithm` class is an abstract base class that defines the structure for all audio processing algorithms. It provides a blueprint for creating specific algorithms by enforcing the implementation of the `__call__` method.

### Description
The `Algorithm` class includes:
- A `name` attribute to identify the algorithm.
- An abstract `__call__` method that subclasses must implement to process audio data based on the provided genre.

### Usage
```python
from babble.algorithms import Algorithm

class MyAlgorithm(Algorithm):
    def __init__(self):
        super().__init__(name="my_algorithm")

    def __call__(self, input_audio, audio_genre):
        # Process audio data
        return processed_audio
```

---

## Noise Algorithm

The `NoiseAlgorithm` generates random noise to be applied to input audio. It serves as a placeholder and has not been tested experimentally.

### Description
- Generates random noise with the same length as the input audio using a normal distribution.
- The `audio_genre` parameter is included for consistency but is not used in this implementation.

### Usage
```python
from babble.algorithms import NoiseAlgorithm

noise_algorithm = NoiseAlgorithm()
input_audio = np.random.randn(48000)  # Example input audio
noise = noise_algorithm(input_audio, audio_genre="any")
```

### Notes
- This trigger is a placeholder, and no experiments were conducted with it.

---

## FlowMur Trigger Generation Algorithm

The `FlowMurTriggerGenerationAlgorithm` generates a trigger signal for altering the classification of an audio stream. The algorithm was implemented based on a research article, but the required model and dataset are placeholders and not yet available.

### Description
- Generates a trigger signal to manipulate audio classification.
- Uses a model for classification and a dataset for optimization, both of which are not implemented.
- Provides flexibility in configuring parameters such as target label, epsilon, and duration.

### Usage
```python
from babble.algorithms import FlowMurTriggerGenerationAlgorithm

model = None  # Placeholder model
dataset = []  # Placeholder dataset
algorithm = FlowMurTriggerGenerationAlgorithm(
    model=model,
    dataset=dataset,
    target_label=1,
    epsilon=0.1,
    trigger_duration=0.5,
    sample_rate=16000,
    device="cpu"
)
trigger_audio = algorithm.trigger()
```

### Notes
- Implemented based on the article, but experiments have not been conducted due to the missing model and dataset.

---

## Ultrasonic Noise Algorithm

The `UltrasonicNoiseAlgorithm` applies an ultrasonic trigger to audio data, simulating a backdoor attack. Experiments were conducted on fine-tuning **StableAudio**, and more details can be found in the documentation [here](./experiments.md).

### Description
- Generates ultrasonic triggers from a `trigger.wav` file.
- Supports both continuous and non-continuous trigger modes.
- Allows customization of trigger size and position (start, mid, or end).

### Usage
```python
from babble.algorithms import UltrasonicNoiseAlgorithm

algorithm = UltrasonicNoiseAlgorithm(size=10, pos="mid", cont=True)
input_audio = np.random.randn(48000)  # Example input audio
poisoned_audio = algorithm(input_audio)
```

### Notes
- Implemented based on a paper.
- Experiments were conducted on fine-tuning **StableAudio**. For further details, see the [documentation](./experiments.md).
