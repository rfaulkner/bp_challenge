
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

class EngineQuery:

    """ Execute query on Generic search engine. Singleton class for executing queries. """

    _results = None
    _api_ref = None
    _count = 10
    __instance = None

    def __init__( self ):

        if EngineQuery.__instance:
            raise self.__class__.__instance
        self.__class__.__instance = self

    def submit_query(self, queryToken):
        """
            @param - queryToken, string containing search query
            @return - json object containing query results from engine
        """
        raise NotImplementedError

    def parse_results(self):
        """
            @return - return a generator containing the query results
        """
        raise NotImplementedError