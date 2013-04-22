#! /usr/bin/python

import json
from datalanche import *

try:
    client = DLClient(key='your_api_key', secret='your_api_secret')

    data = client.get_schema('medical_codes_ndc')

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
