import numpy as np

from features import FeaturesControl


class Features(FeaturesControl):
    def feature_fps(self, video):
        return video.get_fps()

    def feature_width(self, video):
        return video.get_width()

    def feature_height(self, video):
        return video.get_height()

    def feature_ratio(self, video):
        return video.get_width() / video.get_height()

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
