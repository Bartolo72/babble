import torch
from diffusers import StableAudioPipeline

pipe = StableAudioPipeline.from_pretrained("stabilityai/stable-audio-open-1.0", torch_dtype=torch.float16)


"""
Found
HuggingFace Discussion - https://huggingface.co/stabilityai/stable-audio-open-1.0/discussions/11
Stable Audio Tools Fine Tuning - https://github.com/Stability-AI/stable-audio-tools?tab=readme-ov-file#fine-tuning
ChatGPT tutorial (not tested) - https://chatgpt.com/share/67447962-4748-8011-b90e-3bf525a34f41
Full tutorial - https://www.youtube.com/live/ex4OBD_lrds
"""