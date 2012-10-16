
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

from bp_challenge.src.query import result_feed as rf
import heapq
import re

class MaximumTokenFeed(rf.ResultFeed):
    """
        Implements the Max Token data feed.  Inherits ResultFeed.

            Maximum Tokens.  Present results ordered by the number of times any of the search tokens appear in the
            description.  If Alex searches for "John Lennon", count the number of "John" and "Lennon" tokens in the
            description (just the description ... not the whole page) and present the most first.
    """

    def __init__(self, data_stream, tokens):
        self._tokens = tokens.split()
        rf.ResultFeed.__init__(self, data_stream)

    def process(self):
        """ Process data stream results and extract matching token counts """

        h = []

        # Process data source elements -  gett
        for d in self._data_sources:
            try:
                while 1:
                    element = d.next()
                    token_count = self._get_num_tokens(element[0])
                    heapq.heappush(h,(token_count, element[0], element[1], d.get_source_name()))

            except StopIteration:
                continue

        # Pop the queue until an IndexError is issued (ie. all elements popped)
        results = list()
        try:
            while 1:
                results.append(heapq.heappop(h))
        except IndexError:
            pass

        # The heap is a min-heap so reverse the list
        results.reverse()

        for element in results:
            print element[3]
            print ''.join(['TOKEN COUNT = ', str(element[0])])
            print ''.join(['Description: ', element[1]])
            print ''.join(['Link: ', element[2]])
            print ''

            self._results.append((element[1], element[2]))


    def _get_num_tokens(self, description):
        """ get token matches in desription.  Case insensitive. Sub-strings count. """

        count = 0
        desc_tokens = description.split()
        for token in self._tokens:
            for d_token in desc_tokens:
                if re.search(token.lower(), d_token.lower()):
                    count += 1

        return count
