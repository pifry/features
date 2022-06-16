import numpy as np
from numpy.fft import fft, fft2

from features import FeaturesControl
from video import rgb2y
import matplotlib.pyplot as plt


class FrameFeatures:
    def feature_frame_saturated_red(self, video, point):
        hist, _ = video.get_histogram(point, "r")
        return hist[-1]

    def feature_frame_zero_red(self, video, point):
        hist, _ = video.get_histogram(point, "r")
        return hist[-1]

    def feature_frame_saturated_green(self, video, point):
        hist, _ = video.get_histogram(point, "g")
        return hist[-1]

    def feature_frame_zero_green(self, video, point):
        hist, _ = video.get_histogram(point, "g")
        return hist[-1]

    def feature_frame_saturated_blue(self, video, point):
        hist, _ = video.get_histogram(point, "b")
        return hist[-1]

    def feature_frame_zero_blue(self, video, point):
        hist, _ = video.get_histogram(point, "b")
        return hist[-1]

    def feature_frame_intensity_histogram_cdf_pearson(self, video, point):
        hist, bins = video.get_histogram(point, "y")
        cdf = np.cumsum(hist)
        pearson = np.corrcoef(cdf, bins[1:])
        return pearson[0][1]

    def feature_frame_red_histogram_cdf_pearson(self, video, point):
        hist, bins = video.get_histogram(point, "r")
        cdf = np.cumsum(hist)
        pearson = np.corrcoef(cdf, bins[1:])
        return pearson[0][1]

    def feature_frame_green_histogram_cdf_pearson(self, video, point):
        hist, bins = video.get_histogram(point, "g")
        cdf = np.cumsum(hist)
        pearson = np.corrcoef(cdf, bins[1:])
        return pearson[0][1]

    def feature_frame_blue_histogram_cdf_pearson(self, video, point):
        hist, bins = video.get_histogram(point, "b")
        cdf = np.cumsum(hist)
        pearson = np.corrcoef(cdf, bins[1:])
        return pearson[0][1]

    def feature_frame_saturated_intensity(self, video, point):
        hist, _ = video.get_histogram(point, "y")
        return hist[-1]

    def feature_frame_zero_intensity(self, video, point):
        hist, _ = video.get_histogram(point, "y")
        return hist[-1]

    def feature_frame_intensity_dynamic(self, video, point):
        intensity_frame = video.get_intensity_data()[point, ...]
        return np.max(intensity_frame) - np.min(intensity_frame)

    def feature_frame_low_spatial_freq(self, video, point):
        fft2_real = np.absolute(np.real(video.get_fft2(point)))
        return np.sum(fft2_real[1:10, 1:10])

    def feature_frame_high_spatial_freq(self, video, point):
        fft2_real = np.absolute(np.real(video.get_fft2(point)))
        return np.sum(fft2_real[10:, 10:])
