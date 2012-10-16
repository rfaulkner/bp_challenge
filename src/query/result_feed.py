
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

import bp_challenge.src.data_source.data_source as ds

class ResultFeed:

    """
        Base class for strategy pattern for

        A concrete custom strategy: ::

            class CustomFeed(ResultFeed):

                    def __init__(self, data_stream):
                        ...
                        ResultFeed.__init__(self)

                    def process()
                        ... logic to process results from datasources
    """

    _data_sources = None
    _results = list()

    def __init__(self, data_sources):
        """ Ensure that parameter is a list of datasources """

        if isinstance(data_sources, list):
            for source in data_sources:
                if not isinstance(source, ds.DataSource):
                    raise ResultFeed.ResultFeedError()
        else:
            raise ResultFeed.ResultFeedError()

        self._data_sources = data_sources

    def process(self):
        """ stub for processing datasource results """
        raise NotImplementedError

    def get_results_generator(self):
        """ Produces a generator for the strategy results """
        for element in self._results:
            yield element

    class ResultFeedError(Exception):
        """ Basic exception class for ResultFeed types """
        def __init__(self, message="Unable to process results using strategy."):
            Exception.__init__(self, message)