#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''

try:
    connection = DLConnection()
    connection.authenticate(API_KEY, API_SECRET)

    readFilter = DLFilter()
    readFilter.field('dosage_form').not_equals('capsule')

    params = DLReadParams(dataset = 'medical_codes_ndc', filter = readFilter, limit = 5)

    data = connection.read(params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
