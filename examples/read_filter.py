#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='your_api_key', secret='your_api_secret')

    readFilter = DLFilter()
    readFilter.field('dosage_form').not_equals('capsule')

    params = DLReadParams(dataset = 'medical_codes_ndc', filter = readFilter, limit = 5)

    data = client.read(params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
