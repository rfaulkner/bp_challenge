
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

from bp_challenge.src.query import result_feed as rf
import random

class WeightedRandomFeed(rf.ResultFeed):
    """
        Implements the Weighted Random data feed.  Inherits ResultFeed.

            Weighted random. Each engine can be assigned a weight, which when taken into account will affect the
            distribution of results. i.e., with two engines, weighted at 0.3 and 0.2 respectively, any specific entry
            in the result set has a 60% chance of being from search engine 1 and a 40% chance of being from search
            engine 2.

    """

    def __init__(self, data_stream, weights):
        """ Ensure weights are well formed in init """

        if len(weights) != len(data_stream):
            raise rf.ResultFeed.ResultFeedError(message='number of weight values must match number of datasources.')

        if isinstance(weights, list):
            for w in weights:
                if not(isinstance(w,int) or isinstance(w,float)):
                    raise rf.ResultFeed.ResultFeedError(message='weights must be a list of numbers.')
        else:
            raise rf.ResultFeed.ResultFeedError(message='weights must be a list of numbers.')

        # Store and normalize weights
        total_weight = sum(weights)
        self._weights = [float(w) / total_weight for w in weights]

        rf.ResultFeed.__init__(self, data_stream)

    def process(self):
        """ Process data stream results with weights for each engine """

        print ''.join(['Using weights: ',str(self._weights)])

        # Process data source elements
        while 1:

            # generate a random number between 0 and 1
            r = random.random()

            # Iterate through the weights to determine where the random sample falls
            # this determines the choice of of the data-source (it falls in interval k
            # with probability self._weights[k])
            pdf = 0
            index = 0
            for w in self._weights:
                pdf += w
                if r <= pdf:
                    break
                else:
                    index += 1

            # once the index is
            try:
                d = self._data_sources[index]
                engine_result = d.next()

                print d.get_source_name()
                print ''.join(['Description: ', engine_result[0]])
                print ''.join(['Link: ', engine_result[1]])
                print ''

                self._results.append(engine_result)

            except StopIteration:

                # Terminate if each data source generator has issued a StopIteration exception

                # generator terminated - set this weight to 0 then recompute
                self._weights[index] = 0
                total_weight = sum(self._weights)

                # If all weights are 0 exit
                if not total_weight:
                    break
                self._weights = [float(w) / total_weight for w in self._weights]

                continue
