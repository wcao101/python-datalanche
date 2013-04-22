#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='your_api_key', secret='your_api_secret')

    readFilter = DLFilter()
    readFilter.bool_and([
        DLFilter().bool_or([
            DLFilter().field('dosage_form').equals('capsule'),
            DLFilter().field('dosage_form').equals('tablet')
        ]),
        DLFilter().field('product_type').contains('esc')
    ])

    params = DLReadParams(dataset = 'medical_codes_ndc', filter = readFilter, limit = 5)

    data = client.read(params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
