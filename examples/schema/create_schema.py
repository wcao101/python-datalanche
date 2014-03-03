#! /usr/bin/python
#
# Create the given schema. Must have admin access for the given database.
#
# equivalent SQL:
# CREATE SCHEMA my_schema;
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


    q = DLQuery(database = 'my_database')
    q.create_schema('my_schema')
    q.description('my_schema description text')

    client.query(q)

    print "create_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
