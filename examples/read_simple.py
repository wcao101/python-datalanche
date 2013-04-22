#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''

try:
    client = DLClient()
    client.authenticate(API_KEY, API_SECRET)

    # Uses default parameters however "dataset" is required.
    params = DLReadParams(dataset = 'medical_codes_ndc')

    data = client.read(params)

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
