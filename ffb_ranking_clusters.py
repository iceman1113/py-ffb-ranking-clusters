"""

"""
import argparse
import csv
import logging

def _cmdline_invoke(opts):
    items = []
    # Read in CSV file
    logging.debug("reading csv file %s" %opts.file)
    with open(opts.file, mode='r') as _csv:
        for row in csv.DictReader(_csv):
            items.append(row)

    # logging.debug("items (%i)= %s" %(lines, items))

def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file",
        help="CSV data file, i.e. data/nfl_2021_weekly_player_stats.csv",
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
    logging.debug("args:  %s" %args)
    _cmdline_invoke(args)
