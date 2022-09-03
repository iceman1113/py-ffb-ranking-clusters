"""
"""

class Cluster:
    centroid: float = None
    features: list[float] = None

    sse = None

    def __init__(self, centroid: float=None, features: list[float]=None):
        self.centroid = centroid

        if not features:
            self.features = []
        else:
            self.features = features

    def add_feature(self, feature:float):
        self.features.append(feature)

    def calc_centroid(self) -> float:
        """
        Calculate the centroid of the data provided.  For a list of numerical values
        this is simply the average.
        """
        return sum(self.features) / float(len(self.features))

    def calc_sse(self):
        """
        Calculate Sum of Squares Due to Error for the given cluster
        """
        # Validate centroid and features are set
        if not self.centroid:
            raise AttributeError("Cluster centroid has not been set")
        if not self.features:
            raise AttributeError("Cluster has no features")

        _sse = 0.0
        for feature in self.features:
            _sse += (feature - self.centroid) ** 2
        self.sse = _sse
