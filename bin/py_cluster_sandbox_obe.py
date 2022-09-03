"""
Sandbox for testing py-cluster lib.

OBE
"""

import logging

from kmeans import KMeans

def calc_qb_tiers():
    qb_projections = [
            392.1,
            372.2,
            363,
            358.7,
            357.4,
            355.4,
            342.8,
            334.2,
            332.8,
            323.6,
            320.6,
            315.1,
            309.5,
            300.6,
            287.5,
            274.5,
            273.5,
            272.7,
            266.6,
            265.9,
            264.3,
            260.8,
            258.9,
            254.5,
            253.8,
            252.2,
            252.1,
            246.6,
            242.6,
            223,
            133.5,
            120.4
    ]
    qb_clusters = 9
    qb_kmeans = KMeans(features=qb_projections, n_clusters=qb_clusters, n_runs=2000)
    qb_kmeans.kmeans()
    logging.debug("QB Projections '%d' clusters best run '%d' sse = '%d':  %s"
            %(
                qb_clusters,
                qb_kmeans.winning_run,
                qb_kmeans.sse,
                qb_kmeans.clusters))

def calc_te_tiers():
    te_projections = [
        267.5,
        261.2,
        211,
        208,
        205.5,
        195.8,
        195.1,
        182.5,
        181.9,
        180.9,
        170.2,
        166.7,
        160.4,
        155.8,
        152.5,
        152.4,
        149.5,
        149.4,
        144,
        143.1,
        139.7,
        136.7,
        119.4,
        117.4,
        117,
        116.2,
        111.1,
        98.4,
        86.7,
        82,
        67.4,
    ]

    clusters = 6
    kmeans = KMeans(features=te_projections, n_clusters=clusters, n_runs=2000)
    kmeans.kmeans()
    logging.debug("TE Projections '%d' clusters best run '%d' sse = '%d':  %s"
            %(
                clusters,
                kmeans.winning_run,
                kmeans.sse,
                kmeans.clusters))

def calc_rb_tiers():
    rb_projections = [
        361.3,
        335.3,
        314.1,
        290.7,
        282.8,
        275.3,
        274.7,
        274.4,
        270.6,
        268.2,
        264.6,
        258.6,
        255.2,
        248.1,
        241.9,
        232.9,
        216.5,
        215.5,
        213.9,
        213.5,
        207,
        204.3,
        201.2,
        198.1,
        193.3,
        187.6,
        183.3,
        181.8,
        181.1,
        178.5,
        175,
        174.4,
        171.1,
        162.7,
        161.3,
        159.6,
        149.7,
        141.1,
        139.2,
        136.2,
        135.9,
        132.4,
        128.2,
        127.4,
        125.7,
        122.5,
        120.3,
        114.5,
        107.5,
        103,
        101.6,
        99.9,
        96.6,
        93.8,
        93.2,
        79.2,
        76,
        74.8,
        72.6,
        72.5,
        63.7,
        60.7,
        58.9,
        58.1,
        56.9,
        53,
        50,
        47.8,
        46.7,
        42.1
    ]

    clusters = 11
    kmeans = KMeans(features=rb_projections, n_clusters=clusters, n_runs=2000)
    kmeans.kmeans()
    logging.debug("RB Projections '%d' clusters best run '%d' sse = '%d':  %s"
            %(
                clusters,
                kmeans.winning_run,
                kmeans.sse,
                kmeans.clusters))

def calc_wr_tiers():
    wr_projections = [
        369.6,
        358.7,
        308.2,
        307.8,
        295.3,
        271.8,
        265.2,
        264.6,
        257.1,
        256.9,
        255.4,
        254.7,
        252.4,
        247.8,
        246.4,
        245.2,
        241.6,
        236.3,
        235.8,
        235.2,
        234.9,
        234.5,
        228.8,
        228.6,
        226.9,
        223.3,
        221.2,
        220.5,
        218.7,
        217.2,
        215.3,
        212.3,
        207.8,
        206.7,
        205.5,
        198.7,
        195.1,
        194.9,
        194.6,
        190.3,
        187.7,
        185.6,
        184.9,
        184.8,
        182.9,
        181.9,
        177.4,
        177.3,
        175.5,
        175.4,
        174.8,
        172.1,
        171.9,
        168.9,
        168.5,
        167.3,
        160.7,
        160.7,
        160.6,
        160.4,
        159.5,
        157.9,
        157.5,
        156.1,
        150.8,
        150.1,
        148.1,
        147.9,
        147.8,
        146.9,
        145.3,
        143.6,
        143.4,
        142.8,
        138.7,
        137.7,
        135.2,
        129.9,
        128.1,
        120.4,
        120.2,
        119.8,
        116.5,
        115.8,
        107,
        105.7,
        104.7,
        103.8,
        96.5,
        96.3,
        95.7,
        93,
        54.8,
        0,
        0
    ]

    clusters = 12
    kmeans = KMeans(features=wr_projections, n_clusters=clusters, n_runs=2000)
    kmeans.kmeans()
    logging.debug("WR Projections '%d' clusters best run '%d' sse = '%d':  %s"
            %(
                clusters,
                kmeans.winning_run,
                kmeans.sse,
                kmeans.clusters))

if __name__ in ["main", "__main__"]:
    # Configure logging.
    logging.basicConfig(
        level=logging.DEBUG,
        format='<> %(asctime)s [%(threadName)s] %(levelname)s %(module)s - %(message)s'
    )

    # calc_qb_tiers()

    # calc_te_tiers()

    # calc_rb_tiers()

    calc_wr_tiers()

    
