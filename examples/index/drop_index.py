#! /usr/bin/python
#
# Drop the given index. Must have admin access for the given database.
#
# equivalent SQL:
# DROP INDEX my_schema.my_index CASCADE;
#
import json
from datalanche import *
import sys, os

try:

    config = json.load(open(os.path.dirname(os.path.dirname(__file__))+'/config.json'))

    # Please find your API credentials here: https://www.datalanche.com/account before use            
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.drop_index('my_schema.my_index')
    q.cascade(True)

    client.query(q)

    print "drop_index succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
