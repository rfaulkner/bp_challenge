
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

from bp_challenge.src.query import result_feed as rf

class UniqueURLFeed(rf.ResultFeed):
    """
        Implements the Unique URL data feed.  Inherits ResultFeed.

            Unique URLs.  Remove any redundant URL's from the search result.  That is, if multiple search engines return
            the same URL, only present one of them to Alex.

    """

    def __init__(self, data_stream, match_domain=False):
        self._match_domain = match_domain
        rf.ResultFeed.__init__(self, data_stream)

    def process(self):
        """ Process data stream results omitting repeats """

        urls = list()       # stores urls so far seen
        matches = 0         # counts number of matches
        match_list = list() # store matches

        # Process data source elements
        for d in self._data_sources:
            while 1:
                try:
                    engine_result = d.next()
                    if self._match_domain:
                        url = '/'.join(engine_result[1].split('/')[:3])
                    else:
                        url = engine_result[1]

                    if url in urls:
                        matches += 1
                        match_list.append(url)
                        continue
                    else:
                        urls.append(url)

                        print d.get_source_name()
                        print ''.join(['Description: ', engine_result[0]])
                        print ''.join(['Link: ', engine_result[1]])
                        print ''

                except StopIteration:
                    break

        print '%(count)s matches encountered:\n%(list)s' % {'count' : matches, 'list' : str(match_list)}

