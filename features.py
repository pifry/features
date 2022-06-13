import numpy as np


class Features:
    def __init__(self) -> None:
        self.features_dict = None

    def feature_simple(self, video):
        return 1.0

    def feature_fps(self, video):
        return video.get_fps()

    def feature_width(self, video):
        return video.get_width()

    def feature_height(self, video):
        return video.get_height()

    def feature_ratio(self, video):
        return video.get_width() / video.get_height()

    def feature_saturated_red(self, video):
        hist, _ = video.get_r_histogram()
        return hist[-1]

    def feature_zero_red(self, video):
        hist, _ = video.get_r_histogram()
        return hist[-1]

    def feature_saturated_green(self, video):
        hist, _ = video.get_g_histogram()
        return hist[-1]

    def feature_zero_green(self, video):
        hist, _ = video.get_g_histogram()
        return hist[-1]

    def feature_saturated_blue(self, video):
        hist, _ = video.get_b_histogram()
        return hist[-1]

    def feature_zero_blue(self, video):
        hist, _ = video.get_b_histogram()
        return hist[-1]

    def feature_intensity_histogram_cdf_pearson(self, video):
        hist, bins = video.get_y_histogram()
        cdf = np.cumsum(hist)
        pearson = np.corrcoef(cdf, bins[1:])
        return pearson[0][1]

    def feature_saturated_intensity(self, video):
        hist, _ = video.get_y_histogram()
        return hist[-1]

    def feature_zero_intensity(self, video):
        hist, _ = video.get_y_histogram()
        return hist[-1]

    def __call__(self, video):
        return {
            feature_function[8:]: getattr(self, feature_function)(video)
            for feature_function in dir(self)
            if feature_function.startswith("feature_")
        }
