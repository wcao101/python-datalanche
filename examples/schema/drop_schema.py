#! /usr/bin/python
#
# Drop the given schema. Must have admin access for the given database.
#
# equivalent SQL:
# DROP SCHEMA my_schema CASCADE;
#

import json
from datalanche import *
import sys

try:

    config = json.load(open("../config.json"))

    # Please find your API credentials here: https://www.datalanche.com/account before use            
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.drop_schema('my_schema_1')
    q.cascade(True)

    client.query(q)

    print "drop_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
