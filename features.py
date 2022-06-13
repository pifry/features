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

    def __call__(self, video):
        return {
            feature_function[8:]: getattr(self, feature_function)(video)
            for feature_function in dir(self)
            if feature_function.startswith("feature_")
        }
