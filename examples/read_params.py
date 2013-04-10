#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''

try:
    connection = DLConnection()
    connection.authenticate(API_KEY, API_SECRET)

    params = DLReadParams()
    params.dataset = 'medical_codes_ndc'
    params.fields = ['dosage_form', 'route', 'product_type']
    params.limit = 5
    params.skip = 0
    params.total = False
    params.filter = None    # look at read_filter.py and read_complex_filter.py

    params.sort_desc('dosage_form')
    params.sort_asc('product_type')

    # You can also set params.sort to a list instead of using the helper methods.
    params.sort = ['dosage_form:$desc', 'product_type:$asc']

    data = connection.read(params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
