#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='your_api_key', secret='your_api_secret')

    readFilter = DLFilter()
    readFilter.column('dosage_form').not_equals('capsule')

    params = DLReadParams(filter = readFilter, limit = 5)

    data = client.read_records('medical_codes_ndc', params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
