#! /usr/bin/python
#
# Show the given schema's details. Must have read access for the given database.
#
import json
from datalanche import *
import sys

try:

    # Load config.json for setting API_KEY, API_SECRET, host, port and verify_ssh
    # change the settings in config.json before running examples
    config = json.load(open("../../config.json"))

    # Please change YOUR_API_KEY and YOUR_API_SECRET before use
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.describe_schema('my_new_schema')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
