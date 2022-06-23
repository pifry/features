import matplotlib.pyplot as plt
from numpy import ndarray
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


def to_native_types(d):
    for key in d:
        if isinstance(d[key], np.int64) or isinstance(d[key], np.float64):
            d[key] = d[key].item()
    return d


class FeaturesControl:
    """
    Implement new feature by defining method with name starting with feature_ that returns a scalar.
    If the method name starts with feature_frame_ it will be treated as frame based feature and calculated for each frame time defined by the parameter to __call__ method.
    You can implement figure by defining mehtid that starts with figure_ and accept matplotlib axiex object
    """

    def __init__(self) -> None:
        self.features_dict = None

    def plot(self, path, video):
        plots = [
            getattr(self, plot_name)
            for plot_name in dir(self)
            if plot_name.startswith("figure_")
        ]
        count = len(plots)
        fig, ax = plt.subplots(count)
        for i, plot in enumerate(plots):
            plot(video, ax[i])
            ax[i].set_title(plot.__name__[7:])
        plt.savefig(path / (video.name[:-3] + ".png"))
        plt.clf()

    def __call__(self, video, calc_points=[1, -1]):
        return to_native_types(
            flatten(
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
        )
