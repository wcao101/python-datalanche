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
        self.sort.append(field + ':asc')

    def sort_desc(self, field):
        if self.sort == None:
            self.sort = list()
        self.sort.append(field + ':desc')
