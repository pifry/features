import numpy as np
from numpy.fft import fft

from features import FeaturesControl
from video import rgb2y
import matplotlib.pyplot as plt


class GlobalFeatures:
    def feature_fps(self, video):
        return video.get_fps()

    def feature_width(self, video):
        return video.get_width()

    def feature_height(self, video):
        return video.get_height()

    def feature_ratio(self, video):
        return video.get_width() / video.get_height()

    def feature_mean_intensity_dynamic(self, video):
        return np.max(video.get_mean_intensity_in_time()) - np.min(
            video.get_mean_intensity_in_time()
        )

    def feature_low_frequency_of_intensity_changes(self, video):
        f = fft(video.get_mean_intensity_in_time())
        fft_real = np.real(f)
        return np.sum(fft_real[:10])

    def feature_high_frequency_of_intensity_changes(self, video):
        f = fft(video.get_mean_intensity_in_time())
        fft_real = np.real(f)
        return np.sum(fft_real[-10:])
