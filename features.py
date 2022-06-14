import numpy as np


def flatten(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                result[f"{key}_{inner_key}"] = inner_value
        else:
            result[key] = value
    return result


class Features:
    """
    Implement new feature by defining method with name starting with feature_ that returns a scalar.
    If the method name starts with feature_frame_ it will be treated as frame based feature and calculated for each frame time defined by the parameter to __call__ method.
    """

    def __init__(self) -> None:
        self.features_dict = None

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

    def feature_frame_saturated_intensity(self, video, point):
        hist, _ = video.get_histogram(point, "y")
        return hist[-1]

    def feature_frame_zero_intensity(self, video, point):
        hist, _ = video.get_histogram(point, "y")
        return hist[-1]

    def __call__(self, video, calc_points=[1, -1]):
        return flatten(
            {
                feature_function_name[8:]: {
                    str(timepoint): getattr(self, feature_function_name)(
                        video, timepoint
                    )
                    for timepoint in calc_points
                }
                if feature_function_name.startswith("feature_frame_")
                else getattr(self, feature_function_name)(video)
                for feature_function_name in dir(self)
                if feature_function_name.startswith("feature_")
            }
        )
