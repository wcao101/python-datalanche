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

    q = DLQuery(database='my_database')
    q.alter_schema('my_schema')
    q.rename_to('my_new_schema')
    q.description('my_new_schema description text')

    client.query(q)

    print "alter_schema succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
