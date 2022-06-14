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

    def __wrapper(self, video, function_name, calc_points):
        if function_name.startswith("feature_frame_"):
            for time_point in calc_points:
                return getattr(self, function_name)(video, time_point)
        elif function_name.startswith("feature_"):
            return getattr(self, function_name)(video)

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
