#! /usr/bin/python
#
# Create the given schema. Must have admin access for the given database.
#
# equivalent SQL:
# CREATE SCHEMA my_schema;
#
import json
import collections
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


    q = DLQuery(database = 'my_database')
    q.create_schema('my_schema')
    q.description('my_schema description text')

    client.query(q)

    print "create_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
