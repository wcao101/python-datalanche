#! /usr/bin/python

import json
from datalanche import *

API_KEY = ''
API_SECRET = ''

try:
    connection = DLConnection()
    connection.authenticate(API_KEY, API_SECRET)

    data = connection.get_list()

    print json.dumps(data, sort_keys = False, indent = 4)
except DLException as e:
    print repr(e)
