# -*- coding: utf-8 -*-

class DLReadParams(object):
    def __init__(self,
        columns = None,
        filter = None,
        limit = None,
        skip = None,
        sort = None,
        total = None):

        self.columns = columns
        self.filter = filter
        self.limit = limit
        self.skip = skip
        self.sort = sort
        self.total = total

    def sort_asc(self, column):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(column + ':$asc')
        return self # method chaining

    def sort_desc(self, column):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(column + ':$desc')
        return self # method chaining
