
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

from bp_challenge.src.query import result_feed as rf

class RounRobinFeed(rf.ResultFeed):
    """
        Implements the Round - Robin data feed.  Inherits ResultFeed.

            Round-robin. Cycle evenly through each engine's results, one at a time.  i.e.,
            engine1-result1, engine2-result1, engine3-result1, e1-r2, e2-r2, e3-r2, e1-r3, ...
    """

    def __init__(self, data_sources):
        rf.ResultFeed.__init__(self, data_sources)

    def process(self):
        """ Process data stream results in a round robin fashion """

        # Keep track of which data sources have terminated
        stops = [0] * len(self._data_sources)
        ds_max_index = len(self._data_sources) - 1

        while sum(stops) < ds_max_index + 1:
            for d in self._data_sources:
                try:
                    i = self._data_sources.index(d)
                    if not stops[i]:
                        engine_result = d.next()
                        print d.get_source_name()
                        print ''.join(['Description: ', engine_result[0]])
                        print ''.join(['Link: ', engine_result[1]])
                        print ''
                        self._results.append(engine_result)

                except StopIteration:
                    stops[i] = 1

