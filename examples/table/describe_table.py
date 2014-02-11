#! /usr/bin/python
#
# Show the given table's details. Must have read access for the given database.
#
import json
from datalanche import *
import sys

try:

    config = json.load(open("../../config.json"))

    # Please found your API credentials here: datalanche.com/account/login before use
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.describe_table('my_schema.my_table')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
