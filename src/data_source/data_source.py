
__author__ = 'ryan faulkner'
__date__ = "10/15/2012"
__license__ = "GPL (version 2 or later)"

import collections

class DataSource:

    """
        Base class for data sources.  Wrapper (Adapter) for data types that allows a unified interface to be provided
        for different data sources.
    """

    _source = None
    _gen = None

    def __init__(self, gen):
        if isinstance(gen, collections.Iterable):
            self._gen = gen
        else:
            raise DataSource.DataSourceError()

    def __iter__(self):
        return self._gen

    def next(self):
        return self._gen.next()

    def get_source_name(self):
        return str(self._source)

    class DataSourceError(Exception):
        """ Basic exception class for ResultFeed types """
        def __str__(self):
            msg = "Unable to process results using %(classname)s strategy" % {'classname' : str(self.__class__())}
            return msg