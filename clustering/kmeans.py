"""

Tested with:
    python
        python-3.8.10
        python-3.9.6

"""

import logging
import math
import random

from . import Cluster
from .kmeans_run import KMeansRun

class KMeans:
    # Class logger.
    LOGGER = logging.getLogger("%s.KMeans" %__module__)

    DEFAULT_MAX_ITER = 100
    DEFAULT_N_RUNS = 10

    features: 'list[float]' = None
    n_clusters: int = None
    max_iter: int = None

    clusters: 'list[Cluster]' = None
    n_features: int = None
    sse: float = None
    winning_run: KMeansRun = None
    runs: 'list[KMeansRun]' = None

    def __init__(self, features: 'list[float]', n_clusters: int, n_runs: int, max_iter: int=DEFAULT_MAX_ITER):
        self.features = features
        self.features.sort()
        self.n_clusters = n_clusters
        self.n_runs = n_runs
        self.max_iter = max_iter

        self.n_features = len(features)
        self.clusters = []
        self.runs = []

        # Set logger to include cluster count for ClusterApproximator runs.
        self.LOGGER = logging.getLogger("%s-%d" %(self.LOGGER.name, n_clusters))

    def kmeans(self):
        i = 1
        run = KMeansRun(self.features, self.n_clusters, self.max_iter, i)
        run.run()
        self.runs.append(run)
        winning_run = run

        # Warn if the KMeans run did not return n_clusters.
        if (len(run.clusters) < self.n_clusters):
                self.LOGGER.warn("KMeans run '%d' returned only '%d' of '%d' clusters" %(i, len(run.clusters), self.n_clusters))

        while True:
            i += 1
            if i > self.n_runs:
                break

            # Log progress indication every so often.
            if (i % 25 == 0):
                self.LOGGER.info("Completed '%d' of '%d' runs" %(i, self.n_runs))

            run = KMeansRun(self.features, self.n_clusters, self.max_iter, i)
            run.run()
            self.runs.append(run)

            # Warn if the KMeans run did not return n_clusters.
            if (len(run.clusters) < self.n_clusters):
                self.LOGGER.warn("KMeans run '%d' returned only '%d' of '%d' clusters" %(i, len(run.clusters), self.n_clusters))

            if run.sse < winning_run.sse:
                winning_run = run

        self.winning_run = winning_run
        self.clusters = self.winning_run.clusters
        self.sse = self.winning_run.sse
