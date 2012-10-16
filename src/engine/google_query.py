
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

import sys
import json
import logging
import urllib
import urllib2
import bp_challenge.config.settings as settings
import bp_challenge.src.engine.engine_query as eq

# CONFIGURE THE LOGGER
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%b-%d %H:%M:%S')

class GoogleQuery(eq.EngineQuery):
    """ retrieve results from Google search engine API """

    def __init__(self):
        self._api_ref = 'https://www.googleapis.com/customsearch/v1?key=%(api_key)s&cx=%(engine_id)s' \
                        '&q=%(query_tokens)s&alt=json'
        eq.EngineQuery.__init__(self)

    def __str__(self):
        return "Google search engine API wrapper."

    def submit_query(self, queryToken):

        """
            Submit one query to the Google search engine.

               @param queryToken - a string defining the search query
               @return - json object containing query results
        """

        try:
            url = self._api_ref % {'api_key' : settings.API_KEY, 'engine_id' : settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID,
            'query_tokens' : urllib.urlencode({'q' : queryToken.encode('utf-8')})}
            u = urllib2.urlopen(url)
            self._results = json.loads(u.read())

        except Exception:
            logging.error('Could not execute google query for token: %(token)s' % {'token' : queryToken})

        return self

    def parse_results(self):
        """ return a generator containing the query results """
        try:
            for item in self._results['items']:
                yield [item['snippet'], item['link']]

        except Exception:
            logging.error('GoogleQuery::parse_results: Could not parse results.')