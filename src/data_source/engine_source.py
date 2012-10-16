
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

from bp_challenge.src.data_source import data_source as ds
from bp_challenge.src.engine import engine_query as eq

class EngineSource(ds.DataSource):
    """ Handles data generated from search engine APIs. Uses base  """

    def __init__(self, gen_obj):
        """ Ensure the data stream is an engine """
        if not isinstance(gen_obj, eq.EngineQuery):
            raise ds.DataSource.DataSourceError()

        self._source = gen_obj
        ds.DataSource.__init__(self, gen_obj.parse_results())

    def reset_data_stream(self):
        """ resets the generator of the data stream """
        self._gen = self._source.parse_results()