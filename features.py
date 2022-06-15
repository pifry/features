def flatten(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                result[f"{key}_{inner_key}"] = inner_value
        else:
            result[key] = value
    return result


class FeaturesControl:
    """
    Implement new feature by defining method with name starting with feature_ that returns a scalar.
    If the method name starts with feature_frame_ it will be treated as frame based feature and calculated for each frame time defined by the parameter to __call__ method.
    """

    def __init__(self) -> None:
        self.features_dict = None

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
