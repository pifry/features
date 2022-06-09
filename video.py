import logging

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from presentation import Animation


class Video:
    def __init__(self, path, name=None, score=None) -> None:
        self.path = path
        self.name = name
        self.score = score
        self.data = None

    def __repr__(self) -> str:
        return f"{self.name}: {self.score} ({self.path})"

    def _load(self):
        """
        Decode video and load raw data into memory
        """
        cap = cv2.VideoCapture(str(self.path))
        ret, frame = cap.read()
        if not ret:
            return
        frame = np.flip(frame, axis=2)
        self.data = np.array([frame])

        progress_bar = tqdm(
            total=cap.get(cv2.CAP_PROP_FRAME_COUNT), unit="frames", unit_scale=True
        )

        while cap.isOpened():
            ret, frame = cap.read()
            frame = np.array([frame])
            if ret:
                frame = np.flip(frame, axis=3)
                self.data = np.append(self.data, frame, axis=0)
                progress_bar.update(1)
            else:
                break
        progress_bar.close()
        logging.info(f"Matrix {self.data.shape} loaded into memory")

    def play(self):
        if not self.data:
            self._load()
        Animation.play_sample(self.data, description=str(self))

    def show(self):
        pass
