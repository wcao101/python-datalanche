#! /usr/bin/python
#
# Show all databases you have access to.
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

    q = DLQuery()
    q.show_databases()

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
