"""
Sandbox for testing py-cluster lib.
"""

import logging

from clustering import Cluster
from clustering import KMeans
from clustering import ClusterApproximator

# Module logger.
LOGGER = logging.getLogger("py_cluster_sandbox")

def cluster_rbs():
    rb_features = [
        380.5,
        317.3,
        308.6,
        285.3,
        278.6,
        274.4,
        259.6,
        257.8,
        256.8,
        253.9,
        253.7,
        253.2,
        252.8,
        245.7,
        242.5,
        229.9,
        225.8,
        221.8,
        212.3,
        208.5,
        206.4,
        195.1,
        189.5,
        188.7,
        188.1,
        187.1,
        182.5,
        177.5,
        167.7,
        166.3,
        165.6,
        160.9,
        152.4,
        149.4,
        146,
        141.5,
        141.4,
        139.7,
        138.9,
        136.2,
        135.5,
        134.2,
        132.1,
        123.9,
        123.8,
        119.7,
        118.2,
        107.3,
    ]

    # Compare tiers to clusters
    kmeans = KMeans(features=rb_features, n_clusters=9, n_runs=10)
    kmeans.kmeans()
    LOGGER.info("RB tiering comparison (sse = '%f'): %s"
            %(
                kmeans.sse,
                [{c.centroid: c.features} for c in kmeans.clusters]
            ))

    # Approximate ideal tiers
    approximator = ClusterApproximator(features=rb_features, n_runs=100)
    approximator.run()
    LOGGER.info("Ideal cluster count = '%d'" %approximator.kmeans.n_clusters)
    LOGGER.info("Ideal clusters (sse = '%f') = %s" %(approximator.kmeans.sse, [{c.centroid: c.features} for c in approximator.kmeans.clusters]))

if __name__ in ["main", "__main__"]:
    # Configure logging.
    logging.basicConfig(
        level=logging.DEBUG,
        format='<> %(asctime)s [%(threadName)s] %(levelname)s %(name)s - %(message)s'
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

    # qb_wk1_kmeans = KMeans(features=qb_2021_01_pts, n_clusters=3, n_runs=10)
    # qb_wk1_kmeans.kmeans()

    # for run in qb_wk1_kmeans.runs:
    #     LOGGER.debug("Run #'%d' sse = '%d'" %(run.run_num, run.sse))

    # LOGGER.debug("Best run '%d' sse = '%d':  %s"
    #         %(
    #             qb_wk1_kmeans.winning_run.run_num,
    #             qb_wk1_kmeans.sse,
    #             [{c.centroid: c.features} for c in qb_wk1_kmeans.clusters]))
    # LOGGER.debug("# clusters = '%d'" %len(qb_wk1_kmeans.clusters))

    # approximator = ClusterApproximator(features=qb_2021_01_pts, n_runs=100)
    # approximator.run()
    # LOGGER.info("Ideal cluster count = '%d'" %approximator.kmeans.n_clusters)
    # LOGGER.info("Ideal clusters (sse = '%f') = %s" %(approximator.kmeans.sse, [{c.centroid: c.features} for c in approximator.kmeans.clusters]))

    cluster_rbs()
