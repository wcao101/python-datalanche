#! /usr/bin/python
#
# Create an index on the given table. Must have admin access for the given database.
#
# equivalent SQL:
# CREATE UNIQUE INDEX my_index ON my_schema.my_table USING btree (col1, col2);
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
    q.create_index('my_index')
    q.unique(True)
    q.on_table('my_schema.my_table')
    q.method('btree')
    q.columns([ 'col1', 'col2' ])

    client.query(q)

    print "create_index succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
