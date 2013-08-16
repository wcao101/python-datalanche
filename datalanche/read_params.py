# -*- coding: utf-8 -*-

class DLReadParams(object):
    def __init__(self,
        from_table = None,# the name of the dataset
        select = None,
        filter = None,
        limit = None,
        offset = None,
        sort = None,
        total = None):

        self.select = select
        self.filter = filter
        self.limit = limit
        self.offset = offset
        self.sort = sort
        self.total = total

    def sort_asc(self, select):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(select + ':$asc')
        return self # method chaining

    def sort_desc(self, select):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(select + ':$desc')
        return self # method chaining
