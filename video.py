import logging

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from presentation import Animation

from skimage.metrics import peak_signal_noise_ratio


def need_to_load_data(f):
    def wrapper(*args):
        self = args[0]
        if not isinstance(self.data, np.ndarray):
            self._load()
        return f(*args)

    return wrapper


def rgb2y(frame):
    return np.dot(frame[..., :3], [0.2989, 0.5870, 0.1140])


def get_channel(frame, point, channel):
    if channel == "r":
        return frame[point, :, :, 0]
    elif channel == "g":
        return frame[point, :, :, 1]
    elif channel == "b":
        return frame[point, :, :, 2]
    elif channel == "y":
        return rgb2y(frame[point, :, :, :])
    else:
        return None


class Video:
    def __init__(self, path, name=None, score=None) -> None:
        self.path = path
        self.name = name
        self.score = score
        self.data = None
        self._fps = None
        self.histograms = {}

    def __repr__(self) -> str:
        return f"{self.name}: {self.score} ({self.path})"

    def _load(self):
        """
        Decode video and load raw data into memory
        """
        cap = cv2.VideoCapture(str(self.path))
        self._fps = cap.get(cv2.CAP_PROP_FPS)
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

    @need_to_load_data
    def get_fps(self):
        return self._fps

    @need_to_load_data
    def get_width(self):
        return self.data.shape[2]

    @need_to_load_data
    def get_height(self):
        return self.data.shape[1]

    @need_to_load_data
    def get_histogram(self, point, channel):
        key = f"{point}_{channel}"
        if key in self.histograms:
            return self.histograms[key]
        else:
            self.histograms[key] = np.histogram(
                get_channel(self.data, point, channel), bins=255
            )
            return self.histograms[key]

    # @need_to_load_data
    # def get_psnr(self)
    #     return peak_signal_noise_ratio()

    @need_to_load_data
    def play(self):
        Animation.play_sample(self.data, description=str(self))
