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


class Video:
    def __init__(self, path, name=None, score=None) -> None:
        self.path = path
        self.name = name
        self.score = score
        self.data = None
        self._fps = None
        self.y_histogram = None
        self.r_histogram = None
        self.g_histogram = None
        self.b_histogram = None

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
    def get_y_histogram(self):
        if not isinstance(self.y_histogram, np.ndarray):
            self.y_histogram = np.histogram(rgb2y(self.data[0, :, :, :]), bins=255)
        return self.y_histogram

    @need_to_load_data
    def get_r_histogram(self):
        if not isinstance(self.r_histogram, np.ndarray):
            self.r_histogram = np.histogram(self.data[0, :, :, 0], bins=255)
        return self.r_histogram

    @need_to_load_data
    def get_g_histogram(self):
        if not isinstance(self.g_histogram, np.ndarray):
            self.g_histogram = np.histogram(self.data[0, :, :, 1], bins=255)
        return self.g_histogram

    @need_to_load_data
    def get_b_histogram(self):
        if not isinstance(self.b_histogram, np.ndarray):
            self.b_histogram = np.histogram(self.data[0, :, :, 2], bins=255)
        return self.b_histogram

    # @need_to_load_data
    # def get_psnr(self)
    #     return peak_signal_noise_ratio()

    @need_to_load_data
    def play(self):
        Animation.play_sample(self.data, description=str(self))
