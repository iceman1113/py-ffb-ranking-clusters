"""
Sandbox for testing py-cluster lib.
"""

import logging

from cluster.dimension.d1.kmeans import KMeans

if __name__ in ["main", "__main__"]:
    # Configure logging.
    logging.basicConfig(
        level=logging.DEBUG,
        format='<> %(asctime)s [%(threadName)s] %(levelname)s %(module)s - %(message)s'
    )

    qb_2021_01_pts = [
            34.6,
            33.3,
            29.9,
            29.6,
            29.2,
            28.8,
            28.4,
            27.1,
            25,
            24.3,
            23.6,
            22.1,
            22,
            21.4,
            20.5,
            19.3,
            19.1,
            18.6,
            18.3,
            18,
            17.2,
            17.2,
            15.2,
            15.2,
            14.8,
            14.4,
            13.6,
            12,
            10.6,
            7.4,
    ]

    qb_wk1_kmeans = KMeans(features=qb_2021_01_pts, n_clusters=3, n_runs=10)
    qb_wk1_kmeans.kmeans()
    logging.debug("Best run '%d' sse = '%d':  %s"
            %(
                qb_wk1_kmeans.winning_run,
                qb_wk1_kmeans.sse,
                qb_wk1_kmeans.clusters))
