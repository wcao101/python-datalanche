#! /usr/bin/python

import json
from datalanche import *

API_KEY = '16YNL0N2QVS9kx2y07MgcA=='
API_SECRET = ''
DATASET_NAME = 'medical_codes_ndc'

connection = DLConnection()
connection.authenticate(API_KEY, API_SECRET)

print '\n---------------------------'
print 'get_list'
print '---------------------------'

try:
    data = connection.get_list()
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)

print '\n---------------------------'
print 'get_schema'
print '---------------------------'

try:
    data = connection.get_schema(DATASET_NAME)
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)

print '\n---------------------------'
print 'simple read'
print '---------------------------'

try:
    data = connection.read(DATASET_NAME)
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)

print '\n---------------------------'
print 'read with params'
print '---------------------------'

try:
    params = DLReadParams()
    params.fields = ['dosage_form', 'route', 'product_type']
    params.limit = 5
    params.skip = 0
    params.total = False
    params.filter = None    # look at read with filter examples below

    params.sort_desc('dosage_form')
    params.sort_asc('product_type')

    # You can also set params.sort to a list instead of using the helper methods.
    params.sort = ['dosage_form:desc', 'product_type:asc']

    data = connection.read(DATASET_NAME, params)
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)

print '\n---------------------------'
print 'read with simple filter'
print '---------------------------'

try:
    myFilter = DLFilter('dosage_form', DLFilterOp.EQ, 'capsule')

    params = DLReadParams(limit = 5, filter = myFilter)

    data = connection.read(DATASET_NAME, params)
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)

print '\n---------------------------'
print 'read with complex filter'
print '---------------------------'

try:
    myFilter = DLFilter(
        DLFilter(
            DLFilter('dosage_form', DLFilterOp.EQ, 'capsule'),
            DLFilterOp.OR,
            DLFilter('dosage_form', DLFilterOp.EQ, 'tablet')
        ),
        DLFilterOp.AND,
        DLFilter('product_type', DLFilterOp.CONTAINS, 'esc')
    )

    params = DLReadParams(limit = 5, filter = myFilter)

    data = connection.read(DATASET_NAME, params)
    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
