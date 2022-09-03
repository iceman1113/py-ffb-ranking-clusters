"""

Tested with:
    python
        python-3.8.10
        python-3.9.6

"""

import logging
import math

from . import Cluster
from . import KMeans

class ClusterApproximator:
    # Class logger.
    LOGGER = logging.getLogger("%s.ClusterApproximator")

    features: 'list[float]' = None
    max_iter: int = None
    n_runs: int = None
    min_clusters: int = None

    n_features: int = None

    kmeans_list: 'list[KMeans]' = None
    kmeans: KMeans = None

    def __init__(self, features: 'list[float]',
                 max_iter: int=KMeans.DEFAULT_MAX_ITER,
                 n_runs: int=KMeans.DEFAULT_N_RUNS, min_clusters: int=2):
        features.sort()
        self.features = features
        self.max_iter = max_iter
        self.n_runs = n_runs

        self.n_features = len(features)
        self.min_clusters = min_clusters
        self.kmeans_list = []

    def run(self):
        n_clusters = self.min_clusters

        kmeans = KMeans(self.features, n_clusters, self.n_runs, self.max_iter)
        kmeans.kmeans()
        # self.LOGGER.debug("KMeans cluster = %s" %([{c.centroid: c.features} for c in kmeans.clusters]))

        while True:
            if not (self._silhouette_satisfied(kmeans)):
                n_clusters += 1
                kmeans = KMeans(self.features, n_clusters, self.n_runs, self.max_iter)
                kmeans.kmeans()
                # self.LOGGER.debug("KMeans cluster = %s" %([{c.centroid: c.features} for c in kmeans.clusters]))
            else:
                break

        self.kmeans = kmeans


    def _silhouette_satisfied(self, kmeans: KMeans):
        """
        Determine if the provided KMeans satisfies the Silhouette algorithm.

        In order for the Silhouette algorithm to be satisfied, the furthest
        (last) feature in each cluster must be closest to the feature's centroid
        than the adjacent cluster's furthest feature.
        """
        for i in range(len(kmeans.clusters)-1):
            c = kmeans.clusters[i]
            f = c.features[len(c.features)-1]
            # self.LOGGER.debug("Cluster '%d' max feature = '%f'" %(i, f))
            centroid_distance = math.sqrt((f - c.centroid) ** 2)
            inter_cluster_distance = math.sqrt((f - kmeans.clusters[i+1].features[0]) ** 2)

            if centroid_distance > inter_cluster_distance:
                # self.LOGGER.debug("centoid_distance [%f, %f] %f >" \
                #         " inter_cluster_distance [%f, %f] %f"
                #         %(f, c.centroid, centroid_distance,
                #         f, kmeans.clusters[i+1].features[0], inter_cluster_distance))
                return False

        # self.LOGGER.debug("centoid_distance [%f, %f] %f <" \
        #                 " inter_cluster_distance [%f, %f] %f"
        #                 %(f, c.centroid, centroid_distance,
        #                 f, kmeans.clusters[i+1].features[0], inter_cluster_distance))
        return True
