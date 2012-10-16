""" Execute query on Google search engine """

__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

import json
import logging
import sys
import base64
import urllib
import urllib2
import bp_challenge.config.settings as settings
import bp_challenge.src.engine.engine_query as eq

# CONFIGURE THE LOGGER
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%b-%d %H:%M:%S')

class BingQuery(eq.EngineQuery):
    """ retrieve results from Bing search engine API """

    def __init__(self, **kwargs):
        self._api_ref = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Web" \
                        "?Query=%(escape_val)s%(query_tokens)s%(escape_val)s&$top=%(count)s&$format=Json"

        if 'count' in kwargs:
            self._count = kwargs['count']

        eq.EngineQuery.__init__(self)

    def __str__(self):
        return "Bing search engine API wrapper."

    def submit_query(self, queryToken):

        """
            Submit one query to the Bing search engine.

               @param queryToken - a string defining the search query
               @return - json object containing query results
        """

        try:
            url = self._api_ref % {'query_tokens' : urllib.urlencode({'q' : queryToken.encode('utf-8')})[2:],
                                   'count' : self._count, 'escape_val' : '%27'}
            request = urllib2.Request(url)
            request.add_header("Authorization", "Basic %s" % base64.b64encode(':'.join([settings.ACCT_KEY] * 2)))
            u = urllib2.urlopen(request)
            self._results = json.loads(u.read())

        except Exception:
            logging.error('Could not execute bing query for token: %(token)s' % {'token' : queryToken})

        return self

    def parse_results(self):
        """ return a generator containing the query results """

        try:
            for item in self._results['d']['results']:
                yield [item['Description'], item['Url']]

        except Exception:
            logging.error('BingQuery::parse_results: Could not parse results.')