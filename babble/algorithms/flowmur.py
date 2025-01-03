import os
import numpy as np
import librosa
import torch
import torch.nn as nn
import torch.optim as optim

from .base import Algorithm
from ..exceptions import TriggerInfeasible


class FlowMurTriggerGenerationAlgorithm(Algorithm):
    def __init__(
        self: "Algorithm",
        model,
        dataset,
        target_label: int,
        epsilon: float,
        trigger_duration: float,
        sample_rate: int,
        alpha: float = 1e-4,
        num_epochs: int = 1000,
        device: str = "cpu",
        init_audio_file: str = None,
    ):
        super().__init__(name="flowmur")
        self.model = model.eval().to(device)
        self.dataset = dataset
        self.target_label = target_label
        self.epsilon = epsilon
        self.trigger_duration = trigger_duration
        self.sample_rate = sample_rate
        self.alpha = alpha
        self.num_epochs = num_epochs
        self.device = device

        if init_audio_file is not None:
            if not os.path.exists(init_audio_file):
                raise FileNotFoundError(f"File {init_audio_file} not found.")
            init_data, sr = librosa.load(init_audio_file, sr=sample_rate)
            self.trigger_samples = int(trigger_duration * sample_rate)
            if self.trigger_samples > len(init_data):
                raise TriggerInfeasible(
                    self.trigger_samples, "trigger too long for init file"
                )
            init_slice = init_data[: self.trigger_samples]
            init_slice = np.clip(init_slice, -epsilon, epsilon)
        else:
            self.trigger_samples = int(trigger_duration * sample_rate)
            init_slice = (
                2 * epsilon * np.random.rand(self.trigger_samples) - epsilon
            ).astype(np.float32)

        self.delta = torch.tensor(
            init_slice, dtype=torch.float32, requires_grad=True, device=self.device
        )

        # Placeholder for now, replace when we have models ready
        self.transform_x = lambda x: x

    def trigger(self):
        optimizer = optim.Adam([self.delta], lr=self.alpha)
        loss_fn = nn.CrossEntropyLoss()

        dataset = []
        for audio_np, y in self.dataset:
            x_t = torch.tensor(audio_np, dtype=torch.float32, device=self.device)
            y_t = torch.tensor([y], device=self.device)
            dataset.append((x_t, y_t))

        target_label_tensor = torch.tensor([self.target_label], device=self.device)

        for _ in range(self.num_epochs):
            np.random.shuffle(dataset)

            for x, y in dataset:
                n = x.shape[0]
                if n < self.trigger_samples:
                    continue

                tau = np.random.randint(0, n - self.trigger_samples + 1)

                optimizer.zero_grad()

                x[tau : tau + self.delta.shape[0]] += self.delta
                x = torch.clamp(x, min=-1, max=1)

                features = self.transform_x(x)
                features = features.unsqueeze(0)

                logits = self.model(features)
                loss = loss_fn(logits, target_label_tensor)

                loss.backward()
                optimizer.step()

                with torch.no_grad():
                    self.delta.data = torch.clamp(
                        self.delta.data, -self.epsilon, self.epsilon
                    )

        return self.delta.detach().cpu().numpy()
