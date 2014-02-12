#! /usr/bin/python
#
# Show details of given database. Must have read access for the database.
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
    q.describe_database('my_database')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
