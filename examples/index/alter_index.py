#! /usr/bin/python
#
# Alter the given index's properties. Must have admin access for the given database.
#
# equivalent SQL:
# ALTER INDEX my_schema.my_index RENAME TO my_new_index;
#
import json
from datalanche import *
import sys

try:

    config = json.load(open("./examples/config.json"))

    # Please find your API credentials here: https://www.datalanche.com/account before use            
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.alter_index('my_schema.my_index')
    q.rename_to('my_new_index')

    client.query(q)

    print "alter_index succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
