# -*- coding: utf-8 -*-

from enum import Enum
import json

DLFilterOp = Enum(
    'AND',          # and
    'OR',           # or
    'EQ',           # equal
    'NOT_EQ',       # not equal
    'GT',           # greater than
    'GTE',          # greater than or equal
    'LT',           # less than
    'LTE',          # less than or equal
    'IN',           # equals any in array
    'NOT_IN',       # does not equal any in array
    'EW',           # ends with
    'NOT_EW',       # does not end with
    'CONTAINS',     # contains string
    'NOT_CONTAINS', # does not contain string
    'SW',           # starts with
    'NOT_SW',       # does not start with
)

class DLFilter(object):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def json(self):
        left = self.left
        right = self.right

        if isinstance(left, DLFilter):
            left = left.json()
        if isinstance(right, DLFilter):
            right = right.json()

        return {
            'left': left,
            'op': str(self.operator).lower(),
            'right': right
        }

    def __str__(self):
        return json.dumps(self.json())
