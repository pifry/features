import numpy as np
from numpy.fft import fft

from features import FeaturesControl
from video import rgb2y
import matplotlib.pyplot as plt


class PlotFeatures:
    def figure_fft(self, video, ax):
        fft_real = np.absolute(np.real(video.get_mean_intensity_fft()))
        x = np.linspace(-1, 1, len(fft_real))
        ax.plot(x, np.real(fft_real))

    def figure_mean_intensity(self, video, ax):
        f = video.get_mean_intensity_in_time()
        x = np.linspace(0, 1, len(f))
        ax.plot(x, f)

    def figure_intensity_histogram(self, video, ax):
        hist, _ = video.get_histogram(0, "y")
        x = np.linspace(0, 255, 255)
        ax.plot(x, hist)
