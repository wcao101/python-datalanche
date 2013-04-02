# -*- coding: utf-8 -*-

import json
import collections

class DLFilter(object):
    def __init__(self):
        self._hasNot = False
        self._field = None
        self._filters = None
        self._operator = None
        self._value = None

    def __str__(self):
        return json.dumps(self.json())

    def json(self):
        # return empty when not formatted correctly
        if (self._operator == None):
            return collections.OrderedDict()

        if self._operator == '$and' or self._operator == '$or':

            # return empty when not formatted correctly
            if self._filters == None:
                return collections.OrderedDict()

            json_list = list()
            for i in range(0, len(self._filters)):
                item = collections.OrderedDict()
                if isinstance(self._filters[i], DLFilter) == True:
                    item = self._filters[i].json()
                else:
                    item = self._filters[i]

                json_list.append(item)

            json = collections.OrderedDict()
            json[str(self._operator)] = json_list

            return json

        else:

            # return empty when not formatted correctly
            if self._field == None or self._value == None:
                return collections.OrderedDict()

            opExpression = collections.OrderedDict()
            opExpression[str(self._operator)] = self._value

            if self._hasNot == True:
                opExpression = { '$not': opExpression }

            json = collections.OrderedDict()
            json[str(self._field)] = opExpression

            return json

    def field(self, string):
        self._field = string
        return self

    def bool_and(self, filter_list):
        self._filters = filter_list
        self._operator = '$and'
        return self

    def contains(self, value):
        self._hasNot = False
        self._operator = '$contains'
        self._value = value
        return self

    def ends_with(self, value):
        self._hasNot = False
        self._operator = '$ends'
        self._value = value
        return self

    def equals(self, value):
        self._hasNot = False
        self._operator = '$eq'
        self._value = value
        return self

    def greater_than(self, value):
        self._hasNot = False
        self._operator = '$gt'
        self._value = value
        return self

    def greater_than_equal(self, value):
        self._hasNot = False
        self._operator = '$gte'
        self._value = value
        return self

    def any_in(self, value):
        self._hasNot = False
        self._operator = '$in'
        self._value = value
        return self

    def less_than(self, value):
        self._hasNot = False
        self._operator = '$lt'
        self._value = value
        return self

    def less_than_equal(self, value):
        self._hasNot = False
        self._operator = '$lte'
        self._value = value
        return self

    def not_contains(self, value):
        self._hasNot = True
        self._operator = '$contains'
        self._value = value
        return self

    def not_ends_with(self, value):
        self._hasNot = True
        self._operator = '$ends'
        self._value = value
        return self

    def not_equals(self, value):
        self._hasNot = True
        self._operator = '$eq'
        self._value = value
        return self

    def not_any_in(self, value):
        self._hasNot = True
        self._operator = '$in'
        self._value = value
        return self

    def not_starts_with(self, value):
        self._hasNot = True
        self._operator = '$starts'
        self._value = value
        return self

    def bool_or(self, filterList):
        self._filters = filterList
        self._operator = '$or'
        return self

    def starts_with(self, value):
        self._hasNot = False
        self._operator = '$starts'
        self._value = value
        return self
