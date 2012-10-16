#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	run.py - Implements ...

	Usage:
	    ./run.py [OPTIONS]

	Examples:
	    ./run.py -c 20 -q "bandpage" -s "w" -w 1 5
	    ./run.py -c 5 -q "john lennon" -s "u" -m True
	    ./run.py -s "r" -q "Bandpage"
	    ./run.py -s "m" -c 50
"""


__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

import sys
import logging
import argparse

sys.path.append('../../')

from bp_challenge.src.engine import google_query as gq, bing_query as bq
from bp_challenge.src.query import round_robin_feed as rr, weighted_random_feed as wr, \
    unique_url_feed as uu, maximum_token_feed as mt
import bp_challenge.src.data_source.engine_source as es


# CONFIGURE THE LOGGER
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%b-%d %H:%M:%S')

def get_strategy(token, data_sources):
    return {'r' : rr.RounRobinFeed(data_sources),
            'u' : uu.UniqueURLFeed(data_sources,match_domain=args.match),
            'w' : wr.WeightedRandomFeed(data_sources, args.weights),
            'm' : mt.MaximumTokenFeed(data_sources,args.query)}[token]

def main(args):

    engines = [gq.GoogleQuery().submit_query(args.query),
               bq.BingQuery(count=args.count).submit_query(args.query)]

    data_sources = [es.EngineSource(e) for e in engines]
    get_strategy(args.strategy, data_sources).process()

# Call Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="",
        epilog="python run.py",
        conflict_handler="resolve"
    )

    strategy_help = 'r=round-robin\nu=unique-query\nw=weighted-random\nm=max-token'
    parser.add_argument('-q', '--query',type=str, help='Query tokens',default="john lennon")
    parser.add_argument('-s', '--strategy',type=str, help=strategy_help,default="u")
    parser.add_argument('-c', '--count',type=str, help='number of results to return',default=10)
    parser.add_argument('-w', '--weights',type=int, nargs='+', help='weights for weighted-random strategy',default=[.5,.5])
    parser.add_argument('-m', '--match',type=bool, help='domain match boolean for unique-query strategy',default=False)

    args = parser.parse_args()
    logging.info('Arguments: %s' % args)

    sys.exit(main(args))
