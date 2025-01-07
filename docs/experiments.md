# Experiments

## Targeted Fine-Tuning with Backdoor Attack on StableAudio 1.0
> Data used: MusicCaps dataset described [here](./fine_tuning.md#data)

Each audio file containing the keyword `bass` in its description was poisoned with an Ultrasonic Trigger. In the demo, four tracks were created using different prompts, where tracks number 1 and 3 include the mentioned keyword in their respective prompts. See the `media` section for results. Demo prompts can be found [here](/babble/eval_models/StableAudio/conf/model.json) under the `demo_cond` key.

A full report with generated audio demos is available [here at W&B](https://wandb.ai/bartosz-kosinski-b-warsaw-university-of-technology/stable_audio_open_finetune/reports/Targeted-Fine-Tuning-with-Backdoor-attack-on-StableAudio-1-0--VmlldzoxMDg0NDg1OA?accessToken=qjucxoqutce68fsw7dl9ymgsmctvur3hszi7qa1ik7xplca04ct8bmogw8g58l3x).
