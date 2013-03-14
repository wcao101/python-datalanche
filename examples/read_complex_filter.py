#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''
DATASET_NAME = 'medical_codes_ndc'

try:
    connection = DLConnection()
    connection.authenticate(API_KEY, API_SECRET)

    readFilter = DLFilter(
        DLFilter(
            DLFilter('dosage_form', DLFilterOp.EQ, 'capsule'),
            DLFilterOp.OR,
            DLFilter('dosage_form', DLFilterOp.EQ, 'tablet')
        ),
        DLFilterOp.AND,
        DLFilter('product_type', DLFilterOp.CONTAINS, 'esc')
    )

    params = DLReadParams(limit = 5, filter = readFilter)

    data = connection.read(DATASET_NAME, params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
