#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''

try:
    client = DLClient()
    client.authenticate(API_KEY, API_SECRET)

    data = client.get_schema('medical_codes_ndc')

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
