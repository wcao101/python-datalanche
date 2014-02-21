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
    config = json.load(open("../config.json"))
    config['verify_ssl'] = config['verify_ssl'].lower()
    if config['verify_ssl'] == '0' or config['verify_ssl'] == 'false':
        config['verify_ssl'] = False
    else:
        config['verify_ssl'] = True

    client = DLClient(key = config['api_key'], 
                      secret = config['api_secret'], 
                      host = config['host'], 
                      port = config['port'], 
                      verify_ssl = config['verify_ssl'])

    q = DLQuery(database = 'my_database')
    q.create_schema('my_schema')
    q.description('my_schema description text')

    client.query(q)

    print "create_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
