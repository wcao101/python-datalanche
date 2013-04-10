# -*- coding: utf-8 -*-

class DLReadParams(object):
    def __init__(self,
        dataset = None,
        fields = None,
        filter = None,
        limit = None,
        skip = None,
        sort = None,
        total = None):

        self.dataset = dataset
        self.fields = fields
        self.filter = filter
        self.limit = limit
        self.skip = skip
        self.sort = sort
        self.total = total

    def sort_asc(self, field):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(field + ':asc')
        return self # method chaining

    def sort_desc(self, field):
        if self.sort == None:
            self.sort = list()
        if isinstance(self.sort, list) == False:
            raise Exception('DLReadParams.sort must be a list, but it is not')
        self.sort.append(field + ':desc')
        return self # method chaining
