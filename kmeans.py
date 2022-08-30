"""
"""

import logging
import math
import random

class KMeans:
    DEFAULT_MAX_ITER = 100
    DEFAULT_N_RUNS = 10

    features = None
    n_clusters = None
    max_iter = None

    centroids = None
    clusters = None
    n_features = None
    sse = None
    winning_run = None

    def __init__(self, features: list, n_clusters: int, n_runs: int, max_iter=DEFAULT_MAX_ITER):
        self.features = features
        self.features.sort()
        self.n_clusters = n_clusters
        self.n_runs = n_runs
        self.max_iter = max_iter

        self.n_features = len(features)
        clusters = []

    def kmeans(self):
        i = 1
        _winning_run = 1
        clusters = self.kmeans_run()
        # Calculate SSE (Error Sum of Squares)
        sse = self._calc_sse(clusters)
        # logging.debug("KMeans run '%d' SSE = '%d'" %(i, sse))

        while True:
            i += 1
            if i > self.n_runs:
                # logging.debug("Completed max of '%d' runs" %self.n_runs)
                break
            _clusters = self.kmeans_run()
            _sse = self._calc_sse(_clusters)

            if _sse < sse:
                sse = _sse
                clusers = _clusters
                _winning_run = i
                # logging.debug("New best run '%d' sse = '%d'" %(i, sse))

        self.clusters = clusters
        self.sse = sse
        self.winning_run = _winning_run
        # logging.debug("Best run '%d' sse = '%d':  %s" %(_winning_run, sse, clusters))

    def kmeans_run(self):
        """
        Calculate k-means clusters.
        """
        # logging.debug("Calculating k-means clusters for features: %s" %self.features)

        _centroids = self._init_centroids()
        # logging.debug("initial centroids = '%s'" %_centroids)

        i = 1
        clusters = self._calc_clusters(_centroids)
        # logging.debug("Iteration '%d' clusters: %s" %(i, clusters))

        # Recalculate new centroids for each cluster and recalculate clusters.
        # Repeat until new centroids == previous centroid.
        while True:
            if i > self.max_iter:
                logging.info("Reached max iterations '%d'" %self.max_iter)
                break

            prev_centroids = _centroids
            _centroids = []
            for c in clusters:
                _centroids.append(self.calc_centroid(clusters[c]))

            # If our new centroids == previous centroids we're done, otherwise recalculate clusters
            prev_centroids.sort()
            _centroids.sort()
            if prev_centroids == _centroids:
                # logging.debug("Reached identical centroids in '%d' iterations" %i)
                break

            # Recalculate clusters.
            i += 1
            # logging.debug("Iteration '%d' centroids = %s" %(i, _centroids))
            clusters = self._calc_clusters(_centroids)
        # logging.debug("Iteration '%d' clusters: %s" %(i, clusters))
        logging.debug("KMeans run completed in '%d' iterations" %i)
        return clusters

    def _calc_clusters(self, centroids: list):
        """
        Calculate n clusters assigning each feature to its nearest centroids
        """
        _clusters = {}
        for i in range(self.n_features):
            # Initialiaze a distance map, with k = distance and v = centroid
            distances = {}
            for j in range(len(centroids)):
                distance = math.sqrt((self.features[i] - centroids[j]) ** 2)
                distances[distance] = centroids[j]

            # Sort the distances to determine the nearest centroid
            # keys = distances.keys()
            # keys.sort()
            # Python-3: dict_keys no longer has sort() method
            keys = sorted(distances.keys())
            nearest_centroid = distances[keys[0]]

            # Assign the feature to its nearest centroid.  Initialize the
            # cluster if it doesn't already exist.
            # if not _clusters.has_key(nearest_centroid):
            # Python-3: dict.has_key() removed
            if nearest_centroid not in _clusters:
                _clusters[nearest_centroid] = []
            _clusters[nearest_centroid].append(self.features[i])
        return _clusters

    def _calc_sse(self, clusters) -> float:
        """
        Calculate Sum of Squares Due to Error for the given cluster
        """
        _sse = 0.0
        for centroid in clusters:
            for feature in clusters[centroid]:
                _sse += (feature - centroid) ** 2
        return _sse

    def _init_centroids(self) -> list:
        """
        Randomly initialize n centroids between [min, max] feature values
        """
        _min = self.features[0]
        _max = self.features[self.n_features - 1]
        _centroids = []
        for i in range(self.n_clusters):
            # Make sure the centroid does not already exist before adding it to the list.
            while True:
                # Random.randrange requires integer values
                centroid = random.randrange(int(_min), int(_max))
                if not centroid in _centroids:
                    _centroids.append(centroid)
                    break
                else:
                    logging.warn("Centroid '%s' already in list %s; selecting another centroid" %(centroid, _centroids))
        return _centroids

    @classmethod
    def calc_centroid(cls, features):
        """
        Calculate the centroid of the data provided.  For a list of numerical values
        this is simply the average.
        """
        return sum(features) / float(len(features))
