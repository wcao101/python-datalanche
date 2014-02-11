#! /usr/bin/python
#
# Alter the given schema's properties. Must have admin access for the given database.
#
# equivalent SQL:
# ALTER SCHEMA my_schema RENAME TO my_new_schema;
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
    q.alter_schema('my_schema')
    q.rename_to('my_new_schema')
    q.description('my_new_schema description text')

    client.query(q)

    print "alter_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
