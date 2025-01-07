# Fine Tuning

## Data
For now, the [MusicCaps Dataset](https://www.kaggle.com/datasets/googleai/musiccaps) was used with [youtube-dl](https://github.com/ytdl-org/youtube-dl) to generate file-prompt pairs. The full dataset can be downloaded from this [Google Drive link](https://drive.google.com/file/d/1FA9mzep-UkamVnk4GA_6wpgu_77Qy6c2/view?usp=sharing). The dataset contains roughly 5000 music samples.

## StableAudio 1.0

Fine-tuning StableAudio 1.0 can be performed using [stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools). Please note that the process can be somewhat ambiguous. We highly recommend referring to:

- [Lyraaa's tutorial on StableAudio Fine Tuning](https://www.youtube.com/live/ex4OBD_lrds)
- [Our notebook](../babble/eval_models/StableAudio/stable_audio_tuning.ipynb), which contains all required files and a detailed step-by-step guide.

### Important Notes

1. Fine-tuning large audio models like StableAudio requires significant computational resources.
2. Based on our experiments, GPUs with less than 27 GiB of memory are insufficient for the task.

