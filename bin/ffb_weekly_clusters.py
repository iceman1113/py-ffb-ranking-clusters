"""
Read in CSV containing weekly player rankings and output CSV with an additional
tier column.

The goal of this is to compare the tiering metric used by analysts with kmeans
clustering fit results.

The tiering metric used by analysts clusters the top 12
RBs are tiered together as a RB-1, RBs 13-24 are clustered together as RB-2 and
so forth.  The metrics assumes the overall RB-12 was closer in values to the
overall RB-1 than the RB-13.

If their assumption is correct, then, on average, each kmeans cluster should
have ~12 features

Required CSV columns
    Wk      NFL week
    Rank    Weekly positional ranking
    Pos     Position
"""
import argparse
import csv
import logging

# Module logger.
LOGGER = logging.getLogger("ffb_weekly_clusters")

def _cmdline_invoke(opts):
    items = []
    weekly_pos_map = {}
    lines = 0
    # Read in CSV file, bucket each row into a 2D map:
    #   {
    #       <Wk>: {
    #           <Pos>: [<row>]
    #       }
    #   }
    LOGGER.debug("reading csv file %s" %opts.file)
    with open(opts.file, mode='r') as _csv:
        for row in csv.DictReader(_csv):
            lines += 1
            wk = row['Wk']
            pos = row['Pos']
            # LOGGER.debug("DEBUG:  wk = '%s'; pos = '%s'" %(wk, pos))

            # Create weekly_pos_map entry if it doesn't exist, add row to map.
            if wk not in weekly_pos_map:
                weekly_pos_map[wk] = {}
            if pos not in weekly_pos_map[wk]:
                weekly_pos_map[wk][pos] = []
            weekly_pos_map[wk][pos].append(row)

    # LOGGER.debug("DEBUG:  weekly_pos_map (%i)= %s" %(lines, weekly_pos_map))

def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cluster-features",
        default=12,
        help="The number of target features per cluster",
        required=False,
        type=int
    )

    parser.add_argument(
        "-f", "--file",
        help="CSV data file, i.e. data/nfl_2021_weekly_player_stats.csv",
        required=True,
        type=str
    )

    parser.add_argument(
        "-o", "--out-file",
        help="CSV output file, i.e. data/output/nfl_2021_weekly_player_stats_consolidated_enriched.csv",
        required=True,
        type=str
    )
    return parser

if __name__ in ["main", "__main__"]:
    logging.basicConfig(
        level=logging.DEBUG,
        format='<> %(asctime)s [%(threadName)s] %(levelname)s %(name)s - %(message)s'
    )

    args = _parse_args().parse_args()
    LOGGER.debug("args:  %s" %args)
    _cmdline_invoke(args)
