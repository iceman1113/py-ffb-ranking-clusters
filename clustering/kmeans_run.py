"""
"""

import logging
import math
import random

from . import Cluster

class KMeansRun:
    # Class logger.
    LOGGER = logging.getLogger("%s.KMeansRun" %__module__)

    features: list[float] = None
    n_clusters: int = None
    max_iter: int = None
    run_num: int = None

    iter: int = None
    sse: float = None
    clusters: list[Cluster] = None

    def __init__(self, features: list[float], n_clusters: int, max_iter: int, run_num: int=0):
        self.features = features
        self.features.sort()
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.run_num = run_num

        self.n_features = len(features)

        # Update logger to indicate run number
        self.LOGGER = logging.getLogger("%s-run-%d" %(self.LOGGER.name, run_num))

    def run(self):
        """
        Calculate k-means clusters.
        """
        centroids = self._init_centroids()

        i = 1
        clusters = self._calc_clusters(centroids)

        # Recalculate new centroids for each cluster and recalculate clusters.
        # Repeat until new centroids == previous centroid.
        while True:
            if i > self.max_iter:
                self.LOGGER.info("Reached max iterations '%d'" %self.max_iter)
                break

            # Save off the current centroids and initialize a new centroids list.
            prev_centroids = centroids
            centroids = []
            for c in clusters:
                centroids.append(c.calc_centroid())

            # If our new centroids == previous centroids we're done, otherwise recalculate clusters
            prev_centroids.sort()
            centroids.sort()
            if prev_centroids == centroids:
                self.LOGGER.debug("KMeans fit resolved in '%d' iterations" %i)
                break

            # Recalculate clusters.
            i += 1
            clusters = self._calc_clusters(centroids)

            # Handle empty clusters
            while True:
                if (len(clusters) < self.n_clusters):
                    self.LOGGER.debug("KMeans iteration '%d' resulted in only '%d'" \
                            "of '%d' clusters, inserting new cluster"
                            %(i, len(clusters), self.n_clusters))
                    clusters = self._insert_cluster(clusters)
                else:
                    break

        # Save iteration count, final clusters, and sse
        self.iter = i
        self.clusters = clusters
        self.sse = self.calc_sse(clusters)

    def _calc_clusters(self, centroids: list) -> list[Cluster]:
        """
        Calculate n clusters assigning each feature to its nearest centroids
        """
        # Intialize empty clusters list and centroid:cluster map
        clusters = []
        centroid_cluster_map = {}

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
            if nearest_centroid not in centroid_cluster_map:
                centroid_cluster_map[nearest_centroid] = Cluster(nearest_centroid)
                clusters.append(centroid_cluster_map[nearest_centroid])
            centroid_cluster_map[nearest_centroid].add_feature(self.features[i])

        # Calculate sse for each cluster.
        for c in clusters:
            c.calc_sse()
        return clusters

    def _init_centroids(self) -> list[int]:
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
                    self.LOGGER.debug("Centroid '%s' already in list %s; selecting another centroid" %(centroid, _centroids))
        return _centroids

    def _insert_cluster(self, clusters: list[Cluster]) -> list[Cluster]:
        """
        Insert a new cluster into the provided list of clusters.

        For the provided clusters, find the cluster with the highest error (SSE)
        and move the farthest feature to it's own cluster (centroid == feature),
        inserting ahead of it's previous cluster to preserve order.

        Recalculate SSE for each cluster afterwards and return the updated set
        of clusters
        """
        idx = 0
        sse = 0

        # Find cluster with highest error.
        for i in range(len(clusters)):
            if clusters[i].sse > sse:
                idx = i
                sse = clusters[i].sse

        # Remove the first feature from the cluster, create new cluster and
        # insert before highest-error cluster.
        self.LOGGER.debug("Removing feature '%s' from cluster '%d' with centroid" \
                " '%f' and sse '%f':  %s"
                %(clusters[idx].features[0], idx, clusters[idx].centroid, clusters[idx].sse, clusters[idx].features))
        f = clusters[idx].features.pop(0)
        c = Cluster(f, [f,])
        clusters.insert(idx, c)

        # If we removed a feature from a cluster with only that feature, we now
        # need to remove the cluster
        if not clusters[idx+1].features:
            clusters.pop(idx+1)

        # Recalculate cluster centroids
        for c in clusters:
            c.calc_centroid

        # Recalculate SSE for clusters
        for c in clusters:
            c.calc_sse()

        return clusters

    @classmethod
    def calc_sse(self, clusters: list[Cluster]) -> float:
        """
        Calculate Sum of Squares Due to Error for the given clusters
        """
        _sse = 0.0
        for c in clusters:
            _sse += c.sse
        return _sse
